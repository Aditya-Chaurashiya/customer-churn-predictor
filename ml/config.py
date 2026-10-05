import os

FEATURES = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'tenure',
    'PhoneService', 'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV',
    'StreamingMovies', 'Contract', 'PaperlessBilling', 'PaymentMethod',
    'MonthlyCharges', 'TotalCharges'
]

CATEGORICAL_FEATURES = [
    'gender', 'SeniorCitizen', 'Partner', 'Dependents', 'PhoneService',
    'MultipleLines', 'InternetService', 'OnlineSecurity',
    'OnlineBackup', 'DeviceProtection', 'TechSupport',
    'StreamingTV', 'StreamingMovies', 'Contract',
    'PaperlessBilling', 'PaymentMethod'
]

NUMERICAL_FEATURES = ['tenure', 'MonthlyCharges', 'TotalCharges']

TARGET_COLUMN = 'Churn'

MODEL_HYPERPARAMETERS = {
    'learning_rate': 0.001,
    'batch_size': 64,
    'epochs': 100,
    'hidden_layers': [128, 64, 32],
    'dropout': 0.3
}

EARLY_STOPPING_PATIENCE = 10
RANDOM_SEED = 42
SPLIT_RATIOS = {'train': 0.7, 'val': 0.15, 'test': 0.15}
RISK_THRESHOLDS = {'low': 0.3, 'medium': 0.6, 'high': 0.8}

FEATURE_ENGINEERING_CONFIG = {
    'service_count': 'Count of Yes values across PhoneService, OnlineSecurity, OnlineBackup, DeviceProtection, TechSupport, StreamingTV, StreamingMovies',
    'has_internet': "1 if InternetService != 'No' else 0",
    'has_phone': "1 if PhoneService == 'Yes' else 0",
    'has_security': "1 if OnlineSecurity == 'Yes' else 0",
    'has_backup': "1 if OnlineBackup == 'Yes' else 0",
    'has_device_protection': "1 if DeviceProtection == 'Yes' else 0",
    'has_tech_support': "1 if TechSupport == 'Yes' else 0",
    'is_month_to_month': "1 if Contract == 'Month-to-month' else 0",
    'is_paperless': "1 if PaperlessBilling == 'Yes' else 0",
    'tenure_group': 'bin tenure into groups (0-12, 13-24, 25-48, 49-60, 61-72)',
    'monthly_charges_group': 'bin into Low/Medium/High/Very High',
    'avg_monthly_charge': 'TotalCharges / max(tenure, 1)'
}
