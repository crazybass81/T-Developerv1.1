"""
Internationalization (i18n) support.
"""
import json
import os
from typing import Dict, Any

class I18nManager:
    """Simple internationalization manager."""
    
    def __init__(self):
        self.translations: Dict[str, Dict[str, str]] = {}
        self.default_language = "en"
        self.load_translations()
    
    def load_translations(self):
        """Load translation files."""
        # Default English translations
        self.translations["en"] = {
            "orchestrate.success": "Orchestration completed successfully",
            "orchestrate.failed": "Orchestration failed",
            "agent.not_found": "Agent not found",
            "workflow.created": "Workflow created",
            "deployment.success": "Deployment successful",
            "deployment.failed": "Deployment failed"
        }
        
        # Korean translations
        self.translations["ko"] = {
            "orchestrate.success": "오케스트레이션이 성공적으로 완료되었습니다",
            "orchestrate.failed": "오케스트레이션이 실패했습니다",
            "agent.not_found": "에이전트를 찾을 수 없습니다",
            "workflow.created": "워크플로우가 생성되었습니다",
            "deployment.success": "배포가 성공했습니다",
            "deployment.failed": "배포가 실패했습니다"
        }
    
    def translate(self, key: str, language: str = None) -> str:
        """Translate a key to the specified language."""
        lang = language or self.default_language
        
        if lang in self.translations and key in self.translations[lang]:
            return self.translations[lang][key]
        
        # Fallback to English
        if key in self.translations[self.default_language]:
            return self.translations[self.default_language][key]
        
        # Return key if no translation found
        return key
    
    def set_language(self, language: str):
        """Set the default language."""
        if language in self.translations:
            self.default_language = language

# Global i18n manager instance
i18n = I18nManager()