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
    
    # Mock the classifier agent
    mock_classifier = MagicMock()
    mock_classifier.run.return_value = {"type": "agent", "name": "test"}
    mock_registry.get_instance.return_value = mock_classifier
    
    # Create a DevCoordinatorAgent
    coordinator = DevCoordinatorAgent()
    
    # Create a test request with code (not goal)
    request = {
        "code": "test_code.py",
        "options": {"option1": "value1"}
    }
    
    # Run the coordinator
    result = coordinator.run(request)
    
    # Check the result matches actual behavior
    assert result["success"] is True
    assert "result" in result
    assert result["result"]["type"] == "agent"  # Match actual return