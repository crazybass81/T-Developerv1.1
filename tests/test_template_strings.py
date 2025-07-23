#!/usr/bin/env python3
"""
Test script to validate template strings in the codebase.

This script checks that template strings with placeholders can be properly
formatted without syntax errors.
"""
import sys
import os
import unittest

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tdev.agents.auto_agent_composer import AutoAgentComposer

class TemplateStringTest(unittest.TestCase):
    """Test case for template strings."""
    
    def test_agent_templates(self):
        """Test that agent templates can be formatted without errors."""
        composer = AutoAgentComposer()
        
        # Test simple agent template
        template = composer.templates["agent"]["simple"]
        try:
            formatted = template.format(
                name="Test",
                description="A test agent",
                input_desc="Test input",
                output_desc="Test output",
                implementation="result = input_data"
            )
            self.assertIn("class TestAgent", formatted)
            self.assertIn("A test agent", formatted)
        except Exception as e:
            self.fail(f"Simple agent template formatting failed: {e}")
        
        # Test tool wrapper template
        template = composer.templates["agent"]["tool_wrapper"]
        try:
            formatted = template.format(
                name="Test",
                description="A test agent",
                input_desc="Test input",
                output_desc="Test output",
                tool_name="TestTool"
            )
            self.assertIn("class TestAgent", formatted)
            self.assertIn("self.tool = self.registry.get_instance(\"TestTool\")", formatted)
        except Exception as e:
            self.fail(f"Tool wrapper template formatting failed: {e}")
    
    def test_tool_template(self):
        """Test that tool template can be formatted without errors."""
        composer = AutoAgentComposer()
        
        template = composer.templates["tool"]["simple"]
        try:
            formatted = template.format(
                name="Test",
                name_lower="test",
                description="A test tool",
                input_desc="Test input",
                output_desc="Test output",
                implementation="result = input_data"
            )
            self.assertIn("def test_tool", formatted)
            self.assertIn("A test tool", formatted)
        except Exception as e:
            self.fail(f"Tool template formatting failed: {e}")
    
    def test_test_code_generation(self):
        """Test that test code generation works without errors."""
        composer = AutoAgentComposer()
        
        # Mock the necessary methods
        composer._save_code = lambda *args: None
        composer._register_component = lambda *args: None
        
        # Test agent test generation
        try:
            test_path = composer._generate_tests(
                "agent", 
                "Test", 
                "A test agent", 
                "Test input", 
                "Test output"
            )
            self.assertTrue(os.path.exists(test_path))
            os.remove(test_path)  # Clean up
        except Exception as e:
            self.fail(f"Agent test generation failed: {e}")
        
        # Test tool test generation
        try:
            test_path = composer._generate_tests(
                "tool", 
                "Test", 
                "A test tool", 
                "Test input", 
                "Test output"
            )
            self.assertTrue(os.path.exists(test_path))
            os.remove(test_path)  # Clean up
        except Exception as e:
            self.fail(f"Tool test generation failed: {e}")

if __name__ == "__main__":
    unittest.main()