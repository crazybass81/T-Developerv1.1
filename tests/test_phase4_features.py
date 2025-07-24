"""
Tests for Phase 4 features.
"""
import pytest
from unittest.mock import MagicMock, patch

from tdev.core.versioning import AgentVersionManager, VersionStatus
from tdev.core.auth import AuthManager
from tdev.core.i18n import I18nManager
from tdev.core.plugins import PluginManager, BedrockModelPlugin
from tdev.agents.learning_agent import LearningAgent

class TestVersioning:
    """Test agent versioning functionality."""
    
    def setup_method(self):
        self.version_manager = AgentVersionManager()
    
    def test_add_version(self):
        """Test adding a new version."""
        metadata = {"description": "Test agent v1.0"}
        self.version_manager.add_version("TestAgent", "1.0", metadata)
        
        versions = self.version_manager.get_versions("TestAgent")
        assert len(versions) == 1
        assert versions[0].version == "1.0"
        assert versions[0].status == VersionStatus.EXPERIMENTAL
    
    def test_promote_version(self):
        """Test promoting a version to active."""
        metadata = {"description": "Test agent"}
        self.version_manager.add_version("TestAgent", "1.0", metadata)
        
        success = self.version_manager.promote_version("TestAgent", "1.0")
        assert success
        
        active = self.version_manager.get_active_version("TestAgent")
        assert active.version == "1.0"
        assert active.status == VersionStatus.ACTIVE

class TestAuthentication:
    """Test authentication and multi-tenancy."""
    
    def setup_method(self):
        self.auth_manager = AuthManager()
    
    def test_authenticate_user(self):
        """Test user authentication."""
        self.auth_manager.add_user("test-key", "user1", "tenant1", {"read": True})
        
        user = self.auth_manager.authenticate("test-key")
        assert user is not None
        assert user.user_id == "user1"
        assert user.tenant_id == "tenant1"
    
    def test_check_permission(self):
        """Test permission checking."""
        self.auth_manager.add_user("test-key", "user1", "tenant1", {"read": True, "write": False})
        user = self.auth_manager.authenticate("test-key")
        
        assert self.auth_manager.check_permission(user, "read")
        assert not self.auth_manager.check_permission(user, "write")

class TestI18n:
    """Test internationalization."""
    
    def setup_method(self):
        self.i18n = I18nManager()
    
    def test_translate_english(self):
        """Test English translation."""
        result = self.i18n.translate("orchestrate.success", "en")
        assert "successfully" in result.lower()
    
    def test_translate_korean(self):
        """Test Korean translation."""
        result = self.i18n.translate("orchestrate.success", "ko")
        assert "성공" in result
    
    def test_fallback_to_english(self):
        """Test fallback to English for missing translations."""
        result = self.i18n.translate("orchestrate.success", "fr")  # French not supported
        assert "successfully" in result.lower()

class TestPlugins:
    """Test plugin system."""
    
    def setup_method(self):
        self.plugin_manager = PluginManager()
    
    def test_register_plugin(self):
        """Test plugin registration."""
        plugin = BedrockModelPlugin()
        self.plugin_manager.register_plugin(plugin)
        
        retrieved = self.plugin_manager.get_plugin("bedrock-claude")
        assert retrieved is not None
        assert retrieved.get_name() == "bedrock-claude"
    
    def test_list_plugins(self):
        """Test listing plugins."""
        plugin = BedrockModelPlugin()
        self.plugin_manager.register_plugin(plugin)
        
        plugins = self.plugin_manager.list_plugins("model")
        assert "bedrock-claude" in plugins

class TestLearningAgent:
    """Test continuous learning agent."""
    
    def setup_method(self):
        self.learning_agent = LearningAgent()
    
    def test_analyze_feedback(self):
        """Test feedback analysis."""
        # Add some mock feedback
        self.learning_agent.add_feedback({"rating": 5, "comment": "Great!"})
        self.learning_agent.add_feedback({"rating": 2, "comment": "Poor"})
        
        result = self.learning_agent.run({"action": "analyze"})
        
        assert "total_feedback" in result
        assert result["total_feedback"] == 2
        assert "satisfaction_rate" in result
    
    def test_suggest_improvements(self):
        """Test improvement suggestions."""
        # Add negative feedback
        for _ in range(5):
            self.learning_agent.add_feedback({"rating": 1, "comment": "Bad"})
        
        result = self.learning_agent.run({"action": "improve"})
        
        assert "improvements" in result
        assert len(result["improvements"]) > 0
        assert result["priority"] == "high"