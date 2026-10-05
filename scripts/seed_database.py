import os
import sys
import pandas as pd
from datetime import datetime
import json
import logging

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import engine, Base, SessionLocal
from backend.app.models.models import Customer, Prediction, ModelVersion
from ml.src.preprocess import DataPreprocessor
from ml.src.model import CustomerChurnModel
import torch

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_risk_level(prob):
    if prob < 0.30:
        return "Low Risk"
    elif prob < 0.60:
        return "Medium Risk"
    elif prob < 0.80:
        return "High Risk"
    else:
        return "Critical Risk"

def seed_database():
    logging.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # 1. Load Data
        root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        real_data_path = os.path.join(root_dir, "data", "raw", "Telco-Customer-Churn.csv")
        synth_data_path = os.path.join(root_dir, "data", "raw", "Synthetic-Customer-Churn.csv")
        
        preprocessor = DataPreprocessor()
        df = preprocessor.load_data(real_data_path, synth_data_path)
        
        logging.info(f"Loaded {len(df)} records. Cleaning data...")
        df_clean = preprocessor.clean_data(df)
        
        # 2. Insert Customers
        logging.info("Inserting customers into database...")
        # Clear existing
        db.query(Customer).delete()
        db.query(Prediction).delete()
        db.commit()
        
        customers_to_insert = []
        for _, row in df_clean.iterrows():
            customer = Customer(
                customer_id=row["customerID"],
                gender=row["gender"],
                senior_citizen=row["SeniorCitizen"],
                partner=row["Partner"],
                dependents=row["Dependents"],
                tenure=row["tenure"],
                phone_service=row["PhoneService"],
                multiple_lines=row["MultipleLines"],
                internet_service=row["InternetService"],
                online_security=row["OnlineSecurity"],
                online_backup=row["OnlineBackup"],
                device_protection=row["DeviceProtection"],
                tech_support=row["TechSupport"],
                streaming_tv=row["StreamingTV"],
                streaming_movies=row["StreamingMovies"],
                contract=row["Contract"],
                paperless_billing=row["PaperlessBilling"],
                payment_method=row["PaymentMethod"],
                monthly_charges=row["MonthlyCharges"],
                total_charges=row["TotalCharges"],
                data_source=row.get("data_source", "real")
            )
            customers_to_insert.append(customer)
            
            if len(customers_to_insert) >= 1000:
                db.bulk_save_objects(customers_to_insert)
                customers_to_insert = []
                
        if customers_to_insert:
            db.bulk_save_objects(customers_to_insert)
            
        db.commit()
        logging.info("Customers inserted.")
        
        # 3. Load Model and Generate Predictions
        models_dir = os.path.join(root_dir, "models")
        model_path = os.path.join(models_dir, "churn_model.pt")
        config_path = os.path.join(models_dir, "feature_config.json")
        metadata_path = os.path.join(models_dir, "model_metadata.json")
        
        if os.path.exists(model_path) and os.path.exists(config_path):
            logging.info("Loading model for predictions...")
            preprocessor.load(os.path.join(models_dir, "preprocessor.pkl"), config_path)
            
            X, _ = preprocessor.prepare_features_and_target(df_clean)
            X_trans = preprocessor.transform(X)
            
            model = CustomerChurnModel(input_dim=X_trans.shape[1])
            model.load_state_dict(torch.load(model_path, map_location='cpu'))
            model.eval()
            
            with torch.no_grad():
                outputs = model(torch.FloatTensor(X_trans))
                probs = torch.sigmoid(outputs).numpy().flatten()
                
            logging.info("Generating and inserting predictions...")
            
            metadata = {}
            if os.path.exists(metadata_path):
                with open(metadata_path, "r") as f:
                    metadata = json.load(f)
                    
            model_version = metadata.get("model_version", "1.0.0")
            
            if not db.query(ModelVersion).filter(ModelVersion.version == model_version).first():
                metrics = metadata.get("metrics", {})
                mv = ModelVersion(
                    version=model_version,
                    accuracy=metrics.get("accuracy", 0.0),
                    precision=metrics.get("precision", 0.0),
                    recall=metrics.get("recall", 0.0),
                    f1_score=metrics.get("f1", 0.0),
                    roc_auc=metrics.get("roc_auc", 0.0),
                    training_records=metadata.get("training_records", 0)
                )
                db.add(mv)
                db.commit()
            
            predictions_to_insert = []
            for idx, prob in enumerate(probs):
                cust_id = df_clean.iloc[idx]["customerID"]
                pred = Prediction(
                    customer_id=cust_id,
                    churn_probability=float(prob),
                    risk_level=get_risk_level(prob),
                    prediction="Likely to Churn" if prob >= 0.5 else "Retained",
                    model_version=model_version
                )
                predictions_to_insert.append(pred)
                
                if len(predictions_to_insert) >= 1000:
                    db.bulk_save_objects(predictions_to_insert)
                    predictions_to_insert = []
                    
            if predictions_to_insert:
                db.bulk_save_objects(predictions_to_insert)
                
            db.commit()
            logging.info("Predictions inserted.")
        else:
            logging.warning("Model not found. Run train_model.py first to generate predictions.")
            
    except Exception as e:
        logging.error(f"Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()
