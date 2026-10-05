import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, OneHotEncoder, StandardScaler

class ChurnPreprocessor:
    def __init__(self):
        self.binary_cols = ['gender', 'Partner', 'Dependents', 'PhoneService', 'PaperlessBilling', 'Churn']
        self.multi_cols = ['MultipleLines', 'InternetService', 'OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies', 'Contract', 'PaymentMethod']
        self.num_cols = ['tenure', 'MonthlyCharges', 'TotalCharges']
        
        self.label_encoders = {}
        self.onehot_encoder = OneHotEncoder(handle_unknown='ignore', sparse_output=False)
        self.scaler = StandardScaler()
        self.fitted = False
        self.feature_names_ = []
        self.median_total_charges = 0.0
        
    def _clean_data(self, df):
        df_clean = df.copy()
        
        # Replace No phone/internet service with No
        replace_cols = ['OnlineSecurity', 'OnlineBackup', 'DeviceProtection', 'TechSupport', 'StreamingTV', 'StreamingMovies']
        for col in replace_cols:
            if col in df_clean.columns:
                df_clean[col] = df_clean[col].replace('No internet service', 'No')
        if 'MultipleLines' in df_clean.columns:
            df_clean['MultipleLines'] = df_clean['MultipleLines'].replace('No phone service', 'No')
            
        return df_clean
        
    def fit(self, df):
        df_clean = self._clean_data(df)
        
        # Handle TotalCharges NaN
        if 'TotalCharges' in df_clean.columns:
            self.median_total_charges = df_clean['TotalCharges'].median()
            
        # Fit LabelEncoders
        for col in self.binary_cols:
            if col in df_clean.columns:
                le = LabelEncoder()
                le.fit(df_clean[col].astype(str))
                self.label_encoders[col] = le
                
        # Fit OneHotEncoder
        avail_multi = [c for c in self.multi_cols if c in df_clean.columns]
        if avail_multi:
            self.onehot_encoder.fit(df_clean[avail_multi].astype(str))
            
        # Fit StandardScaler
        avail_num = [c for c in self.num_cols if c in df_clean.columns]
        if avail_num:
            df_clean[avail_num] = df_clean[avail_num].fillna(self.median_total_charges if 'TotalCharges' in avail_num else 0)
            self.scaler.fit(df_clean[avail_num])
            
        self.fitted = True
        
        # Store feature names
        self.feature_names_ = []
        for col in self.binary_cols:
            if col in df_clean.columns and col != 'Churn':
                self.feature_names_.append(col)
        if avail_multi:
            self.feature_names_.extend(list(self.onehot_encoder.get_feature_names_out(avail_multi)))
        self.feature_names_.extend(avail_num)
        
        return self
        
    def transform(self, df):
        if not self.fitted:
            raise ValueError("Preprocessor not fitted yet.")
            
        df_clean = self._clean_data(df)
        out_dfs = []
        
        # Binary
        bin_data = {}
        for col in self.binary_cols:
            if col in df_clean.columns:
                le = self.label_encoders[col]
                # Handle unseen labels by mapping them to majority class or 'No' equivalent (simplified via mapping fallback)
                known_classes = set(le.classes_)
                safe_col = df_clean[col].astype(str).apply(lambda x: x if x in known_classes else le.classes_[0])
                bin_data[col] = le.transform(safe_col)
        
        bin_df = pd.DataFrame(bin_data, index=df_clean.index)
        # Separate features from target if target exists
        feature_bin_cols = [c for c in bin_df.columns if c != 'Churn']
        if feature_bin_cols:
            out_dfs.append(bin_df[feature_bin_cols])
            
        # Multi-class
        avail_multi = [c for c in self.multi_cols if c in df_clean.columns]
        if avail_multi:
            multi_trans = self.onehot_encoder.transform(df_clean[avail_multi].astype(str))
            multi_df = pd.DataFrame(multi_trans, columns=self.onehot_encoder.get_feature_names_out(avail_multi), index=df_clean.index)
            out_dfs.append(multi_df)
            
        # Numerical
        avail_num = [c for c in self.num_cols if c in df_clean.columns]
        if avail_num:
            num_data = df_clean[avail_num].copy()
            if 'TotalCharges' in num_data.columns:
                num_data['TotalCharges'] = num_data['TotalCharges'].fillna(self.median_total_charges)
            num_data = num_data.fillna(0)
            num_trans = self.scaler.transform(num_data)
            num_df = pd.DataFrame(num_trans, columns=avail_num, index=df_clean.index)
            out_dfs.append(num_df)
            
        if not out_dfs:
            return np.array([])
            
        X = pd.concat(out_dfs, axis=1)
        
        if 'Churn' in bin_df.columns:
            return X, bin_df['Churn'].values
        return X
        
    def fit_transform(self, df):
        return self.fit(df).transform(df)
        
    def save(self, filepath):
        joblib.dump(self, filepath)
        
    @classmethod
    def load(cls, filepath):
        return joblib.load(filepath)
        
    def get_feature_names(self) -> list:
        return self.feature_names_
