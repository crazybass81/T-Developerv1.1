# Debugging GitHub Actions CI Failure

This guide provides solutions for common CI pipeline failures in the T-Developer project.

## Common Issues and Solutions

### 1. Syntax Errors in Code

**Problem:** The CI fails during linting because of syntax errors in the code.

**Examples:**
- Triple-quoted strings incorrectly constructed (e.g., in templates)
- Multi-line return statements not properly enclosed in parentheses
- Missing colons, parentheses, or other syntax elements

**Solution:**
- Run `python -m compileall tdev/` locally to check for syntax errors
- For string templates, use different quoting styles (e.g., `'''` for outer strings, `\"\"\"` for inner strings)
- Ensure multi-line expressions are properly enclosed in parentheses or use line continuation

### 2. Outdated Pylint Configuration

**Problem:** The lint step uses deprecated Pylint rule codes.

**Solution:**
- Keep the Pylint disable list updated with valid rule codes
- Remove deprecated codes like `C0330` and `C0326`
- Run `pylint --list-msgs` to see all available messages

### 3. Missing Dependencies

**Problem:** CI fails because required Python packages are missing.

**Solution:**
- Ensure all dependencies are listed in `requirements.txt`
- Update the CI workflow to install all dependencies with `pip install -r requirements.txt`
- For specific steps that need additional packages, install them in that step

### 4. Slack Notification Failures

**Problem:** CI fails because Slack notifications can't be sent (missing webhook URL).

**Solution:**
- Make Slack notification steps conditional: `if: success() && secrets.SLACK_WEBHOOK_URL`
- Modify the notification script to exit with code 0 if webhook URL is missing
- Set the `SLACK_WEBHOOK_URL` secret in the repository settings if notifications are desired

### 5. Test Failures

**Problem:** Tests fail in CI but pass locally.

**Solution:**
- Ensure tests don't depend on local environment variables or configurations
- Add debug output to failing tests to understand the issue
- Check for race conditions or timing issues in tests

## Improving CI Workflow

1. **Separate Linting from Testing:** Consider running linting in a separate job so that tests can run even if linting fails.

2. **Add Caching:** Use GitHub Actions caching to speed up dependency installation:
   ```yaml
   - uses: actions/cache@v2
     with:
       path: ~/.cache/pip
       key: ${{ runner.os }}-pip-${{ hashFiles('**/requirements.txt') }}
       restore-keys: ${{ runner.os }}-pip-
   ```

3. **Improve Error Reporting:** Add steps to collect and display detailed error information when tests fail.

4. **Add Status Checks:** Configure branch protection rules to require CI to pass before merging PRs.

## Quick Fixes for Common Errors

### Fix Syntax Errors
```bash
# Check for syntax errors
python -m compileall tdev/

# Fix string template issues by using different quote styles
# Instead of:
test_code = f\"\"\"...\"\"\"

# Use:
test_code = f'''...'''
```

### Fix Pylint Configuration
```yaml
# Remove deprecated rules
- name: Lint with pylint
  run: |
    pylint tdev/ --disable=C0111,C0103,C0303,W0511,R0903,R0913,R0914,R0801
```

### Fix Slack Notifications
```yaml
- name: Notify Slack
  if: ${{ success() && env.SLACK_WEBHOOK_URL != '' }}
  env:
    SLACK_WEBHOOK_URL: ${{ secrets.SLACK_WEBHOOK_URL }}
  run: |
    python scripts/notify_slack.py --message "✅ Success" --status "success"
```