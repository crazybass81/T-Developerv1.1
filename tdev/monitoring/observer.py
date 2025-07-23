"""
Observer for monitoring deployed agents.

This module provides functionality for monitoring deployed agents
and collecting metrics and logs.
"""
import os
import json
import boto3
import time
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

from tdev.core.registry import get_registry
from tdev.core.agent import Agent

class ObserverAgent(Agent):
    """
    Agent responsible for monitoring deployed agents.
    
    The ObserverAgent collects metrics, logs, and feedback for deployed agents
    and provides insights for continuous improvement.
    """
    
    def __init__(self):
        """Initialize the ObserverAgent."""
        self.registry = get_registry()
        self.region_name = os.environ.get("AWS_REGION", "us-east-1")
        self.cloudwatch = boto3.client("cloudwatch", region_name=self.region_name)
        self.logs = boto3.client("logs", region_name=self.region_name)
    
    def run(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Monitor deployed agents and collect metrics.
        
        Args:
            request: A dictionary containing the monitoring request:
                - agent_name: Optional name of the agent to monitor
                - time_range: Optional time range for metrics (e.g., "1h", "1d")
                - metrics: Optional list of metrics to collect
                
        Returns:
            A dictionary containing monitoring results
        """
        agent_name = request.get("agent_name")
        time_range = request.get("time_range", "1h")
        metrics = request.get("metrics", ["invocations", "errors", "duration"])
        
        # Convert time range to seconds
        seconds = self._parse_time_range(time_range)
        
        # Get agents to monitor
        agents_to_monitor = []
        if agent_name:
            agent_meta = self.registry.get(agent_name)
            if agent_meta and "deployment" in agent_meta:
                agents_to_monitor.append(agent_meta)
        else:
            # Get all deployed agents
            for agent_meta in self.registry.get_all().values():
                if "deployment" in agent_meta:
                    agents_to_monitor.append(agent_meta)
        
        # Collect metrics for each agent
        results = {}
        for agent_meta in agents_to_monitor:
            agent_name = agent_meta["name"]
            deployment = agent_meta["deployment"]
            
            # Skip if not deployed to Lambda
            if deployment.get("type") != "lambda" and deployment.get("type") != "bedrock":
                continue
            
            # Get function name
            function_name = deployment.get("function_name", f"t-developer-{agent_name.lower()}")
            
            # Collect metrics
            agent_metrics = self._collect_metrics(function_name, seconds, metrics)
            
            # Collect logs
            agent_logs = self._collect_logs(function_name, seconds)
            
            # Store results
            results[agent_name] = {
                "metrics": agent_metrics,
                "logs": agent_logs,
                "deployment": deployment
            }
        
        return {
            "timestamp": datetime.now().isoformat(),
            "time_range": time_range,
            "results": results
        }
    
    def _parse_time_range(self, time_range: str) -> int:
        """
        Parse a time range string into seconds.
        
        Args:
            time_range: Time range string (e.g., "1h", "1d")
            
        Returns:
            Number of seconds
        """
        unit = time_range[-1]
        value = int(time_range[:-1])
        
        if unit == "m":
            return value * 60
        elif unit == "h":
            return value * 3600
        elif unit == "d":
            return value * 86400
        else:
            return 3600  # Default to 1 hour
    
    def _collect_metrics(self, function_name: str, seconds: int, metrics: List[str]) -> Dict[str, Any]:
        """
        Collect metrics for a Lambda function.
        
        Args:
            function_name: Name of the Lambda function
            seconds: Time range in seconds
            metrics: List of metrics to collect
            
        Returns:
            Dictionary of metrics
        """
        end_time = datetime.now()
        start_time = end_time - timedelta(seconds=seconds)
        
        metric_data = {}
        
        # Define metric mappings
        metric_mappings = {
            "invocations": {"namespace": "AWS/Lambda", "name": "Invocations", "stat": "Sum"},
            "errors": {"namespace": "AWS/Lambda", "name": "Errors", "stat": "Sum"},
            "duration": {"namespace": "AWS/Lambda", "name": "Duration", "stat": "Average"},
            "throttles": {"namespace": "AWS/Lambda", "name": "Throttles", "stat": "Sum"},
            "concurrent_executions": {"namespace": "AWS/Lambda", "name": "ConcurrentExecutions", "stat": "Maximum"}
        }
        
        # Collect requested metrics
        for metric in metrics:
            if metric in metric_mappings:
                mapping = metric_mappings[metric]
                
                try:
                    response = self.cloudwatch.get_metric_statistics(
                        Namespace=mapping["namespace"],
                        MetricName=mapping["name"],
                        Dimensions=[{"Name": "FunctionName", "Value": function_name}],
                        StartTime=start_time,
                        EndTime=end_time,
                        Period=60,  # 1-minute periods
                        Statistics=[mapping["stat"]]
                    )
                    
                    # Extract datapoints
                    datapoints = response.get("Datapoints", [])
                    if datapoints:
                        # Sort by timestamp
                        datapoints.sort(key=lambda x: x["Timestamp"])
                        
                        # Extract values
                        values = [dp[mapping["stat"]] for dp in datapoints]
                        timestamps = [dp["Timestamp"].isoformat() for dp in datapoints]
                        
                        metric_data[metric] = {
                            "values": values,
                            "timestamps": timestamps,
                            "total": sum(values) if mapping["stat"] == "Sum" else None,
                            "average": sum(values) / len(values) if values else None
                        }
                    else:
                        metric_data[metric] = {"values": [], "timestamps": [], "total": 0, "average": None}
                
                except Exception as e:
                    metric_data[metric] = {"error": str(e)}
        
        return metric_data
    
    def _collect_logs(self, function_name: str, seconds: int) -> Dict[str, Any]:
        """
        Collect logs for a Lambda function.
        
        Args:
            function_name: Name of the Lambda function
            seconds: Time range in seconds
            
        Returns:
            Dictionary of logs
        """
        log_group_name = f"/aws/lambda/{function_name}"
        end_time = int(time.time() * 1000)
        start_time = end_time - (seconds * 1000)
        
        try:
            # Get log streams
            response = self.logs.describe_log_streams(
                logGroupName=log_group_name,
                orderBy="LastEventTime",
                descending=True,
                limit=5
            )
            
            log_streams = response.get("logStreams", [])
            
            # Collect logs from each stream
            all_events = []
            for stream in log_streams:
                stream_name = stream["logStreamName"]
                
                try:
                    events_response = self.logs.get_log_events(
                        logGroupName=log_group_name,
                        logStreamName=stream_name,
                        startTime=start_time,
                        endTime=end_time,
                        limit=100
                    )
                    
                    events = events_response.get("events", [])
                    for event in events:
                        all_events.append({
                            "timestamp": event["timestamp"],
                            "message": event["message"],
                            "stream": stream_name
                        })
                
                except Exception as e:
                    all_events.append({
                        "error": f"Error getting events from stream {stream_name}: {str(e)}"
                    })
            
            # Sort events by timestamp
            all_events.sort(key=lambda x: x.get("timestamp", 0))
            
            return {
                "events": all_events,
                "count": len(all_events)
            }
        
        except Exception as e:
            return {"error": str(e)}
    
    def collect_feedback(self, agent_name: str, feedback: Dict[str, Any]) -> Dict[str, Any]:
        """
        Collect user feedback for an agent.
        
        Args:
            agent_name: Name of the agent
            feedback: Feedback data
                - rating: Numeric rating (1-5)
                - comment: Optional comment
                - source: Source of the feedback (e.g., "ui", "slack")
                
        Returns:
            Result of feedback collection
        """
        # Get agent from registry
        agent_meta = self.registry.get(agent_name)
        if not agent_meta:
            return {"success": False, "error": f"Agent {agent_name} not found"}
        
        # Initialize feedback list if not exists
        if "feedback" not in agent_meta:
            agent_meta["feedback"] = []
        
        # Add timestamp to feedback
        feedback["timestamp"] = datetime.now().isoformat()
        
        # Add feedback to agent metadata
        agent_meta["feedback"].append(feedback)
        
        # Update registry
        self.registry.update(agent_name, agent_meta)
        
        # If rating is low, create an issue
        rating = feedback.get("rating", 0)
        if rating <= 2:
            self._create_issue(agent_name, feedback)
        
        return {"success": True}
    
    def _create_issue(self, agent_name: str, feedback: Dict[str, Any]) -> None:
        """
        Create an issue for low-rated feedback.
        
        Args:
            agent_name: Name of the agent
            feedback: Feedback data
        """
        # In a production system, this would create a GitHub issue or Jira ticket
        # For now, just print to console
        print(f"ISSUE: Low rating ({feedback.get('rating')}) for {agent_name}")
        print(f"Comment: {feedback.get('comment', 'No comment')}")
        print(f"Source: {feedback.get('source', 'Unknown')}")
        print(f"Timestamp: {feedback.get('timestamp')}")
        
        # TODO: Integrate with GitHub API to create an issue