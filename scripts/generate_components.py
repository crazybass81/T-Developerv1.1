#!/usr/bin/env python3
"""
Script to generate all core agents and tools using Agno.

This script reads specifications from the specs directory and uses
the AutoAgentComposer to generate the corresponding components.
"""
import os
import json
import sys
from pathlib import Path

# Add the project root to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from tdev.core.registry import get_registry

def generate_from_specs(specs_dir, component_type):
    """Generate components from specifications in the given directory."""
    registry = get_registry()
    composer = registry.get_instance("AutoAgentComposerAgent")
    
    if not composer:
        print("AutoAgentComposerAgent not found in registry")
        return False
    
    # Get all JSON files in the specs directory
    specs_path = Path(specs_dir)
    spec_files = list(specs_path.glob("*.json"))
    
    if not spec_files:
        print(f"No specification files found in {specs_dir}")
        return False
    
    print(f"Found {len(spec_files)} specification files")
    
    # Generate each component
    for spec_file in spec_files:
        print(f"Generating from {spec_file}...")
        
        # Load the specification
        with open(spec_file, 'r') as f:
            spec = json.load(f)
        
        # Ensure the type is set correctly
        spec["type"] = component_type
        
        # Generate the component
        result = composer.run(spec)
        
        if result.get("success"):
            print(f"Generated {spec['name']} at {result.get('path')}")
        else:
            print(f"Failed to generate {spec['name']}: {result.get('error')}")
    
    return True

def main():
    """Main function."""
    print("Generating agents and tools using Agno...")
    
    # Generate agents
    print("\nGenerating agents...")
    generate_from_specs("specs/agents", "agent")
    
    # Generate tools
    print("\nGenerating tools...")
    generate_from_specs("specs/tools", "tool")
    
    print("\nGeneration complete!")

if __name__ == "__main__":
    main()