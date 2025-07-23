# T-Developer v1.1

T-Developer v1.1 is an **agent orchestration platform** that can turn natural-language feature requests into working software without direct human coding. It automates the software development pipeline from requirements analysis through implementation, testing, and deployment.

**Current Phase: Phase 3 Complete - Ready for Phase 4 (Extended Features and Refinement)**

## System Overview

T-Developer enables complex goals to be achieved by a coordinated "squad" of specialized AI agents. When a user describes a new software feature in plain language, the platform:

1. Automatically analyzes the request
2. Breaks it down into sub-tasks
3. Assembles or creates specialized AI agents for each task
4. Generates, tests, deploys, and executes the code

## Core Components

- **Tools**: Pure functional units without decision logic (0 brains)
- **Agents**: Components with a single decision-making point (1 brain)
- **Teams**: Collaborative structures composed of multiple agents (2+ brains)

## Key Features

- **Component Registry**: Central directory of all available agents, tools, and teams
- **Workflow System**: Define and execute sequences of steps using agents and teams
- **CLI/IDE Interface**: Command-line tools and IDE integrations for managing components
- **Testing Framework**: Automated testing for agents, tools, and teams
- **Agno (AutoAgentComposer)**: Automatically generate new agents or tools based on specifications using AWS Bedrock
- **Agent Squad Orchestrator**: Coordinate specialized agents to fulfill complex tasks
- **AWS Integration**: Deploy agents to AWS Lambda and Bedrock Agent Core
- **Monitoring & Feedback**: Monitor deployed agents and collect user feedback
- **API Server**: Interact with T-Developer through REST API and WebSockets

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

### Project Information
- [Architecture](docs/ARCHITECTURE.md) - System architecture and component interactions
- [Roadmap](docs/ROADMAP.md) - Development phases and current progress
- [Phase Transition](docs/PHASE_TRANSITION.md) - Summary of the transition from Phase 2 to Phase 3
- [Phase 3 Completion](docs/PHASE3_COMPLETION.md) - Summary of Phase 3 completion and next steps

### Development Guides
- [Agent Development](docs/AGENTS.md) - How to create and register agents
- [Tool Development](docs/TOOLS.md) - How to create and register tools
- [Team Development](docs/TEAMS.md) - How to create and register teams
- [Workflow Guide](docs/WORKFLOWS.md) - How to define and use workflows
- [Code Quality](docs/CODE_QUALITY.md) - Guidelines for maintaining code quality

### System Components
- [Orchestrator](docs/ORCHESTRATOR.md) - How the Agent Squad orchestrator works
- [AutoDevTeam](docs/AUTO_DEV_TEAM.md) - How core agents work together in Phase 3
- [Execution Flow](docs/EXECUTION_FLOW.md) - Detailed execution flow in the system
- [Agent Core](tdev/agent_core/README.md) - AWS Bedrock Agent Core integration
- [API Server](tdev/api/README.md) - API server for UI integration
- [Monitoring](tdev/monitoring/README.md) - Monitoring and feedback collection
- [Notifications](docs/NOTIFICATIONS.md) - Slack and other notification systems

### User Guides
- [CLI Usage](docs/CLI_USAGE.md) - Command-line interface reference
- [Deployment](deployment/cloudformation.yaml) - AWS CloudFormation template for deployment
- [CI Debugging](docs/CI_DEBUGGING.md) - Guide for debugging CI pipeline failures

## Core Agent Squad

T-Developer uses the Agent Squad orchestration pattern, where specialized agents work together under the coordination of a SupervisorAgent:

1. **SupervisorAgent (DevCoordinator)**: Coordinates the flow between specialized agents using AWS Bedrock
2. **ClassifierAgent**: Analyzes code to determine its type (Tool/Agent/Team)
3. **PlannerAgent**: Breaks down goals into steps and selects appropriate agents using AWS Bedrock
4. **EvaluatorAgent**: Scores workflows for quality and efficiency using AWS Bedrock
5. **WorkflowExecutorAgent**: Runs the composed workflows step by step
6. **AutoAgentComposer (Agno)**: Generates new agents and tools as needed using AWS Bedrock
7. **ObserverAgent**: Monitors deployed agents and collects metrics and logs
8. **FeedbackCollector**: Collects and processes user feedback for agents

## Development Examples

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

## Deployment

Deploy the infrastructure to AWS:

```bash
# Deploy the CloudFormation stack
python scripts/deploy_infrastructure.py

# Deploy an agent to AWS Lambda
tdev deploy agent MyAgent --target lambda

# Deploy an agent to Bedrock Agent Core
tdev deploy agent MyAgent --target bedrock
```

## API Server

Start the API server for UI integration:

```bash
tdev serve --port 8000
```

## Monitoring

Monitor deployed agents:

```bash
# Get metrics for an agent
tdev monitor metrics MyAgent --time-range 1h

# Get logs for an agent
tdev monitor logs MyAgent --time-range 1h --limit 10
```