#!/usr/bin/env python
"""
Test the Slack notification script locally.

This script tests the notify_slack.py script by sending a test message to Slack.
"""
import os
import sys
import subprocess

def main():
    """Main function."""
    # Check if SLACK_WEBHOOK_URL is set
    webhook_url = os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("Error: SLACK_WEBHOOK_URL environment variable not set")
        print("Please set it with: export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...")
        sys.exit(1)
    
    # Install requirements
    print("Installing requirements...")
    subprocess.run(["pip", "install", "-r", "scripts/requirements.txt"], check=True)
    
    # Send test notification
    print("Sending test notification to Slack...")
    result = subprocess.run(
        ["python", "scripts/notify_slack.py", "--message", "🧪 Test notification from T-Developer", "--status", "success"],
        check=False
    )
    
    if result.returncode == 0:
        print("✅ Test notification sent successfully")
    else:
        print("❌ Failed to send test notification")
        sys.exit(1)

if __name__ == "__main__":
    main()