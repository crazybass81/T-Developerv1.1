# Tool Development Guide

## What is a Tool?

In T-Developer, a **Tool** is a pure functional component without decision logic ("0 brains"). Tools perform specific operations with well-defined inputs and outputs, making them the simplest building blocks in the system.

## Creating a New Tool

### Using the CLI

```bash
# Create a new tool
tdev init tool --name MyTool

# Edit the tool file
vim tdev/tools/my_tool.py

# Register the tool
tdev register tdev/tools/my_tool.py

# Test the tool
tdev test MyTool
```

### Tool Structure

A basic tool follows this structure:

```python
from tdev.core import tool

@tool
def my_tool(input_data):
    """
    My custom tool that performs a specific operation.
    
    Args:
        input_data: The input data for the tool
        
    Returns:
        The processed output
    """
    # Tool logic here
    result = transform_data(input_data)
    return result
```

## Tool Metadata

Each tool has associated metadata that describes its capabilities:

- **name**: Unique identifier for the tool
- **description**: What the tool does
- **input_schema**: Expected input format
- **output_schema**: Expected output format
- **brain_count**: Always 0 for tools
- **reusability**: Rating of how reusable the tool is (A-D)

## Testing Tools

Tools should be tested to ensure they work as expected:

```bash
# Test a tool with specific input
tdev test MyTool --input '{"key": "value"}'

# Run all tests for a tool
tdev test MyTool --all
```

## Tool Categories

Tools can be categorized based on their functionality:

1. **Data Processing Tools**: Transform, filter, or analyze data
2. **Integration Tools**: Connect to external services or APIs
3. **Utility Tools**: Perform common operations (parsing, formatting, etc.)
4. **Domain-Specific Tools**: Specialized for particular domains or tasks

## Best Practices

1. **Pure Functions**: Tools should be pure functions without side effects
2. **Single Responsibility**: Each tool should do one thing well
3. **Clear Documentation**: Document inputs, outputs, and behavior
4. **Error Handling**: Return clear error messages for invalid inputs
5. **Performance**: Optimize for efficiency, especially for frequently used tools
6. **Testing**: Create comprehensive tests for your tool