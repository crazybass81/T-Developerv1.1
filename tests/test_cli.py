"""
Tests for CLI module.
"""
import pytest
from unittest.mock import MagicMock, patch
from click.testing import CliRunner
from tdev.cli import main, classify, register

class TestCLI:
    """Test the CLI commands."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.runner = CliRunner()
        self.mock_registry = MagicMock()
    
    def test_main_help(self):
        """Test main command help."""
        result = self.runner.invoke(main, ['--help'])
        assert result.exit_code == 0
        assert 'T-Developer CLI' in result.output
    
    @patch('tdev.cli.get_registry')
    def test_classify_command(self, mock_get_registry):
        """Test classify command."""
        mock_get_registry.return_value = self.mock_registry
        mock_agent = MagicMock()
        mock_agent.run.return_value = {"type": "agent", "name": "TestAgent"}
        self.mock_registry.get_instance.return_value = mock_agent
        
        with self.runner.isolated_filesystem():
            with open('test_file.py', 'w') as f:
                f.write('def test(): pass')
            
            result = self.runner.invoke(classify, ['test_file.py'])
            assert result.exit_code == 0
    
    @patch('tdev.cli.get_registry')
    def test_register_command(self, mock_get_registry):
        """Test register command."""
        mock_get_registry.return_value = self.mock_registry
        mock_agent = MagicMock()
        mock_agent.run.return_value = {"type": "agent", "name": "TestAgent"}
        self.mock_registry.get_instance.return_value = mock_agent
        
        with self.runner.isolated_filesystem():
            with open('test_file.py', 'w') as f:
                f.write('class TestAgent: pass')
            
            result = self.runner.invoke(register, ['test_file.py'])
            assert result.exit_code == 0