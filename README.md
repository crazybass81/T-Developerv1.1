# T-Developer v1.1

T-Developer is an agent orchestration system designed to build SaaS applications by composing Tools, Agents, and Teams. This repository contains the architectural specifications and component definitions for the T-Developer platform.

## Core Components

- **Tools**: Pure functional units without decision logic
- **Agents**: Tools with a single decision-making logic
- **Teams**: Collaborative structures composed of 2 or more Agents

## Documentation

Comprehensive documentation is available in this repository:

- [Documentation Index](Documentation_Index.md) - Complete list of all documentation
- [Architecture Overview](T-developer-architecture-v1.md) - System philosophy and component definitions
- [Rule Definitions](Rule_Definitions.md) - System rule sets and classification criteria
- [Agent Squad Architecture](Agent_Squad_Architecture.md) - How agents work together
- [Service Composition](Service_Composition.md) - How services are composed from components
- [Glossary](Glossary.md) - Definitions of key terms

## Architecture

T-Developer uses the number of decision units (brains) as its primary classification standard:

- **Tool**: Pure function (0 brains)
- **Agent**: One decision point (1 brain)
- **Team**: Multiple decisions + coordination (2+ brains)

T-Developer classifies defined tools and agents, automatically assembles them to match a given purpose, and executes complete SaaS workflows from reusable components.

## T-Developer v1.1 System Design

This version includes comprehensive documentation on:

- Agent generation and classification
- Service composition and workflow execution
- Integration and deployment
- Versioning and change control
- Testing and evaluation

Refer to the [Documentation Index](Documentation_Index.md) for a complete list of all documentation files.