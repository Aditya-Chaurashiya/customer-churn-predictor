import pandas as pd
import numpy as np
import json
import os
import joblib

class DataPreprocessor:
    def __init__(self):
        self.num_cols = []
        self.cat_cols = []
        self.feature_names = []
        self.means = {}
        self.stds = {}
        self.categories = {}
    
    def load_data(self, real_path, synthetic_path=None):
        df_real = pd.read_csv(real_path)
        if "data_source" not in df_real.columns:
            df_real["data_source"] = "real"
            
        df = df_real.copy()
        
        if synthetic_path and os.path.exists(synthetic_path):
            df_synth = pd.read_csv(synthetic_path)
            if "data_source" not in df_synth.columns:
                df_synth["data_source"] = "synthetic"
            df = pd.concat([df_real, df_synth], ignore_index=True)
            
        return df

    def clean_data(self, df):
        df["TotalCharges"] = pd.to_numeric(df["TotalCharges"].replace(" ", ""), errors="coerce")
        df["TotalCharges"] = df["TotalCharges"].fillna(0)
        df = df.drop_duplicates(subset=["customerID"], keep="first")
        return df

    def engineer_features(self, df):
        return df.copy()

    def prepare_features_and_target(self, df):
        if "Churn" not in df.columns:
            return df, None
            
        X = df.drop(columns=["customerID", "Churn", "data_source"], errors="ignore")
        y = (df["Churn"] == "Yes").astype(int)
        return X, y

    def fit(self, X):
        self.num_cols = ["tenure", "MonthlyCharges", "TotalCharges"]
        self.cat_cols = [col for col in X.columns if col not in self.num_cols]
        
        for col in self.num_cols:
            self.means[col] = X[col].mean()
            self.stds[col] = X[col].std() if X[col].std() != 0 else 1.0
            
        self.feature_names = list(self.num_cols)
        
        for col in self.cat_cols:
            cats = list(X[col].unique())
            # Drop first for one-hot encoding
            if len(cats) > 1:
                cats = cats[1:]
            self.categories[col] = cats
            for c in cats:
                self.feature_names.append(f"{col}_{c}")
                
        return self

    def transform(self, X):
        X_out = pd.DataFrame(index=X.index)
        
        for col in self.num_cols:
            X_out[col] = (X[col] - self.means[col]) / self.stds[col]
            
        for col in self.cat_cols:
            for c in self.categories[col]:
                X_out[f"{col}_{c}"] = (X[col] == c).astype(float)
                
        return X_out.values

    def fit_transform(self, X):
        self.fit(X)
        return self.transform(X)
        
    def save(self, filepath, config_path):
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        
        # Convert numpy types to python native types
        def convert_to_native(obj):
            if isinstance(obj, dict):
                return {k: convert_to_native(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_native(i) for i in obj]
            elif isinstance(obj, (np.integer, np.int64)):
                return int(obj)
            elif isinstance(obj, (np.floating, np.float64, np.float32)):
                return float(obj)
            elif isinstance(obj, np.ndarray):
                return convert_to_native(obj.tolist())
            return obj

        config = {
            "num_cols": self.num_cols,
            "cat_cols": self.cat_cols,
            "feature_names": self.feature_names,
            "means": self.means,
            "stds": self.stds,
            "categories": self.categories
        }
        
        with open(config_path, "w") as f:
            json.dump(convert_to_native(config), f, indent=4)
            
        import pickle
        with open(filepath, "wb") as f:
            pickle.dump("dummy", f)
            
    def load(self, filepath, config_path):
        with open(config_path, "r") as f:
            config = json.load(f)
            self.num_cols = config["num_cols"]
            self.cat_cols = config["cat_cols"]
            self.feature_names = config["feature_names"]
            self.means = config["means"]
            self.stds = config["stds"]
            self.categories = config["categories"]

def split_data(X, y, test_size=0.2, val_size=0.1):
    # Pure numpy split
    np.random.seed(42)
    indices = np.random.permutation(len(X))
    
    val_count = int(len(X) * val_size)
    test_count = int(len(X) * test_size)
    
    val_idx = indices[:val_count]
    test_idx = indices[val_count:val_count+test_count]
    train_idx = indices[val_count+test_count:]
    
    X_train, y_train = X.iloc[train_idx], y[train_idx]
    X_val, y_val = X.iloc[val_idx], y[val_idx]
    X_test, y_test = X.iloc[test_idx], y[test_idx]
    
    return X_train, X_val, X_test, y_train, y_val, y_test
