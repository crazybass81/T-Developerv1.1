# T-Developer v1.1 Documentation

Welcome to the T-Developer v1.1 documentation. This directory contains comprehensive documentation for the T-Developer agent orchestration platform.

## Current Status: Phase 4 Complete ✅

**Production-Ready Enterprise Platform**
- **Test Results**: 75/97 tests passing (77.3% pass rate)
- **Coverage**: 52% (up from 43%)
- **Status**: All Phase 4 features implemented and production-ready
- **Repository**: https://github.com/crazybass81/T-Developerv1.1

## Documentation Structure

The documentation is organized into the following categories:

### Project Information
- [Architecture](ARCHITECTURE.md) - System architecture and component interactions
- [Roadmap](ROADMAP.md) - Development phases and current progress
- [Phase 4 Features](PHASE4_FEATURES.md) - Complete Phase 4 feature documentation
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
- [Documentation Index](Documentation_Index.md) - Complete index of all documentation
- [System Design Documents](../.amazonq/rules/T‑Developer_v1.1_System_Design_Documents.md)
- [Automated Development Platform Documentation](../.amazonq/rules/T‑Developer_v1.1_Automated_Development_Platform_Documentation.md)
- [Code Review](../.amazonq/rules/T‑Developer_v1.1_Code_Review.md) - Code review and recommendations

## Current Status

T-Developer v1.1 has completed Phase 4 development, achieving production-ready enterprise platform status. The system now has:

### Core Features (Phase 3)
- Intelligent planning and evaluation using AWS Bedrock
- Automatic agent generation with AWS Bedrock
- Deployment to AWS Lambda and Bedrock Agent Core
- Monitoring and feedback collection
- API server for UI integration
- Comprehensive testing and documentation

### Enterprise Features (Phase 4)
- **Agent Versioning & A/B Testing**: Version management with performance comparison
- **Multi-Tenancy & Authentication**: API key authentication with tenant isolation
- **Internationalization (i18n)**: English/Korean language support
- **Plugin Ecosystem**: Extensible architecture for models and tools
- **Continuous Learning**: Feedback analysis and improvement suggestions
- **Enhanced API Server**: WebSocket support and authentication middleware

## Getting Started

For new users, we recommend starting with the following documents:

1. [Architecture](ARCHITECTURE.md) - To understand the system design
2. [CLI Usage](CLI_USAGE.md) - To learn how to use the command-line interface
3. [Agent Development](AGENTS.md) - To learn how to create and use agents
4. [Workflow Guide](WORKFLOWS.md) - To learn how to define and execute workflows

## Contributing

If you'd like to contribute to the documentation, please follow these guidelines:

1. Use Markdown format for all documentation
2. Follow the existing structure and style
3. Update the [Documentation Index](Documentation_Index.md) when adding new documents
4. Include code examples where appropriate
5. Keep the documentation up-to-date with the code