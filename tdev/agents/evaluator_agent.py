from typing import Dict, Any, List, Union, Optional
import os
import json
from tdev.core.agent import Agent
from tdev.core.workflow import Workflow, load_workflow
from tdev.core.registry import get_registry
from tdev.agent_core.bedrock_client import BedrockClient

class EvaluatorAgent(Agent):
    """
    Agent responsible for evaluating workflows and agents.
    
    The EvaluatorAgent scores workflows based on quality, efficiency,
    and other metrics to ensure they meet standards. It uses AWS Bedrock
    for intelligent evaluation when available.
    """
    
    def __init__(self):
        """Initialize the EvaluatorAgent."""
        super().__init__()
        self.bedrock_client = None
        try:
            self.bedrock_client = BedrockClient()
        except Exception as e:
            print(f"Warning: Could not initialize Bedrock client: {e}")
    
    def run(self, workflow_data: Union[str, Dict], test_results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Evaluate a workflow.
        
        Args:
            workflow_data: Either a path to the workflow file or a workflow dictionary
            test_results: Optional test results to incorporate in evaluation
            
        Returns:
            A dictionary with evaluation results
        """
        # Load the workflow
        workflow = None
        if isinstance(workflow_data, str):
            print(f"EvaluatorAgent: Evaluating workflow at {workflow_data}")
            workflow = load_workflow(workflow_data)
            if not workflow:
                return {
                    "score": 0,
                    "error": f"Could not load workflow: {workflow_data}"
                }
        else:
            print("EvaluatorAgent: Evaluating workflow from dictionary")
            workflow = workflow_data
        
        # Perform evaluation using Bedrock if available
        if self.bedrock_client and isinstance(workflow, dict):
            evaluation = self._evaluate_with_bedrock(workflow, test_results)
        else:
            # Fall back to rule-based evaluation
            evaluation = self._evaluate_workflow(workflow, test_results)
        
        # Determine if the workflow needs improvement
        needs_improvement = evaluation["score"] < 70 or len(evaluation["suggestions"]) > 0
        
        # Add improvement flag to the result
        evaluation["needs_improvement"] = needs_improvement
        
        return evaluation
    
    def _evaluate_with_bedrock(self, workflow: Dict, test_results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Evaluate a workflow using AWS Bedrock for intelligent analysis.
        
        Args:
            workflow: The workflow to evaluate
            test_results: Optional test results to incorporate
            
        Returns:
            Evaluation results
        """
        # Prepare the prompt for Bedrock
        workflow_json = json.dumps(workflow, indent=2)
        test_results_str = "No test results available"
        if test_results:
            test_results_str = json.dumps(test_results, indent=2)
        
        prompt = f"""You are an AI workflow evaluator. Your task is to evaluate a workflow plan and provide a quality score and suggestions for improvement.

Workflow:
```json
{workflow_json}
```

Test Results:
```json
{test_results_str}
```

Evaluate this workflow based on the following criteria:
1. Structural completeness: Does the workflow have all necessary steps?
2. Agent suitability: Are the selected agents appropriate for their tasks?
3. Error resilience: Does the workflow handle potential errors?
4. Efficiency: Is the workflow efficient or are there redundant steps?
5. Clarity: Is the workflow well-documented and clear?

Provide your evaluation as a JSON object with the following fields:
- score: A numeric score from 0-100
- metrics: An object with scores for each criterion (0.0-1.0)
- suggestions: An array of specific suggestions for improvement

Evaluation:
"""
        
        try:
            # Call Bedrock to generate the evaluation
            model_id = os.environ.get("BEDROCK_MODEL_ID", "anthropic.claude-v2")
            response = self.bedrock_client.invoke_model(
                model_id=model_id,
                prompt=prompt,
                parameters={
                    "maxTokens": 1000,
                    "temperature": 0.2,
                    "topP": 0.9
                }
            )
            
            # Extract the evaluation from the response
            if "anthropic" in model_id.lower():
                completion = response.get("completion", "")
            else:
                completion = response.get("outputText", "")
            
            # Try to parse the JSON response
            try:
                # Find JSON object in the response
                json_start = completion.find('{')
                json_end = completion.rfind('}') + 1
                if json_start >= 0 and json_end > json_start:
                    json_str = completion[json_start:json_end]
                    evaluation = json.loads(json_str)
                    
                    # Ensure the evaluation has the required fields
                    if "score" not in evaluation:
                        evaluation["score"] = 70  # Default score
                    if "metrics" not in evaluation:
                        evaluation["metrics"] = {}
                    if "suggestions" not in evaluation:
                        evaluation["suggestions"] = []
                    
                    # Add improvement flag
                    evaluation["needs_improvement"] = evaluation["score"] < 70 or len(evaluation["suggestions"]) > 0
                    
                    return evaluation
            except Exception as e:
                print(f"Error parsing Bedrock evaluation response: {e}")
        except Exception as e:
            print(f"Error calling Bedrock for evaluation: {e}")
        
        # Fall back to rule-based evaluation if Bedrock fails
        return self._evaluate_workflow(workflow, test_results)
    
    def _evaluate_workflow(self, workflow: Dict, test_results: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Evaluate a workflow based on various criteria.
        """
        # Get registry to check for agent availability
        registry = get_registry()
        
        # Initialize metrics
        metrics = {
            "structural_completeness": 0.0,
            "agent_suitability": 0.0,
            "error_resilience": 0.0,
            "efficiency": 0.0,
            "clarity": 0.0
        }
        
        suggestions = []
        
        # Check structural completeness
        steps = workflow.get("steps", [])
        if not steps:
            suggestions.append("Workflow has no steps defined.")
            metrics["structural_completeness"] = 0.0
        else:
            metrics["structural_completeness"] = min(1.0, len(steps) / 5)  # More steps = more complete, up to 5
        
        # Check agent suitability
        available_agents = {name: metadata for name, metadata in registry.get_all().items() if metadata.get("type") == "agent"}
        missing_agents = []
        for i, step in enumerate(steps):
            agent_name = step.get("agent")
            if not agent_name:
                suggestions.append(f"Step {i+1} does not specify an agent.")
                continue
                
            if agent_name not in available_agents:
                missing_agents.append(agent_name)
                suggestions.append(f"Agent '{agent_name}' in step {i+1} is not available in the registry.")
        
        if missing_agents:
            metrics["agent_suitability"] = 0.0
        else:
            metrics["agent_suitability"] = 1.0
        
        # Check data flow between steps
        for i, step in enumerate(steps):
            if i > 0 and "input" not in step:
                suggestions.append(f"Step {i+1} does not specify how to get input from previous steps.")
                metrics["structural_completeness"] *= 0.8  # Reduce completeness score
        
        # Check error resilience
        has_error_handling = any("on_error" in step for step in steps)
        metrics["error_resilience"] = 0.5 if has_error_handling else 0.2
        if not has_error_handling:
            suggestions.append("Workflow does not include error handling for steps.")
        
        # Check efficiency
        # Simple heuristic: penalize very long workflows
        if len(steps) > 10:
            metrics["efficiency"] = 0.6
            suggestions.append("Workflow has many steps. Consider consolidating some steps.")
        else:
            metrics["efficiency"] = 0.9
        
        # Check clarity
        has_description = "description" in workflow and workflow["description"]
        has_step_descriptions = all("description" in step for step in steps)
        if has_description and has_step_descriptions:
            metrics["clarity"] = 1.0
        elif has_description:
            metrics["clarity"] = 0.7
            suggestions.append("Add descriptions to individual steps for better clarity.")
        else:
            metrics["clarity"] = 0.3
            suggestions.append("Workflow lacks a clear description.")
        
        # Incorporate test results if available
        if test_results:
            self._incorporate_test_results(metrics, suggestions, test_results)
        
        # Calculate overall score (weighted average)
        weights = {
            "structural_completeness": 0.25,
            "agent_suitability": 0.3,
            "error_resilience": 0.15,
            "efficiency": 0.15,
            "clarity": 0.15
        }
        
        score = sum(metrics[key] * weights[key] for key in metrics) * 100
        
        result = {
            "score": round(score),
            "metrics": metrics,
            "suggestions": suggestions,
            "needs_improvement": round(score) < 70 or len(suggestions) > 0
        }
        
        return result
    
    def _incorporate_test_results(self, metrics: Dict[str, float], suggestions: List[str], test_results: Dict) -> None:
        """
        Incorporate test results into the evaluation.
        """
        # Check if tests passed
        tests_passed = test_results.get("passed", False)
        if not tests_passed:
            metrics["structural_completeness"] *= 0.7  # Reduce score
            suggestions.append("Workflow failed tests. Review test results for details.")
            
            # Add specific test failures to suggestions
            failures = test_results.get("failures", [])
            for failure in failures[:3]:  # Limit to first 3 failures
                suggestions.append(f"Test failure: {failure}")
        else:
            # Boost score slightly for passing tests
            for key in metrics:
                metrics[key] = min(1.0, metrics[key] * 1.1)