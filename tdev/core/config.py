import os
import json
from pathlib import Path

# Default configuration
DEFAULT_CONFIG = {
    "registry_path": ".tdev/registry.json",
    "workflows_path": ".tdev/workflows",
    "instances_path": ".tdev/instances",
}

def get_config_dir():
    """Get the configuration directory path, creating it if it doesn't exist."""
    home_dir = Path.home()
    config_dir = home_dir / ".tdev"
    
    if not config_dir.exists():
        config_dir.mkdir(parents=True)
        
    # Create subdirectories if they don't exist
    workflows_dir = config_dir / "workflows"
    if not workflows_dir.exists():
        workflows_dir.mkdir()
        
    instances_dir = config_dir / "instances"
    if not instances_dir.exists():
        instances_dir.mkdir()
    
    return config_dir

def get_registry_path():
    """Get the path to the registry file."""
    config_dir = get_config_dir()
    return config_dir / "registry.json"

def ensure_registry_exists():
    """Ensure the registry file exists, creating it if it doesn't."""
    registry_path = get_registry_path()
    if not registry_path.exists():
        with open(registry_path, 'w') as f:
            json.dump({}, f)
    
    return registry_path

def get_workflows_dir():
    """Get the workflows directory path."""
    config_dir = get_config_dir()
    return config_dir / "workflows"

def get_instances_dir():
    """Get the instances directory path."""
    config_dir = get_config_dir()
    return config_dir / "instances"