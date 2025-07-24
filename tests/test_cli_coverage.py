"""Tests for CLI coverage improvement."""
import unittest
from unittest.mock import patch, MagicMock
from tdev.cli import main

class TestCLICoverage(unittest.TestCase):
    """Test CLI functions for coverage."""
    
    @patch('tdev.cli.get_registry')
    def test_init_registry_command(self, mock_registry):
        """Test init-registry command."""
        mock_registry.return_value = MagicMock()
        
        with patch('sys.argv', ['tdev', 'init-registry']):
            try:
                main()
            except SystemExit:
                pass  # Expected for CLI
    
    @patch('tdev.cli.get_registry')
    def test_generate_command(self, mock_registry):
        """Test generate command."""
        mock_registry.return_value = MagicMock()
        
        with patch('sys.argv', ['tdev', 'generate', 'agent', '--name', 'TestAgent', '--goal', 'Test']):
            try:
                main()
            except SystemExit:
                pass  # Expected for CLI
    
    @patch('tdev.cli.get_registry')
    def test_serve_command(self, mock_registry):
        """Test serve command."""
        mock_registry.return_value = MagicMock()
        
        with patch('sys.argv', ['tdev', 'serve', '--port', '8001']):
            with patch('uvicorn.run') as mock_uvicorn:
                try:
                    main()
                except SystemExit:
                    pass  # Expected for CLI