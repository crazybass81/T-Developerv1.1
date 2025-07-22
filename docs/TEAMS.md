# Teams in T-Developer

This document explains what Teams are in the T-Developer system, how to create and use them, and how they differ from Agents and Tools.

## What is a Team?

In T-Developer, a **Team** is a composite component consisting of multiple agents acting as one unit. Teams have more than one decision-making point (2+ "brains") and include internal coordination logic to orchestrate the behavior of their member agents.

Teams are the highest-level component type in the system, designed to accomplish larger tasks by coordinating the work of multiple specialized agents.

Key characteristics of Teams:
- Multiple decision points (2+ brains)
- Internal coordination logic
- Lower reusability (Tier D) compared to Agents and Tools
- Ability to encapsulate complex workflows as a single component

## Creating a New Team

### Using the CLI

The easiest way to create a new Team is using the T-Developer CLI:

```bash
tdev init team --name MyTeam
```

This command will:
1. Create a new Python file at `tdev/teams/my_team.py`
2. Generate a class template that inherits from `Team`
3. Include placeholder methods for adding agents and implementing coordination logic

### Manual Creation

To create a Team manually:

1. Create a new Python file in the `tdev/teams/` directory
2. Define a class that inherits from `Team`
3. Implement the required methods

Here's a basic template:

```python
from tdev.core.team import Team
from tdev.core.registry import get_registry

class MyTeam(Team):
    """
    MyTeam description.
    """
    
    def __init__(self):
        """Initialize the team with its member agents."""
        super().__init__()
        
        # Get the registry
        registry = get_registry()
        
        # Add member agents
        self.add_agent("agent1", registry.get_instance("Agent1"))
        self.add_agent("agent2", registry.get_instance("Agent2"))
    
    def run(self, input_data):
        """
        Coordinate the team's workflow.
        
        Args:
            input_data: The input data for the team
            
        Returns:
            The output data from the team
        """
        # Get the first agent
        agent1 = self.agents.get("agent1")
        
        # Run the first agent
        intermediate_result = agent1.run(input_data)
        
        # Get the second agent
        agent2 = self.agents.get("agent2")
        
        # Run the second agent with the result from the first
        final_result = agent2.run(intermediate_result)
        
        return final_result
```

## Implementing Team Logic

The core of a Team is its `run` method, which coordinates the execution of its member agents. This typically involves:

1. Retrieving member agents from the `self.agents` dictionary
2. Executing each agent in the appropriate sequence
3. Managing the data flow between agents
4. Handling any errors or exceptions
5. Returning the final result

For most teams, the coordination logic follows a sequential pattern, where the output of one agent becomes the input to the next. However, more complex patterns are possible, such as:

- Conditional execution based on intermediate results
- Parallel execution of independent agents
- Iterative execution with feedback loops

## Registering a Team

After creating a Team, you need to register it with the system:

```bash
tdev register tdev/teams/my_team.py
```

This will:
1. Analyze the file to determine it's a Team
2. Add an entry to the registry with type "team"
3. Set appropriate metadata (brain_count: 2+, reusability: "D")

You can also register a Team programmatically:

```python
from tdev.core.registry import get_registry
from tdev.core.schema import TeamMeta

team_meta = TeamMeta(
    name="MyTeam",
    class_path="tdev.teams.my_team.MyTeam",
    description="My custom team that does X and Y.",
    tags=["custom", "example"]
)

registry = get_registry()
registry.register("MyTeam", team_meta.to_dict())
```

## Running and Using Teams

### Direct Execution

You can run a Team directly using the CLI:

```bash
tdev run-team MyTeam --input '{"key": "value"}'
```

This will:
1. Look up the Team in the registry
2. Instantiate it
3. Call its `run` method with the provided input
4. Display the result

### In Workflows

Once registered, a Team can be used as a step in a workflow, just like an Agent:

```bash
tdev compose --name my-workflow --steps "MyTeam,AnotherAgent"
```

The workflow executor will treat the Team as a single step, executing its entire internal sequence as one unit.

