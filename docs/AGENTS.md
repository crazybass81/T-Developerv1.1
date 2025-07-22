# Agent Development Guide

## Overview

Agents in T-Developer are components with a single decision-making point (1 brain) that perform specific roles. As of Phase 3, agents can be created manually or generated automatically using the Agno system (AutoAgentComposer).

This guide explains how to create and register agents in the T-Developer system.

## Agent Roles in T-Developer

In T-Developer, an **Agent** is a component with a single decision point (1 brain) that performs a specific role. Agents are more complex than Tools but simpler than Teams. They can use Tools internally to accomplish their tasks.

### Agents vs. Teams

While both Agents and Teams perform tasks, they differ in complexity:

- **Agents** have a single decision point (1 brain) and typically focus on a specific task
- **Teams** have multiple decision points (2+ brains) and coordinate multiple agents to accomplish more complex tasks

For information on creating Teams, see the [Team Development Guide](TEAMS.md).

Core agent types in the system include:

- **ClassifierAgent**: Analyzes code to determine its type (Tool/Agent/Team)
- **PlannerAgent**: Plans workflows by selecting and ordering agents and teams
- **EvaluatorAgent**: Evaluates workflows for quality and efficiency
- **WorkflowExecutorAgent**: Executes workflows step by step
- **TeamExecutorAgent**: Executes teams and their member agents
- **AgentTesterAgent**: Tests agents with sample inputs

## Steps to Implement a New Agent

### Option 1: Generate an Agent using Agno

The easiest way to create a new agent is to use the Agno system (AutoAgentComposer):

```bash
tdev generate agent --name MyAgent --goal "Description of what the agent should do"
```

You can also provide a more detailed specification in a JSON file:

```bash
tdev generate agent --spec path/to/specification.json
```

The specification file should have this format:

```json
{
  "type": "agent",
  "name": "MyAgent",
  "goal": "Description of what the agent should do",
  "input": "Description of the input data",
  "output": "Description of the output data"
}
```

### Option 2: Create an Agent Manually

#### 1. Create a New Agent File

You can use the CLI to create a new agent:

```bash
tdev init agent --name MyAgent
```

This will create a file at `tdev/agents/my_agent.py` with a basic agent template.

Alternatively, you can create the file manually:

```python
from tdev.core.agent import Agent

class MyAgent(Agent):
    """
    My custom agent.
    """
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: The input data
            
        Returns:
            The output data
        """
        # TODO: Implement agent logic
        return input_data
```

### 2. Implement the Agent Logic

Implement the `run` method with your agent's logic. This method should:

- Accept input data (any type)
- Process the data according to the agent's purpose
- Return output data (any type)

Example:

```python
from tdev.core.agent import Agent
from tdev.core.registry import get_registry

class SummarizerAgent(Agent):
    """
    Agent that summarizes text.
    """
    
    def run(self, text):
        """
        Summarize the input text.
        
        Args:
            text: The text to summarize
            
        Returns:
            A summary of the text
        """
        # Get a tool from the registry
        registry = get_registry()
        gpt_tool = registry.get_instance("GPTCallerTool")
        
        if gpt_tool:
            # Use the tool to generate a summary
            prompt = f"Summarize the following text:\n\n{text}"
            summary = gpt_tool.run(prompt)
            return summary
        else:
            # Fallback to a simple summary
            words = text.split()
            if len(words) > 50:
                return " ".join(words[:50]) + "..."
            return text
```

### 3. Using Tools in Agents

Agents can use Tools to perform specific tasks. To use a Tool:

1. Get the registry
2. Get the tool instance
3. Call the tool's `run` method

```python
def run(self, input_data):
    # Get the registry
    registry = get_registry()
    
    # Get a tool
    tool = registry.get_instance("SomeTool")
    
    # Use the tool
    result = tool.run(input_data)
    
    # Process the result
    # ...
    
    return processed_result
```

### 4. Registering the Agent

Register your agent in the registry using the CLI:

```bash
tdev register tdev/agents/my_agent.py
```

This will add your agent to the registry, making it available for use in workflows.

Alternatively, you can register the agent programmatically:

```python
from tdev.core.registry import get_registry
from tdev.core.schema import AgentMeta

# Get the registry
registry = get_registry()

# Create agent metadata
agent_meta = AgentMeta(
    name="MyAgent",
    class_path="tdev.agents.my_agent.MyAgent",
    description="My custom agent",
    tags=["custom"]
)

# Register the agent
registry.register("MyAgent", agent_meta.to_dict())
```

## Agent Metadata

Agent metadata includes:

- **name**: The name of the agent
- **type**: Always "agent" for agents
- **class_path**: The import path to the agent class
- **description**: A description of the agent
- **brain_count**: The number of decision points (1 for agents)
- **reusability**: The reusability tier ("B" for agents)
- **input_schema**: Optional schema for input data
- **output_schema**: Optional schema for output data
- **tags**: Optional tags for categorization

## Testing Agents

You can test your agent using the AgentTesterAgent:

```bash
tdev test MyAgent
```

This will run the agent with a simple test case and report the result.

For more thorough testing, you can create unit tests in the `tests/` directory:

```python
def test_my_agent():
    agent = MyAgent()
    result = agent.run("test input")
    assert result == "expected output"
```

## Best Practices

1. **Single Responsibility**: Each agent should have a clear, focused purpose
2. **Error Handling**: Handle exceptions gracefully and provide meaningful error messages
3. **Documentation**: Include docstrings explaining the agent's purpose and parameters
4. **Reusability**: Design agents to be as reusable as possible
5. **Testing**: Create tests to verify the agent's behavior

## Example: EchoAgent

Here's a complete example of a simple agent:

```python
from tdev.core.agent import Agent

class EchoAgent(Agent):
    """
    A simple agent that echoes the input data.
    """
    
    def run(self, input_data):
        """
        Run the agent.
        
        Args:
            input_data: The input data
            
        Returns:
            The same input data
        """
        print(f"EchoAgent received: {input_data}")
        return input_data
```

This agent simply returns the input it receives, demonstrating the basic structure of an agent.