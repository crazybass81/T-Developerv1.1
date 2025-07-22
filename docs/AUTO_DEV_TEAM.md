# AutoDevTeam Assembly Approach

This document outlines how the core agents work together in Phase 3 of T-Developer as the AutoDevTeam, coordinated by the MetaAgent (Orchestrator).

## Overview

The AutoDevTeam is a coordinated group of specialized agents that work together to fulfill user requests end-to-end. The MetaAgent serves as the central orchestrator that sequences the other agents in the appropriate order.

## Team Composition

The AutoDevTeam consists of the following core agents:

1. **MetaAgent (Orchestrator)**: The central coordinator that manages the flow between other agents
2. **ClassifierAgent**: Analyzes code to classify it as Tool, Agent, or Team
3. **PlannerAgent**: Plans workflows by selecting and ordering appropriate agents
4. **EvaluatorAgent**: Evaluates workflows for quality and efficiency
5. **WorkflowExecutorAgent**: Executes workflows step by step
6. **AutoAgentComposer (Agno)**: Generates new agents when needed

## Interaction Pattern

The interaction pattern follows this sequence:

1. **User Request**: The user submits a goal or code to the MetaAgent
2. **Classification (if code provided)**: The MetaAgent invokes the ClassifierAgent to analyze the code
3. **Planning**: The MetaAgent invokes the PlannerAgent to generate a workflow plan
4. **Evaluation**: The MetaAgent invokes the EvaluatorAgent to assess the plan's quality
5. **Refinement (if needed)**: If the evaluation score is below threshold, the MetaAgent requests the PlannerAgent to refine the plan
6. **Execution**: The MetaAgent invokes the WorkflowExecutorAgent to run the workflow
7. **Dynamic Agent Generation (if needed)**: If the PlannerAgent identifies a missing capability, the MetaAgent invokes the AutoAgentComposer to generate a new agent

## Data Flow

The data flows between agents as follows:

1. **User → MetaAgent**: Goal description and optional code
2. **MetaAgent → ClassifierAgent**: Code to classify
3. **ClassifierAgent → MetaAgent**: Classification results (type, brain count, etc.)
4. **MetaAgent → PlannerAgent**: Goal and classification results
5. **PlannerAgent → MetaAgent**: Workflow plan
6. **MetaAgent → EvaluatorAgent**: Workflow plan
7. **EvaluatorAgent → MetaAgent**: Evaluation score and feedback
8. **MetaAgent → WorkflowExecutorAgent**: Workflow plan
9. **WorkflowExecutorAgent → MetaAgent**: Execution results
10. **MetaAgent → User**: Final results

If a missing capability is identified:

1. **PlannerAgent → MetaAgent**: Missing capability notification
2. **MetaAgent → AutoAgentComposer**: Capability specification
3. **AutoAgentComposer → MetaAgent**: New agent metadata
4. **MetaAgent → PlannerAgent**: Updated agent registry information

## Implementation

The AutoDevTeam is implemented as:

1. **OrchestratorTeam**: A formal Team entity that encapsulates the MetaAgent and core agents
2. **MetaAgent**: The central Agent that coordinates the workflow
3. **Core Agents**: Individual specialized agents that perform specific roles

### MetaAgent Implementation

The MetaAgent is implemented as a standard Agent with a `run` method that orchestrates the core agents:

```python
def run(self, request: Dict[str, Any]) -> Dict[str, Any]:
    """Process a user request by orchestrating the appropriate agents."""
    # Extract request details
    goal = request.get("goal", "")
    code = request.get("code")
    
    # Step 1: If code is provided, classify it
    if code:
        classifier = self.registry.get_instance("ClassifierAgent")
        classification_result = classifier.run(code)
    
    # Step 2: Plan a workflow to fulfill the goal
    planner = self.registry.get_instance("PlannerAgent")
    workflow_plan = planner.run({"goal": goal, "classification": classification_result})
    
    # Step 3: Evaluate the workflow plan
    evaluator = self.registry.get_instance("EvaluatorAgent")
    evaluation = evaluator.run(workflow_plan)
    
    # Step 4: Execute the workflow
    executor = self.registry.get_instance("WorkflowExecutorAgent")
    execution_result = executor.run(workflow_plan)
    
    return execution_result
```

This implementation follows the sequence diagram in the Architecture Diagrams document, ensuring that each agent is invoked in the correct order with the appropriate inputs.

## Usage

The AutoDevTeam can be invoked via the CLI:

```bash
tdev orchestrate "Build a service that summarizes documents"
```

Or programmatically:

```python
from tdev.core.registry import get_registry

registry = get_registry()
team = registry.get_instance("OrchestratorTeam")
result = team.run({"goal": "Build a service that summarizes documents"})
```

## Future Extensions

In future iterations, the AutoDevTeam will be enhanced with:

1. **Parallel Execution**: Running independent steps concurrently
2. **Feedback Loops**: Incorporating user feedback into the workflow
3. **Learning**: Improving planning and evaluation based on past executions
4. **Advanced Composition**: Creating more complex workflows with branching and conditions