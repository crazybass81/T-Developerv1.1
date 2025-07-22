from typing import Dict, Any, List, Optional
from tdev.core.agent import Agent
from tdev.core.registry import get_registry

class AgentTesterAgent(Agent):
    """
    Agent responsible for testing other agents and tools.
    
    The AgentTesterAgent runs test cases against agents and tools
    to verify their behavior and performance.
    """
    
    def run(self, target_name: str, test_cases: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """
        Test an agent or tool.
        
        Args:
            target_name: The name of the agent or tool to test
            test_cases: Optional list of test cases, each with input and expected output
            
        Returns:
            A dictionary with test results
        """
        print(f"AgentTesterAgent: Testing {target_name}")
        
        # Get the registry
        registry = get_registry()
        
        # Get the target agent or tool
        target = registry.get_instance(target_name)
        if not target:
            return {
                "success": False,
                "error": f"Agent or tool not found: {target_name}"
            }
        
        # If no test cases provided, use a simple echo test
        if not test_cases:
            test_cases = [
                {
                    "input": "test input",
                    "expected": "test input"
                }
            ]
        
        # Run the test cases
        results = []
        passed = 0
        
        for i, test_case in enumerate(test_cases):
            test_input = test_case.get("input")
            expected = test_case.get("expected")
            
            try:
                # Run the target
                actual = target.run(test_input)
                
                # Compare the result
                success = actual == expected
                if success:
                    passed += 1
                
                results.append({
                    "test_case": i + 1,
                    "input": test_input,
                    "expected": expected,
                    "actual": actual,
                    "success": success
                })
            except Exception as e:
                results.append({
                    "test_case": i + 1,
                    "input": test_input,
                    "error": str(e),
                    "success": False
                })
        
        # Calculate overall success
        success_rate = passed / len(test_cases) if test_cases else 0
        
        return {
            "success": success_rate == 1.0,
            "success_rate": success_rate,
            "passed": passed,
            "total": len(test_cases),
            "results": results
        }