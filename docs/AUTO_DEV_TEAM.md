# AutoDevTeam Assembly Approach

This document outlines how the core agents work together in Phase 3 of T-Developer as the AutoDevTeam, coordinated by the SupervisorAgent (DevCoordinator) using Agent Squad.

## Overview

The AutoDevTeam is a coordinated group of specialized agents that work together to fulfill user requests end-to-end. The SupervisorAgent (DevCoordinator) serves as the central orchestrator that sequences the other agents in the appropriate order.

## Team Composition

The AutoDevTeam consists of the following core agents:

1. **SupervisorAgent (DevCoordinator)**: The central coordinator that manages the flow between other agents using Agent Squad
2. **ClassifierAgent**: Analyzes code to classify it as Tool, Agent, or Team
3. **PlannerAgent**: Plans workflows by selecting and ordering appropriate agents
4. **EvaluatorAgent**: Evaluates workflows for quality and efficiency
5. **WorkflowExecutorAgent**: Executes workflows step by step
6. **AutoAgentComposer (Agno)**: Generates new agents when needed

## Interaction Pattern

The interaction pattern follows this sequence:

1. **User Request**: The user submits a goal or code to the DevCoordinator
2. **Classification (if code provided)**: The DevCoordinator invokes the ClassifierAgent to analyze the code
3. **Planning**: The DevCoordinator invokes the PlannerAgent to generate a workflow plan
4. **Evaluation**: The DevCoordinator invokes the EvaluatorAgent to assess the plan's quality
5. **Refinement (if needed)**: If the evaluation score is below threshold, the DevCoordinator requests the PlannerAgent to refine the plan
6. **Execution**: The DevCoordinator invokes the WorkflowExecutorAgent to run the workflow
7. **Dynamic Agent Generation (if needed)**: If the PlannerAgent identifies a missing capability, the DevCoordinator invokes the AutoAgentComposer to generate a new agent

## Data Flow

The data flows between agents as follows:

1. **User → DevCoordinator**: Goal description and optional code
2. **DevCoordinator → ClassifierAgent**: Code to classify
3. **ClassifierAgent → DevCoordinator**: Classification results (type, brain count, etc.)
4. **DevCoordinator → PlannerAgent**: Goal and classification results
5. **PlannerAgent → DevCoordinator**: Workflow plan
6. **DevCoordinator → EvaluatorAgent**: Workflow plan
7. **EvaluatorAgent → DevCoordinator**: Evaluation score and feedback
8. **DevCoordinator → WorkflowExecutorAgent**: Workflow plan
9. **WorkflowExecutorAgent → DevCoordinator**: Execution results
10. **DevCoordinator → User**: Final results

If a missing capability is identified:

1. **PlannerAgent → DevCoordinator**: Missing capability notification
2. **DevCoordinator → AutoAgentComposer**: Capability specification
3. **AutoAgentComposer → DevCoordinator**: New agent metadata
4. **DevCoordinator → PlannerAgent**: Updated agent registry information

## Implementation

The AutoDevTeam is implemented as:

1. **OrchestratorTeam**: A formal Team entity that encapsulates the DevCoordinator and core agents
2. **DevCoordinatorAgent**: The central Agent that coordinates the workflow using Agent Squad
3. **Core Agents**: Individual specialized agents that perform specific roles

### DevCoordinator Implementation

The DevCoordinator is implemented as a SupervisorAgent from the Agent Squad framework:

```python
def run(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """Process a user request by orchestrating the appropriate agents."""
    # Extract request details
    goal = request.get("goal", "")
    code = request.get("code")
    
    # Prepare the input for the supervisor
    input_text = f"Goal: {goal}"
    if code:
        input_text += f"\nCode: {code}"
    
    # Run the supervisor
    result = self.supervisor.process_request(
        input_text=input_text,
        additional_params={"options": request.get("options", {})}
    )
    
    return {
        "success": True,
        "result": result.get("text", ""),
        "context": result.get("context", {})
    }
```

This implementation uses Agent Squad's SupervisorAgent to coordinate the core agents, providing a more flexible and extensible orchestration mechanism.

## Usage

The AutoDevTeam can be invoked via the CLI:

```bash
tdev orchestrate "Build a service that summarizes documents"
```

Or programmatically:

```python
from tdev.core.registry import get_registry

registry = get_registry()
coordinator = registry.get_instance("DevCoordinatorAgent")
result = coordinator.run({"goal": "Build a service that summarizes documents"})
```

## Future Extensions

In future iterations, the AutoDevTeam will be enhanced with:

1. **Parallel Execution**: Running independent steps concurrently
2. **Feedback Loops**: Incorporating user feedback into the workflow
3. **Learning**: Improving planning and evaluation based on past executions
4. **Advanced Composition**: Creating more complex workflows with branching and conditions