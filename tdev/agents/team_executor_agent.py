from tdev.core.agent import Agent
from tdev.core.registry import get_registry

class TeamExecutorAgent(Agent):
    """
    Agent responsible for executing a team's internal workflow.
    
    The TeamExecutorAgent loads a team by name and executes its
    internal sequence of agents in order.
    """
    
    def run(self, team_name: str, input_data=None):
        """
        Execute a team by name.
        
        Args:
            team_name: The name of the team to execute
            input_data: Optional input data for the team
            
        Returns:
            The output from the team execution
        """
        print(f"TeamExecutorAgent: Executing team {team_name}")
        
        # Initialize input data if not provided
        if input_data is None:
            input_data = {}
        
        # Get the registry
        registry = get_registry()
        
        # Get the team instance
        team = registry.get_instance(team_name)
        if not team:
            print(f"Team not found: {team_name}")
            return {"error": f"Team not found: {team_name}"}
        
        try:
            # Execute the team
            result = team.run(input_data)
            return result
        except Exception as e:
            print(f"Error executing team {team_name}: {e}")
            return {"error": str(e)}