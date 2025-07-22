import json
import importlib
from pathlib import Path
from typing import Dict, Any, Optional, Union, Type

from tdev.core import config
from tdev.core.agent import Agent
from tdev.core.tool import Tool

class AgentRegistry:
    """
    Registry for agents, tools, and teams in T-Developer.
    
    The registry maintains metadata about all components and provides
    methods to register, retrieve, and instantiate them.
    """
    
    def __init__(self):
        """Initialize the registry."""
        self._registry = {}
        self._load_registry()
    
    def _load_registry(self):
        """Load the registry from the registry file."""
        registry_path = config.get_registry_path()
        try:
            with open(registry_path, 'r') as f:
                self._registry = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            self._registry = {}
            self._save_registry()
    
    def _save_registry(self):
        """Save the registry to the registry file."""
        registry_path = config.get_registry_path()
        with open(registry_path, 'w') as f:
            json.dump(self._registry, f, indent=2)
    
    def register(self, name: str, metadata: Dict[str, Any]):
        """
        Register a component with the registry.
        
        Args:
            name: The name of the component
            metadata: The metadata for the component
        """
        self._registry[name] = metadata
        self._save_registry()
    
    def get_metadata(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get the metadata for a component.
        
        Args:
            name: The name of the component
            
        Returns:
            The metadata for the component, or None if not found
        """
        return self._registry.get(name)
    
    def get_instance(self, name: str) -> Optional[Union[Agent, Tool]]:
        """
        Get an instance of a component.
        
        Args:
            name: The name of the component
            
        Returns:
            An instance of the component, or None if not found
        """
        metadata = self.get_metadata(name)
        if not metadata:
            return None
        
        class_path = metadata.get('class')
        if not class_path:
            return None
        
        try:
            # Split the class path into module and class name
            module_path, class_name = class_path.rsplit('.', 1)
            
            # Import the module
            module = importlib.import_module(module_path)
            
            # Get the class
            cls = getattr(module, class_name)
            
            # Instantiate the class
            return cls()
        except (ImportError, AttributeError, ValueError) as e:
            print(f"Error instantiating {name}: {e}")
            return None
    
    def list_components(self, component_type: Optional[str] = None) -> Dict[str, Dict[str, Any]]:
        """
        List all components in the registry.
        
        Args:
            component_type: Optional type to filter by ('agent', 'tool', 'team')
            
        Returns:
            A dictionary of component names to metadata
        """
        if component_type:
            return {name: meta for name, meta in self._registry.items() 
                   if meta.get('type') == component_type}
        return self._registry

# Singleton instance
_registry = None

def get_registry() -> AgentRegistry:
    """
    Get the singleton registry instance.
    
    Returns:
        The registry instance
    """
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
    return _registry