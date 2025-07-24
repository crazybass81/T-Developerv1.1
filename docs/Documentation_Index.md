# T-Developer v1.1 Documentation

## Overview

T-Developer v1.1 is an agent orchestration platform that automates software development tasks by composing Tools, Agents, and Teams. This documentation provides comprehensive information about the system architecture, components, and usage.

## Documentation Index

### Project Information
- [Architecture](ARCHITECTURE.md) - System architecture and component interactions
- [Roadmap](ROADMAP.md) - Development phases and current progress
- [Phase Transition](PHASE_TRANSITION.md) - Summary of the transition from Phase 2 to Phase 3
- [Phase 3 Completion](PHASE3_COMPLETION.md) - Summary of Phase 3 completion and next steps

### Development Guides
- [Agent Development](AGENTS.md) - How to create and register agents
- [Tool Development](TOOLS.md) - How to create and register tools
- [Team Development](TEAMS.md) - How to create and register teams
- [Workflow Guide](WORKFLOWS.md) - How to define and use workflows

### System Components
- [Orchestrator](ORCHESTRATOR.md) - How the Agent Squad orchestrator works
- [AutoDevTeam](AUTO_DEV_TEAM.md) - How core agents work together in Phase 3
- [Execution Flow](EXECUTION_FLOW.md) - Detailed execution flow in the system
- [Agent Core](../tdev/agent_core/README.md) - AWS Bedrock Agent Core integration
- [API Server](../tdev/api/README.md) - API server for UI integration
- [Monitoring](../tdev/monitoring/README.md) - Monitoring and feedback collection

### User Guides
- [CLI Usage](CLI_USAGE.md) - Command-line interface reference
- [Deployment](../deployment/cloudformation.yaml) - AWS CloudFormation template for deployment

### Reference Documents
- [System Design Documents](../.amazonq/rules/T‑Developer_v1.1_System_Design_Documents.md)
- [Automated Development Platform Documentation](../.amazonq/rules/T‑Developer_v1.1_Automated_Development_Platform_Documentation.md)
- [Code Review](../.amazonq/rules/T‑Developer_v1.1_Code_Review.md) - Code review and recommendations

### Testing
- [API Server Tests](../tests/api/test_server.py) - Tests for the API server
- [Agent Core Tests](../tests/agent_core/test_bedrock_client.py) - Tests for the Bedrock client
- [Monitoring Tests](../tests/monitoring/test_feedback.py) - Tests for the feedback collector
- [Integration Tests](../tests/integration/test_api_server.py) - Integration tests for the API server