#!/usr/bin/env python
"""
Send notifications to Slack about CI/CD pipeline status.

This script sends notifications to a Slack webhook when the CI/CD pipeline
completes a stage or encounters an error.
"""
import os
import sys
import json
import argparse
import requests
from datetime import datetime

def send_slack_notification(webhook_url, message, status="success"):
    """
    Send a notification to Slack.
    
    Args:
        webhook_url: Slack webhook URL
        message: Message to send
        status: Status of the notification (success, warning, error)
    
    Returns:
        Response from Slack API
    """
    # Set color based on status
    if status == "success":
        color = "#36a64f"  # Green
    elif status == "warning":
        color = "#ffcc00"  # Yellow
    else:
        color = "#ff0000"  # Red
    
    # Create payload
    payload = {
        "attachments": [
            {
                "color": color,
                "title": "T-Developer CI/CD Pipeline",
                "text": message,
                "footer": f"T-Developer v1.1 • {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "fields": [
                    {
                        "title": "Status",
                        "value": status.capitalize(),
                        "short": True
                    },
                    {
                        "title": "Repository",
                        "value": os.environ.get("GITHUB_REPOSITORY", "Unknown"),
                        "short": True
                    }
                ]
            }
        ]
    }
    
    # Add commit info if available
    commit_sha = os.environ.get("GITHUB_SHA")
    if commit_sha:
        payload["attachments"][0]["fields"].append({
            "title": "Commit",
            "value": f"`{commit_sha[:7]}`",
            "short": True
        })
    
    # Add workflow info if available
    workflow = os.environ.get("GITHUB_WORKFLOW")
    if workflow:
        payload["attachments"][0]["fields"].append({
            "title": "Workflow",
            "value": workflow,
            "short": True
        })
    
    # Send the notification
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        return response
    except Exception as e:
        print(f"Error sending Slack notification: {e}")
        return None

def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Send notifications to Slack")
    parser.add_argument("--webhook", help="Slack webhook URL")
    parser.add_argument("--message", required=True, help="Message to send")
    parser.add_argument("--status", default="success", choices=["success", "warning", "error"], help="Status of the notification")
    
    args = parser.parse_args()
    
    # Get webhook URL from args or environment
    webhook_url = args.webhook or os.environ.get("SLACK_WEBHOOK_URL")
    if not webhook_url:
        print("Warning: Slack webhook URL not provided, skipping notification")
        # Exit with success code since this is now considered optional
        sys.exit(0)
    
    # Send notification
    response = send_slack_notification(webhook_url, args.message, args.status)
    if response and response.status_code == 200:
        print("Slack notification sent successfully")
    else:
        print("Warning: Failed to send Slack notification")
        # Don't fail the build if Slack notification fails
        sys.exit(0)

if __name__ == "__main__":
    main()