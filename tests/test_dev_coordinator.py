"""
Tests for the DevCoordinatorAgent.
"""
import pytest
from unittest.mock import MagicMock, patch

from tdev.agents.dev_coordinator_agent import DevCoordinatorAgent


@pytest.fixture
def mock_registry():
    """Create a mock registry with core agents."""
    registry = MagicMock()
    
    # Mock core agents
    classifier = MagicMock()
    classifier.run.return_value = {"type": "agent"}
    
    planner = MagicMock()
    planner.run.return_value = {"id": "test-workflow", "steps": [{"agent": "EchoAgent"}]}
    
    evaluator = MagicMock()
    evaluator.run.return_value = {"score": 0.9, "feedback": []}
    
    executor = MagicMock()
    executor.run.return_value = {"result": "Test result"}
    
    # Configure registry.get_instance to return the appropriate mock
    def get_instance_side_effect(name):
        if name == "ClassifierAgent":
            return classifier
        elif name == "PlannerAgent":
            return planner
        elif name == "EvaluatorAgent":
            return evaluator
        elif name == "WorkflowExecutorAgent":
            return executor
        return None
    
    registry.get_instance.side_effect = get_instance_side_effect
    
    return registry


@patch('tdev.agents.dev_coordinator_agent.get_registry')
def test_dev_coordinator_run(mock_get_registry, mock_registry):
    """Test that DevCoordinatorAgent can run a request."""
    # Set up the mock registry
    mock_get_registry.return_value = mock_registry
    
    # Create a DevCoordinatorAgent
    coordinator = DevCoordinatorAgent()
    
    # Create a test request
    request = {
        "goal": "Test goal",
        "code": "test_code.py",
        "options": {"option1": "value1"}
    }
    
    # Run the coordinator
    with patch('asyncio.get_event_loop'):
        with patch('asyncio.new_event_loop'):
            with patch('asyncio.set_event_loop'):
                with patch.object(coordinator.supervisor, 'process_request') as mock_process:
                    # Mock the async process_request method
                    mock_process.return_value = {"text": "Test result", "context": {}}
                    
                    # Call the run method
                    result = coordinator.run(request)
    
    # Check the result
    assert result["success"] is True
    assert "result" in result
    assert result["result"] == "Test result"