from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, mm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT


class PDFService:

    def __init__(self):
        # Soft, modern color palette
        self.colors = {
            'purple': HexColor('#7c3aed'),
            'purple_light': HexColor('#ede9fe'),
            'pink': HexColor('#ec4899'),
            'pink_light': HexColor('#fce7f3'),
            'blue': HexColor('#3b82f6'),
            'blue_light': HexColor('#dbeafe'),
            'green': HexColor('#10b981'),
            'green_light': HexColor('#d1fae5'),
            'amber': HexColor('#f59e0b'),
            'amber_light': HexColor('#fef3c7'),
            'red': HexColor('#ef4444'),
            'red_light': HexColor('#fee2e2'),
            'text_dark': HexColor('#1e1b4b'),
            'text_mid': HexColor('#4b5563'),
            'text_light': HexColor('#9ca3af'),
            'border': HexColor('#e5e7eb'),
            'bg_light': HexColor('#f9fafb'),
        }

        self.page_width = A4[0] - 100  # 50 margin each side
        self.styles = getSampleStyleSheet()
        self._setup_styles()

    def _setup_styles(self):
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            fontName='Helvetica-Bold',
            fontSize=20,
            textColor=self.colors['text_dark'],
            spaceAfter=2,
            leading=26,
        ))

        self.styles.add(ParagraphStyle(
            name='Subtitle',
            fontName='Helvetica',
            fontSize=9,
            textColor=self.colors['text_light'],
            spaceAfter=0,
        ))

        self.styles.add(ParagraphStyle(
            name='SectionTitle',
            fontName='Helvetica-Bold',
            fontSize=12,
            textColor=self.colors['purple'],
            spaceBefore=18,
            spaceAfter=8,
        ))

        self.styles.add(ParagraphStyle(
            name='Body',
            fontName='Helvetica',
            fontSize=10,
            textColor=self.colors['text_mid'],
            leading=14,
            spaceAfter=6,
        ))

        self.styles.add(ParagraphStyle(
            name='BodySmall',
            fontName='Helvetica',
            fontSize=9,
            textColor=self.colors['text_mid'],
            leading=13,
            spaceAfter=4,
        ))

        self.styles.add(ParagraphStyle(
            name='Label',
            fontName='Helvetica-Bold',
            fontSize=9,
            textColor=self.colors['text_light'],
            spaceAfter=2,
        ))

        self.styles.add(ParagraphStyle(
            name='Value',
            fontName='Helvetica',
            fontSize=10,
            textColor=self.colors['text_dark'],
            spaceAfter=8,
        ))

    def generate_report(self, diagnosis_data: Dict[str, Any]) -> bytes:
        buffer = BytesIO()

        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50, leftMargin=50,
            topMargin=40, bottomMargin=40,
        )

        story = []
        story.extend(self._build_header(diagnosis_data))
        story.extend(self._build_patient_card(diagnosis_data))
        story.extend(self._build_risk_badge(diagnosis_data))
        story.extend(self._build_factors_table(diagnosis_data))
        story.extend(self._build_recommendations(diagnosis_data))
        story.extend(self._build_footer())

        doc.build(story)
        content = buffer.getvalue()
        buffer.close()
        return content

    def _build_header(self, data: Dict) -> List:
        elements = []

        # Title
        elements.append(Paragraph("PCOS Diagnostic Report", self.styles['ReportTitle']))

        # Thin purple accent line
        elements.append(HRFlowable(
            width="100%", thickness=2,
            color=self.colors['purple'], spaceAfter=8, spaceBefore=4,
        ))

        # Report meta line
        created = data.get('created_at', datetime.now())
        date_str = created.strftime("%B %d, %Y") if created else datetime.now().strftime("%B %d, %Y")
        report_type = "Confirmed Diagnosis" if data.get('is_confirmed') else "Preliminary Screening"

        meta_text = f"{date_str}  ·  {report_type}"
        elements.append(Paragraph(meta_text, self.styles['Subtitle']))
        elements.append(Spacer(1, 16))

        return elements

    def _build_patient_card(self, data: Dict) -> List:
        elements = []

        elements.append(Paragraph("Patient Information", self.styles['SectionTitle']))

        name = data.get('patient_name', 'N/A')
        age = data.get('patient_age', 'N/A')
        created = data.get('created_at', datetime.now())
        date_str = created.strftime("%B %d, %Y") if created else "N/A"

        # Two-column layout for patient info
        col1 = [
            Paragraph("PATIENT NAME", self.styles['Label']),
            Paragraph(str(name), self.styles['Value']),
            Paragraph("DATE OF ASSESSMENT", self.styles['Label']),
            Paragraph(date_str, self.styles['Value']),
        ]

        col2 = [
            Paragraph("AGE", self.styles['Label']),
            Paragraph(f"{age} years", self.styles['Value']),
            Paragraph("ASSESSMENT TYPE", self.styles['Label']),
            Paragraph(
                "Confirmed (Stage 2)" if data.get('is_confirmed') else "Preliminary (Stage 1)",
                self.styles['Value']
            ),
        ]

        # Build the two-column table
        info_table = Table(
            [[col1[0], col2[0]],
             [col1[1], col2[1]],
             [col1[2], col2[2]],
             [col1[3], col2[3]]],
            colWidths=[self.page_width * 0.55, self.page_width * 0.45],
        )
        info_table.setStyle(TableStyle([
            ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ('LEFTPADDING', (0, 0), (-1, -1), 12),
            ('RIGHTPADDING', (0, 0), (-1, -1), 12),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['bg_light']),
            ('BOX', (0, 0), (-1, -1), 0.5, self.colors['border']),
        ]))

        elements.append(info_table)
        elements.append(Spacer(1, 10))

        return elements

    def _build_risk_badge(self, data: Dict) -> List:
        elements = []

        elements.append(Paragraph("Risk Assessment", self.styles['SectionTitle']))

        probability = data.get('probability', 0)
        risk_level = data.get('risk_level', 'LOW')

        # Colors per risk level
        risk_config = {
            'HIGH':     {'bg': self.colors['red_light'],   'text': self.colors['red'],   'border': self.colors['red']},
            'MODERATE': {'bg': self.colors['amber_light'], 'text': self.colors['amber'], 'border': self.colors['amber']},
            'LOW':      {'bg': self.colors['green_light'], 'text': self.colors['green'], 'border': self.colors['green']},
        }
        config = risk_config.get(risk_level, risk_config['LOW'])

        # Risk level badge
        risk_para = Paragraph(
            f"<b>{risk_level} RISK</b>",
            ParagraphStyle(
                name='RiskLabel', fontName='Helvetica-Bold',
                fontSize=13, textColor=config['text'], alignment=TA_CENTER,
            )
        )

        prob_para = Paragraph(
            f"Probability: <b>{probability * 100:.1f}%</b>",
            ParagraphStyle(
                name='ProbLabel', fontName='Helvetica',
                fontSize=11, textColor=config['text'], alignment=TA_CENTER,
            )
        )

        badge_data = [[risk_para, prob_para]]
        badge = Table(badge_data, colWidths=[self.page_width * 0.45, self.page_width * 0.55])
        badge.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), config['bg']),
            ('BOX', (0, 0), (-1, -1), 1, config['border']),
            ('TOPPADDING', (0, 0), (-1, -1), 12),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ('LEFTPADDING', (0, 0), (-1, -1), 16),
            ('RIGHTPADDING', (0, 0), (-1, -1), 16),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ]))

        elements.append(badge)
        elements.append(Spacer(1, 10))

        return elements

    def _build_factors_table(self, data: Dict) -> List:
        elements = []

        elements.append(Paragraph("Contributing Factors", self.styles['SectionTitle']))
        elements.append(Paragraph(
            "Top factors influencing this assessment, ranked by impact.",
            self.styles['BodySmall']
        ))

        shap_data = data.get('shap_chart_data', [])

        if not shap_data:
            elements.append(Paragraph("No factor data available.", self.styles['Body']))
            elements.append(Spacer(1, 10))
            return elements

        # Build table rows
        header = [
            Paragraph("<b>Factor</b>", ParagraphStyle(name='TH1', fontName='Helvetica-Bold', fontSize=9, textColor=self.colors['text_dark'])),
            Paragraph("<b>Value</b>", ParagraphStyle(name='TH2', fontName='Helvetica-Bold', fontSize=9, textColor=self.colors['text_dark'], alignment=TA_CENTER)),
            Paragraph("<b>Impact</b>", ParagraphStyle(name='TH3', fontName='Helvetica-Bold', fontSize=9, textColor=self.colors['text_dark'], alignment=TA_CENTER)),
            Paragraph("<b>Direction</b>", ParagraphStyle(name='TH4', fontName='Helvetica-Bold', fontSize=9, textColor=self.colors['text_dark'])),
        ]
        table_rows = [header]

        cell_style = ParagraphStyle(name='CellText', fontName='Helvetica', fontSize=9, textColor=self.colors['text_mid'])
        cell_center = ParagraphStyle(name='CellCenter', fontName='Helvetica', fontSize=9, textColor=self.colors['text_mid'], alignment=TA_CENTER)

        for item in shap_data[:8]:
            feature = item.get('feature', '')
            value = item.get('value', 0)
            impact = item.get('impact', 0)
            direction = item.get('direction', '')

            # Color code direction
            if direction == 'increases':
                dir_color = self.colors['pink']
                dir_text = "↑ Increases risk"
            else:
                dir_color = self.colors['green']
                dir_text = "↓ Decreases risk"

            dir_style = ParagraphStyle(name=f'Dir_{feature}', fontName='Helvetica', fontSize=9, textColor=dir_color)

            table_rows.append([
                Paragraph(feature, cell_style),
                Paragraph(f"{value:.1f}", cell_center),
                Paragraph(f"{abs(impact) * 100:.1f}%", cell_center),
                Paragraph(dir_text, dir_style),
            ])

        table = Table(
            table_rows,
            colWidths=[self.page_width * 0.38, self.page_width * 0.15, self.page_width * 0.15, self.page_width * 0.32],
        )
        table.setStyle(TableStyle([
            # Header
            ('BACKGROUND', (0, 0), (-1, 0), self.colors['purple_light']),
            ('TOPPADDING', (0, 0), (-1, 0), 8),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
            # All cells
            ('TOPPADDING', (0, 1), (-1, -1), 6),
            ('BOTTOMPADDING', (0, 1), (-1, -1), 6),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            # Grid lines
            ('LINEBELOW', (0, 0), (-1, 0), 1, self.colors['purple']),
            ('LINEBELOW', (0, 1), (-1, -2), 0.5, self.colors['border']),
            # Alternating rows
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.colors['bg_light']]),
        ]))

        elements.append(table)
        elements.append(Spacer(1, 10))

        return elements

    def _build_recommendations(self, data: Dict) -> List:
        elements = []

        elements.append(Paragraph("Clinical Recommendations", self.styles['SectionTitle']))

        recommendation = data.get('recommendation', 'No recommendation available.')

        # Split into sections by " | " delimiter
        sections = [s.strip() for s in recommendation.split(" | ") if s.strip()]

        # Config for each section type
        section_styles = [
            {"title": "Diagnosis Summary",    "accent": self.colors['purple'], "bg": self.colors['purple_light']},
            {"title": "Model Confidence",     "accent": self.colors['blue'],   "bg": self.colors['blue_light']},
            {"title": "Age Consideration",    "accent": self.colors['pink'],   "bg": self.colors['pink_light']},
            {"title": "Symptom Patterns",     "accent": self.colors['green'],  "bg": self.colors['green_light']},
            {"title": "Additional Notes",     "accent": self.colors['amber'],  "bg": self.colors['amber_light']},
        ]

        for i, section_text in enumerate(sections):
            # Get style config
            style = section_styles[i] if i < len(section_styles) else section_styles[-1]

            # Title paragraph
            title_para = Paragraph(
                f"<b>{style['title']}</b>",
                ParagraphStyle(
                    name=f'SecTitle_{i}', fontName='Helvetica-Bold',
                    fontSize=9, textColor=style['accent'],
                    spaceBefore=0, spaceAfter=0,
                )
            )

            # Body paragraph
            body_para = Paragraph(
                section_text,
                ParagraphStyle(
                    name=f'SecBody_{i}', fontName='Helvetica',
                    fontSize=9, textColor=self.colors['text_mid'],
                    leading=13, spaceBefore=0, spaceAfter=0,
                )
            )

            # Left-border accent card using a two-column table
            accent_cell = ""  # Empty narrow cell for the colored left border
            content_cell = [title_para, Spacer(1, 4), body_para]

            # Stack title + body into one cell
            content_table = Table([[p] for p in content_cell], colWidths=[self.page_width - 32])
            content_table.setStyle(TableStyle([
                ('TOPPADDING', (0, 0), (-1, -1), 0),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
                ('LEFTPADDING', (0, 0), (-1, -1), 0),
                ('RIGHTPADDING', (0, 0), (-1, -1), 0),
            ]))

            card_data = [[accent_cell, content_table]]
            card = Table(card_data, colWidths=[4, self.page_width - 4])
            card.setStyle(TableStyle([
                # Left accent border
                ('BACKGROUND', (0, 0), (0, -1), style['accent']),
                # Content area
                ('BACKGROUND', (1, 0), (1, -1), style['bg']),
                ('TOPPADDING', (1, 0), (1, -1), 10),
                ('BOTTOMPADDING', (1, 0), (1, -1), 10),
                ('LEFTPADDING', (1, 0), (1, -1), 12),
                ('RIGHTPADDING', (1, 0), (1, -1), 12),
                ('TOPPADDING', (0, 0), (0, -1), 0),
                ('BOTTOMPADDING', (0, 0), (0, -1), 0),
                ('LEFTPADDING', (0, 0), (0, -1), 0),
                ('RIGHTPADDING', (0, 0), (0, -1), 0),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
            ]))

            elements.append(card)
            elements.append(Spacer(1, 6))

        return elements

    def _build_footer(self) -> List:
        elements = []

        elements.append(Spacer(1, 20))

        # Thin separator line
        elements.append(HRFlowable(
            width="100%", thickness=0.5,
            color=self.colors['border'], spaceAfter=8, spaceBefore=0,
        ))

        # Disclaimer
        disclaimer_style = ParagraphStyle(
            name='Disclaimer', fontName='Helvetica',
            fontSize=8, textColor=self.colors['text_light'],
            leading=11, spaceAfter=6,
        )

        elements.append(Paragraph(
            "<b>Disclaimer:</b> This report is generated by an AI-powered diagnostic support tool "
            "and is intended to assist clinical decision-making. It should not be used as the sole "
            "basis for diagnosis. Always consult with qualified healthcare professionals for "
            "final medical decisions.",
            disclaimer_style
        ))

        # Timestamp
        elements.append(Paragraph(
            f"Report generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}",
            ParagraphStyle(
                name='Timestamp', fontName='Helvetica-Oblique',
                fontSize=8, textColor=self.colors['text_light'],
            )
        ))

        return elements


# Singleton instance
pdf_service = PDFService()