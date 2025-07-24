"""
Pytest configuration and fixtures.
"""
import pytest
from unittest.mock import MagicMock

@pytest.fixture
def mock_registry():
    """Create a mock registry for testing."""
    registry = MagicMock()
    registry.get.return_value = {"name": "TestAgent", "type": "agent"}
    registry.get_by_type.return_value = [
        {"name": "Agent1", "type": "agent"},
        {"name": "Agent2", "type": "agent"}
    ]
    registry.get_all.return_value = {
        "Agent1": {"name": "Agent1", "type": "agent"},
        "Tool1": {"name": "Tool1", "type": "tool"}
    }
    return registry

@pytest.fixture
def mock_bedrock_client():
    """Create a mock Bedrock client for testing."""
    client = MagicMock()
    client.invoke_model.return_value = {
        "completion": "Test response",
        "outputText": "Test response"
    }
    return client