import os
import sys
import requests
import pandas as pd

# Add project root to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def download_data():
    url = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(data_dir, exist_ok=True)
    
    file_path = os.path.join(data_dir, "Telco-Customer-Churn.csv")
    
    print(f"Downloading dataset from {url}...")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(response.text)
            
        print(f"Dataset downloaded successfully to {file_path}")
        
        df = pd.read_csv(file_path)
        print(f"Dataset Info:\nRows: {len(df)}\nColumns: {len(df.columns)}")
        
    except Exception as e:
        print(f"Error downloading data: {e}")
        sys.exit(1)

if __name__ == '__main__':
    download_data()
