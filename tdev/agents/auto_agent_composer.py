"""
AutoAgentComposer (Agno) - Agent generator for T-Developer.

This agent is responsible for automatically creating new agent definitions
when the existing library does not have what is needed for a given task.
"""
from typing import Dict, Any, Optional, Union
import json
from pathlib import Path

from tdev.core.agent import Agent
from tdev.core.registry import get_registry
from tdev.core.schema import AgentMeta, ToolMeta

class AutoAgentComposer(Agent):
    """
    Agent responsible for generating new agents and tools based on specifications.
    
    This is the implementation of the "agno" system described in the architecture.
    """
    
    def __init__(self):
        """Initialize the AutoAgentComposer."""
        self.registry = get_registry()
        self.templates = {
            "agent": {
                "simple": """from tdev.core.agent import Agent

class {name}Agent(Agent):
    """
    {description}
    """
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: {input_desc}
            
        Returns:
            {output_desc}
        """
        # TODO: Implement agent logic
        {implementation}
        return result
""",
                "tool_wrapper": """from tdev.core.agent import Agent

class {name}Agent(Agent):
    """
    {description}
    """
    
    def __init__(self):
        """Initialize the agent."""
        from tdev.core.registry import get_registry
        self.registry = get_registry()
        self.tool = self.registry.get_instance("{tool_name}")
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: {input_desc}
            
        Returns:
            {output_desc}
        """
        # Use the tool to process the input
        result = self.tool.run(input_data)
        return result
"""
            },
            "tool": {
                "simple": """from tdev.core.tool import tool

@tool
def {name_lower}_tool(input_data):
    """
    {description}
    
    Args:
        input_data: {input_desc}
        
    Returns:
        {output_desc}
    """
    # TODO: Implement tool logic
    {implementation}
    return result
"""
            }
        }
    
    def run(self, spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate a new agent or tool based on the specification.
        
        Args:
            spec: A dictionary containing the specification for the new component.
                Required keys:
                - type: "agent" or "tool"
                - name: Name of the component
                - goal: Description of what the component should do
                Optional keys:
                - tools: List of tool names to use (for agents)
                - input: Description of input data
                - output: Description of output data
                - template: Template to use (e.g., "simple", "tool_wrapper")
                
        Returns:
            A dictionary containing the result of the generation:
            - success: Whether the generation was successful
            - path: Path to the generated file
            - metadata: Metadata for the new component
        """
        # Extract required information
        component_type = spec.get("type", "agent").lower()
        name = spec.get("name")
        goal = spec.get("goal", "")
        
        if not name:
            return {"success": False, "error": "Name is required"}
        
        # Extract optional information
        tools = spec.get("tools", [])
        input_desc = spec.get("input", "The input data")
        output_desc = spec.get("output", "The output data")
        template_name = spec.get("template", "simple")
        
        # Generate the code
        if component_type == "agent":
            code, metadata = self._generate_agent(name, goal, tools, input_desc, output_desc, template_name)
        elif component_type == "tool":
            code, metadata = self._generate_tool(name, goal, input_desc, output_desc, template_name)
        else:
            return {"success": False, "error": f"Unknown component type: {component_type}"}
        
        # Save the code to a file
        file_path = self._save_code(component_type, name, code)
        
        # Register the component
        self._register_component(metadata)
        
        return {
            "success": True,
            "path": str(file_path),
            "metadata": metadata.to_dict()
        }
    
    def _generate_agent(self, name, goal, tools, input_desc, output_desc, template_name):
        """Generate code for an agent."""
        # Choose the template
        if tools and template_name == "tool_wrapper":
            template = self.templates["agent"]["tool_wrapper"]
            implementation = ""
            tool_name = tools[0] if isinstance(tools, list) else tools
        else:
            template = self.templates["agent"]["simple"]
            implementation = "result = input_data  # Replace with actual implementation"
            tool_name = ""
        
        # Format the template
        code = template.format(
            name=name,
            description=goal,
            input_desc=input_desc,
            output_desc=output_desc,
            implementation=implementation,
            tool_name=tool_name
        )
        
        # Create metadata
        metadata = AgentMeta(
            name=f"{name}Agent",
            class_path=f"tdev.agents.{name.lower()}_agent.{name}Agent",
            description=goal,
            tags=["generated", "agno"]
        )
        
        return code, metadata
    
    def _generate_tool(self, name, goal, input_desc, output_desc, template_name):
        """Generate code for a tool."""
        # Choose the template
        template = self.templates["tool"]["simple"]
        
        # Format the template
        code = template.format(
            name=name,
            name_lower=name.lower(),
            description=goal,
            input_desc=input_desc,
            output_desc=output_desc,
            implementation="result = input_data  # Replace with actual implementation"
        )
        
        # Create metadata
        metadata = ToolMeta(
            name=f"{name}Tool",
            class_path=f"tdev.tools.{name.lower()}_tool.{name.lower()}_tool",
            description=goal,
            tags=["generated", "agno"]
        )
        
        return code, metadata
    
    def _save_code(self, component_type, name, code):
        """Save the generated code to a file."""
        if component_type == "agent":
            directory = Path("tdev/agents")
            filename = f"{name.lower()}_agent.py"
        else:  # tool
            directory = Path("tdev/tools")
            filename = f"{name.lower()}_tool.py"
        
        file_path = directory / filename
        
        with open(file_path, "w") as f:
            f.write(code)
        
        return file_path
    
    def _register_component(self, metadata):
        """Register the component in the registry."""
        self.registry.register(metadata.name, metadata.to_dict())