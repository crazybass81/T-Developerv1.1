# Code Quality Guidelines for T-Developer v1.1

This document outlines best practices for maintaining code quality in the T-Developer v1.1 project, with a focus on linting, testing, and CI/CD integration.

## Pylint Configuration

We use Pylint to enforce code quality standards. Our configuration is defined in `.pylintrc` at the project root.

### Current Configuration

- **Score Threshold**: We require a minimum score of 9.0/10
- **Disabled Rules**: We've disabled certain rules that are less relevant to our project
- **Generated Members**: We've configured Pylint to recognize dynamic attributes in our registry

### Gradually Improving Code Quality

As we improve the codebase, we should aim to:

1. **Re-enable disabled rules** one by one
2. **Increase the score threshold** gradually (aim for 9.5, then 10.0)
3. **Add more specific rules** for our project's needs

## Common Pylint Issues and How to Fix Them

| Issue | Description | Fix |
|-------|-------------|-----|
| **Unused Variables** | Variables defined but not used | Prefix with `_` or remove |
| **Import Order** | Imports not grouped correctly | Group as: stdlib → third-party → local |
| **Line Too Long** | Lines exceeding max length | Break into multiple lines or use parentheses |
| **Reimported** | Module imported multiple times | Consolidate imports at the top of the file |
| **No Member** | Attribute not found in class | Add to `generated-members` in `.pylintrc` |

## CI Pipeline

Our CI pipeline in GitHub Actions:

1. **Checks Python syntax** using `compileall`
2. **Runs Pylint** with our configuration
3. **Uses pylint-exit** to only fail on errors
4. **Runs tests** with coverage
5. **Tests template strings** for validity
6. **Tests core agents** and agent generation
7. **Runs security analysis** with Bandit

### Handling Pylint Exit Codes

Pylint uses bit-encoded exit codes:
- 1: Fatal message issued
- 2: Error message issued
- 4: Warning message issued
- 8: Refactor message issued
- 16: Convention message issued

We use `pylint-exit --error-fail` to only fail the build on fatal or error messages (bits 1 and 2).

## Best Practices for Developers

1. **Run Linting Locally**: Before committing, run `pylint tdev/ --rcfile=.pylintrc`
2. **Fix Critical Issues**: Always fix fatal and error-level issues
3. **Incremental Improvement**: Address warnings and refactor suggestions when possible
4. **Add Tests**: Ensure new code has test coverage
5. **Document Changes**: Update documentation when changing functionality

## Long-term Code Quality Goals

1. **Achieve 10/10 Pylint Score**: Gradually fix all issues
2. **100% Test Coverage**: Add tests for all code paths
3. **Automated Documentation**: Keep documentation in sync with code
4. **Type Annotations**: Add type hints to improve code clarity and catch errors

By following these guidelines, we can maintain high code quality while allowing for efficient development.