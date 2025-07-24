"""Tests for echo_tool function."""
import unittest
from tdev.tools.echo_tool import echo_tool

class TestEchoTool(unittest.TestCase):
    """Test echo_tool functionality."""
    
    def test_echo_basic(self):
        """Test basic echo functionality."""
        result = echo_tool("Hello World")
        self.assertEqual(result, "Hello World")
    
    def test_echo_empty(self):
        """Test echo with empty input."""
        result = echo_tool("")
        self.assertEqual(result, "")
    
    def test_echo_none(self):
        """Test echo with None input."""
        result = echo_tool(None)
        self.assertIsNone(result)
    
    def test_echo_dict(self):
        """Test echo with dict input."""
        data = {"key": "value"}
        result = echo_tool(data)
        self.assertEqual(result, data)