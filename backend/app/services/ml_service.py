import joblib
import json
import numpy as np
import pandas as pd
from pathlib import Path
from typing import Dict, List, Any, Optional
import shap


class MLService:
    def __init__(self):
        self.model = None
        self.scaler = None
        self.training_means = None
        self.explainer = None
        self.feature_names = None
        self.model_info = None
        self._load_artifacts()
    
    def _load_artifacts(self):
        # Path to ML artifacts (relative to backend folder)
        ml_dir = Path(__file__).parent.parent.parent.parent / "ml" / "models"
        
        try:
            # Load model
            self.model = joblib.load(ml_dir / "pcos_random_forest.pkl")
            
            # Load scaler
            self.scaler = joblib.load(ml_dir / "scaler.pkl")
            
            # Load training means for imputation
            with open(ml_dir / "training_means.json", 'r') as f:
                self.training_means = json.load(f)
            
            # Load model info
            with open(ml_dir / "model_info.json", 'r') as f:
                self.model_info = json.load(f)
            
            self.feature_names = list(self.training_means.keys())
            
            # Create SHAP explainer
            self.explainer = shap.TreeExplainer(self.model)
            
            print("ML Service: All artifacts loaded successfully")
            
        except Exception as e:
            print(f"ML Service: Failed to load artifacts - {e}")
            raise
    
    def predict_stage1(self, input_data: Dict) -> Dict[str, Any]:
        # Build feature vector
        features = self._build_feature_vector(input_data, is_stage2=False)
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict
        probability = self.model.predict_proba(features_scaled)[0][1]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(features_scaled)
        shap_values_pcos = shap_values[:, :, 1][0]  # PCOS class
        
        # Build response
        return self._build_response(probability, shap_values_pcos, features, is_stage2=False, input_data=input_data)
    
    def predict_stage2(self, input_data: Dict) -> Dict[str, Any]:
        # Build feature vector with real clinical values
        features = self._build_feature_vector(input_data, is_stage2=True)
        
        # Scale features
        features_scaled = self.scaler.transform([features])
        
        # Predict
        probability = self.model.predict_proba(features_scaled)[0][1]
        
        # Get SHAP values
        shap_values = self.explainer.shap_values(features_scaled)
        shap_values_pcos = shap_values[:, :, 1][0]
        
        # Build response
        return self._build_response(probability, shap_values_pcos, features, is_stage2=True, input_data=input_data)
    
    # Build the feature vector, imputing missing values for Stage 1
    def _build_feature_vector(self, input_data: Dict, is_stage2: bool) -> List[float]:
        features = []
        
        # Calculate BMI if not provided
        if 'bmi' not in input_data and 'weight' in input_data and 'height' in input_data:
            input_data['bmi'] = input_data['weight'] / ((input_data['height'] / 100) ** 2)

        # Calculate FSH/LH ratio if both values provided
        lh_value = input_data.get('lh')
        fsh_value = input_data.get('fsh')
        if fsh_value is not None and lh_value is not None and lh_value > 0:
            input_data['fsh_lh_ratio'] = fsh_value / lh_value

        # Calculate waist:hip ratio if both values provided
        waist_value = input_data.get('waist')
        hip_value = input_data.get('hip')
        if waist_value is not None and hip_value is not None and hip_value > 0:
            input_data['waist_hip_ratio'] = waist_value / hip_value

        
        # Map input field names to training feature names
        field_mapping = {
            'age': 'Age (yrs)',
            'weight': 'Weight (Kg)',
            'height': 'Height(Cm)',
            'bmi': 'BMI',
            'cycle_regularity': 'Cycle(R/I)',
            'cycle_length': 'Cycle length(days)',
            'weight_gain': 'Weight gain(Y/N)',
            'hair_growth': 'hair growth(Y/N)',
            'skin_darkening': 'Skin darkening (Y/N)',
            'hair_loss': 'Hair loss(Y/N)',
            'pimples': 'Pimples(Y/N)',
            'fast_food': 'Fast food (Y/N)',
            'regular_exercise': 'Reg.Exercise(Y/N)',
            'marriage_years': 'Marraige Status (Yrs)',
            'pregnant': 'Pregnant(Y/N)',
            'num_abortions': 'No. of aborptions',
            'fsh': 'FSH(mIU/mL)',
            'lh': 'LH(mIU/mL)',
            'amh': 'AMH(ng/mL)',
            'tsh': 'TSH (mIU/L)',
            'prl': 'PRL(ng/mL)',
            'prg': 'PRG(ng/mL)',
            'follicle_l': 'Follicle No. (L)',
            'follicle_r': 'Follicle No. (R)',
            'avg_f_size_l': 'Avg. F size (L) (mm)',
            'avg_f_size_r': 'Avg. F size (R) (mm)',
            'endometrium': 'Endometrium (mm)',
            'vit_d3': 'Vit D3 (ng/mL)',
            'hb': 'Hb(g/dl)',
            'rbs': 'RBS(mg/dl)',
            'blood_group': 'Blood Group',
            'pulse_rate': 'Pulse rate(bpm)',
            'respiratory_rate': 'RR (breaths/min)',
            'hip': 'Hip(inch)',
            'waist': 'Waist(inch)',
            'waist_hip_ratio': 'Waist:Hip Ratio',
            'bp_systolic': 'BP _Systolic (mmHg)',
            'bp_diastolic': 'BP _Diastolic (mmHg)',
        }
        
        # Build feature vector in correct order
        for feature_name in self.feature_names:
            # Find the input key for this feature
            input_key = None
            for key, mapped_name in field_mapping.items():
                if mapped_name == feature_name:
                    input_key = key
                    break
            
            if input_key and input_key in input_data and input_data[input_key] is not None:
                features.append(float(input_data[input_key]))
            else:
                # Impute with training mean
                features.append(self.training_means.get(feature_name, 0))
        
        return features
        
    # Generate detailed clinical recommendations based on risk level and stage.
    def _get_detailed_recommendation(self, risk_level: str, is_stage2: bool) -> str:
        if is_stage2:
            if risk_level == "HIGH":
                return (
                    "CONFIRMED PCOS DIAGNOSIS: Patient meets diagnostic criteria for PCOS. "
                    "Recommend comprehensive treatment plan including lifestyle modifications, "
                    "hormonal therapy consideration, and regular follow-up monitoring. "
                    "Evaluate for insulin resistance (HOMA-IR). Screen for metabolic syndrome. "
                    "Consider referral to endocrinologist. Discuss fertility planning if applicable."
                )
            elif risk_level == "MODERATE":
                return (
                    "BORDERLINE RESULT: Patient shows some indicators but does not fully meet "
                    "PCOS criteria. Recommend continued monitoring and repeat assessment in 3-6 months. "
                    "Consider lifestyle modifications (diet, exercise). Follow-up appointment recommended."
                )
            else:
                return (
                    "LOW RISK CONFIRMED: Clinical data does not support PCOS diagnosis. "
                    "Continue routine health monitoring. Consider other differential diagnoses if symptoms persist."
                )
        else:
            if risk_level == "HIGH":
                return (
                    "HIGH RISK - PRESUMPTIVE: Strong indicators suggest PCOS. "
                    "ACTION: Refer for confirmatory ultrasound and hormonal panel (FSH, LH, AMH). "
                    "Evaluate for insulin resistance. Screen for metabolic syndrome."
                )
            elif risk_level == "MODERATE":
                return (
                    "MODERATE RISK - INCONCLUSIVE: Some indicators present but insufficient for diagnosis. "
                    "ACTION: Consider ultrasound examination and hormonal testing. "
                    "Monitor symptoms for 3-6 months before reassessment."
                )
            else:
                return (
                    "LOW RISK: No significant PCOS indicators detected based on symptoms and vitals. "
                    "Continue routine health monitoring. Return if new symptoms develop."
                )
    
    # Build the API response with SHAP explanation.
    def _build_response(self, probability: float, shap_values: np.ndarray, 
                    features: List[float], is_stage2: bool, 
                    input_data: Dict = None) -> Dict[str, Any]:
    
        # Determine risk level
        if probability > 0.7:
            risk_level = "HIGH"
        elif probability > 0.3:
            risk_level = "MODERATE"
        else:
            risk_level = "LOW"

        # Get personalized recommendation (NEW!)
        recommendation = self._get_personalized_recommendation(
            risk_level=risk_level,
            probability=probability,
            is_stage2=is_stage2,
            input_data=input_data or {},
            shap_data=None  # Will add after SHAP processing
        )
        
        # Build SHAP chart data (top 8 features)
        shap_data = []
        indices = np.argsort(np.abs(shap_values))[::-1][:8]
        
        for idx in indices:
            shap_data.append({
                'feature': self.feature_names[idx],
                'impact': round(float(shap_values[idx]), 4),
                'direction': 'increases' if shap_values[idx] > 0 else 'decreases',
                'value': round(features[idx], 2),
                'color': '#fb6f92' if shap_values[idx] > 0 else '#38b000'
            })
        
        # Now update recommendation with SHAP context
        recommendation = self._get_personalized_recommendation(
            risk_level=risk_level,
            probability=probability,
            is_stage2=is_stage2,
            input_data=input_data or {},
            shap_data=shap_data
        )
        
        return {
            'probability': float(round(probability, 4)),
            'risk_level': risk_level,
            'is_confirmed': is_stage2,
            'recommendation': recommendation,
            'shap_chart_data': shap_data
        }
    
    def _get_personalized_recommendation(
        self, 
        risk_level: str, 
        probability: float,
        is_stage2: bool, 
        input_data: Dict,
        shap_data: List[Dict] = None
    ) -> str:
        
        sections = []
        
        # BASE RECOMMENDATION (keep existing logic)
        base = self._get_detailed_recommendation(risk_level, is_stage2)
        sections.append(base)
        
        # UNCERTAINTY LANGUAGE (based on probability confidence)
        uncertainty = self._get_uncertainty_context(probability, risk_level)
        if uncertainty:
            sections.append(uncertainty)
        
        # AGE CONTEXT
        age = input_data.get('age')
        age_context = self._get_age_context(age, risk_level)
        if age_context:
            sections.append(age_context)
        
        # SYMPTOM-SPECIFIC GUIDANCE
        symptom_context = self._get_symptom_context(input_data, shap_data)
        if symptom_context:
            sections.append(symptom_context)
        
        return " | ".join(sections)


    def _get_uncertainty_context(self, probability: float, risk_level: str) -> str:
        
        # High confidence zones
        if probability > 0.85:
            return "CONFIDENCE: HIGH - Strong model certainty in this assessment."
        elif probability < 0.15:
            return "CONFIDENCE: HIGH - Strong model certainty in low-risk classification."
        
        # Moderate/borderline zones - acknowledge uncertainty
        elif 0.4 <= probability <= 0.6:
            return (
                "CONFIDENCE: BORDERLINE - Probability near decision threshold (50%). "
                "Clinical judgment is especially important. Consider additional testing."
            )
        elif 0.25 <= probability < 0.4:
            return (
                "CONFIDENCE: MODERATE - Some indicators present but below threshold. "
                "Monitor for symptom progression."
            )
        elif 0.6 < probability <= 0.75:
            return (
                "CONFIDENCE: MODERATE - Elevated risk but not conclusive. "
                "Recommend confirmatory testing."
            )
        
        return ""


    def _get_age_context(self, age: float, risk_level: str) -> str:
        if age is None:
            return ""
        
        if age < 18:
            return (
                "AGE CONSIDERATION (Adolescent): PCOS diagnosis requires caution in adolescents. "
                "Irregular cycles may be normal during pubertal maturation. "
                "Consider waiting 2+ years post-menarche before definitive diagnosis. "
                "Focus on lifestyle counseling and symptom management."
            )
        elif 18 <= age <= 25:
            return (
                "AGE CONSIDERATION (Young Adult): Early reproductive years. "
                "Lifestyle intervention is first-line treatment. "
                "Screen for metabolic syndrome."
                "Discuss fertility planning early if relevant. "
            )
        elif 25 < age <= 35:
            return (
                "AGE CONSIDERATION (Reproductive Age): If planning pregnancy, discuss fertility options. "
                "Strongly recommend metabolic screening (glucose, lipids). "
                "Consider insulin sensitizers if metabolic dysfunction present."
            )
        elif 35 < age <= 45:
            return (
                "AGE CONSIDERATION (Late Reproductive): Increased cardiometabolic risk. "
                "Annual screening for type 2 diabetes and cardiovascular risk factors. "
                "Discuss long-term health management beyond fertility."
            )
        else:  # > 45
            return (
                "AGE CONSIDERATION (Perimenopause/Menopause): PCOS symptoms may change. "
                "Focus shifts to cardiometabolic health and cancer screening. "
                "Continue lifestyle management and metabolic monitoring."
            )


    def _get_symptom_context(self, input_data: Dict, shap_data: List[Dict] = None) -> str: 
        symptom_notes = []
        
        # Check for metabolic pattern
        bmi = input_data.get('bmi')
        weight_gain = input_data.get('weight_gain')
        fast_food = input_data.get('fast_food')
        exercise = input_data.get('regular_exercise')
        
        metabolic_flags = sum([
            bmi and bmi > 25,
            weight_gain == 1,
            fast_food == 1,
            exercise == 0
        ])
        
        if metabolic_flags >= 2:
            symptom_notes.append(
                "METABOLIC PATTERN DETECTED: Elevated BMI and/or lifestyle factors present. "
                "Priority: Weight management, dietary intervention, physical activity program. "
                "Screen for insulin resistance (fasting glucose, HbA1c, HOMA-IR)."
            )
        
        # Check for hyperandrogenic pattern
        hair_growth = input_data.get('hair_growth')
        hair_loss = input_data.get('hair_loss')
        pimples = input_data.get('pimples')
        skin_darkening = input_data.get('skin_darkening')
        
        androgen_flags = sum([
            hair_growth == 1,
            hair_loss == 1,
            pimples == 1,
            skin_darkening == 1
        ])
        
        if androgen_flags >= 2:
            symptom_notes.append(
                "HYPERANDROGENIC PATTERN DETECTED: Multiple androgen-related symptoms. "
                "Consider hormonal therapy (anti-androgens, combined OCP if appropriate). "
                "Dermatology referral may benefit patient quality of life."
            )
        
        # Check for reproductive pattern
        cycle_regularity = input_data.get('cycle_regularity')
        cycle_length = input_data.get('cycle_length')
        
        if cycle_regularity == 1 or (cycle_length and cycle_length > 35):
            symptom_notes.append(
                "MENSTRUAL IRREGULARITY NOTED: Oligo-ovulation likely present. "
                "If fertility desired, discuss ovulation induction options. "
                "Endometrial protection important - consider cyclic progesterone or OCP."
            )
        
        # Combine symptom notes
        if symptom_notes:
            return " ".join(symptom_notes)
        
        return ""


# Singleton instance
ml_service = MLService()