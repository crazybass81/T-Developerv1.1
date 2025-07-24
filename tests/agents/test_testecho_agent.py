import pytest
from tdev.agents.testecho_agent import TestEchoAgent

def test_testecho_basic():
    """Test that the TestEchoAgent works with basic input."""
    # Arrange
    agent = TestEchoAgent()
    input_data = "test_input"  # Replace with appropriate test input
    
    # Act
    result = agent.run(input_data)
    
    # Assert
    assert result is not None
    # Add more specific assertions based on expected behavior
