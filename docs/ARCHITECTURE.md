# T-Developer v1.1 Architecture

## System Overview

T-Developer v1.1 is a **meta-agent orchestration framework** for automating software development tasks and composing SaaS applications from reusable components. The system enables complex goals to be achieved by a coordinated "squad" of specialized AI agents, automating the workflow from understanding a request to delivering a functional deployed service.

## Core Components

### Hierarchical Component Model

All building blocks are classified as:
- **Tools**: No decision logic ("0 brains")
- **Agents**: Single decision point ("1 brain")
- **Teams**: Multi-agent assemblies ("2+ brains")

### Agent Squad Orchestrator (MetaAgent)

The central coordinator of the system, implemented as a MetaAgent (also called **DevCoordinator** or SupervisorAgent). It controls the flow of tasks and information among specialized agents:

- Initiates and manages end-to-end workflows for user requests
- Delegates tasks to core agents and collects their outputs
- Makes high-level decisions based on agent outputs
- Handles exceptions and control flow
- Coordinates parallelism or team execution when applicable

### Core Agents

1. **ClassifierAgent**: Determines what kind of component an input is
2. **PlannerAgent**: Devises a plan (workflow) to achieve the goal using AWS Bedrock
3. **EvaluatorAgent**: Reviews plan quality and provides feedback using AWS Bedrock
4. **WorkflowExecutorAgent**: Carries out the plan step by step
5. **ObserverAgent**: Monitors deployed agents and collects metrics and logs
6. **FeedbackCollector**: Collects and processes user feedback for agents

### Agno (AutoAgentComposer)

The agent generation subsystem that automatically creates new agents or tools when existing components lack a capability for a given task. Key functions:

- Takes specifications for desired capabilities
- Analyzes requirements and plans implementation
- Generates code and metadata for new components using AWS Bedrock
- Registers new components in the system
- Tests newly generated components automatically

### AWS Bedrock Agent Core

The underlying AI and agent execution framework providing:
- Foundation models for language understanding and generation
- Agent Core SDK for easy integration with AWS services
- Decision logic framework for agent behavior
- Deployment targets for agents (Lambda, Bedrock Agent)
- Monitoring and logging capabilities

### User Interface Integrations

- **CLI**: Command-line interface for direct control
- **API Server**: REST API and WebSocket server for UI integration
- **Web UI**: Visual interface for interaction and monitoring
- **Future IDE Plugins**: Integration with development environments

## Data Flow and Integration

T-Developer integrates with development workflows and cloud infrastructure:
- Runs locally via CLI for development
- Deploys services to AWS (Lambda, Bedrock Agent Core) for production
- Hooks into CI/CD pipelines for automated testing and deployment
- Monitors deployed agents using CloudWatch
- Collects feedback and creates GitHub issues for improvements

All agents and tools are registered in a central **AgentRegistry**, enabling reuse in future workflows. The system is extensible – new components can be added manually or via generation.

## Current Status

T-Developer v1.1 has completed Phase 3 development, with all core features implemented and ready for Phase 4 (Extended Features and Refinement). The system now has:

- Intelligent planning and evaluation using AWS Bedrock
- Automatic agent generation with AWS Bedrock
- Deployment to AWS Lambda and Bedrock Agent Core
- Monitoring and feedback collection
- API server for UI integration
- Comprehensive testing and documentation