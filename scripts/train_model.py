import os
import sys

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml.src.preprocess import DataPreprocessor, split_data
from ml.src.model import CustomerChurnModel
from ml.src.train import train_model, save_model

import logging

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def main():
    root_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    real_data_path = os.path.join(root_dir, "data", "raw", "Telco-Customer-Churn.csv")
    synth_data_path = os.path.join(root_dir, "data", "raw", "Synthetic-Customer-Churn.csv")
    
    if not os.path.exists(real_data_path):
        logging.error(f"Real data not found at {real_data_path}")
        return
        
    logging.info("Loading data...")
    preprocessor = DataPreprocessor()
    df = preprocessor.load_data(real_data_path, synth_data_path)
    
    logging.info("Cleaning data...")
    df = preprocessor.clean_data(df)
    
    logging.info("Engineering features...")
    df = preprocessor.engineer_features(df)
    
    logging.info("Preparing features and target...")
    X, y = preprocessor.prepare_features_and_target(df)
    
    logging.info("Splitting data...")
    X_train_df, X_val_df, X_test_df, y_train, y_val, y_test = split_data(X, y.values)
    
    logging.info("Fitting preprocessor...")
    X_train = preprocessor.fit_transform(X_train_df)
    X_val = preprocessor.transform(X_val_df)
    X_test = preprocessor.transform(X_test_df)
    
    logging.info("Saving preprocessor...")
    models_dir = os.path.join(root_dir, "models")
    preprocessor.save(
        os.path.join(models_dir, "preprocessor.pkl"),
        os.path.join(models_dir, "feature_config.json")
    )
    
    logging.info(f"Training model with {X_train.shape[1]} features...")
    model = CustomerChurnModel(input_dim=X_train.shape[1])
    
    trained_model, metrics = train_model(
        model, X_train, y_train, X_val, y_val, X_test, y_test,
        epochs=100, batch_size=64, lr=0.001, patience=10
    )
    
    logging.info(f"Training complete. Metrics: {metrics}")
    
    config = {
        "training_records": len(X_train),
        "validation_records": len(X_val),
        "test_records": len(X_test)
    }
    
    logging.info("Saving model and metadata...")
    save_model(trained_model, metrics, config, models_dir, version="1.0.0")
    logging.info("Process finished successfully.")

if __name__ == "__main__":
    main()
