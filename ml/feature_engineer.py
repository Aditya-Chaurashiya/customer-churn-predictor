import pandas as pd
import numpy as np
from .config import FEATURE_ENGINEERING_CONFIG

class FeatureEngineer:
    def engineer_features(self, df) -> pd.DataFrame:
        df_out = df.copy()
        
        services = ['PhoneService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        
        # service_count
        if all(s in df_out.columns for s in services):
            df_out['service_count'] = df_out[services].apply(lambda row: (row == 'Yes').sum(), axis=1)
            
        # Binary flags
        if 'InternetService' in df_out.columns:
            df_out['has_internet'] = (df_out['InternetService'] != 'No').astype(int)
        if 'PhoneService' in df_out.columns:
            df_out['has_phone'] = (df_out['PhoneService'] == 'Yes').astype(int)
        if 'OnlineSecurity' in df_out.columns:
            df_out['has_security'] = (df_out['OnlineSecurity'] == 'Yes').astype(int)
        if 'OnlineBackup' in df_out.columns:
            df_out['has_backup'] = (df_out['OnlineBackup'] == 'Yes').astype(int)
        if 'DeviceProtection' in df_out.columns:
            df_out['has_device_protection'] = (df_out['DeviceProtection'] == 'Yes').astype(int)
        if 'TechSupport' in df_out.columns:
            df_out['has_tech_support'] = (df_out['TechSupport'] == 'Yes').astype(int)
        if 'Contract' in df_out.columns:
            df_out['is_month_to_month'] = (df_out['Contract'] == 'Month-to-month').astype(int)
        if 'PaperlessBilling' in df_out.columns:
            df_out['is_paperless'] = (df_out['PaperlessBilling'] == 'Yes').astype(int)
            
        # tenure_group
        if 'tenure' in df_out.columns:
            bins = [-1, 12, 24, 48, 60, 72, np.inf]
            labels = ['0-12', '13-24', '25-48', '49-60', '61-72', '73+']
            df_out['tenure_group'] = pd.cut(df_out['tenure'], bins=bins, labels=labels).astype(str)
            
        # monthly_charges_group
        if 'MonthlyCharges' in df_out.columns:
            mc_bins = [-1, 30, 70, 100, np.inf]
            mc_labels = ['Low', 'Medium', 'High', 'Very High']
            df_out['monthly_charges_group'] = pd.cut(df_out['MonthlyCharges'], bins=mc_bins, labels=mc_labels).astype(str)
            
        # avg_monthly_charge
        if 'TotalCharges' in df_out.columns and 'tenure' in df_out.columns:
            # handle max(tenure, 1) properly
            safe_tenure = df_out['tenure'].clip(lower=1)
            # handle potential NaN in TotalCharges temporarily
            tc = df_out['TotalCharges'].fillna(0)
            df_out['avg_monthly_charge'] = tc / safe_tenure
            
        return df_out
        
    def get_feature_descriptions(self) -> dict:
        return FEATURE_ENGINEERING_CONFIG
