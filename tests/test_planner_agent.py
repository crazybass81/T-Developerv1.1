"""
Tests for PlannerAgent.
"""
import pytest
from unittest.mock import MagicMock, patch
from tdev.agents.planner_agent import PlannerAgent

class TestPlannerAgent:
    """Test the PlannerAgent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.mock_registry = MagicMock()
        self.mock_registry.get_by_type.return_value = [
            {"name": "EchoAgent", "type": "agent"},
            {"name": "TestAgent", "type": "agent"}
        ]
        
        with patch('tdev.agents.planner_agent.get_registry', return_value=self.mock_registry):
            self.agent = PlannerAgent()
    
    def test_run_simple_goal(self):
        """Test planning for a simple goal."""
        result = self.agent.run("Echo the input")
        
        assert "workflow" in result
        assert "missing_capabilities" in result
        workflow = result["workflow"]
        assert workflow["id"] is not None
        assert len(workflow["steps"]) > 0
    
    def test_analyze_goal(self):
        """Test goal analysis."""
        available_agents = [{"name": "EchoAgent"}]
        available_tools = []
        
        steps = self.agent._analyze_goal("Echo test input", available_agents, available_tools)
        
        assert len(steps) > 0
        assert all("agent" in step for step in steps)
    
    def test_identify_missing_capabilities(self):
        """Test missing capability identification."""
        workflow_steps = [{"agent": "NonExistentAgent"}]
        available_agents = [{"name": "EchoAgent"}]
        available_tools = []
        
        missing = self.agent._identify_missing_capabilities(
            workflow_steps, available_agents, available_tools
        )
        
        assert len(missing) == 1
        assert missing[0]["name"] == "NonExistentAgent"
    
    def test_generate_id(self):
        """Test ID generation."""
        workflow_id = self.agent._generate_id("test goal")
        
        assert isinstance(workflow_id, str)
        assert len(workflow_id) > 0