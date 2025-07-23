# T-Developer Notifications

This document explains how to set up and use the notification system in T-Developer v1.1.

## Slack Notifications

T-Developer can send notifications to Slack about CI/CD pipeline status and other important events.

### Setup

1. Create a Slack app and webhook URL:
   - Go to https://api.slack.com/apps
   - Click "Create New App" and select "From scratch"
   - Name your app (e.g., "T-Developer Bot") and select your workspace
   - Navigate to "Incoming Webhooks" and activate them
   - Click "Add New Webhook to Workspace" and select a channel
   - Copy the webhook URL

2. Add the webhook URL to your environment:
   - For local development: `export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...`
   - For GitHub Actions: Add it as a repository secret named `SLACK_WEBHOOK_URL`

### Usage

The notification script can be used directly:

```bash
# Send a success notification
python scripts/notify_slack.py --message "✅ Task completed successfully" --status "success"

# Send a warning notification
python scripts/notify_slack.py --message "⚠️ Warning: Task completed with issues" --status "warning"

# Send an error notification
python scripts/notify_slack.py --message "❌ Error: Task failed" --status "error"
```

### Testing

You can test the Slack notification system using the provided test script:

```bash
# Make sure SLACK_WEBHOOK_URL is set in your environment
export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...

# Run the test script
python scripts/test_slack_notification.py
```

### CI/CD Integration

The Slack notification system is automatically integrated with the CI/CD pipeline:

- Successful CI runs trigger a success notification
- Failed CI runs trigger an error notification
- Successful deployments trigger a success notification
- Failed deployments trigger an error notification

### Customization

You can customize the notification format by modifying the `send_slack_notification` function in `scripts/notify_slack.py`. The function supports:

- Different colors based on status (green for success, yellow for warning, red for error)
- Adding commit information
- Adding workflow information
- Custom timestamps

## Future Enhancements

Planned enhancements for the notification system include:

- Support for other notification channels (email, Discord, Microsoft Teams)
- More detailed notifications with links to logs and artifacts
- Customizable notification templates
- Rate limiting to prevent notification spam