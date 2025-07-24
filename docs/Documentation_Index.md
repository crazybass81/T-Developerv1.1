# T-Developer v1.1 Documentation

## Overview

T-Developer v1.1 is an agent orchestration platform that automates software development tasks by composing Tools, Agents, and Teams. This documentation provides comprehensive information about the system architecture, components, and usage.

## Current Status: Phase 4 Complete ✅

**Production-Ready Enterprise Platform**
- **Test Results**: 75/97 tests passing (77.3% pass rate)
- **Coverage**: 52% (up from 43%)
- **Enterprise Features**: All 6 Phase 4 action items implemented
- **Repository**: https://github.com/crazybass81/T-Developerv1.1

## Documentation Index

### Project Information
- [Architecture](ARCHITECTURE.md) - System architecture and component interactions
- [Roadmap](ROADMAP.md) - Development phases and current progress
- [Phase 4 Features](PHASE4_FEATURES.md) - Complete Phase 4 feature documentation
- [Phase 5 Roadmap](PHASE5_ROADMAP.md) - Future development roadmap

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
- [Code Review](../.amazonq/rules/T‑Developer_v1.1_Codereview.md) - Phase 4 completion code review
- [Changelog](../CHANGELOG.md) - Version history and changes
- [Phase 4 Completion Report](../PHASE4_COMPLETION_REPORT.md) - Detailed Phase 4 completion report
- [Current Status Summary](../CURRENT_STATUS_SUMMARY.md) - Executive summary of current state

### Testing & Quality Assurance
- [API Server Tests](../tests/api/test_server.py) - Tests for the API server
- [Agent Core Tests](../tests/agent_core/test_bedrock_client.py) - Tests for the Bedrock client
- [Monitoring Tests](../tests/monitoring/test_feedback.py) - Tests for the feedback collector
- [Integration Tests](../tests/integration/test_api_server.py) - Integration tests for the API server
- [Phase 4 Feature Tests](../tests/test_phase4_features.py) - Comprehensive Phase 4 feature testing
- [Coverage Report](../TEST_COVERAGE_REPORT.md) - Test coverage analysis
- [CI Debugging](CI_DEBUGGING.md) - Guide for debugging CI pipeline failures

### Enterprise Features (Phase 4)
- **Agent Versioning & A/B Testing**: Version management with performance comparison
- **Multi-Tenancy & Authentication**: API key authentication with tenant isolation
- **Internationalization (i18n)**: English/Korean language support
- **Plugin Ecosystem**: Extensible architecture for models and tools
- **Continuous Learning**: Feedback analysis and improvement suggestions
- **Enhanced API Server**: WebSocket support and authentication middleware