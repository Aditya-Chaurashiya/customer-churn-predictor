import os
import sys
import argparse
import numpy as np
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def generate_synthetic(rows):
    np.random.seed(42)
    data = {}
    
    # Generate customerIDs
    data['customerID'] = [f"SYN-{i:04d}-{np.random.randint(1000, 9999)}" for i in range(rows)]
    
    # Categorical distributions (approx)
    data['gender'] = np.random.choice(['Male', 'Female'], rows)
    data['SeniorCitizen'] = np.random.choice([0, 1], rows, p=[0.8, 0.2])
    data['Partner'] = np.random.choice(['Yes', 'No'], rows)
    data['Dependents'] = np.random.choice(['Yes', 'No'], rows, p=[0.3, 0.7])
    
    data['PhoneService'] = np.random.choice(['Yes', 'No'], rows, p=[0.9, 0.1])
    data['MultipleLines'] = np.random.choice(['Yes', 'No', 'No phone service'], rows)
    data['InternetService'] = np.random.choice(['DSL', 'Fiber optic', 'No'], rows, p=[0.35, 0.45, 0.2])
    
    services = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
    for svc in services:
        data[svc] = np.random.choice(['Yes', 'No', 'No internet service'], rows)
        
    data['Contract'] = np.random.choice(['Month-to-month', 'One year', 'Two year'], rows, p=[0.55, 0.2, 0.25])
    data['PaperlessBilling'] = np.random.choice(['Yes', 'No'], rows, p=[0.6, 0.4])
    data['PaymentMethod'] = np.random.choice(['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)'], rows)
    
    # Numerical features
    data['tenure'] = np.random.randint(0, 73, rows)
    data['MonthlyCharges'] = np.round(np.random.uniform(18.0, 120.0, rows), 2)
    data['TotalCharges'] = np.round(data['tenure'] * data['MonthlyCharges'], 2)
    data['TotalCharges'] = data['TotalCharges'].astype(str) # Match raw blank/string formats
    
    # Target
    data['Churn'] = np.random.choice(['Yes', 'No'], rows, p=[0.25, 0.75])
    
    df = pd.DataFrame(data)
    df['data_source'] = 'synthetic'
    return df

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate synthetic customer data")
    parser.add_argument("--rows", type=int, default=3000, help="Number of rows to generate")
    args = parser.parse_args()
    
    df = generate_synthetic(args.rows)
    
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(project_root, "data", "raw")
    os.makedirs(data_dir, exist_ok=True)
    
    out_path = os.path.join(data_dir, "Synthetic-Customer-Churn.csv")
    df.to_csv(out_path, index=False)
    print(f"Generated {args.rows} synthetic records at {out_path}")
