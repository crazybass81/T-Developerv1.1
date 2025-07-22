# T-Developer Scripts

This directory contains utility scripts for T-Developer.

## Available Scripts

### generate_components.py

Generates agents and tools using Agno (AutoAgentComposer) based on specifications in the `specs` directory.

Usage:
```bash
./generate_components.py
```

### test_orchestration.py

Tests the orchestration system, including the MetaAgent, AutoAgentComposer, and OrchestratorTeam.

Usage:
```bash
./test_orchestration.py
```

## Adding New Scripts

When adding new scripts:
1. Make them executable (`chmod +x script_name.py`)
2. Add a description to this README
3. Include proper documentation within the script