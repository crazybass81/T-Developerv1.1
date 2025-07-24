#!/usr/bin/env python3
"""
Test script for the MetaAgent and AutoAgentComposer.

This script performs a simple end-to-end test of the orchestration system.
"""
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from tdev.core.registry import get_registry

def test_meta_agent():
    """Test the MetaAgent with a simple goal."""
    print("Testing MetaAgent...")
    
    # Get the registry
    registry = get_registry()
    
    # Get the MetaAgent
    meta_agent = registry.get_instance("MetaAgent")
    if not meta_agent:
        print("MetaAgent not found in registry")
        return False
    
    # Prepare a simple request
    request = {
        "goal": "Echo the input data",
        "options": {
            "input_data": "Hello, MetaAgent!"
        }
    }
    
    # Run the MetaAgent
    print("Running MetaAgent with request:", request)
    result = meta_agent.run(request)
    
    # Display the result
    print("MetaAgent result:", result)
    
    return result.get("success", False)

def test_auto_agent_composer():
    """Test the AutoAgentComposer with a simple specification."""
    print("\nTesting AutoAgentComposer...")
    
    # Get the registry
    registry = get_registry()
    
    # Get the AutoAgentComposer
    composer = registry.get_instance("AutoAgentComposerAgent")
    if not composer:
        print("AutoAgentComposerAgent not found in registry")
        return False
    
    # Prepare a simple specification
    spec = {
        "type": "agent",
        "name": "TestEcho",
        "goal": "A test agent that echoes the input data",
        "input": "Any data to echo",
        "output": "The same data that was provided as input"
    }
    
    # Run the AutoAgentComposer
    print("Running AutoAgentComposer with spec:", spec)
    result = composer.run(spec)
    
    # Display the result
    print("AutoAgentComposer result:", result)
    
    return result.get("success", False)

def test_orchestrator_team():
    """Test the OrchestratorTeam with a simple goal."""
    print("\nTesting OrchestratorTeam...")
    
    # Get the registry
    registry = get_registry()
    
    # Get the OrchestratorTeam
    team = registry.get_instance("OrchestratorTeam")
    if not team:
        print("OrchestratorTeam not found in registry")
        return False
    
    # Prepare a simple input
    input_data = {
        "goal": "Echo the input data",
        "options": {
            "input_data": "Hello, OrchestratorTeam!"
        }
    }
    
    # Run the OrchestratorTeam
    print("Running OrchestratorTeam with input:", input_data)
    result = team.run(input_data)
    
    # Display the result
    print("OrchestratorTeam result:", result)
    
    return True

def main():
    """Main function."""
    print("Running orchestration tests...\n")
    
    # Test the MetaAgent
    meta_success = test_meta_agent()
    
    # Test the AutoAgentComposer
    composer_success = test_auto_agent_composer()
    
    # Test the OrchestratorTeam
    team_success = test_orchestrator_team()
    
    # Print summary
    print("\nTest Summary:")
    print(f"MetaAgent: {'PASS' if meta_success else 'FAIL'}")
    print(f"AutoAgentComposer: {'PASS' if composer_success else 'FAIL'}")
    print(f"OrchestratorTeam: {'PASS' if team_success else 'FAIL'}")
    
    # Overall result
    overall = all([meta_success, composer_success, team_success])
    print(f"\nOverall: {'PASS' if overall else 'FAIL'}")
    
    return 0 if overall else 1

if __name__ == "__main__":
    sys.exit(main())