"""
Tests for ClassifierAgent.
"""
import pytest
from unittest.mock import patch, mock_open
from tdev.agents.classifier_agent import ClassifierAgent

class TestClassifierAgent:
    """Test the ClassifierAgent."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.agent = ClassifierAgent()
    
    def test_run_with_file_path(self):
        """Test run with file path."""
        mock_content = '''
from tdev.core.agent import Agent

class TestAgent(Agent):
    def run(self, input_data):
        return input_data
'''
        with patch("builtins.open", mock_open(read_data=mock_content)):
            result = self.agent.run("test_agent.py")
        
        assert result["type"] == "agent"
        assert result["brain_count"] == 1
        assert result["reusability"] == "B"
    
    def test_run_with_dict_input(self):
        """Test run with dictionary input containing code."""
        code_content = '''
@tool
def test_tool(input_data):
    return input_data
'''
        result = self.agent.run({"code": code_content})
        
        assert result["type"] == "tool"
        assert result["brain_count"] == 0
        assert result["reusability"] == "A"
    
    def test_is_team(self):
        """Test team detection."""
        team_content = '''
from tdev.core.team import Team

class TestTeam(Team):
    pass
'''
        assert self.agent._is_team(team_content) is True
        assert self.agent._is_team("class TestAgent(Agent):") is False
    
    def test_is_tool(self):
        """Test tool detection."""
        tool_content = "@tool\ndef test_tool():"
        assert self.agent._is_tool(tool_content) is True
        assert self.agent._is_tool("def regular_function():") is False
    
    def test_extract_name(self):
        """Test name extraction."""
        agent_content = "class MyAgent(Agent):"
        assert self.agent._extract_name("file", agent_content, "agent") == "My"
        
        tool_content = "@tool\ndef my_tool():"
        assert self.agent._extract_name("file", tool_content, "tool") == "my_tool"
    
    def test_default_classification(self):
        """Test default classification."""
        result = self.agent._default_classification("test_agent.py")
        assert result["type"] == "agent"
        
        result = self.agent._default_classification("test_tool.py")
        assert result["type"] == "tool"
        
        result = self.agent._default_classification("test_team.py")
        assert result["type"] == "team"