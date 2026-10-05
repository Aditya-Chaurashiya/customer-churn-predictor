export interface Customer {
  customer_id: string;
  gender?: string;
  senior_citizen?: number;
  partner?: string;
  dependents?: string;
  tenure: number;
  phone_service?: string;
  multiple_lines?: string;
  internet_service?: string;
  online_security?: string;
  online_backup?: string;
  device_protection?: string;
  tech_support?: string;
  streaming_tv?: string;
  streaming_movies?: string;
  contract: string;
  paperless_billing?: string;
  payment_method: string;
  monthly_charges: number;
  total_charges?: number;
  churn?: string;
}

export interface CustomerWithPrediction extends Customer {
  churn_probability: number;
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical';
  prediction: string;
  risk_factors?: string[];
  protective_factors?: string[];
}

export interface PredictionResult {
  customer_id: string;
  churn_probability: number;
  risk_level: 'Low' | 'Medium' | 'High' | 'Critical';
  prediction: string;
  model_version: string;
  risk_factors: string[];
  protective_factors: string[];
}

export interface AnalyticsOverview {
  total_customers: number;
  predicted_churn: number;
  high_risk: number;
  critical_risk: number;
  average_probability: number;
  model_accuracy: number;
  model_version: string;
  last_trained: string;
  dataset_info: {
    source: string;
    total_records: number;
    real_records: number;
    synthetic_records: number;
  };
}

export interface ChurnByContract {
  contract_type: string;
  total: number;
  churned: number;
  churn_rate: number;
}

export interface RiskDistribution {
  risk_level: string;
  count: number;
  percentage: number;
}

export interface ModelMetrics {
  version: string;
  accuracy: number;
  precision_score: number;
  recall: number;
  f1_score: number;
  roc_auc: number;
  training_records: number;
  created_at: string;
}

export interface DatasetInfo {
  source: string;
  total_records: number;
  real_records: number;
  synthetic_records: number;
  missing_values?: number;
  duplicates?: number;
}

export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  limit: number;
}

export interface BatchPredictionResult {
  total: number;
  processed: number;
  results: PredictionResult[];
}

export interface ConfusionMatrix {
  true_positive: number;
  false_positive: number;
  true_negative: number;
  false_negative: number;
}

export interface ChurnIndicator {
  feature: string;
  importance: number;
  direction: string;
}
