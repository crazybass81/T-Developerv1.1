# T-Developer v1.1

T-Developer is an agent orchestration system designed to build SaaS applications by composing Tools, Agents, and Teams. This repository contains the implementation of the T-Developer platform based on the architectural specifications.

## Core Components

- **Tools**: Pure functional units without decision logic (0 brains)
- **Agents**: Components with a single decision-making point (1 brain)
- **Teams**: Collaborative structures composed of multiple agents (2+ brains)

## Features

- **Component Registry**: Central directory of all available agents and tools
- **Workflow System**: Define and execute sequences of agent steps
- **CLI Interface**: Command-line tools for creating and managing components
- **Testing Framework**: Test agents and tools with sample inputs

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
```

## Documentation

Comprehensive documentation is available in the `docs/` directory:

- [Architecture](docs/ARCHITECTURE.md) - System architecture and component interactions
- [Agent Development Guide](docs/AGENTS.md) - How to create and register agents
- [Tool Development Guide](docs/TOOLS.md) - How to create and register tools
- [Workflow Guide](docs/WORKFLOWS.md) - How to define and use workflows
- [CLI Usage Guide](docs/CLI_USAGE.md) - Command-line interface reference

## Architecture

T-Developer uses the meta-agent orchestration pattern, where specialized agents work together under the coordination of an orchestrator to fulfill complex tasks:

1. **ClassifierAgent** analyzes code to determine its type (Tool/Agent/Team)
2. **PlannerAgent** breaks down goals into steps and selects appropriate agents
3. **EvaluatorAgent** scores workflows for quality and efficiency
4. **WorkflowExecutorAgent** runs the composed workflows step by step

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

## Testing

Run the test suite with pytest:

```bash
pytest
```