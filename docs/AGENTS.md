# Agent Development Guide

## What is an Agent?

In T-Developer, an **Agent** is a component with a single decision-making point ("1 brain"). Agents are more complex than Tools but simpler than Teams. They can make decisions, process inputs, and produce outputs based on their specialized functionality.

## Core System Agents

T-Developer includes several built-in agents that form the backbone of the orchestration system:

1. **ClassifierAgent**: Analyzes code to determine its type (Tool/Agent/Team)
2. **PlannerAgent**: Breaks down goals into steps and selects appropriate agents
3. **EvaluatorAgent**: Scores workflows for quality and efficiency
4. **WorkflowExecutorAgent**: Runs the composed workflows step by step
5. **AutoAgentComposer (Agno)**: Generates new agents and tools based on specifications

## Creating a New Agent

### Using the CLI

```bash
# Create a new agent
tdev init agent --name MyAgent

# Edit the agent file
vim tdev/agents/my_agent.py

# Register the agent
tdev register tdev/agents/my_agent.py

# Test the agent
tdev test MyAgent
```

### Agent Structure

A basic agent follows this structure:

```python
from tdev.core import agent

@agent
def my_agent(input_data):
    """
    My custom agent that does something specific.
    
    Args:
        input_data: The input data for the agent
        
    Returns:
        The processed output
    """
    # Agent logic here
    result = process_data(input_data)
    return result
```

### Using Tools within Agents

Agents can use Tools to perform specific functions:

```python
from tdev.core import agent
from tdev.tools import some_tool, another_tool

@agent
def my_agent(input_data):
    # Use tools within your agent
    intermediate_result = some_tool(input_data)
    final_result = another_tool(intermediate_result)
    return final_result
```

## Agent Metadata

Each agent has associated metadata that describes its capabilities:

- **name**: Unique identifier for the agent
- **description**: What the agent does
- **input_schema**: Expected input format
- **output_schema**: Expected output format
- **tools**: List of tools used by the agent
- **brain_count**: Always 1 for agents
- **reusability**: Rating of how reusable the agent is (A-D)

## Testing Agents

Agents should be tested to ensure they work as expected:

```bash
# Test an agent with specific input
tdev test MyAgent --input '{"key": "value"}'

# Run all tests for an agent
tdev test MyAgent --all
```

## Best Practices

1. **Single Responsibility**: Each agent should have a clear, focused purpose
2. **Clear Documentation**: Document inputs, outputs, and behavior
3. **Error Handling**: Handle exceptions gracefully
4. **Tool Composition**: Use existing tools rather than reimplementing functionality
5. **Statelessness**: Design agents to be stateless when possible
6. **Testing**: Create comprehensive tests for your agent