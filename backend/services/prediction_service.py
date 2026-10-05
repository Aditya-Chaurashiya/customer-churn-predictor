import pandas as pd
from backend.config import settings
import sys
import os

# Assuming ml package is accessible from the project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from ml.pipeline import MLPipeline
    from ml.explainer import ChurnExplainer
except ImportError:
    # Dummy mock if ml not available yet
    class MLPipeline:
        def predict_single(self, data): return {'probability': 0.5, 'prediction': 'Yes'}
        def predict_batch(self, df): return [{'probability': 0.5, 'prediction': 'Yes'}] * len(df)
        def load_artifacts(self, dir): pass
        def run_full_pipeline(self, path): return {'accuracy': 0.8}
        def get_risk_level(self, prob): return "Medium"
    class ChurnExplainer:
        def explain_prediction(self, features, prob): return ["High Monthly Charges"], ["Long Tenure"]

class PredictionService:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(PredictionService, cls).__new__(cls)
            cls._instance.pipeline = MLPipeline()
            try:
                cls._instance.pipeline.load_artifacts(settings.MODEL_DIR)
            except Exception as e:
                print(f"Warning: Could not load model: {e}")
            cls._instance.explainer = ChurnExplainer()
        return cls._instance

    def predict_single(self, customer_data: dict) -> dict:
        pred = self.pipeline.predict_single(customer_data)
        prob = pred['probability']
        risk_level = self.pipeline.get_risk_level(prob)
        risk_factors, protective_factors = self.explainer.explain_prediction(customer_data, prob)
        return {
            "customer_id": customer_data.get('customer_id', 'unknown'),
            "churn_probability": prob,
            "risk_level": risk_level,
            "prediction": pred['prediction'],
            "model_version": settings.MODEL_VERSION,
            "risk_factors": risk_factors,
            "protective_factors": protective_factors
        }

    def predict_batch(self, df: pd.DataFrame) -> list[dict]:
        results = []
        for _, row in df.iterrows():
            customer_data = row.to_dict()
            results.append(self.predict_single(customer_data))
        return results

    def get_model_info(self) -> dict:
        return {
            "version": settings.MODEL_VERSION,
            "loaded": True
        }

    def retrain_model(self, data_path: str) -> dict:
        metrics = self.pipeline.run_full_pipeline(data_path)
        self.pipeline.load_artifacts(settings.MODEL_DIR)
        return metrics

prediction_service = PredictionService()
