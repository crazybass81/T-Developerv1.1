import json
import yaml
from pathlib import Path
from typing import List, Dict, Any, Optional

from tdev.core import config

class Workflow:
    """
    Represents a workflow definition in T-Developer.
    
    A workflow is a sequence of steps, each referencing an agent.
    """
    
    def __init__(self, id: str, steps: List[Dict[str, str]], inputs: Optional[Dict[str, str]] = None, 
                 outputs: Optional[Dict[str, str]] = None, description: Optional[str] = None):
        """
        Initialize a workflow.
        
        Args:
            id: The workflow ID
            steps: A list of steps, each with an agent reference
            inputs: Optional input definitions
            outputs: Optional output definitions
            description: Optional description
        """
        self.id = id
        self.steps = steps
        self.inputs = inputs or {}
        self.outputs = outputs or {}
        self.description = description or f"Workflow {id}"
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert the workflow to a dictionary.
        
        Returns:
            A dictionary representation of the workflow
        """
        return {
            "id": self.id,
            "steps": self.steps,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "description": self.description,
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Workflow':
        """
        Create a workflow from a dictionary.
        
        Args:
            data: The dictionary representation of the workflow
            
        Returns:
            A Workflow instance
        """
        return cls(
            id=data.get("id"),
            steps=data.get("steps", []),
            inputs=data.get("inputs", {}),
            outputs=data.get("outputs", {}),
            description=data.get("description"),
        )


def load_workflow(file_path: str) -> Optional[Workflow]:
    """
    Load a workflow from a file.
    
    Args:
        file_path: The path to the workflow file
        
    Returns:
        A Workflow instance, or None if the file could not be loaded
    """
    path = Path(file_path)
    if not path.exists():
        return None
    
    try:
        with open(path, 'r') as f:
            if path.suffix == '.json':
                data = json.load(f)
            elif path.suffix in ('.yaml', '.yml'):
                data = yaml.safe_load(f)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
        
        return Workflow.from_dict(data)
    except (json.JSONDecodeError, yaml.YAMLError, ValueError) as e:
        print(f"Error loading workflow: {e}")
        return None


def save_workflow(workflow: Workflow, file_path: str) -> bool:
    """
    Save a workflow to a file.
    
    Args:
        workflow: The workflow to save
        file_path: The path to save the workflow to
        
    Returns:
        True if the workflow was saved successfully, False otherwise
    """
    path = Path(file_path)
    
    try:
        with open(path, 'w') as f:
            if path.suffix == '.json':
                json.dump(workflow.to_dict(), f, indent=2)
            elif path.suffix in ('.yaml', '.yml'):
                yaml.dump(workflow.to_dict(), f, default_flow_style=False)
            else:
                raise ValueError(f"Unsupported file format: {path.suffix}")
        
        return True
    except (IOError, ValueError) as e:
        print(f"Error saving workflow: {e}")
        return False


def get_workflow_path(workflow_id: str) -> Path:
    """
    Get the path to a workflow file.
    
    Args:
        workflow_id: The ID of the workflow
        
    Returns:
        The path to the workflow file
    """
    workflows_dir = config.get_workflows_dir()
    return workflows_dir / f"{workflow_id}.json"