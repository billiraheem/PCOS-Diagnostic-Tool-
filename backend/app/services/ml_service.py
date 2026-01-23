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
            
            self.feature_names = self.model_info['stage1_features'] + self.model_info['stage2_features']
            
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
        return self._build_response(probability, shap_values_pcos, features, is_stage2=False)
    
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
        return self._build_response(probability, shap_values_pcos, features, is_stage2=True)
    
    # Build the feature vector, imputing missing values for Stage 1
    def _build_feature_vector(self, input_data: Dict, is_stage2: bool) -> List[float]:
        features = []
        
        # Calculate BMI if not provided
        if 'bmi' not in input_data and 'weight' in input_data and 'height' in input_data:
            input_data['bmi'] = input_data['weight'] / ((input_data['height'] / 100) ** 2)
        
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
            'fsh': 'FSH(mIU/mL)',
            'lh': 'LH(mIU/mL)',
            'amh': 'AMH(ng/mL)',
            'tsh': 'TSH (mIU/L)',
            'follicle_l': 'Follicle No. (L)',
            'follicle_r': 'Follicle No. (R)',
            'avg_f_size_l': 'Avg. F size (L) (mm)',
            'avg_f_size_r': 'Avg. F size (R) (mm)',
            'endometrium': 'Endometrium (mm)',
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
    
    # Build the API response with SHAP explanation.
    def _build_response(self, probability: float, shap_values: np.ndarray, features: List[float], is_stage2: bool) -> Dict[str, Any]:
        
        # Determine risk level
        if probability > 0.7:
            risk_level = "HIGH"
            recommendation = "High risk of PCOS. Recommend comprehensive evaluation and specialist referral."
        elif probability > 0.3:
            risk_level = "MODERATE"
            recommendation = "Moderate risk. Consider additional testing and lifestyle modifications."
        else:
            risk_level = "LOW"
            recommendation = "Low risk. Continue regular health monitoring."
        
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
        
        return {
            'probability': round(probability, 4),
            'risk_level': risk_level,
            'is_confirmed': is_stage2,
            'recommendation': recommendation,
            'shap_chart_data': shap_data
        }


# Singleton instance
ml_service = MLService()