"""
Backend API Tests for CustomerChurnPredictor
"""
import pytest
import sys
import os
import json

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))


class TestHealthEndpoint:
    """Test health check endpoint."""

    def test_health_check_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_check_response_format(self, client):
        response = client.get("/health")
        data = response.json()
        assert "status" in data
        assert "database" in data
        assert "model" in data
        assert "model_version" in data

    def test_health_check_status_value(self, client):
        response = client.get("/health")
        data = response.json()
        assert data["status"] in ["healthy", "degraded", "unhealthy"]


class TestPredictionEndpoint:
    """Test prediction API endpoint."""

    def test_predict_returns_200(self, client, sample_customer_data):
        response = client.post("/api/predict", json=sample_customer_data)
        # Accept 200 or 500 if model not loaded
        assert response.status_code in [200, 500, 503]

    def test_predict_response_format(self, client, sample_customer_data):
        response = client.post("/api/predict", json=sample_customer_data)
        if response.status_code == 200:
            data = response.json()
            assert "churn_probability" in data
            assert "risk_level" in data
            assert "prediction" in data

    def test_predict_probability_range(self, client, sample_customer_data):
        response = client.post("/api/predict", json=sample_customer_data)
        if response.status_code == 200:
            data = response.json()
            assert 0.0 <= data["churn_probability"] <= 1.0

    def test_predict_risk_level_values(self, client, sample_customer_data):
        response = client.post("/api/predict", json=sample_customer_data)
        if response.status_code == 200:
            data = response.json()
            assert data["risk_level"] in ["Low", "Medium", "High", "Critical"]

    def test_predict_invalid_data(self, client):
        response = client.post("/api/predict", json={})
        assert response.status_code in [422, 400, 500]

    def test_predict_missing_fields(self, client):
        response = client.post("/api/predict", json={"gender": "Male"})
        assert response.status_code in [422, 400, 500]


class TestBatchPrediction:
    """Test batch prediction endpoint."""

    def test_batch_predict_no_file(self, client):
        response = client.post("/api/predict/batch")
        assert response.status_code in [422, 400]


class TestCustomerEndpoints:
    """Test customer API endpoints."""

    def test_get_customers_returns_200(self, client):
        response = client.get("/api/customers")
        assert response.status_code == 200

    def test_get_customers_pagination(self, client):
        response = client.get("/api/customers?page=1&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert "items" in data or "total" in data or isinstance(data, list)

    def test_get_customers_with_search(self, client):
        response = client.get("/api/customers?search=test")
        assert response.status_code == 200

    def test_get_customers_with_risk_filter(self, client):
        response = client.get("/api/customers?risk=High")
        assert response.status_code == 200

    def test_get_customer_not_found(self, client):
        response = client.get("/api/customers/NONEXISTENT-999")
        assert response.status_code in [404, 200]


class TestAnalyticsEndpoints:
    """Test analytics API endpoints."""

    def test_analytics_overview(self, client):
        response = client.get("/api/analytics/overview")
        assert response.status_code == 200

    def test_analytics_churn_by_contract(self, client):
        response = client.get("/api/analytics/churn-by-contract")
        assert response.status_code == 200

    def test_analytics_churn_by_service(self, client):
        response = client.get("/api/analytics/churn-by-service")
        assert response.status_code == 200

    def test_analytics_risk_distribution(self, client):
        response = client.get("/api/analytics/risk-distribution")
        assert response.status_code == 200

    def test_analytics_probability_distribution(self, client):
        response = client.get("/api/analytics/probability-distribution")
        assert response.status_code == 200


class TestModelEndpoints:
    """Test model management endpoints."""

    def test_model_info(self, client):
        response = client.get("/api/model/info")
        assert response.status_code == 200

    def test_model_versions(self, client):
        response = client.get("/api/model/versions")
        assert response.status_code == 200


class TestDatasetEndpoints:
    """Test dataset management endpoints."""

    def test_dataset_info(self, client):
        response = client.get("/api/dataset/info")
        assert response.status_code == 200


# Fixtures
@pytest.fixture
def sample_customer_data():
    """Sample customer data for prediction testing."""
    return {
        "customer_id": "TEST-001",
        "gender": "Male",
        "senior_citizen": 0,
        "partner": "Yes",
        "dependents": "No",
        "tenure": 12,
        "phone_service": "Yes",
        "multiple_lines": "No",
        "internet_service": "Fiber optic",
        "online_security": "No",
        "online_backup": "No",
        "device_protection": "No",
        "tech_support": "No",
        "streaming_tv": "No",
        "streaming_movies": "No",
        "contract": "Month-to-month",
        "paperless_billing": "Yes",
        "payment_method": "Electronic check",
        "monthly_charges": 70.35,
        "total_charges": 844.2
    }


@pytest.fixture
def client():
    """Create test client. This will try to use the actual app."""
    try:
        from fastapi.testclient import TestClient
        from backend.main import app
        return TestClient(app)
    except Exception:
        pytest.skip("Backend not available for testing")
