# CLI Usage Guide

This guide documents the command-line interface (CLI) for T-Developer.

## Overview

The T-Developer CLI provides commands for:
- Initializing new agents, tools, and teams
- Classifying components
- Registering components in the registry
- Composing workflows
- Running workflows and teams
- Testing agents

## Installation

To install the T-Developer CLI:

```bash
# Clone the repository
git clone https://github.com/your-org/T-Developerv1.1.git

# Install the package
cd T-Developerv1.1
pip install -e .
```

After installation, the `tdev` command will be available in your terminal.

## Command Reference

### Help

To see available commands:

```bash
tdev --help
```

To get help for a specific command:

```bash
tdev <command> --help
```

### Generation Commands

#### Generate Agent

Generate a new agent using Agno:

```bash
tdev generate agent --name MyAgent --goal "Description of what the agent should do"
```

You can also provide a tool to use:

```bash
tdev generate agent --name MyAgent --goal "Description" --tool ToolName
```

Or use a specification file:

```bash
tdev generate agent --spec path/to/specification.json
```

#### Generate Tool

Generate a new tool using Agno:

```bash
tdev generate tool --name MyTool --goal "Description of what the tool should do"
```

Or use a specification file:

```bash
tdev generate tool --spec path/to/specification.json
```

### Orchestration Commands

#### Orchestrate

Use the orchestrator to fulfill a goal:

```bash
tdev orchestrate "Goal description"
```

You can also provide a code file to classify:

```bash
tdev orchestrate "Goal description" --code path/to/code.py
```

And additional options as JSON:

```bash
tdev orchestrate "Goal description" --options '{"key": "value"}'
```

### Initialization Commands

#### Initialize Agent

Create a new agent:

```bash
tdev init agent --name MyAgent
```

This creates a file at `tdev/agents/my_agent.py` with a basic agent template.

#### Initialize Tool

Create a new tool:

```bash
tdev init tool --name MyTool
```

This creates a file at `tdev/tools/my_tool.py` with a basic tool template.

#### Initialize Team

Create a new team:

```bash
tdev init team --name MyTeam
```

This creates a file at `tdev/teams/my_team.py` with a basic team template.

#### Initialize Registry

Initialize the registry with core components:

```bash
tdev init-registry
```

This registers the core agents and tools in the registry.

### Classification Commands

#### Classify a File

Analyze a file to determine its type:

```bash
tdev classify path/to/file.py
```

This returns the classification (tool, agent, or team) of the file.

### Registration Commands

#### Register a Component

Register an agent, tool, or team in the registry:

```bash
tdev register path/to/component.py
```

This adds the component to the registry, making it available for use in workflows.

### Workflow Commands

#### Compose a Workflow

Create a workflow from agents and teams:

```bash
tdev compose --name my-workflow --steps AgentA,TeamB,AgentC
```

This creates a workflow definition at `.tdev/workflows/my-workflow.json`.

#### Run a Workflow

Execute a workflow:

```bash
tdev run my-workflow
```

This runs the workflow and displays the results.

#### Run a Team

Execute a team directly:

```bash
tdev run-team MyTeam --input '{"key": "value"}'
```

This instantiates the team, calls its `run` method with the provided input, and displays the results.

### Testing Commands

#### Test an Agent

Test an agent with a simple input:

```bash
tdev test MyAgent
```

This runs the agent with a test input and reports the result.

### Other Commands

#### Status

Check the status of services (not implemented in the skeleton):

```bash
tdev status [service-id]
```

#### Build

Build commands (not implemented in the skeleton):

```bash
tdev build package
```

#### Deploy

Deployment commands (not implemented in the skeleton):

```bash
tdev deploy lambda-function my-service
```

## Examples

### Creating and Running a Simple Workflow

```bash
# Initialize the registry
tdev init-registry

# Create a workflow using the EchoAgent
tdev compose --name echo-flow --steps EchoAgent

# Run the workflow
tdev run echo-flow
```

### Using the Orchestrator

```bash
# Use the orchestrator to fulfill a goal
tdev orchestrate "Echo the input data"

# Orchestrate with a code file
tdev orchestrate "Classify this code" --code path/to/code.py

# Orchestrate with options
tdev orchestrate "Process this data" --options '{"data": "example"}'
```

### Generating Components with Agno

```bash
# Generate a new agent
tdev generate agent --name Summarizer --goal "Summarize text documents"

# Generate a tool wrapper agent
tdev generate agent --name TextProcessor --goal "Process text" --tool TextProcessingTool

# Generate a new tool
tdev generate tool --name TextFormatter --goal "Format text with proper spacing and capitalization"
```

### Creating and Running a Team

```bash
# Create a new team
tdev init team --name MyTeam

# Edit the team file at tdev/teams/my_team.py

# Register the team
tdev register tdev/teams/my_team.py

# Run the team
tdev run-team MyTeam --input '{"message": "Hello, Team!"}'
```

### Creating and Testing a Custom Agent

```bash
# Create a new agent
tdev init agent --name MyCustomAgent

# Edit the agent file at tdev/agents/my_custom_agent.py

# Register the agent
tdev register tdev/agents/my_custom_agent.py

# Test the agent
tdev test MyCustomAgent
```

## Environment Setup

The T-Developer CLI stores its data in the `.tdev` directory in your home directory:

- `.tdev/registry.json`: The component registry
- `.tdev/workflows/`: Workflow definitions
- `.tdev/instances/`: Service instance metadata

No special environment variables are required for the basic functionality.