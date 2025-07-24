#!/usr/bin/env python3
"""
Phase 4 Stabilization Fixes
Quick fixes for critical issues preventing Phase 4 entry
"""

import os
import subprocess
import sys
from pathlib import Path

def run_command(cmd, description):
    """Run a command and report results"""
    print(f"🔧 {description}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Success: {description}")
            return True
        else:
            print(f"❌ Failed: {description}")
            print(f"Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Exception: {description} - {e}")
        return False

def fix_pydantic_compatibility():
    """Fix Pydantic v2 compatibility issues"""
    print("\n📦 Fixing Pydantic v2 compatibility...")
    
    # Find and replace .model_dump() with .model_dump()
    cmd = "find . -name '*.py' -not -path './venv/*' -not -path './.venv/*' -exec sed -i 's/\\.model_dump()/\\.model_dump()/g' {} \\;"
    return run_command(cmd, "Replace .model_dump() with .model_dump()")

def install_missing_dependencies():
    """Install missing test dependencies"""
    print("\n📦 Installing missing dependencies...")
    
    dependencies = [
        "pytest-asyncio",
        "httpx",  # For FastAPI TestClient
    ]
    
    success = True
    for dep in dependencies:
        if not run_command(f"pip install {dep}", f"Install {dep}"):
            success = False
    
    return success

def create_aws_mock_fixture():
    """Create AWS mocking fixture for tests"""
    print("\n🔧 Creating AWS mock fixture...")
    
    conftest_content = '''"""
Test configuration and fixtures
"""
import pytest
from unittest.mock import patch, MagicMock

@pytest.fixture(autouse=True)
def mock_aws_services():
    """Mock AWS services to prevent actual API calls during testing"""
    with patch('boto3.client') as mock_client:
        # Mock Bedrock client
        mock_bedrock = MagicMock()
        mock_bedrock.invoke_model.return_value = {
            'body': MagicMock(read=lambda: b'{"completion": "mocked response"}')
        }
        
        # Mock Lambda client
        mock_lambda = MagicMock()
        mock_lambda.create_function.return_value = {'FunctionArn': 'arn:aws:lambda:us-east-1:123456789012:function:test'}
        
        # Configure mock client to return appropriate service mocks
        def client_side_effect(service_name, **kwargs):
            if service_name == 'bedrock-runtime':
                return mock_bedrock
            elif service_name == 'lambda':
                return mock_lambda
            else:
                return MagicMock()
        
        mock_client.side_effect = client_side_effect
        yield mock_client

@pytest.fixture
def mock_bedrock_client():
    """Specific Bedrock client mock"""
    with patch('tdev.agent_core.bedrock_client.BedrockClient') as mock:
        mock_instance = MagicMock()
        mock_instance.invoke_model.return_value = "Mocked AI response"
        mock.return_value = mock_instance
        yield mock_instance
'''
    
    conftest_path = Path("tests/conftest.py")
    try:
        with open(conftest_path, 'w') as f:
            f.write(conftest_content)
        print("✅ Created AWS mock fixture in tests/conftest.py")
        return True
    except Exception as e:
        print(f"❌ Failed to create conftest.py: {e}")
        return False

def fix_api_test_client():
    """Fix API test client initialization"""
    print("\n🔧 Fixing API test client...")
    
    # Read the current test file
    test_file = Path("tests/api/test_server.py")
    if not test_file.exists():
        print("❌ API test file not found")
        return False
    
    try:
        with open(test_file, 'r') as f:
            content = f.read()
        
        # Replace TestClient import and usage
        content = content.replace(
            "from starlette.testclient import TestClient",
            "from fastapi.testclient import TestClient"
        )
        
        # Fix TestClient initialization
        content = content.replace(
            "self.client = TestClient(app)",
            "self.client = TestClient(app)"
        )
        
        with open(test_file, 'w') as f:
            f.write(content)
        
        print("✅ Fixed API test client initialization")
        return True
    except Exception as e:
        print(f"❌ Failed to fix API test client: {e}")
        return False

def run_test_validation():
    """Run tests to validate fixes"""
    print("\n🧪 Running test validation...")
    
    # Run a subset of tests to check fixes
    test_commands = [
        ("python3 -m pytest tests/test_registry.py -v", "Registry tests"),
        ("python3 -m pytest tests/test_classifier_agent.py -v", "Classifier agent tests"),
        ("python3 -m pytest tests/api/test_server_simple.py::TestAPIServerSimple::test_list_agents -v", "Simple API test"),
    ]
    
    success_count = 0
    for cmd, desc in test_commands:
        if run_command(cmd, desc):
            success_count += 1
    
    print(f"\n📊 Test validation: {success_count}/{len(test_commands)} test suites passing")
    return success_count == len(test_commands)

def main():
    """Main stabilization script"""
    print("🚀 T-Developer v1.1 Phase 4 Stabilization Fixes")
    print("=" * 50)
    
    fixes = [
        ("Install missing dependencies", install_missing_dependencies),
        ("Fix Pydantic compatibility", fix_pydantic_compatibility),
        ("Create AWS mock fixture", create_aws_mock_fixture),
        ("Fix API test client", fix_api_test_client),
    ]
    
    success_count = 0
    for desc, fix_func in fixes:
        print(f"\n🔧 {desc}")
        if fix_func():
            success_count += 1
        else:
            print(f"❌ Failed: {desc}")
    
    print(f"\n📊 Fixes applied: {success_count}/{len(fixes)}")
    
    # Run validation
    print("\n" + "=" * 50)
    if run_test_validation():
        print("\n✅ Stabilization fixes successful!")
        print("🎯 Ready to re-evaluate Phase 4 entry criteria")
    else:
        print("\n⚠️ Some issues remain - manual intervention may be needed")
        print("📋 Check test output for specific failures")
    
    return success_count == len(fixes)

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)