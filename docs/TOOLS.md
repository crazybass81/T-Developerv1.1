# Tool Development Guide

## Overview

Tools in T-Developer are pure functions with no decision logic (0 brains) that perform specific tasks. As of Phase 3, tools can be created manually or generated automatically using the Agno system (AutoAgentComposer).

This guide explains how to create and register tools in the T-Developer system.

## What is a Tool vs an Agent

In T-Developer, a **Tool** is a pure function with no decision logic (0 brains). Tools are the simplest components in the system and serve as highly reusable, atomic operations that perform specific tasks.

Key differences between Tools and Agents:

| Aspect | Tool | Agent |
| ------ | ---- | ----- |
| Decision Logic | None | One or more decision points |
| Brain Count | 0 | 1+ |
| Reusability | Very High (A) | High to Medium (B-C) |
| Implementation | Function with `@tool` decorator | Class inheriting from `Agent` |

## Steps to Create a Tool

### Option 1: Generate a Tool using Agno

The easiest way to create a new tool is to use the Agno system (AutoAgentComposer):

```bash
tdev generate tool --name MyTool --goal "Description of what the tool should do"
```

You can also provide a more detailed specification in a JSON file:

```bash
tdev generate tool --spec path/to/specification.json
```

The specification file should have this format:

```json
{
  "type": "tool",
  "name": "MyTool",
  "goal": "Description of what the tool should do",
  "input": "Description of the input data",
  "output": "Description of the output data"
}
```

### Option 2: Create a Tool Manually

#### 1. Create a New Tool File

You can use the CLI to create a new tool:

```bash
tdev init tool --name MyTool
```

This will create a file at `tdev/tools/my_tool.py` with a basic tool template.

Alternatively, you can create the file manually:

```python
from tdev.core.tool import tool

@tool
def my_tool(input_data):
    """
    My custom tool.
    
    Args:
        input_data: The input data
        
    Returns:
        The output data
    """
    # TODO: Implement tool logic
    return input_data
```

### 2. Implement the Tool Logic

Implement the tool function with your logic. This function should:

- Accept input parameters
- Process the data according to the tool's purpose
- Return output data
- Have no decision logic (no if/else statements based on the input)

Example:

```python
from tdev.core.tool import tool

@tool
def uppercase_tool(text):
    """
    Convert text to uppercase.
    
    Args:
        text: The text to convert
        
    Returns:
        The uppercase text
    """
    return text.upper()
```

### 3. Using the Tool Decorator

The `@tool` decorator marks a function as a tool and registers it with the system. It adds metadata to the function that can be used by the registry.

```python
@tool
def my_tool(param1, param2):
    # Tool logic here
    return result
```

### 4. Registering the Tool

Register your tool in the registry using the CLI:

```bash
tdev register tdev/tools/my_tool.py
```

This will add your tool to the registry, making it available for use by agents and in workflows.

Alternatively, you can register the tool programmatically:

```python
from tdev.core.registry import get_registry
from tdev.core.schema import ToolMeta

# Get the registry
registry = get_registry()

# Create tool metadata
tool_meta = ToolMeta(
    name="MyTool",
    class_path="tdev.tools.my_tool.my_tool",
    description="My custom tool",
    tags=["custom"]
)

# Register the tool
registry.register("MyTool", tool_meta.to_dict())
```

## Tool Metadata

Tool metadata includes:

- **name**: The name of the tool
- **type**: Always "tool" for tools
- **class_path**: The import path to the tool function
- **description**: A description of the tool
- **brain_count**: The number of decision points (0 for tools)
- **reusability**: The reusability tier ("A" for tools)
- **input_schema**: Optional schema for input data
- **output_schema**: Optional schema for output data
- **tags**: Optional tags for categorization

## Testing Tools

You can test your tool using the AgentTesterAgent:

```bash
tdev test MyTool
```

This will run the tool with a simple test case and report the result.

For more thorough testing, you can create unit tests in the `tests/` directory:

```python
def test_my_tool():
    from tdev.tools.my_tool import my_tool
    result = my_tool("test input")
    assert result == "expected output"
```

## Class-Based Tools

While most tools are implemented as functions with the `@tool` decorator, you can also create class-based tools by inheriting from the `Tool` class:

```python
from tdev.core.tool import Tool

class UppercaseTool(Tool):
    """
    Tool that converts text to uppercase.
    """
    
    def run(self, text):
        """
        Convert text to uppercase.
        
        Args:
            text: The text to convert
            
        Returns:
            The uppercase text
        """
        return text.upper()
```

## Best Practices

1. **Pure Functions**: Tools should be pure functions with no side effects
2. **No Decision Logic**: Tools should not contain decision logic based on the input
3. **Single Responsibility**: Each tool should do one thing well
4. **Error Handling**: Handle exceptions gracefully and provide meaningful error messages
5. **Documentation**: Include docstrings explaining the tool's purpose and parameters
6. **Type Hints**: Use type hints to clarify input and output types

## Example: LLM Caller Tool

Here's an example of a tool that calls an LLM API:

```python
from tdev.core.tool import tool
import requests

@tool
def gpt_caller_tool(prompt, model="gpt-3.5-turbo", temperature=0.7):
    """
    Call an LLM API to generate text.
    
    Args:
        prompt: The prompt to send to the LLM
        model: The model to use (default: gpt-3.5-turbo)
        temperature: The temperature parameter (default: 0.7)
        
    Returns:
        The generated text
    """
    # This is a simplified example - in a real tool, you would use the OpenAI SDK
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        return "Error: OPENAI_API_KEY environment variable not set"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": temperature
    }
    
    response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=data)
    
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return f"Error: {response.status_code} - {response.text}"
```

This tool demonstrates how to create a more complex tool that interacts with an external API.