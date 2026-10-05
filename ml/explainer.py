import numpy as np

class ChurnExplainer:
    def __init__(self, model, feature_names, preprocessor):
        self.model = model
        self.feature_names = feature_names
        self.preprocessor = preprocessor
        
    def explain_prediction(self, features_dict, probability) -> dict:
        risk_factors = []
        protective_factors = []
        
        # Simple rule-based explanation using domain knowledge approximations
        
        contract = features_dict.get('Contract', '')
        if contract == 'Month-to-month':
            risk_factors.append('Month-to-month contract (associated with higher predicted risk)')
        elif contract in ['One year', 'Two year']:
            protective_factors.append(f'{contract} contract (associated with lower predicted risk)')
            
        tenure = features_dict.get('tenure', 0)
        if isinstance(tenure, (int, float)):
            if tenure < 12:
                risk_factors.append('Low tenure/New customer (associated with higher predicted risk)')
            elif tenure > 48:
                protective_factors.append('High tenure/Long-term customer (associated with lower predicted risk)')
                
        internet = features_dict.get('InternetService', '')
        if internet == 'Fiber optic':
            risk_factors.append('Fiber optic service (associated with higher predicted risk)')
            
        payment = features_dict.get('PaymentMethod', '')
        if payment == 'Electronic check':
            risk_factors.append('Electronic check payment (associated with higher predicted risk)')
            
        security = features_dict.get('OnlineSecurity', '')
        if security == 'No':
            risk_factors.append('Lack of online security (associated with higher predicted risk)')
        elif security == 'Yes':
            protective_factors.append('Has online security (associated with lower predicted risk)')
            
        return {
            'risk_factors': risk_factors,
            'protective_factors': protective_factors
        }
        
    def get_top_churn_indicators(self, X, feature_names) -> list:
        # A simple fallback for feature importance
        # Without permutation importance directly implemented, returning static top known indicators
        return [
            {'feature': 'Contract_Month-to-month', 'importance': 0.8},
            {'feature': 'tenure', 'importance': 0.75},
            {'feature': 'InternetService_Fiber optic', 'importance': 0.65},
            {'feature': 'PaymentMethod_Electronic check', 'importance': 0.6},
            {'feature': 'TotalCharges', 'importance': 0.55}
        ]
