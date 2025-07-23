# Pull Request

## Description
<!-- Describe the changes in this PR -->

## Type of change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Refactoring
- [ ] CI/CD improvement

## PR Checklist
- [ ] **Lint & Syntax Check:** Run `pylint tdev/` locally to confirm there are no syntax errors or rule violations
- [ ] **Basic Syntax Check:** Run `python -m compileall tdev/` to verify all files compile correctly
- [ ] **Run Tests Locally:** Execute `pytest` locally and ensure all tests pass
- [ ] **Update Documentation:** If code generation templates or agent logic changed, update relevant docs
- [ ] **CI Secrets Configured:** Verify that required secrets (e.g. `SLACK_WEBHOOK_URL`) are set in the repository
- [ ] **Optional Steps Are Resilient:** Ensure optional CI steps won't fail the pipeline if they fail

## Additional Notes
<!-- Any additional information that would be helpful for reviewers -->