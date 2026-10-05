import os
import torch
import pandas as pd
from typing import List, Dict, Any
from fastapi import HTTPException
import json

from ml.src.preprocess import DataPreprocessor
from ml.src.model import CustomerChurnModel

class PredictionService:
    def __init__(self):
        self.root_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        self.models_dir = os.path.join(self.root_dir, "models")
        self.model_path = os.path.join(self.models_dir, "churn_model.pt")
        self.config_path = os.path.join(self.models_dir, "feature_config.json")
        self.preprocessor_path = os.path.join(self.models_dir, "preprocessor.pkl")
        self.metadata_path = os.path.join(self.models_dir, "model_metadata.json")
        
        self.model = None
        self.preprocessor = None
        self.metadata = {}
        
        self.load_model()
        
    def load_model(self):
        if not (os.path.exists(self.model_path) and os.path.exists(self.config_path) and os.path.exists(self.preprocessor_path)):
            print("Model files not found. Skipping load.")
            return False
            
        try:
            self.preprocessor = DataPreprocessor()
            self.preprocessor.load(self.preprocessor_path, self.config_path)
            
            # Recreate model with correct input dim
            input_dim = len(self.preprocessor.feature_names)
            self.model = CustomerChurnModel(input_dim=input_dim)
            self.model.load_state_dict(torch.load(self.model_path, map_location=torch.device('cpu')))
            self.model.eval()
            
            if os.path.exists(self.metadata_path):
                with open(self.metadata_path, "r") as f:
                    self.metadata = json.load(f)
                    
            return True
        except Exception as e:
            print(f"Error loading model: {e}")
            return False
            
    def get_risk_level(self, prob: float) -> str:
        if prob < 0.30:
            return "Low Risk"
        elif prob < 0.60:
            return "Medium Risk"
        elif prob < 0.80:
            return "High Risk"
        else:
            return "Critical Risk"

    def predict_single(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not self.model or not self.preprocessor:
            if not self.load_model():
                raise HTTPException(status_code=503, detail="Model not loaded or available")
                
        df = pd.DataFrame([data])
        
        try:
            X, _ = self.preprocessor.prepare_features_and_target(df)
            X_trans = self.preprocessor.transform(X)
            
            with torch.no_grad():
                outputs = self.model(torch.FloatTensor(X_trans))
                prob = torch.sigmoid(outputs).item()
                
            return {
                "customer_id": data.get("customer_id", "Unknown"),
                "churn_probability": round(prob, 4),
                "risk_level": self.get_risk_level(prob),
                "prediction": "Likely to Churn" if prob >= 0.5 else "Retained",
                "model_version": self.metadata.get("model_version", "unknown")
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    def predict_batch(self, df: pd.DataFrame) -> List[Dict[str, Any]]:
        if not self.model or not self.preprocessor:
            if not self.load_model():
                raise HTTPException(status_code=503, detail="Model not loaded or available")
                
        try:
            df_clean = self.preprocessor.clean_data(df)
            X, _ = self.preprocessor.prepare_features_and_target(df_clean)
            X_trans = self.preprocessor.transform(X)
            
            with torch.no_grad():
                outputs = self.model(torch.FloatTensor(X_trans))
                probs = torch.sigmoid(outputs).numpy().flatten()
                
            results = []
            for i, prob in enumerate(probs):
                results.append({
                    "customer_id": df_clean.iloc[i].get("customerID", f"ROW-{i}"),
                    "churn_probability": round(float(prob), 4),
                    "risk_level": self.get_risk_level(float(prob)),
                    "prediction": "Likely to Churn" if prob >= 0.5 else "Retained",
                    "model_version": self.metadata.get("model_version", "unknown")
                })
            return results
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Batch prediction error: {str(e)}")

prediction_service = PredictionService()
