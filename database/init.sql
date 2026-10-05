CREATE DATABASE IF NOT EXISTS customer_churn_db;
USE customer_churn_db;

-- Customers table
CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL UNIQUE,
    gender VARCHAR(20),
    senior_citizen INT DEFAULT 0,
    partner VARCHAR(10),
    dependents VARCHAR(10),
    tenure INT DEFAULT 0,
    phone_service VARCHAR(10),
    multiple_lines VARCHAR(30),
    internet_service VARCHAR(30),
    online_security VARCHAR(30),
    online_backup VARCHAR(30),
    device_protection VARCHAR(30),
    tech_support VARCHAR(30),
    streaming_tv VARCHAR(30),
    streaming_movies VARCHAR(30),
    contract VARCHAR(30),
    paperless_billing VARCHAR(10),
    payment_method VARCHAR(50),
    monthly_charges FLOAT DEFAULT 0.0,
    total_charges FLOAT DEFAULT 0.0,
    churn VARCHAR(10),
    data_source VARCHAR(20) DEFAULT 'real',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_customer_id (customer_id),
    INDEX idx_churn (churn),
    INDEX idx_contract (contract),
    INDEX idx_internet_service (internet_service),
    INDEX idx_data_source (data_source),
    INDEX idx_monthly_charges (monthly_charges),
    INDEX idx_tenure (tenure)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Predictions table
CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id VARCHAR(50) NOT NULL,
    churn_probability FLOAT NOT NULL,
    risk_level VARCHAR(20) NOT NULL,
    prediction VARCHAR(30) NOT NULL,
    model_version VARCHAR(20),
    predicted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_pred_customer_id (customer_id),
    INDEX idx_risk_level (risk_level),
    INDEX idx_churn_probability (churn_probability),
    INDEX idx_predicted_at (predicted_at),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Model versions table
CREATE TABLE IF NOT EXISTS model_versions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    version VARCHAR(20) NOT NULL,
    accuracy FLOAT,
    precision_score FLOAT,
    recall_score FLOAT,
    f1_score FLOAT,
    roc_auc FLOAT,
    training_records INT DEFAULT 0,
    validation_records INT DEFAULT 0,
    test_records INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_version (version)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Dataset runs table
CREATE TABLE IF NOT EXISTS dataset_runs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    filename VARCHAR(255),
    total_records INT DEFAULT 0,
    real_records INT DEFAULT 0,
    synthetic_records INT DEFAULT 0,
    valid_records INT DEFAULT 0,
    invalid_records INT DEFAULT 0,
    imported_at DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Prediction requests log table
CREATE TABLE IF NOT EXISTS prediction_requests (
    id INT AUTO_INCREMENT PRIMARY KEY,
    request_type VARCHAR(20) NOT NULL,
    records_processed INT DEFAULT 0,
    model_version VARCHAR(20),
    response_time_ms FLOAT,
    requested_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_request_type (request_type),
    INDEX idx_requested_at (requested_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