## Teams vs. Agents vs. Tools

| Aspect | Team | Agent | Tool |
|--------|------|-------|------|
| Decision Points | 2+ | 1 | 0 |
| Brain Count | 2+ | 1 | 0 |
| Reusability | Low (D) | Medium (B) | High (A) |
| Complexity | High | Medium | Low |
| Purpose | Coordinate multiple agents | Perform a specific role | Execute a single function |
| Implementation | Class with member agents | Class with decision logic | Pure function |

## Best Practices

When creating Teams:

1. **Keep it focused**: A Team should have a clear, well-defined purpose
2. **Ensure data compatibility**: Make sure the output of one agent can serve as input to the next
3. **Document the workflow**: Clearly describe the sequence and purpose of each step
4. **Handle errors gracefully**: Include error handling for each agent call
5. **Consider reusability**: If a sequence of agents is used frequently, it's a good candidate for a Team
6. **Avoid deep nesting**: While Teams can include other Teams as members, avoid deep hierarchies

## Example: DoubleEchoTeam

Here's a complete example of a simple Team that calls an EchoAgent twice in sequence:

```python
from tdev.core.team import Team
from tdev.core.registry import get_registry

class DoubleEchoTeam(Team):
    """
    DoubleEchoTeam demonstrates a simple team that calls EchoAgent twice.
    """
    
    def __init__(self):
        """Initialize the team with EchoAgent instances."""
        super().__init__()
        
        # Get the registry
        registry = get_registry()
        
        # Add two instances of EchoAgent
        self.add_agent("echo1", registry.get_instance("EchoAgent"))
        self.add_agent("echo2", registry.get_instance("EchoAgent"))
    
    def run(self, input_data):
        """
        Run the team by calling EchoAgent twice in sequence.
        
        Args:
            input_data: The input data for the first echo
            
        Returns:
            The result of the second echo
        """
        # First echo
        echo1 = self.agents.get("echo1")
        first_result = echo1.run(input_data)
        
        # Second echo
        echo2 = self.agents.get("echo2")
        second_result = echo2.run(first_result)
        
        return second_result
```

To use this Team:

```bash
# Register the team
tdev register tdev/teams/double_echo_team.py

# Run the team
tdev run-team DoubleEchoTeam --input '{"message": "Hello, Team!"}'
```

## Case Study: OrchestratorTeam and AutoDevTeam

The `OrchestratorTeam` is a core component of T-Developer that demonstrates how Teams can encapsulate complex workflows. In Phase 3, it has been enhanced to use the MetaAgent as the central coordinator.

### Phase 3 Architecture: AutoDevTeam

The AutoDevTeam is the Phase 3 implementation of the OrchestratorTeam, which uses the MetaAgent to coordinate the following core agents:

1. **MetaAgent**: The central orchestrator that coordinates the flow
2. **ClassifierAgent**: Analyzes code to determine its type
3. **PlannerAgent**: Designs a workflow based on the goal and classification
4. **EvaluatorAgent**: Assesses the quality of the proposed workflow
5. **WorkflowExecutorAgent**: Executes the approved workflow
6. **AutoAgentComposer**: Generates new agents when needed

By packaging these agents into a Team, the orchestration logic becomes a single, reusable component that can be invoked with a simple call:

```bash
tdev run-team OrchestratorTeam --input '{"goal": "Build a document summarizer", "code": "path/to/code.py"}'
```

In Phase 3, you can also use the dedicated orchestrate command:

```bash
tdev orchestrate "Build a document summarizer" --code path/to/code.py
```

This demonstrates how Teams can abstract complex multi-agent processes into higher-level components. The MetaAgent within the OrchestratorTeam ensures that all agents work together seamlessly, and can even trigger the AutoAgentComposer to generate new agents when needed.

## Related Documentation

- [Agents in T-Developer](AGENTS.md) - For information about individual agents
- [Tools in T-Developer](TOOLS.md) - For information about tools
- [Workflows in T-Developer](WORKFLOWS.md) - For information about workflow composition