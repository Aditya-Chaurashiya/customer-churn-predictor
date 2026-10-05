import os
import sys
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ml.data_loader import DataLoader

def prepare_data():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    raw_dir = os.path.join(project_root, "data", "raw")
    processed_dir = os.path.join(project_root, "data", "processed")
    os.makedirs(processed_dir, exist_ok=True)
    
    real_path = os.path.join(raw_dir, "Telco-Customer-Churn.csv")
    synth_path = os.path.join(raw_dir, "Synthetic-Customer-Churn.csv")
    
    loader = DataLoader()
    dfs = []
    
    if os.path.exists(real_path):
        df_real = loader.load_csv(real_path)
        if 'data_source' not in df_real.columns:
            df_real['data_source'] = 'real'
        dfs.append(df_real)
        
    if os.path.exists(synth_path):
        df_synth = loader.load_csv(synth_path)
        dfs.append(df_synth)
        
    if not dfs:
        print("No raw data found. Run download_data.py first.")
        sys.exit(1)
        
    combined_df = pd.concat(dfs, ignore_index=True)
    
    report = loader.validate_schema(combined_df)
    print("Data Quality Report:")
    print(f"- Missing values: {report['missing_values']}")
    print(f"- Duplicates: {report['duplicates']}")
    
    out_path = os.path.join(processed_dir, "prepared_data.csv")
    combined_df.to_csv(out_path, index=False)
    print(f"Prepared data saved to {out_path} with {len(combined_df)} records.")

if __name__ == '__main__':
    prepare_data()
