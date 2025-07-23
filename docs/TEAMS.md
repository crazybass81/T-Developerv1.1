# Team Development Guide

## What is a Team?

In T-Developer, a **Team** is a collaborative structure composed of multiple agents ("2+ brains"). Teams handle complex tasks by coordinating the work of multiple specialized agents, enabling more sophisticated workflows than individual agents can achieve.

## Creating a New Team

### Using the CLI

```bash
# Create a new team
tdev init team --name MyTeam

# Edit the team file
vim tdev/teams/my_team.py

# Register the team
tdev register tdev/teams/my_team.py

# Run the team
tdev run-team MyTeam --input '{"message": "Hello, Team!"}'
```

### Team Structure

A basic team follows this structure:

```python
from tdev.core import team
from tdev.agents import agent_one, agent_two

@team
def my_team(input_data):
    """
    My custom team that coordinates multiple agents.
    
    Args:
        input_data: The input data for the team
        
    Returns:
        The final output after all agents have processed the data
    """
    # Team workflow
    result1 = agent_one(input_data)
    result2 = agent_two(result1)
    return result2
```

## Team Metadata

Each team has associated metadata that describes its capabilities:

- **name**: Unique identifier for the team
- **description**: What the team does
- **input_schema**: Expected input format
- **output_schema**: Expected output format
- **agents**: List of agents used by the team
- **brain_count**: Number of decision points (2+)
- **reusability**: Rating of how reusable the team is (A-D)

## Team Types

T-Developer supports different types of teams:

1. **Sequential Teams**: Agents execute in a predefined sequence
2. **Parallel Teams**: Multiple agents execute simultaneously
3. **Conditional Teams**: Different agents execute based on conditions
4. **Recursive Teams**: Teams that can call themselves or other teams

## The OrchestratorTeam

The **OrchestratorTeam** is a special team that implements the Agent Squad Orchestrator. It coordinates the core system agents (Classifier, Planner, Evaluator, Executor) to process user requests and execute workflows.

## Best Practices

1. **Clear Workflow**: Define a clear sequence or structure for agent interactions
2. **Error Handling**: Handle failures in individual agents gracefully
3. **Data Flow**: Ensure proper data transformation between agents
4. **Reusability**: Design teams to be reusable for similar tasks
5. **Testing**: Test the team as a whole and individual agent interactions