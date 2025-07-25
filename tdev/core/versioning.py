"""
Agent versioning and A/B testing support.
"""
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
import json

class VersionStatus(Enum):
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    EXPERIMENTAL = "experimental"

@dataclass
class AgentVersion:
    version: str
    status: VersionStatus
    metadata: Dict[str, Any]
    created_at: str
    performance_metrics: Dict[str, float] = None

class AgentVersionManager:
    """Manages multiple versions of agents for A/B testing."""
    
    def __init__(self):
        self.versions: Dict[str, List[AgentVersion]] = {}
    
    def add_version(self, agent_name: str, version: str, metadata: Dict[str, Any], 
                   status: VersionStatus = VersionStatus.EXPERIMENTAL) -> None:
        """Add a new version of an agent."""
        if agent_name not in self.versions:
            self.versions[agent_name] = []
        
        agent_version = AgentVersion(
            version=version,
            status=status,
            metadata=metadata,
            created_at=json.dumps({"timestamp": "now"}),
            performance_metrics={}
        )
        self.versions[agent_name].append(agent_version)
    
    def get_active_version(self, agent_name: str) -> Optional[AgentVersion]:
        """Get the active version of an agent."""
        if agent_name not in self.versions:
            return None
        
        for version in self.versions[agent_name]:
            if version.status == VersionStatus.ACTIVE:
                return version
        return None
    
    def promote_version(self, agent_name: str, version: str) -> bool:
        """Promote a version to active status."""
        if agent_name not in self.versions:
            return False
        
        # Demote current active version
        for v in self.versions[agent_name]:
            if v.status == VersionStatus.ACTIVE:
                v.status = VersionStatus.DEPRECATED
        
        # Promote new version
        for v in self.versions[agent_name]:
            if v.version == version:
                v.status = VersionStatus.ACTIVE
                return True
        return False
    
    def get_versions(self, agent_name: str) -> List[AgentVersion]:
        """Get all versions of an agent."""
        return self.versions.get(agent_name, [])

# Global version manager instance
version_manager = AgentVersionManager()