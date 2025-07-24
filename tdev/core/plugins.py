"""
Plugin ecosystem for tools and models.
"""
import importlib
import os
from typing import Dict, Any, List, Type
from abc import ABC, abstractmethod

class PluginInterface(ABC):
    """Base interface for all plugins."""
    
    @abstractmethod
    def get_name(self) -> str:
        """Return plugin name."""
        pass
    
    @abstractmethod
    def get_version(self) -> str:
        """Return plugin version."""
        pass
    
    @abstractmethod
    def initialize(self, config: Dict[str, Any]) -> None:
        """Initialize the plugin."""
        pass

class ModelPlugin(PluginInterface):
    """Base class for model plugins."""
    
    @abstractmethod
    def invoke(self, prompt: str, parameters: Dict[str, Any] = None) -> str:
        """Invoke the model with a prompt."""
        pass

class ToolPlugin(PluginInterface):
    """Base class for tool plugins."""
    
    @abstractmethod
    def execute(self, input_data: Any) -> Any:
        """Execute the tool."""
        pass

class PluginManager:
    """Manages plugins for tools and models."""
    
    def __init__(self):
        self.plugins: Dict[str, PluginInterface] = {}
        self.plugin_types: Dict[str, Type] = {
            "model": ModelPlugin,
            "tool": ToolPlugin
        }
    
    def register_plugin(self, plugin: PluginInterface) -> None:
        """Register a plugin."""
        self.plugins[plugin.get_name()] = plugin
    
    def get_plugin(self, name: str) -> PluginInterface:
        """Get a plugin by name."""
        return self.plugins.get(name)
    
    def list_plugins(self, plugin_type: str = None) -> List[str]:
        """List all plugins or plugins of a specific type."""
        if plugin_type:
            return [name for name, plugin in self.plugins.items() 
                   if isinstance(plugin, self.plugin_types.get(plugin_type, PluginInterface))]
        return list(self.plugins.keys())
    
    def load_plugin_from_file(self, file_path: str, plugin_class: str) -> None:
        """Load a plugin from a Python file."""
        spec = importlib.util.spec_from_file_location("plugin", file_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        plugin_cls = getattr(module, plugin_class)
        plugin = plugin_cls()
        self.register_plugin(plugin)

# Example model plugin
class BedrockModelPlugin(ModelPlugin):
    """Bedrock model plugin."""
    
    def get_name(self) -> str:
        return "bedrock-claude"
    
    def get_version(self) -> str:
        return "1.0.0"
    
    def initialize(self, config: Dict[str, Any]) -> None:
        self.model_id = config.get("model_id", "anthropic.claude-v2")
    
    def invoke(self, prompt: str, parameters: Dict[str, Any] = None) -> str:
        # Mock implementation
        return f"Bedrock response for: {prompt}"

# Global plugin manager instance
plugin_manager = PluginManager()
plugin_manager.register_plugin(BedrockModelPlugin())