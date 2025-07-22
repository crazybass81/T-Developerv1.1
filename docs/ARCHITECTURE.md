# T-Developer Architecture

This document describes the architecture of the T-Developer system, a meta-agent orchestration framework for building SaaS applications by composing Tools, Agents, and Teams.

## System Overview

T-Developer is designed as a meta-agent system where specialized agents work together under the coordination of an orchestrator to fulfill complex tasks. The system classifies components based on their decision-making complexity (brain count) and provides mechanisms for composing these components into workflows.

### Core Components

- **Tools**: Pure functional units with no decision logic (0 brains)
- **Agents**: Components with a single decision-making point (1 brain)
- **Teams**: Collaborative structures composed of multiple agents (2+ brains)

### Meta-Agent Orchestration

The heart of T-Developer is the meta-agent orchestration pattern, where specialized agents work together in a coordinated sequence:

1. **ClassifierAgent** analyzes code to determine its type (Tool/Agent/Team)
2. **PlannerAgent** breaks down goals into steps and selects appropriate agents or teams
3. **EvaluatorAgent** scores workflows for quality and efficiency
4. **WorkflowExecutorAgent** runs the composed workflows step by step

This orchestration can be encapsulated in the **OrchestratorTeam**, which coordinates these core agents to fulfill a user request. The orchestration allows T-Developer to dynamically assemble solutions from reusable components.

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Agent Code     │     │    Workflow     │     │  Configuration  │
│  (Python Files) │     │  Definition     │     │  (Parameters)   │
└────────┬────────┘     └────────┬────────┘     └────────┬────────┘
         │                       │                       │
         └───────────┬───────────┴───────────┬───────────┘
                     │                       │
           ┌─────────▼───────────┐  ┌────────▼────────┐
           │  CLI Commands       │  │  AgentRegistry  │
           │                     │  │   (JSON)        │
           └─────────┬───────────┘  └────────┬────────┘
                     │                       │
                     └───────────┬───────────┘
                                 │
                     ┌───────────▼───────────┐
                     │  WorkflowExecutor     │
                     └───────────┬───────────┘
                                 │
                     ┌───────────▼───────────┐
                     │  Execution Results    │
                     └─────────────────────┘
```

### Key Components

#### 1. AgentRegistry

The AgentRegistry is the central directory of all available components. It maintains metadata about each agent, tool, and team, and provides methods to retrieve and instantiate them. The registry is stored as a JSON file in the `.tdev` directory.

#### 2. CLI Interface

The command-line interface provides the primary way to interact with T-Developer. It includes commands for:
- Initializing new agents and tools
- Classifying components
- Registering components in the registry
- Composing workflows
- Running workflows
- Testing agents

#### 3. Workflow System

Workflows define sequences of steps, each referencing an agent to execute. The WorkflowExecutorAgent loads these definitions and runs each step in order, passing data between steps as needed.

#### 4. Core Agents

- **ClassifierAgent**: Analyzes code to determine its type
- **PlannerAgent**: Plans workflows by selecting and ordering agents
- **EvaluatorAgent**: Evaluates workflows for quality and efficiency
- **WorkflowExecutorAgent**: Executes workflows step by step
- **TeamExecutorAgent**: Executes teams and their member agents
- **AgentTesterAgent**: Tests agents with sample inputs

#### 5. Core Teams

- **OrchestratorTeam**: Coordinates the core agents (Classifier, Planner, Evaluator, Executor)
- **DoubleEchoTeam**: A simple example team that calls EchoAgent twice in sequence

## Data Flow

1. **Component Registration**:
   - Agents and tools are defined in Python files
   - They are registered in the AgentRegistry with metadata
   - The registry serves as the central lookup for all components

2. **Workflow Composition**:
   - The user defines a goal or requirement
   - The PlannerAgent selects appropriate agents for each step
   - A workflow definition is created and stored

3. **Workflow Execution**:
   - The WorkflowExecutorAgent loads the workflow definition
   - It resolves each agent reference through the registry
   - It executes each step in sequence, passing data between steps
   - The final output is returned to the user

## Deployment Context

T-Developer is designed to run on EC2 instances without containers. The system uses local file storage for the registry and workflow definitions, making it simple to deploy and use.

### File Structure

```
.tdev/                  # Runtime data directory
  ├── registry.json     # Component registry
  ├── workflows/        # Workflow definitions
  └── instances/        # Service instance metadata

tdev/                   # Python package
  ├── core/             # Core framework
  ├── agents/           # Agent implementations
  ├── tools/            # Tool implementations
  ├── teams/            # Team implementations
  └── workflows/        # Workflow utilities
```

## Extensibility

T-Developer is designed to be easily extended with new components:

1. **Adding Agents**: Create a new Python class inheriting from `Agent` and implement the `run` method
2. **Adding Tools**: Create a function with the `@tool` decorator or a class inheriting from `Tool`
3. **Adding Teams**: Create a new Python class inheriting from `Team`, add member agents, and implement the coordination logic
4. **Registering Components**: Use the CLI to register new components in the registry

This extensibility allows T-Developer to grow its capabilities over time.

## Future Directions

Future enhancements to the architecture may include:

- Cloud storage for the registry and workflows
- Distributed execution of workflows
- More sophisticated planning and evaluation algorithms
- Integration with CI/CD pipelines
- Web interface for workflow visualization and management