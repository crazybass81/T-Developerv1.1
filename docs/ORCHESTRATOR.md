# Orchestrator

## Overview

The **Agent Squad Orchestrator** (also called **DevCoordinator** or **SupervisorAgent**) is the central coordinator of the T-Developer system. It acts as the "brain of the operation," controlling the flow of tasks and information among various specialized agents.

## Core Responsibilities

1. **Workflow Management**: Initiates and manages end-to-end workflows for user requests
2. **Task Delegation**: Assigns tasks to appropriate agents and collects their outputs
3. **Decision Making**: Evaluates agent outputs and determines next steps
4. **Exception Handling**: Manages errors and unexpected situations
5. **Coordination**: Ensures proper sequencing and data flow between agents

## Orchestration Process

When a user submits a request, the Orchestrator follows this general process:

1. **Request Analysis**: The Orchestrator receives the user request and determines if it contains code or a goal
2. **Classification**: If code is provided, the Orchestrator calls the ClassifierAgent to determine its type
3. **Planning**: For goals, the Orchestrator calls the PlannerAgent to create a workflow plan
4. **Evaluation**: The EvaluatorAgent reviews the plan for quality and feasibility
5. **Execution**: If the plan is approved, the WorkflowExecutorAgent carries out the steps
6. **Result Delivery**: The final output is returned to the user

## Implementation

The Orchestrator is implemented as a MetaAgent that embodies the logic of coordinating other agents. It often takes the form of a loop or sequence encoded in the **OrchestratorTeam** – a predefined team that uses the orchestrator to call the core agents in order.

```python
from tdev.core import team
from tdev.agents import classifier_agent, planner_agent, evaluator_agent, workflow_executor_agent

@team
def orchestrator_team(request):
    """
    Coordinates the core agents to process a user request.
    """
    # Determine if the request contains code or a goal
    if "code" in request:
        # Classify the code
        classification = classifier_agent(request["code"])
        # Handle based on classification
        # ...
    else:
        # Plan a workflow for the goal
        plan = planner_agent(request["goal"])
        # Evaluate the plan
        evaluation = evaluator_agent(plan)
        # Execute if quality is sufficient
        if evaluation["score"] >= 85:
            result = workflow_executor_agent(plan)
            return result
        else:
            # Refine the plan or report issues
            # ...
```

## Dynamic Agent Generation

If the Orchestrator identifies that no existing component can fulfill a required functionality, it invokes **Agno (AutoAgentComposer)** to generate a new agent or tool on demand:

```python
# If no suitable agent exists for a task
if not registry.has_agent_for(task):
    # Generate a new agent
    agent_spec = {"goal": task["description"], "input": task["input_schema"], "output": task["output_schema"]}
    new_agent = agno.generate(agent_spec)
    # Register and use the new agent
    registry.register(new_agent)
    # Continue with the workflow
```

## Using the Orchestrator

The Orchestrator can be invoked via the CLI:

```bash
# Use the orchestrator to fulfill a goal
tdev orchestrate "Echo the input data"

# Provide additional context or constraints
tdev orchestrate "Create a dashboard for the data" --context '{"data_source": "api", "format": "web"}'
```

## Advanced Features

- **Parallel Orchestration**: Coordinate multiple agent workflows simultaneously
- **Adaptive Planning**: Adjust workflows based on intermediate results
- **Feedback Integration**: Incorporate user feedback to improve future orchestration
- **Resource Management**: Optimize resource allocation for efficient execution