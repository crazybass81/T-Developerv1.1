"""
Direct API endpoint tests without TestClient.
"""
import pytest
from unittest.mock import MagicMock, patch
from tdev.api.server import list_agents, orchestrate, classify, submit_feedback, root
from tdev.api.server import OrchestrationRequest, CodeRequest, FeedbackRequest

class TestAPIEndpoints:
    """Test API endpoints directly."""
    
    def setup_method(self):
        """Set up test fixtures."""
        # Create proper mock registry
        self.mock_registry = MagicMock()
        self.mock_registry.get.return_value = {"name": "PlannerAgent", "type": "agent"}
        self.mock_registry.get_by_type.return_value = [
            {"name": "Agent1", "type": "agent"},
            {"name": "Agent2", "type": "agent"}
        ]
        
        # Patch dependencies
        self.registry_patcher = patch('tdev.api.server.registry', self.mock_registry)
        self.registry_patcher.start()
        
        self.coordinator_patcher = patch('tdev.api.server.coordinator')
        self.mock_coordinator = self.coordinator_patcher.start()
        
        self.feedback_patcher = patch('tdev.api.server.feedback_collector')
        self.mock_feedback = self.feedback_patcher.start()
    
    def teardown_method(self):
        """Clean up patches."""
        self.registry_patcher.stop()
        self.coordinator_patcher.stop()
        self.feedback_patcher.stop()
    
    @pytest.mark.asyncio
    async def test_root_endpoint(self):
        """Test the root endpoint."""
        result = await root()
        assert result["message"] == "T-Developer API"
        assert result["version"] == "1.1.0"
    
    @pytest.mark.asyncio
    async def test_list_agents(self):
        """Test the list_agents endpoint."""
        result = await list_agents()
        assert "agents" in result
        assert len(result["agents"]) == 2
        assert result["agents"][0]["name"] == "Agent1"
    
    @pytest.mark.asyncio
    async def test_orchestrate_success(self):
        """Test successful orchestration."""
        self.mock_coordinator.run.return_value = {
            "success": True,
            "result": "Test result",
            "workflow_id": "test-workflow"
        }
        
        request = OrchestrationRequest(goal="Test goal", options={"key": "value"})
        result = await orchestrate(request)
        
        assert result["success"] is True
        assert result["result"] == "Test result"
    
    @pytest.mark.asyncio
    async def test_classify_success(self):
        """Test successful classification."""
        self.mock_coordinator.run.return_value = {
            "success": True,
            "result": {"type": "agent", "brain_count": 1}
        }
        
        request = CodeRequest(code="def test(): pass", options={})
        result = await classify(request)
        
        assert result["success"] is True
        assert result["result"]["type"] == "agent"
    
    @pytest.mark.asyncio
    async def test_feedback_success(self):
        """Test successful feedback submission."""
        self.mock_feedback.collect.return_value = {
            "success": True,
            "message": "Feedback collected"
        }
        
        request = FeedbackRequest(
            agent_name="TestAgent",
            rating=5,
            comment="Great agent!",
            source="test"
        )
        result = await submit_feedback(request)
        
        assert result["success"] is True