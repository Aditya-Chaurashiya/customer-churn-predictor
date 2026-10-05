import os
import json
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split

from .config import MODEL_HYPERPARAMETERS, SPLIT_RATIOS, RISK_THRESHOLDS
from .data_loader import DataLoader
from .preprocessor import ChurnPreprocessor
from .feature_engineer import FeatureEngineer
from .model import ChurnNet
from .trainer import ModelTrainer
from .explainer import ChurnExplainer

class MLPipeline:
    def __init__(self, config=None):
        self.config = config or MODEL_HYPERPARAMETERS
        self.data_loader = DataLoader()
        self.feature_engineer = FeatureEngineer()
        self.preprocessor = ChurnPreprocessor()
        self.model = None
        self.trainer = None
        self.explainer = None
        
    def run_full_pipeline(self, data_path) -> dict:
        # Load
        df = self.data_loader.load_csv(data_path)
        
        # Validate
        validation_report = self.data_loader.validate_schema(df)
        print("Validation report:", validation_report)
        
        # Feature Engineer
        df_engineered = self.feature_engineer.engineer_features(df)
        
        # Preprocess
        # Separate features and target
        if 'Churn' not in df_engineered.columns:
            raise ValueError("Target column 'Churn' not found in dataset.")
            
        X, y = self.preprocessor.fit_transform(df_engineered)
        feature_names = self.preprocessor.get_feature_names()
        
        # Add engineered feature names to preprocessor if needed
        # We'll just rely on preprocessor's internal names
        
        # Split (stratified)
        X_train_val, X_test, y_train_val, y_test = train_test_split(
            X, y, test_size=SPLIT_RATIOS['test'], stratify=y, random_state=42
        )
        
        val_ratio_adjusted = SPLIT_RATIOS['val'] / (SPLIT_RATIOS['train'] + SPLIT_RATIOS['val'])
        X_train, X_val, y_train, y_val = train_test_split(
            X_train_val, y_train_val, test_size=val_ratio_adjusted, stratify=y_train_val, random_state=42
        )
        
        # Train
        input_dim = X_train.shape[1]
        self.model = ChurnNet(input_dim=input_dim, hidden_layers=self.config['hidden_layers'], dropout_rate=self.config['dropout'])
        self.trainer = ModelTrainer(self.model, self.config)
        
        history = self.trainer.train(X_train, y_train, X_val, y_val)
        
        # Evaluate
        eval_metrics = self.trainer.evaluate(X_test, y_test)
        
        self.explainer = ChurnExplainer(self.model, feature_names, self.preprocessor)
        
        return {
            'history': history,
            'metrics': eval_metrics,
            'input_dim': input_dim
        }
        
    def preprocess_for_prediction(self, customer_data) -> np.ndarray:
        if isinstance(customer_data, dict):
            df = pd.DataFrame([customer_data])
        else:
            df = customer_data
            
        df_engineered = self.feature_engineer.engineer_features(df)
        X = self.preprocessor.transform(df_engineered)
        return X
        
    def predict_single(self, customer_data) -> dict:
        X = self.preprocess_for_prediction(customer_data)
        preds, probs = self.trainer.predict(X)
        prob = float(probs[0])
        
        explanations = self.explainer.explain_prediction(customer_data, prob)
        
        return {
            'churn_probability': prob,
            'risk_level': self.get_risk_level(prob),
            'prediction': int(preds[0]),
            'risk_factors': explanations['risk_factors'],
            'protective_factors': explanations['protective_factors']
        }
        
    def predict_batch(self, df) -> pd.DataFrame:
        out_df = df.copy()
        X = self.preprocess_for_prediction(df)
        preds, probs = self.trainer.predict(X)
        
        out_df['churn_probability'] = probs
        out_df['prediction'] = preds
        out_df['risk_level'] = out_df['churn_probability'].apply(self.get_risk_level)
        return out_df
        
    def get_risk_level(self, probability) -> str:
        if probability >= RISK_THRESHOLDS['high']:
            return 'Critical'
        elif probability >= RISK_THRESHOLDS['medium']:
            return 'High'
        elif probability >= RISK_THRESHOLDS['low']:
            return 'Medium'
        return 'Low'
        
    def save_artifacts(self, output_dir):
        os.makedirs(output_dir, exist_ok=True)
        self.trainer.save_model(os.path.join(output_dir, 'model.pt'))
        self.preprocessor.save(os.path.join(output_dir, 'preprocessor.joblib'))
        
        with open(os.path.join(output_dir, 'feature_config.json'), 'w') as f:
            json.dump(self.feature_engineer.get_feature_descriptions(), f)
            
    def load_artifacts(self, artifacts_dir, input_dim):
        self.preprocessor = ChurnPreprocessor.load(os.path.join(artifacts_dir, 'preprocessor.joblib'))
        self.model = ChurnNet(input_dim=input_dim, hidden_layers=self.config['hidden_layers'], dropout_rate=self.config['dropout'])
        self.trainer = ModelTrainer.load_model(os.path.join(artifacts_dir, 'model.pt'), input_dim, self.config, ChurnNet)
        self.explainer = ChurnExplainer(self.model, self.preprocessor.get_feature_names(), self.preprocessor)
