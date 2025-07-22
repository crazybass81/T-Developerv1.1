from tdev.core.registry import get_registry
from tdev.core.schema import ToolMeta, AgentMeta, TeamMeta

def initialize_registry():
    """Initialize the registry with core components."""
    registry = get_registry()
    
    # Register EchoTool
    echo_tool_meta = ToolMeta(
        name="EchoTool",
        class_path="tdev.tools.echo_tool.echo_tool",
        description="A simple tool that returns the input data unchanged.",
        tags=["utility", "example"]
    )
    registry.register("EchoTool", echo_tool_meta.to_dict())
    
    # Register EchoAgent
    echo_agent_meta = AgentMeta(
        name="EchoAgent",
        class_path="tdev.agents.echo_agent.EchoAgent",
        description="A simple agent that echoes the input data.",
        tags=["utility", "example"]
    )
    registry.register("EchoAgent", echo_agent_meta.to_dict())
    
    # Register WorkflowExecutorAgent
    workflow_executor_meta = AgentMeta(
        name="WorkflowExecutorAgent",
        class_path="tdev.agents.workflow_executor_agent.WorkflowExecutorAgent",
        description="Agent responsible for executing workflows.",
        tags=["core", "workflow"]
    )
    registry.register("WorkflowExecutorAgent", workflow_executor_meta.to_dict())
    
    # Register ClassifierAgent
    classifier_meta = AgentMeta(
        name="ClassifierAgent",
        class_path="tdev.agents.classifier_agent.ClassifierAgent",
        description="Agent responsible for classifying components as Tool, Agent, or Team.",
        tags=["core", "classification"]
    )
    registry.register("ClassifierAgent", classifier_meta.to_dict())
    
    # Register PlannerAgent
    planner_meta = AgentMeta(
        name="PlannerAgent",
        class_path="tdev.agents.planner_agent.PlannerAgent",
        description="Agent responsible for planning workflows.",
        tags=["core", "planning"]
    )
    registry.register("PlannerAgent", planner_meta.to_dict())
    
    # Register EvaluatorAgent
    evaluator_meta = AgentMeta(
        name="EvaluatorAgent",
        class_path="tdev.agents.evaluator_agent.EvaluatorAgent",
        description="Agent responsible for evaluating workflows and agents.",
        tags=["core", "evaluation"]
    )
    registry.register("EvaluatorAgent", evaluator_meta.to_dict())
    
    # Register AgentTesterAgent
    tester_meta = AgentMeta(
        name="AgentTesterAgent",
        class_path="tdev.agents.agent_tester_agent.AgentTesterAgent",
        description="Agent responsible for testing other agents and tools.",
        tags=["core", "testing"]
    )
    registry.register("AgentTesterAgent", tester_meta.to_dict())
    
    # Register TeamExecutorAgent
    team_executor_meta = AgentMeta(
        name="TeamExecutorAgent",
        class_path="tdev.agents.team_executor_agent.TeamExecutorAgent",
        description="Agent responsible for executing teams.",
        tags=["core", "team", "execution"]
    )
    registry.register("TeamExecutorAgent", team_executor_meta.to_dict())
    
    # Register AutoAgentComposer (Agno)
    auto_agent_composer_meta = AgentMeta(
        name="AutoAgentComposerAgent",
        class_path="tdev.agents.auto_agent_composer.AutoAgentComposer",
        description="Agent responsible for generating new agents and tools (Agno).",
        tags=["core", "generation", "agno"]
    )
    registry.register("AutoAgentComposerAgent", auto_agent_composer_meta.to_dict())
    
    # Register MetaAgent (Orchestrator)
    meta_agent_meta = AgentMeta(
        name="MetaAgent",
        class_path="tdev.agents.meta_agent.MetaAgent",
        description="The central orchestrator that coordinates other agents to fulfill user requests.",
        tags=["core", "orchestration", "meta"]
    )
    registry.register("MetaAgent", meta_agent_meta.to_dict())
    
    # Register OrchestratorTeam
    orchestrator_team_meta = TeamMeta(
        name="OrchestratorTeam",
        class_path="tdev.teams.orchestrator_team.OrchestratorTeam",
        description="Team that coordinates the core agents of T-Developer.",
        tags=["core", "orchestration"]
    )
    registry.register("OrchestratorTeam", orchestrator_team_meta.to_dict())
    
    # Register DoubleEchoTeam
    double_echo_team_meta = TeamMeta(
        name="DoubleEchoTeam",
        class_path="tdev.teams.double_echo_team.DoubleEchoTeam",
        description="A simple team that calls EchoAgent twice in sequence.",
        tags=["example", "demo"]
    )
    registry.register("DoubleEchoTeam", double_echo_team_meta.to_dict())
    
    print("Registry initialized with core components.")

if __name__ == "__main__":
    initialize_registry()