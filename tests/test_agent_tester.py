import pytest
from tdev.agents.agent_tester_agent import AgentTesterAgent
from tdev.core.registry import AgentRegistry

class MockAgent:
    """A mock agent for testing."""
    
    def __init__(self, return_value=None):
        """Initialize the mock agent."""
        self.return_value = return_value
    
    def run(self, input_data):
        """Run the mock agent."""
        return self.return_value or input_data

class MockRegistry:
    """A mock registry for testing."""
    
    def __init__(self, agents=None):
        """Initialize the mock registry."""
        self.agents = agents or {}
    
    def get_instance(self, name):
        """Get an instance of a component."""
        return self.agents.get(name)

class TestAgentTester:
    """Tests for the AgentTesterAgent."""
    
    def setup_method(self):
        """Set up for testing."""
        # Create a mock agent that returns the input
        self.echo_agent = MockAgent()
        
        # Create a mock agent that returns a fixed value
        self.fixed_agent = MockAgent("fixed output")
        
        # Create a mock registry
        self.mock_registry = MockRegistry({
            "EchoAgent": self.echo_agent,
            "FixedAgent": self.fixed_agent
        })
        
        # Create an agent tester
        self.tester = AgentTesterAgent()
        
        # Monkey patch the tester to use the mock registry
        self.tester._get_registry = lambda: self.mock_registry
    
    def test_echo_agent_test(self, monkeypatch):
        """Test testing an echo agent."""
        # Monkey patch the get_registry function
        monkeypatch.setattr("tdev.agents.agent_tester_agent.get_registry", lambda: self.mock_registry)
        
        # Test the echo agent
        result = self.tester.run("EchoAgent", [
            {"input": "test input", "expected": "test input"}
        ])
        
        # Check the result
        assert result["success"] is True
        assert result["success_rate"] == 1.0
        assert result["passed"] == 1
        assert result["total"] == 1
    
    def test_fixed_agent_test(self, monkeypatch):
        """Test testing a fixed agent."""
        # Monkey patch the get_registry function
        monkeypatch.setattr("tdev.agents.agent_tester_agent.get_registry", lambda: self.mock_registry)
        
        # Test the fixed agent
        result = self.tester.run("FixedAgent", [
            {"input": "test input", "expected": "fixed output"}
        ])
        
        # Check the result
        assert result["success"] is True
        assert result["success_rate"] == 1.0
        assert result["passed"] == 1
        assert result["total"] == 1
    
    def test_failing_test(self, monkeypatch):
        """Test a failing test."""
        # Monkey patch the get_registry function
        monkeypatch.setattr("tdev.agents.agent_tester_agent.get_registry", lambda: self.mock_registry)
        
        # Test the fixed agent with wrong expectation
        result = self.tester.run("FixedAgent", [
            {"input": "test input", "expected": "wrong output"}
        ])
        
        # Check the result
        assert result["success"] is False
        assert result["success_rate"] == 0.0
        assert result["passed"] == 0
        assert result["total"] == 1