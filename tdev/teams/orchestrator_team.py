from tdev.core.team import Team
from tdev.core.registry import get_registry

class OrchestratorTeam(Team):
    """
    OrchestratorTeam coordinates the core agents of T-Developer.
    
    This team encapsulates the main orchestration workflow by using the MetaAgent
    to coordinate ClassifierAgent, PlannerAgent, EvaluatorAgent, and
    WorkflowExecutorAgent to fulfill a user request.
    """
    
    def __init__(self):
        """Initialize the orchestrator team with its member agents."""
        super().__init__()
        
        # Get the registry
        registry = get_registry()
        
        # Add the DevCoordinatorAgent as the main orchestrator
        self.add_agent("coordinator", registry.get_instance("DevCoordinatorAgent"))
        
        # Add other core agents for direct access if needed
        self.add_agent("classifier", registry.get_instance("ClassifierAgent"))
        self.add_agent("planner", registry.get_instance("PlannerAgent"))
        self.add_agent("evaluator", registry.get_instance("EvaluatorAgent"))
        self.add_agent("executor", registry.get_instance("WorkflowExecutorAgent"))
        self.add_agent("composer", registry.get_instance("AutoAgentComposerAgent"))
    
    def run(self, input_data):
        """
        Coordinate the orchestration workflow using the DevCoordinatorAgent.
        
        Args:
            input_data: A dictionary containing either:
                - 'code': A path to code that needs classification
                - 'goal': A description of the goal to achieve
                - 'options': Optional configuration options
                
        Returns:
            The result of the workflow execution
        """
        print("OrchestratorTeam: Starting orchestration workflow using DevCoordinatorAgent")
        
        # Get the DevCoordinatorAgent
        coordinator = self.agents.get("coordinator")
        if not coordinator:
            print("OrchestratorTeam: DevCoordinatorAgent not found, falling back to direct orchestration")
            return self._legacy_run(input_data)
        
        # Prepare the request for the DevCoordinatorAgent
        request = {
            "goal": input_data.get("goal", ""),
            "code": input_data.get("code"),
            "options": input_data.get("options", {})
        }
        
        # Run the DevCoordinatorAgent
        print("OrchestratorTeam: Delegating to DevCoordinatorAgent")
        result = coordinator.run(request)
        
        print("OrchestratorTeam: DevCoordinatorAgent execution completed")
        return result
    
    def _legacy_run(self, input_data):
        """
        Legacy direct orchestration method (fallback if MetaAgent is not available).
        
        Args:
            input_data: A dictionary containing either:
                - 'code': A path to code that needs classification
                - 'goal': A description of the goal to achieve
                
        Returns:
            The result of the workflow execution
        """
        print("OrchestratorTeam: Using legacy direct orchestration")
        
        # Initialize context
        context = {}
        
        # Step 1: If code is provided, classify it
        if 'code' in input_data:
            print("OrchestratorTeam: Classifying code")
            classifier = self.agents.get("classifier")
            if classifier:
                classification = classifier.run(input_data['code'])
                context['classification'] = classification
                print(f"OrchestratorTeam: Classification result - {classification['type']}")
        
        # Step 2: Plan a workflow based on the goal
        if 'goal' in input_data:
            print("OrchestratorTeam: Planning workflow")
            planner = self.agents.get("planner")
            if planner:
                workflow = planner.run({
                    'goal': input_data['goal'],
                    'classification': context.get('classification')
                })
                context['workflow'] = workflow
                print(f"OrchestratorTeam: Workflow planned - {workflow.get('id', 'unknown')}")
        
        # Step 3: Evaluate the workflow quality
        if 'workflow' in context:
            print("OrchestratorTeam: Evaluating workflow")
            evaluator = self.agents.get("evaluator")
            if evaluator:
                evaluation = evaluator.run(context['workflow'])
                context['evaluation'] = evaluation
                print(f"OrchestratorTeam: Evaluation score - {evaluation.get('score', 0)}")
                
                # If score is too low, we could request refinement
                # (simplified for now - always proceed)
        
        # Step 4: Execute the workflow
        if 'workflow' in context:
            print("OrchestratorTeam: Executing workflow")
            executor = self.agents.get("executor")
            if executor:
                result = executor.run(context['workflow'])
                context['result'] = result
                print("OrchestratorTeam: Execution completed")
        
        # Return the final result or the entire context
        return context.get('result', context)