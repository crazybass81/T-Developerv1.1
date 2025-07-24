import pytest
import os
import json
import tempfile
from pathlib import Path

from tdev.core.registry import AgentRegistry
from tdev.core.schema import AgentMeta, ToolMeta

class TestRegistry:
    """Tests for the AgentRegistry."""
    
    def setup_method(self):
        """Set up a temporary registry for testing."""
        # Create a temporary directory for the registry
        self.temp_dir = tempfile.TemporaryDirectory()
        self.registry_path = Path(self.temp_dir.name) / "registry.json"
        
        # Create an empty registry file
        with open(self.registry_path, 'w') as f:
            json.dump({}, f)
        
        # Create a registry instance
        self.registry = AgentRegistry()
        # Monkey patch the registry path
        self.registry._registry_path = self.registry_path
    
    def teardown_method(self):
        """Clean up the temporary registry."""
        self.temp_dir.cleanup()
    
    def test_register_agent(self):
        """Test registering an agent."""
        # Create agent metadata
        agent_meta = AgentMeta(
            name="TestAgent",
            class_path="tdev.agents.test_agent.TestAgent",
            description="A test agent"
        )
        
        # Register the agent
        self.registry.register("TestAgent", agent_meta.to_dict())
        
        # Check that the agent is in the registry
        assert "TestAgent" in self.registry._registry
        assert self.registry._registry["TestAgent"]["type"] == "agent"
        assert self.registry._registry["TestAgent"]["class"] == "tdev.agents.test_agent.TestAgent"
    
    def test_register_tool(self):
        """Test registering a tool."""
        # Create tool metadata
        tool_meta = ToolMeta(
            name="TestTool",
            class_path="tdev.tools.test_tool.test_tool",
            description="A test tool"
        )
        
        # Register the tool
        self.registry.register("TestTool", tool_meta.to_dict())
        
        # Check that the tool is in the registry
        assert "TestTool" in self.registry._registry
        assert self.registry._registry["TestTool"]["type"] == "tool"
        assert self.registry._registry["TestTool"]["class"] == "tdev.tools.test_tool.test_tool"
    
    def test_get_metadata(self):
        """Test getting metadata for a component."""
        # Register a component
        self.registry.register("TestComponent", {"type": "agent", "class": "test.TestClass"})
        
        # Get the metadata
        metadata = self.registry.get_metadata("TestComponent")
        
        # Check the metadata
        assert metadata is not None
        assert metadata["type"] == "agent"
        assert metadata["class"] == "test.TestClass"
    
    def test_list_components(self):
        """Test listing components."""
        # Create a new registry with only our test components
        self.registry._registry = {}
        
        # Register some components
        self.registry.register("TestAgent", {"type": "agent", "class": "test.TestAgent"})
        self.registry.register("TestTool", {"type": "tool", "class": "test.TestTool"})
        
        # List all components
        components = self.registry.list_components()
        assert len(components) == 2
        assert "TestAgent" in components
        assert "TestTool" in components
        
        # List only agents
        agents = self.registry.list_components("agent")
        assert len(agents) == 1
        assert "TestAgent" in agents
        assert "TestTool" not in agents
        
        # List only tools
        tools = self.registry.list_components("tool")
        assert len(tools) == 1
        assert "TestTool" in tools
        assert "TestAgent" not in tools