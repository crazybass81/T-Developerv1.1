# T-Developer Orchestrator

This document details how the orchestration logic works in T-Developer using the Agent Squad framework.

## Overview

The orchestration in T-Developer is handled by the **Agent Squad** framework, which provides a flexible and extensible mechanism for coordinating multiple agents. The central component is the **SupervisorAgent (DevCoordinator)**, which manages the flow between specialized agents to fulfill user requests.

## SupervisorAgent (DevCoordinator)

The DevCoordinator is implemented as a SupervisorAgent from the Agent Squad framework. It consists of:

- **Lead Agent**: An LLM-based agent that serves as the "brain" of the coordinator, deciding which team member to call at each step
- **Team Members**: The core T-Developer agents (ClassifierAgent, PlannerAgent, EvaluatorAgent, WorkflowExecutorAgent)
- **Extra Tools**: Additional tools that can be used by the agents

The SupervisorAgent uses an "agents-as-tools" approach, meaning it exposes each team member as a tool that the lead agent can call.

## Orchestration Flow

When a user input is received, the orchestration follows this sequence:

1. **Input Processing**: The user's goal and optional code are passed to the DevCoordinator
2. **Classification (if code provided)**: The SupervisorAgent's lead determines the need to classify code and invokes the ClassifierAgent
3. **Planning**: The classification result is used to prompt the PlannerAgent for a workflow
4. **Evaluation**: The plan is evaluated by the EvaluatorAgent
5. **Refinement (if needed)**: If the evaluation score is below threshold, the plan is refined
6. **Execution**: The final plan is executed by the WorkflowExecutorAgent
7. **Result Aggregation**: The SupervisorAgent aggregates the responses and returns the final result

## Differences from Previous Design

The Agent Squad-based orchestration differs from the previous design in several ways:

- **No hardcoded sequence**: The sequence is either learned by the LLM agent or handled by the DevCoordinator logic
- **More flexible framework**: Agent Squad provides a more flexible and extensible orchestration mechanism
- **Parallel execution**: Agent Squad supports parallel agent execution (though currently we use sequential execution)
- **Intelligent routing**: Agent Squad can intelligently route requests to the appropriate agents
- **Context management**: Agent Squad provides built-in context management for multi-turn conversations

## Integration with Registry

The Agent Squad orchestrator is dynamically integrated with the T-Developer registry:

- When the registry is initialized or updated, the orchestrator's agent list is synchronized
- New agents registered via `tdev register` are automatically available to the orchestrator
- The T-Developer AgentRegistry remains the single source of truth for available agents/tools

## Usage

The Agent Squad orchestrator can be invoked via the CLI:

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

## Benefits

We integrated AWS's Agent Squad framework to manage our agents because it provides a more flexible and extensible orchestration mechanism, allowing parallel agent execution and intelligent routing, which prepares T-Developer for more complex scenarios and future growth.