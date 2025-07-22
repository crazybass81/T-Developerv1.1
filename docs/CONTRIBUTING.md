# Contributing to T-Developer

This guide provides information for contributors to the T-Developer project.

## Development Environment

### Prerequisites

- Python 3.9 or higher
- Git

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/your-org/T-Developerv1.1.git
   cd T-Developerv1.1
   ```

2. Install the package in development mode:
   ```bash
   pip install -e .
   ```

3. Initialize the registry:
   ```bash
   tdev init-registry
   ```

## Project Structure

```
T-Developerv1.1/
├── tdev/                   # Main package
│   ├── core/               # Core framework
│   │   ├── agent.py        # Base Agent class
│   │   ├── tool.py         # Tool decorator and base class
│   │   ├── team.py         # Base Team class
│   │   ├── registry.py     # AgentRegistry implementation
│   │   ├── schema.py       # Metadata schemas
│   │   ├── workflow.py     # Workflow definition and utilities
│   │   └── config.py       # Configuration utilities
│   ├── agents/             # Agent implementations
│   ├── tools/              # Tool implementations
│   └── workflows/          # Workflow utilities
├── tests/                  # Test suite
├── docs/                   # Documentation
├── .github/                # GitHub workflows
├── setup.py                # Package configuration
└── requirements.txt        # Dependencies
```

## Coding Conventions

### Python Style

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Include docstrings for all classes and functions
- Use meaningful variable and function names

### Documentation

- Update relevant documentation when adding or changing features
- Include examples in docstrings
- Keep the README.md up to date

## Adding New Components

### Adding a New Agent

1. Create a new agent file:
   ```bash
   tdev init agent --name MyAgent
   ```

2. Implement the agent logic in `tdev/agents/my_agent.py`

3. Register the agent:
   ```bash
   tdev register tdev/agents/my_agent.py
   ```

4. Add tests in `tests/`

5. Update documentation if necessary

See [Agent Development Guide](AGENTS.md) for more details.

### Adding a New Tool

1. Create a new tool file:
   ```bash
   tdev init tool --name MyTool
   ```

2. Implement the tool logic in `tdev/tools/my_tool.py`

3. Register the tool:
   ```bash
   tdev register tdev/tools/my_tool.py
   ```

4. Add tests in `tests/`

5. Update documentation if necessary

See [Tool Development Guide](TOOLS.md) for more details.

### Adding a New Team

1. Create a new team file:
   ```bash
   tdev init team --name MyTeam
   ```

2. Implement the team logic in `tdev/teams/my_team.py`:
   - Add member agents in the constructor
   - Implement the coordination logic in the `run` method

3. Register the team:
   ```bash
   tdev register tdev/teams/my_team.py
   ```

4. Add tests in `tests/`

5. Update documentation if necessary

See [Team Development Guide](TEAMS.md) for more details.

## Testing

### Running Tests

Run the test suite with pytest:

```bash
pytest
```

Run a specific test file:

```bash
pytest tests/test_registry.py
```

### Writing Tests

- Place tests in the `tests/` directory
- Name test files with the `test_` prefix
- Use descriptive test function names
- Include assertions to verify expected behavior
- Use fixtures for common setup and teardown

## Pull Request Process

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Update documentation if necessary
7. Submit a pull request

## Code Review Checklist

- [ ] Code follows style guidelines
- [ ] Tests are included and pass
- [ ] Documentation is updated
- [ ] Changes are properly tested
- [ ] No unnecessary dependencies added
- [ ] No security vulnerabilities introduced

## License

By contributing to T-Developer, you agree that your contributions will be licensed under the project's license.