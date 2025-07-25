"""
Fixed API server tests using httpx directly.
"""
import pytest
import asyncio
from unittest.mock import MagicMock, patch
import httpx
from fastapi.testclient import TestClient

from tdev.api.server import app

class TestAPIServerFixed:
    """Test the API server with proper client."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create test client
        self.client = TestClient(app)
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    def test_health_endpoint(self):
        """Test the health endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
    
    def test_list_agents_endpoint(self):
        """Test listing agents."""
        response = self.client.get("/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
    
    def test_orchestrate_endpoint(self):
        """Test orchestration endpoint."""
        payload = {"goal": "test goal"}
        response = self.client.post("/orchestrate", json=payload)
        # Should return either success or error, not crash
        assert response.status_code in [200, 400]
    
    def test_feedback_endpoint(self):
        """Test feedback endpoint."""
        payload = {
            "agent_name": "TestAgent",
            "rating": 5,
            "comment": "Great!"
        }
        response = self.client.post("/feedback", json=payload)
        # Should return either success or error, not crash
        assert response.status_code in [200, 400]