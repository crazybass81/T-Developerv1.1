"""
Simple API server tests using httpx directly.
"""
import pytest
from unittest.mock import MagicMock, patch
import httpx
from tdev.api.server import app

class TestAPIServerSimple:
    """Test the API server with httpx."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create proper mock registry
        self.mock_registry = MagicMock()
        self.mock_registry.get.return_value = {"name": "TestAgent", "type": "agent"}
        self.mock_registry.get_by_type.return_value = {
            "Agent1": {"name": "Agent1", "type": "agent"},
            "Agent2": {"name": "Agent2", "type": "agent"}
        }
        
        # Patch all dependencies
        self.registry_patcher = patch('tdev.api.server.get_registry')
        self.mock_get_registry = self.registry_patcher.start()
        self.mock_get_registry.return_value = self.mock_registry
        
        self.coordinator_patcher = patch('tdev.api.server.DevCoordinatorAgent')
        self.mock_coordinator_class = self.coordinator_patcher.start()
        self.mock_coordinator = MagicMock()
        self.mock_coordinator_class.return_value = self.mock_coordinator
        
        self.feedback_patcher = patch('tdev.api.server.FeedbackCollector')
        self.mock_feedback_class = self.feedback_patcher.start()
        self.mock_feedback = MagicMock()
        self.mock_feedback_class.return_value = self.mock_feedback
        
        # Create httpx client
        from httpx import ASGITransport
        self.client = httpx.AsyncClient(transport=ASGITransport(app=app), base_url="http://test")
    
    def teardown_method(self):
        """Clean up patches."""
        self.registry_patcher.stop()
        self.coordinator_patcher.stop()
        self.feedback_patcher.stop()
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test the root endpoint."""
        response = await self.client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
    
    @pytest.mark.asyncio
    async def test_list_agents(self):
        """Test the list_agents endpoint."""
        response = await self.client.get("/agents")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert len(data["agents"]) == 2
    
    @pytest.mark.asyncio
    async def test_orchestrate(self):
        """Test the orchestrate endpoint."""
        self.mock_coordinator.run.return_value = {
            "success": True,
            "result": "Test result",
            "workflow_id": "test-workflow"
        }
        
        response = await self.client.post(
            "/orchestrate",
            json={"goal": "Test goal", "options": {"key": "value"}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"] == "Test result"
    
    @pytest.mark.asyncio
    async def test_classify(self):
        """Test the classify endpoint."""
        self.mock_coordinator.run.return_value = {
            "success": True,
            "result": {"type": "agent", "brain_count": 1}
        }
        
        response = await self.client.post(
            "/classify",
            json={"code": "def test(): pass", "options": {}}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True
        assert data["result"]["type"] == "agent"
    
    @pytest.mark.asyncio
    async def test_feedback(self):
        """Test the feedback endpoint."""
        self.mock_feedback.collect.return_value = {
            "success": True,
            "message": "Feedback collected"
        }
        
        response = await self.client.post(
            "/feedback",
            json={
                "agent_name": "TestAgent",
                "rating": 5,
                "comment": "Great agent!",
                "source": "test"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["success"] is True