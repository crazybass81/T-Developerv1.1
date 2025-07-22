# T-Developer v1.1

T-Developer is an agent orchestration system designed to build SaaS applications by composing Tools, Agents, and Teams. This repository contains the implementation of the T-Developer platform based on the architectural specifications.

**Current Phase: Phase 3 (Team Composition and Orchestration)**

## Core Components

- **Tools**: Pure functional units without decision logic (0 brains)
- **Agents**: Components with a single decision-making point (1 brain)
- **Teams**: Collaborative structures composed of multiple agents (2+ brains)

## Features

- **Component Registry**: Central directory of all available agents, tools, and teams
- **Workflow System**: Define and execute sequences of agent and team steps
- **CLI Interface**: Command-line tools for creating and managing components
- **Testing Framework**: Test agents, tools, and teams with sample inputs
- **Agno (AutoAgentComposer)**: Automatically generate new agents and tools based on specifications
- **Agent Squad Orchestrator**: Coordinate specialized agents to fulfill complex tasks

## Getting Started

### Installation

```bash
# Clone the repository
git clone https://github.com/your-org/T-Developerv1.1.git

# Install the package
cd T-Developerv1.1
pip install -e .
```

### Quick Start

```bash
# Initialize the registry with core components
tdev init-registry

# Create a simple workflow using the EchoAgent
tdev compose --name echo-flow --steps EchoAgent

# Run the workflow
tdev run echo-flow

# Use the orchestrator to fulfill a goal
tdev orchestrate "Echo the input data"

# Generate a new agent using Agno
tdev generate agent --name CustomAgent --goal "A custom agent that does something specific"
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture](docs/ARCHITECTURE.md) - System architecture and component interactions
- [Agent Development Guide](docs/AGENTS.md) - How to create and register agents
- [Tool Development Guide](docs/TOOLS.md) - How to create and register tools
- [Team Development Guide](docs/TEAMS.md) - How to create and register teams
- [Workflow Guide](docs/WORKFLOWS.md) - How to define and use workflows
- [CLI Usage Guide](docs/CLI_USAGE.md) - Command-line interface reference
- [Orchestrator](docs/ORCHESTRATOR.md) - How the Agent Squad orchestrator works
- [Execution Flow](docs/EXECUTION_FLOW.md) - Detailed execution flow in the system
- [AutoDevTeam Assembly](docs/AUTO_DEV_TEAM.md) - How core agents work together in Phase 3
- [Phase Transition](docs/PHASE_TRANSITION.md) - Summary of the transition from Phase 2 to Phase 3

## Architecture

T-Developer uses the Agent Squad orchestration pattern, where specialized agents work together under the coordination of a SupervisorAgent to fulfill complex tasks:

1. **SupervisorAgent (DevCoordinator)** coordinates the flow between specialized agents
2. **ClassifierAgent** analyzes code to determine its type (Tool/Agent/Team)
3. **PlannerAgent** breaks down goals into steps and selects appropriate agents
4. **EvaluatorAgent** scores workflows for quality and efficiency
5. **WorkflowExecutorAgent** runs the composed workflows step by step

T-Developer integrates the AWS Agent Squad framework to provide a more flexible and extensible orchestration mechanism.

Components are classified based on their decision-making complexity (brain count):

- **Tool**: Pure function (0 brains)
- **Agent**: One decision point (1 brain)
- **Team**: Multiple decisions + coordination (2+ brains)

## Development

### Creating a New Agent

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

### Creating a New Tool

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

### Creating a New Team

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

## Testing

Run the test suite with pytest:

```bash
pytest
```