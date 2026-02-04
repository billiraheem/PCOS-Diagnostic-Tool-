from io import BytesIO
from datetime import datetime
from typing import Dict, List, Any
from reportlab.lib.pagesizes import A4
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.graphics.charts.barcharts import HorizontalBarChart


class PDFService:
    def __init__(self):
        # Color palette matching our app's design
        self.colors = {
            'primary': HexColor('#6366f1'),      # Indigo
            'high_risk': HexColor('#ef4444'),    # Red
            'moderate_risk': HexColor('#f59e0b'), # Amber
            'low_risk': HexColor('#22c55e'),     # Green
            'text': HexColor('#1f2937'),         # Dark gray
            'light_bg': HexColor('#f3f4f6'),     # Light gray
        }
        
        # Standard styles for text
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        # Title style - large, bold, primary color
        self.styles.add(ParagraphStyle(
            name='ReportTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=self.colors['primary'],
            spaceAfter=20,
        ))
        
        # Section header style
        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=14,
            textColor=self.colors['text'],
            spaceBefore=15,
            spaceAfter=10,
        ))
        
        # Body text style
        self.styles.add(ParagraphStyle(
            name='ReportBodyText',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=self.colors['text'],
            spaceAfter=8,
        ))
    
    def generate_report(self, diagnosis_data: Dict[str, Any]) -> bytes:
        # Create a bytes buffer to hold the PDF
        buffer = BytesIO()
        
        # Create the PDF document
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=50,
            bottomMargin=50,
        )
        
        # Build the content (list of flowable elements)
        story = []
        
        # Add each section
        story.extend(self._build_header())
        story.extend(self._build_patient_info(diagnosis_data))
        story.extend(self._build_risk_status(diagnosis_data))
        story.extend(self._build_shap_section(diagnosis_data))
        story.extend(self._build_recommendation(diagnosis_data))
        story.extend(self._build_footer(diagnosis_data))
        
        # Generate the PDF
        doc.build(story)
        
        # Get the PDF content
        pdf_content = buffer.getvalue()
        buffer.close()
        
        return pdf_content
    
    def _build_header(self) -> List:
        elements = []
        
        # Main title
        elements.append(Paragraph(
            "PCOS Diagnostic Report",
            self.styles['ReportTitle']
        ))
        
        # Subtitle
        elements.append(Paragraph(
            "AI-Powered Diagnostic Analysis with Explainable Results",
            self.styles['ReportBodyText']
        ))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_patient_info(self, data: Dict) -> List:
        elements = []
        
        elements.append(Paragraph("Patient Information", self.styles['SectionHeader']))
        
        # Create info table
        info_data = [
            ["Patient Name:", data.get('patient_name', 'N/A')],
            ["Age:", f"{data.get('patient_age', 'N/A')} years"],
            ["Assessment Date:", data.get('created_at', datetime.now()).strftime("%B %d, %Y")],
            ["Assessment Type:", "Confirmed Diagnosis" if data.get('is_confirmed') else "Presumptive Screening"],
        ]
        
        table = Table(info_data, colWidths=[150, 300])
        table.setStyle(TableStyle([
            ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
            ('FONTNAME', (1, 0), (1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['text']),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 15))
        
        return elements
    
    def _build_risk_status(self, data: Dict) -> List:
        elements = []
        
        elements.append(Paragraph("Risk Assessment", self.styles['SectionHeader']))
        
        probability = data.get('probability', 0)
        risk_level = data.get('risk_level', 'LOW')
        
        # Choose color based on risk level
        risk_colors = {
            'HIGH': self.colors['high_risk'],
            'MODERATE': self.colors['moderate_risk'],
            'LOW': self.colors['low_risk'],
        }
        risk_color = risk_colors.get(risk_level, self.colors['low_risk'])
        
        # Create risk indicator table
        risk_data = [
            [f"Risk Level: {risk_level}", f"Probability: {probability * 100:.1f}%"],
        ]
        
        table = Table(risk_data, colWidths=[230, 230])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), risk_color),
            ('TEXTCOLOR', (0, 0), (-1, -1), white),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 14),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 20),
            ('RIGHTPADDING', (0, 0), (-1, -1), 20),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_shap_section(self, data: Dict) -> List:
        elements = []
        
        elements.append(Paragraph(
            "Contributing Factors (AI Explanation)",
            self.styles['SectionHeader']
        ))
        
        elements.append(Paragraph(
            "The following factors contributed most significantly to this assessment. "
            "Positive values increase PCOS risk, negative values decrease risk.",
            self.styles['ReportBodyText']
        ))
        
        shap_data = data.get('shap_chart_data', [])
        
        if shap_data:
            # Create a table showing features and their impacts
            table_data = [["Feature", "Impact", "Direction"]]
            
            for item in shap_data[:6]:  # Top 6 features
                feature = item.get('feature', '')
                impact = item.get('impact', 0)
                direction = item.get('direction', '')
                
                # Format impact as percentage
                impact_str = f"{abs(impact) * 100:.1f}%"
                direction_symbol = "↑ Increases Risk" if direction == 'increases' else "↓ Decreases Risk"
                
                table_data.append([feature, impact_str, direction_symbol])
            
            table = Table(table_data, colWidths=[200, 80, 150])
            table.setStyle(TableStyle([
                # Header row
                ('BACKGROUND', (0, 0), (-1, 0), self.colors['primary']),
                ('TEXTCOLOR', (0, 0), (-1, 0), white),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                # Data rows
                ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('ALIGN', (1, 0), (1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('GRID', (0, 0), (-1, -1), 0.5, self.colors['light_bg']),
                ('TOPPADDING', (0, 0), (-1, -1), 8),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
                # Alternate row colors
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, self.colors['light_bg']]),
            ]))
            
            elements.append(table)
        else:
            elements.append(Paragraph(
                "No explanation data available.",
                self.styles['ReportBodyText']
            ))
        
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_recommendation(self, data: Dict) -> List:
        elements = []
        
        elements.append(Paragraph("Clinical Recommendation", self.styles['SectionHeader']))
        
        recommendation = data.get('recommendation', 'No recommendation available.')
        
        # Create a styled recommendation box
        rec_data = [[recommendation]]
        table = Table(rec_data, colWidths=[460])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), self.colors['light_bg']),
            ('FONTNAME', (0, 0), (-1, -1), 'Helvetica'),
            ('FONTSIZE', (0, 0), (-1, -1), 11),
            ('TEXTCOLOR', (0, 0), (-1, -1), self.colors['text']),
            ('TOPPADDING', (0, 0), (-1, -1), 15),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 15),
            ('LEFTPADDING', (0, 0), (-1, -1), 15),
            ('RIGHTPADDING', (0, 0), (-1, -1), 15),
        ]))
        
        elements.append(table)
        elements.append(Spacer(1, 20))
        
        return elements
    
    def _build_footer(self, data: Dict) -> List:
        elements = []
        
        elements.append(Spacer(1, 30))
        
        # Disclaimer
        disclaimer = (
            "<b>Disclaimer:</b> This report is generated by an AI-powered diagnostic support tool "
            "and is intended to assist clinical decision-making. It should not be used as the sole "
            "basis for diagnosis. Always consult with qualified healthcare professionals for "
            "final medical decisions."
        )
        
        elements.append(Paragraph(disclaimer, ParagraphStyle(
            name='Disclaimer',
            parent=self.styles['Normal'],
            fontSize=9,
            textColor=HexColor('#6b7280'),
            spaceAfter=10,
        )))
        
        # Generated timestamp
        elements.append(Paragraph(
            f"Report generated on: {datetime.now().strftime('%B %d, %Y at %H:%M')}",
            ParagraphStyle(
                name='Timestamp',
                parent=self.styles['Normal'],
                fontSize=9,
                textColor=HexColor('#9ca3af'),
            )
        ))
        
        return elements


# Create singleton instance for use in the app
pdf_service = PDFService()