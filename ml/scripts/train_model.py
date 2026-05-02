"""
Retrain the PCOS Random Forest model and save all artifacts.
Run from the ml/ directory:  python scripts/train_model.py
"""

import pandas as pd
import numpy as np
import json
import joblib
import warnings
from pathlib import Path

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
from imblearn.over_sampling import SMOTE
import shap

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"

# Load data and config
df = pd.read_csv(DATA_DIR / "pcos_cleaned.csv")
with open(DATA_DIR / "feature_config.json", 'r') as f:
    config = json.load(f)

TARGET = config['target']
STAGE1_FEATURES = config['stage1_features']
STAGE2_FEATURES = config['stage2_features']
ALL_FEATURES = config['all_features']

print(f"Dataset: {df.shape[0]} rows x {df.shape[1]} columns")

# Prepare features and target
X = df[ALL_FEATURES]
y = df[TARGET]

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

# Scale features
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# SMOTE on training data
smote = SMOTE(random_state=42)
X_train_resampled, y_train_resampled = smote.fit_resample(X_train_scaled, y_train)
print(f"After SMOTE: {len(X_train_resampled)} training samples")

# Train Random Forest
best_model = RandomForestClassifier(n_estimators=100, max_depth=10, random_state=42)
best_model.fit(X_train_resampled, y_train_resampled)

# Evaluate
y_pred = best_model.predict(X_test_scaled)
y_pred_proba = best_model.predict_proba(X_test_scaled)[:, 1]

test_accuracy = accuracy_score(y_test, y_pred)
test_precision = precision_score(y_test, y_pred)
test_recall = recall_score(y_test, y_pred)
test_f1 = f1_score(y_test, y_pred)
test_roc_auc = roc_auc_score(y_test, y_pred_proba)

print(f"\nTest Results:")
print(f"  Accuracy:  {test_accuracy:.2%}")
print(f"  Precision: {test_precision:.2%}")
print(f"  Recall:    {test_recall:.2%}")
print(f"  F1 Score:  {test_f1:.2%}")
print(f"  ROC-AUC:   {test_roc_auc:.2%}")

# SHAP explainer
explainer = shap.TreeExplainer(best_model)

# ---- Save artifacts ----

# 1. Model
joblib.dump(best_model, MODELS_DIR / "pcos_random_forest.pkl")
print(f"\nSaved: pcos_random_forest.pkl")

# 2. Scaler
joblib.dump(scaler, MODELS_DIR / "scaler.pkl")
print(f"Saved: scaler.pkl")

# 3. Training means (for Stage 1 imputation)
training_means = X_train.mean().to_dict()
with open(MODELS_DIR / "training_means.json", 'w') as f:
    json.dump(training_means, f, indent=2)
print(f"Saved: training_means.json")

# 4. Explainer config
explainer_config = {
    'expected_value_class0': float(explainer.expected_value[0]),
    'expected_value_class1': float(explainer.expected_value[1]),
}
with open(MODELS_DIR / "explainer_config.json", 'w') as f:
    json.dump(explainer_config, f, indent=2)
print(f"Saved: explainer_config.json")

# 5. Model info
model_info = {
    'model_type': 'RandomForestClassifier',
    'accuracy': float(test_accuracy),
    'f1_score': float(test_f1),
    'roc_auc': float(test_roc_auc),
    'precision': float(test_precision),
    'recall': float(test_recall),
    'n_features': len(ALL_FEATURES),
    'stage1_features': STAGE1_FEATURES,
    'stage2_features': STAGE2_FEATURES,
    'target': TARGET,
    'training_samples': len(X_train_resampled),
    'test_samples': len(X_test),
}
with open(MODELS_DIR / "model_info.json", 'w') as f:
    json.dump(model_info, f, indent=2)
print(f"Saved: model_info.json")

print("\n" + "=" * 50)
print("ALL ARTIFACTS SAVED SUCCESSFULLY!")
print("=" * 50)
