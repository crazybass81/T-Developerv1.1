"""
Tests for AutoAgentComposer (Agno).
"""
import pytest
from unittest.mock import MagicMock, patch

from tdev.agents.auto_agent_composer import AutoAgentComposer

class TestAutoAgentComposer:
    """Test the Auto Agent Composer."""
    
    def setup_method(self):
        """Set up test fixtures."""
        with patch('tdev.agents.auto_agent_composer.get_registry') as mock_registry:
            self.mock_registry = MagicMock()
            mock_registry.return_value = self.mock_registry
            self.composer = AutoAgentComposer()
    
    def test_generate_agent_success(self):
        """Test successful agent generation."""
        input_data = {
            "type": "agent",
            "name": "TestAgent",
            "goal": "Process test data"
        }
        
        result = self.composer.run(input_data)
        
        assert result["success"] is True
        assert result["name"] == "TestAgent"
        assert result["type"] == "agent"
        assert "code" in result
        assert "metadata" in result
        
        # Verify registry was called
        self.mock_registry.register.assert_called_once()
    
    def test_generate_tool_success(self):
        """Test successful tool generation."""
        input_data = {
            "type": "tool",
            "name": "TestTool",
            "goal": "Process test data"
        }
        
        result = self.composer.run(input_data)
        
        assert result["success"] is True
        assert result["name"] == "TestTool"
        assert result["type"] == "tool"
        assert "code" in result
        assert "metadata" in result
    
    def test_missing_goal_error(self):
        """Test error when goal is missing."""
        input_data = {
            "type": "agent",
            "name": "TestAgent"
        }
        
        result = self.composer.run(input_data)
        
        assert result["success"] is False
        assert "Goal is required" in result["error"]
    
    def test_unknown_type_error(self):
        """Test error for unknown component type."""
        input_data = {
            "type": "unknown",
            "name": "TestComponent",
            "goal": "Do something"
        }
        
        result = self.composer.run(input_data)
        
        assert result["success"] is False
        assert "Unknown type" in result["error"]
    
    def test_list_generated_components(self):
        """Test listing generated components."""
        self.mock_registry.get_all.return_value = {
            "Agent1": {"generated": True, "type": "agent"},
            "Agent2": {"generated": False, "type": "agent"},
            "Tool1": {"generated": True, "type": "tool"}
        }
        
        result = self.composer.list_generated_components()
        
        assert result["success"] is True
        assert result["count"] == 2
        assert "Agent1" in result["components"]
        assert "Tool1" in result["components"]
        assert "Agent2" not in result["components"]
    
    def test_regenerate_component(self):
        """Test regenerating an existing component."""
        self.mock_registry.get.return_value = {
            "type": "agent",
            "generated": True
        }
        
        result = self.composer.regenerate_component("TestAgent", "New goal")
        
        assert result["success"] is True
        assert result["name"] == "TestAgent"
    
    def test_regenerate_nonexistent_component(self):
        """Test regenerating a non-existent component."""
        self.mock_registry.get.return_value = None
        
        result = self.composer.regenerate_component("NonExistent", "New goal")
        
        assert result["success"] is False
        assert "not found" in result["error"]