# T-Developer v1.1

T-Developer is an agent orchestration system designed to build SaaS applications by composing Tools, Agents, and Teams. This repository contains the architectural specifications and component definitions for the T-Developer platform.

## Core Components

- **Tools**: Pure functional units without decision logic
- **Agents**: Tools with a single decision-making logic
- **Teams**: Collaborative structures composed of 2 or more Agents

## Repository Structure

This repository contains specification documents for all T-Developer components, including:

- Agent Registry
- Agent Classification
- Workflow Execution
- Testing Framework
- Evaluation System
- Service Instance Management

## Architecture

T-Developer uses the number of decision units (brains) as its primary classification standard:

- **Tool**: Pure function (0 brains)
- **Agent**: One decision point (1 brain)
- **Team**: Multiple decisions + coordination (2+ brains)

T-Developer classifies defined tools and agents, automatically assembles them to match a given purpose, and executes complete SaaS workflows from reusable components.