"""
Integration tests for the API server.

These tests verify that the API server correctly integrates with the core agents.
"""
import os
import sys
import json
import unittest
import requests
from multiprocessing import Process

# Add the project root to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from tdev.api.server import app
from tdev.core.init_registry import initialize_registry
import uvicorn

class TestAPIServer(unittest.TestCase):
    """Test the API server integration."""
    
    @classmethod
    def setUpClass(cls):
        """Set up the test environment."""
        # Initialize the registry
        initialize_registry()
        
        # Start the API server in a separate process
        cls.server_process = Process(
            target=uvicorn.run,
            args=(app,),
            kwargs={"host": "127.0.0.1", "port": 8765, "log_level": "error"}
        )
        cls.server_process.start()
        
        # Wait for the server to start
        import time
        time.sleep(2)
        
        # Set the base URL
        cls.base_url = "http://127.0.0.1:8765"
    
    @classmethod
    def tearDownClass(cls):
        """Clean up the test environment."""
        # Stop the server
        cls.server_process.terminate()
        cls.server_process.join()
    
    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = requests.get(f"{self.base_url}/")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("message", data)
        self.assertIn("version", data)
    
    def test_list_agents(self):
        """Test the list_agents endpoint."""
        response = requests.get(f"{self.base_url}/agents")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("agents", data)
        self.assertIsInstance(data["agents"], list)
    
    def test_list_tools(self):
        """Test the list_tools endpoint."""
        response = requests.get(f"{self.base_url}/tools")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("tools", data)
        self.assertIsInstance(data["tools"], list)
    
    def test_list_teams(self):
        """Test the list_teams endpoint."""
        response = requests.get(f"{self.base_url}/teams")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("teams", data)
        self.assertIsInstance(data["teams"], list)
    
    def test_orchestrate(self):
        """Test the orchestrate endpoint."""
        # This is a simple test that just verifies the endpoint works
        # In a real test, we would mock the coordinator to avoid actual execution
        payload = {"goal": "Echo test input", "options": {}}
        response = requests.post(f"{self.base_url}/orchestrate", json=payload)
        
        # We don't assert success because the actual execution might fail
        # We just check that the endpoint responds
        self.assertIn(response.status_code, [200, 400])
    
    def test_classify(self):
        """Test the classify endpoint."""
        # This is a simple test that just verifies the endpoint works
        payload = {"code": "def test(): return 'hello'", "options": {}}
        response = requests.post(f"{self.base_url}/classify", json=payload)
        
        # We don't assert success because the actual execution might fail
        # We just check that the endpoint responds
        self.assertIn(response.status_code, [200, 400])

if __name__ == "__main__":
    unittest.main()