import pandas as pd
import numpy as np

class DataLoader:
    def load_csv(self, filepath) -> pd.DataFrame:
        df = pd.read_csv(filepath, encoding='utf-8')
        if 'TotalCharges' in df.columns:
            df['TotalCharges'] = pd.to_numeric(df['TotalCharges'].replace(r'^\s*$', np.nan, regex=True), errors='coerce')
        return df

    def validate_schema(self, df) -> dict:
        report = {
            'missing_values': df.isnull().sum().to_dict(),
            'duplicates': int(df.duplicated().sum()),
            'invalid_values': {}
        }
        return report

    def get_dataset_info(self, df) -> dict:
        info = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing_values_count': int(df.isnull().sum().sum()),
            'duplicate_ids_count': int(df['customerID'].duplicated().sum()) if 'customerID' in df.columns else 0,
            'target_distribution': df['Churn'].value_counts(normalize=True).to_dict() if 'Churn' in df.columns else {}
        }
        return info
