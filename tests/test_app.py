"""Tests for the Flask monitoring application."""

import os

# pyrefly: ignore [missing-import]
import pytest

# Disable chaos mode for tests
os.environ["ENABLE_CHAOS"] = "false"

from app import create_app  # noqa: E402


@pytest.fixture
def client():
    """Create a test client for the Flask app."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


class TestHealthEndpoints:
    """Test health and readiness probes."""

    def test_health_returns_200(self, client):
        response = client.get("/health")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ok"

    def test_ready_returns_200(self, client):
        response = client.get("/ready")
        assert response.status_code == 200
        assert response.get_json()["status"] == "ready"


class TestAppEndpoints:
    """Test application endpoints."""

    def test_home_returns_200(self, client):
        response = client.get("/")
        assert response.status_code == 200
        data = response.get_json()
        assert "message" in data

    def test_404_returns_json(self, client):
        response = client.get("/nonexistent-route")
        assert response.status_code == 404
        data = response.get_json()
        assert "error" in data


class TestMetricsEndpoint:
    """Test Prometheus metrics exposure."""

    def test_metrics_returns_200(self, client):
        # Hit home page first to generate some metrics
        client.get("/")
        response = client.get("/metrics")
        assert response.status_code == 200
        # Prometheus metrics are returned as text/plain
        assert "flask_http" in response.data.decode("utf-8") or "python_info" in response.data.decode("utf-8")
