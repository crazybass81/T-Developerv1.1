#!/usr/bin/env python3
"""
Script to test template strings in the codebase.

This script is designed to be run in CI to ensure that all template strings
in the codebase are valid and can be formatted without errors.
"""
import sys
import os
import unittest
import importlib
import inspect
import re
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def find_template_strings(module_path):
    """Find all template strings in a module."""
    templates = []
    
    try:
        # Import the module
        spec = importlib.util.spec_from_file_location("module", module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Find all classes in the module
        for name, obj in inspect.getmembers(module):
            if inspect.isclass(obj):
                # Check if the class has a templates attribute
                if hasattr(obj, 'templates'):
                    templates.append((name, obj.templates))
                
                # Check for template strings in methods
                for method_name, method in inspect.getmembers(obj, inspect.isfunction):
                    source = inspect.getsource(method)
                    # Look for f-strings with triple quotes
                    if re.search(r'f[\'\"]{3}', source):
                        templates.append((f"{name}.{method_name}", "f-string template found"))
    except Exception as e:
        print(f"Error processing {module_path}: {e}")
    
    return templates

def find_all_template_strings():
    """Find all template strings in the codebase."""
    templates = []
    
    # Walk through the tdev directory
    for root, _, files in os.walk("tdev"):
        for file in files:
            if file.endswith(".py"):
                module_path = os.path.join(root, file)
                module_templates = find_template_strings(module_path)
                if module_templates:
                    templates.append((module_path, module_templates))
    
    return templates

def main():
    """Main function."""
    print("Checking template strings in the codebase...")
    templates = find_all_template_strings()
    
    if not templates:
        print("No template strings found.")
        return 0
    
    print(f"Found template strings in {len(templates)} modules:")
    for module_path, module_templates in templates:
        print(f"  {module_path}:")
        for name, template in module_templates:
            print(f"    {name}")
    
    # Run the template string tests
    print("\nRunning template string tests...")
    test_result = unittest.TextTestRunner().run(
        unittest.defaultTestLoader.loadTestsFromName("tests.test_template_strings")
    )
    
    if test_result.wasSuccessful():
        print("All template string tests passed!")
        return 0
    else:
        print("Template string tests failed!")
        return 1

if __name__ == "__main__":
    sys.exit(main())