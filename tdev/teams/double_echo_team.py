from tdev.core.team import Team
from tdev.core.registry import get_registry

class DoubleEchoTeam(Team):
    """
    DoubleEchoTeam demonstrates a simple team that calls EchoAgent twice.
    
    This is a minimal example to show how teams can coordinate multiple agents.
    """
    
    def __init__(self):
        """Initialize the team with EchoAgent instances."""
        super().__init__()
        
        # Get the registry
        registry = get_registry()
        
        # Add two instances of EchoAgent
        self.add_agent("echo1", registry.get_instance("EchoAgent"))
        self.add_agent("echo2", registry.get_instance("EchoAgent"))
    
    def run(self, input_data):
        """
        Run the team by calling EchoAgent twice in sequence.
        
        Args:
            input_data: The input data for the first echo
            
        Returns:
            The result of the second echo
        """
        print("DoubleEchoTeam: Starting sequence")
        
        # First echo
        echo1 = self.agents.get("echo1")
        if not echo1:
            return {"error": "First echo agent not found"}
        
        first_result = echo1.run(input_data)
        print(f"DoubleEchoTeam: First echo result - {first_result}")
        
        # Second echo
        echo2 = self.agents.get("echo2")
        if not echo2:
            return {"error": "Second echo agent not found"}
        
        # Add a prefix to show it's the second echo
        if isinstance(first_result, dict):
            second_input = {**first_result, "prefix": "Second echo: "}
        else:
            second_input = {"message": f"Second echo: {first_result}"}
        
        second_result = echo2.run(second_input)
        print(f"DoubleEchoTeam: Second echo result - {second_result}")
        
        return second_result