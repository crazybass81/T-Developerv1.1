"""
AutoAgentComposer (Agno) - Agent generator for T-Developer.

This agent is responsible for automatically creating new agent definitions
when the existing library does not have what is needed for a given task.
"""
from typing import Dict, Any, Optional, Union
import json
import os
from pathlib import Path

from tdev.core.agent import Agent
from tdev.core.registry import get_registry
from tdev.core.schema import AgentMeta, ToolMeta
from tdev.agent_core.bedrock_client import BedrockClient

class AutoAgentComposer(Agent):
    """
    Agent responsible for generating new agents and tools based on specifications.
    
    This is the implementation of the "agno" system described in the architecture.
    It uses AWS Bedrock for intelligent code generation when available.
    """
    
    def __init__(self):
        """Initialize the AutoAgentComposer."""
        self.registry = get_registry()
        self.bedrock_client = None
        try:
            self.bedrock_client = BedrockClient()
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
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
                - implementation_hints: Hints for implementing the component
                
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
        implementation_hints = spec.get("implementation_hints", "")
        
        # Analyze available tools that might be useful
        available_tools = self._find_relevant_tools(goal)
        if available_tools and not tools:
            tools = [tool["name"] for tool in available_tools[:2]]  # Use up to 2 relevant tools
        
        # Generate the code
        if component_type == "agent":
            code, metadata = self._generate_agent(name, goal, tools, input_desc, output_desc, template_name, implementation_hints)
        elif component_type == "tool":
            code, metadata = self._generate_tool(name, goal, input_desc, output_desc, template_name, implementation_hints)
        else:
            return {"success": False, "error": f"Unknown component type: {component_type}"}
        
        # Save the code to a file
        file_path = self._save_code(component_type, name, code)
        
        # Register the component
        self._register_component(metadata)
        
        # Generate tests for the component
        test_file_path = self._generate_tests(component_type, name, goal, input_desc, output_desc)
        
        return {
            "success": True,
            "path": str(file_path),
            "test_path": str(test_file_path) if test_file_path else None,
            "metadata": metadata.to_dict(),
            "used_tools": tools
        }
    
    def _generate_agent(self, name, goal, tools, input_desc, output_desc, template_name, implementation_hints=""):
        """Generate code for an agent."""
        # Choose the template
        if tools and template_name == "tool_wrapper":
            template = self.templates["agent"]["tool_wrapper"]
            implementation = ""
            tool_name = tools[0] if isinstance(tools, list) else tools
        else:
            template = self.templates["agent"]["simple"]
            implementation = self._generate_implementation("agent", name, goal, tools, implementation_hints)
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
            tags=["generated", "agno"],
            tools=tools
        )
        
        return code, metadata
    
    def _generate_tool(self, name, goal, input_desc, output_desc, template_name, implementation_hints=""):
        """Generate code for a tool."""
        # Choose the template
        template = self.templates["tool"]["simple"]
        
        # Generate implementation based on the goal
        implementation = self._generate_implementation("tool", name, goal, [], implementation_hints)
        
        # Format the template
        code = template.format(
            name=name,
            name_lower=name.lower(),
            description=goal,
            input_desc=input_desc,
            output_desc=output_desc,
            implementation=implementation
        )
        
        # Create metadata
        metadata = ToolMeta(
            name=f"{name}Tool",
            class_path=f"tdev.tools.{name.lower()}_tool.{name.lower()}_tool",
            description=goal,
            tags=["generated", "agno"]
        )
        
        return code, metadata
        
    def _generate_implementation(self, component_type, name, goal, tools, implementation_hints=""):
        """Generate implementation code based on the goal and available tools."""
        # Use Bedrock for intelligent code generation if available
        if self.bedrock_client:
            implementation = self._generate_with_bedrock(component_type, name, goal, tools, implementation_hints)
            if implementation:
                return implementation
        
        # Default implementation if Bedrock is not available or fails
        default_impl = "result = input_data  # Replace with actual implementation"
        
        # If we have implementation hints, use them
        if implementation_hints:
            return f"# Implementation based on hints:\n        # {implementation_hints}\n        {default_impl}"
        
        # Generate implementation based on the goal
        if "echo" in goal.lower() or "repeat" in goal.lower():
            return "result = input_data  # Simple echo implementation"
        
        if "transform" in goal.lower() or "convert" in goal.lower():
            return "# Transform the input data\n        # This is a placeholder for the transformation logic\n        result = self._transform_data(input_data)\n        \n    def _transform_data(self, data):\n        # Implement the transformation logic here\n        return data  # Replace with actual transformation"
        
        if "analyze" in goal.lower() or "process" in goal.lower():
            return "# Analyze the input data\n        # This is a placeholder for the analysis logic\n        result = {}\n        result['analysis'] = 'Analysis of ' + str(input_data)\n        result['processed'] = True\n        return result"
        
        if "fetch" in goal.lower() or "retrieve" in goal.lower() or "get" in goal.lower():
            return "# Fetch data from a source\n        # This is a placeholder for the fetching logic\n        import requests\n        \n        # Example: Make an API request\n        # url = f'https://api.example.com/data?q={input_data}'\n        # response = requests.get(url)\n        # result = response.json()\n        \n        # For now, return a mock result\n        result = {'data': f'Fetched data for: {input_data}', 'status': 'success'}\n        return result"
        
        # If we have tools, generate code to use them
        if tools:
            tool_code = """# Use available tools to process the input
        """
            for i, tool in enumerate(tools):
                tool_var = f"tool{i+1}"
                tool_code += f"\n        {tool_var} = self.registry.get_instance(\"{tool}\")\n"
            
            tool_code += "\n        # Process with tools\n"
            if len(tools) == 1:
                tool_code += "        result = tool1.run(input_data)\n"
            else:
                tool_code += "        intermediate = tool1.run(input_data)\n"
                for i in range(1, len(tools)):
                    if i == len(tools) - 1:
                        tool_code += f"        result = tool{i+1}.run(intermediate)\n"
                    else:
                        tool_code += f"        intermediate = tool{i+1}.run(intermediate)\n"
            
            return tool_code
        
        # Default implementation with a TODO comment
        return f"# TODO: Implement {component_type} logic for: {goal}\n        {default_impl}"
        
    def _generate_with_bedrock(self, component_type, name, goal, tools, implementation_hints=""):
        """
        Generate implementation code using AWS Bedrock.
        
        Args:
            component_type: Type of component ("agent" or "tool")
            name: Name of the component
            goal: Description of what the component should do
            tools: List of tools to use (for agents)
            implementation_hints: Optional hints for implementation
            
        Returns:
            Generated implementation code or None if generation fails
        """
        try:
            # Prepare the prompt for Bedrock
            tools_str = ", ".join(tools) if tools else "None"
            
            prompt = f"""You are an AI code generator. Your task is to generate Python code for a {component_type} in the T-Developer framework.

Details:
- Name: {name}
- Type: {component_type}
- Goal: {goal}
- Available tools: {tools_str}
- Implementation hints: {implementation_hints}

Requirements:
- The code should be a Python function or method body that can be inserted into a {component_type} class/function
- For an agent, the code should implement the 'run' method that takes 'input_data' as parameter
- For a tool, the code should implement a function that takes 'input_data' as parameter
- The code should return a result variable
- The code should be well-commented and follow best practices
- If tools are available, use them appropriately

Generate ONLY the implementation code (function/method body), not the entire class or function definition.
Do not include the function/method signature or decorators.

Code:
"""
            
            # Call Bedrock to generate the code
            model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v2")
            response = self.bedrock_client.invoke_model(
                model_id=model_id,
                prompt=prompt,
                parameters={
                    "maxTokens": 1500,
                    "temperature": 0.4,
                    "topP": 0.9
                }
            )
            
            # Extract the code from the response
            if "anthropic" in model_id.lower():
                completion = response.get("completion", "")
            else:
                completion = response.get("outputText", "")
            
            # Clean up the code
            # Remove any markdown code block markers
            code = completion.replace("```python", "").replace("```", "")
            
            # Remove any function/method signature
            if "def run" in code:
                code = code[code.find("def run"):]
                code = code[code.find(":") + 1:]
            elif "def " in code:
                code = code[code.find("def "):]
                code = code[code.find(":") + 1:]
            
            # Ensure proper indentation
            lines = code.strip().split("\n")
            cleaned_lines = []
            for line in lines:
                # Remove excessive indentation but keep some for method body
                stripped = line.lstrip()
                if stripped:
                    cleaned_lines.append("        " + stripped)
                else:
                    cleaned_lines.append("")
            
            # Join the lines back together
            cleaned_code = "\n".join(cleaned_lines)
            
            # Ensure the code returns a result
            if "return" not in cleaned_code:
                cleaned_code += "\n        return input_data  # Default return if no return statement was generated"
            
            return cleaned_code
            
        except Exception as e:
            print(f"Error generating code with Bedrock: {e}")
            return None
    
    def _find_relevant_tools(self, goal):
        """Find tools that might be relevant for the given goal."""
        available_tools = self.registry.get_by_type("tool")
        relevant_tools = []
        
        # Simple keyword matching for now
        # In a production system, this would use semantic similarity or an LLM
        keywords = goal.lower().split()
        for tool in available_tools:
            tool_desc = tool.get("description", "").lower()
            if any(keyword in tool_desc for keyword in keywords):
                relevant_tools.append(tool)
        
        return relevant_tools
    
    def _generate_tests(self, component_type, name, goal, input_desc, output_desc):
        """Generate tests for the component."""
        # In a production system, this would generate actual test cases
        # For now, we'll just create a test file with a basic test
        
        if component_type == "agent":
            test_dir = Path("tests/agents")
            test_filename = f"test_{name.lower()}_agent.py"
            component_name = f"{name}Agent"
            import_path = f"tdev.agents.{name.lower()}_agent"
        else:  # tool
            test_dir = Path("tests/tools")
            test_filename = f"test_{name.lower()}_tool.py"
            component_name = f"{name.lower()}_tool"
            import_path = f"tdev.tools.{name.lower()}_tool"
        
        # Create test directory if it doesn't exist
        test_dir.mkdir(parents=True, exist_ok=True)
        
        test_file_path = test_dir / test_filename
        
        # Generate a basic test
        test_code = f"""import pytest
from {import_path} import {component_name}

def test_{name.lower()}_basic():
    """Test that the {component_name} works with basic input."""
    # Arrange
    {'agent = ' + component_name + '()' if component_type == 'agent' else 'pass'}
    input_data = "test_input"  # Replace with appropriate test input
    
    # Act
    {'result = agent.run(input_data)' if component_type == 'agent' else 'result = ' + component_name + '(input_data)'}
    
    # Assert
    assert result is not None
    # Add more specific assertions based on expected behavior
"""
        
        with open(test_file_path, "w") as f:
            f.write(test_code)
        
        return test_file_path
    
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