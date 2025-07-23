# T-Developer Monitoring Module

This module provides monitoring and feedback capabilities for T-Developer v1.1. It includes components for collecting metrics, logs, and user feedback for deployed agents.

## Components

### Observer Agent

The `ObserverAgent` is responsible for monitoring deployed agents and collecting metrics and logs. It can:

- Collect CloudWatch metrics for Lambda functions
- Retrieve CloudWatch logs for Lambda functions
- Monitor agent performance and health

Example usage:

```python
from tdev.monitoring.observer import ObserverAgent

# Create an observer
observer = ObserverAgent()

# Monitor an agent
result = observer.run({
    "agent_name": "MyAgent",
    "time_range": "1h",
    "metrics": ["invocations", "errors", "duration"]
})

# Print the results
print(result)
```

### Feedback Collector

The `FeedbackCollector` is responsible for collecting and processing user feedback for agents. It can:

- Store feedback in the registry and DynamoDB
- Create GitHub issues for low-rated feedback
- Retrieve feedback for analysis

Example usage:

```python
from tdev.monitoring.feedback import FeedbackCollector

# Create a feedback collector
collector = FeedbackCollector()

# Collect feedback
result = collector.collect({
    "agent_name": "MyAgent",
    "rating": 4,
    "comment": "Works well, but could be faster",
    "source": "ui"
})

# Get feedback for an agent
feedback = collector.get_feedback("MyAgent")
```

## Integration with AWS CloudWatch

The monitoring module integrates with AWS CloudWatch to collect metrics and logs for deployed agents. It requires the following permissions:

- `cloudwatch:GetMetricStatistics`
- `logs:DescribeLogStreams`
- `logs:GetLogEvents`

These permissions are included in the CloudFormation template in the `LambdaExecutionRole`.

## Integration with GitHub

The feedback collector can create GitHub issues for low-rated feedback. To enable this feature, set the following environment variables:

- `GITHUB_TOKEN`: A GitHub personal access token with repo permissions
- `GITHUB_REPO`: The repository to create issues in (e.g., `username/repo`)

## CLI Commands

The monitoring module provides the following CLI commands:

```bash
# Get metrics for an agent
tdev monitor metrics MyAgent --time-range 1h

# Get logs for an agent
tdev monitor logs MyAgent --time-range 1h --limit 10
```

## API Endpoints

The monitoring module exposes the following API endpoints:

- `POST /feedback`: Submit feedback for an agent
- `GET /feedback/{agent_name}`: Get feedback for an agent