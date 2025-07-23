# T-Developer v1.1 Scripts

This directory contains utility scripts for T-Developer v1.1.

## Available Scripts

### generate_components.py

Generates agents and tools using Agno (AutoAgentComposer) based on specifications in the `specs` directory. This script demonstrates the automatic agent generation capabilities of the platform.

Usage:
```bash
python generate_components.py
```

### test_orchestration.py

Tests the orchestration system, including the MetaAgent, AutoAgentComposer, and OrchestratorTeam. This script validates the core orchestration functionality of the Agent Squad pattern.

Usage:
```bash
python test_orchestration.py
```

## Adding New Scripts

When adding new scripts:
1. Make them executable (`chmod +x script_name.py`)
2. Add a description to this README
3. Include proper documentation within the script
4. Follow the T-Developer coding standards
5. Add appropriate error handling and logging