from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, field

# Type aliases for clarity
MetadataDict = Dict[str, Any]
SchemaDict = Dict[str, str]

@dataclass
class BaseMeta:
    """Base class for component metadata."""
    name: str
    type: str
    class_path: Optional[str] = None
    description: Optional[str] = None
    brain_count: int = 0
    reusability: str = "A"
    input_schema: Dict[str, str] = field(default_factory=dict)
    output_schema: Dict[str, str] = field(default_factory=dict)
    tags: List[str] = field(default_factory=list)
    path: Optional[str] = None
    
    def to_dict(self) -> MetadataDict:
        """Convert the metadata to a dictionary."""
        return {
            "name": self.name,
            "type": self.type,
            "class": self.class_path,
            "description": self.description,
            "brain_count": self.brain_count,
            "reusability": self.reusability,
            "input_schema": self.input_schema,
            "output_schema": self.output_schema,
            "tags": self.tags,
            "path": self.path,
        }

@dataclass
class TeamMeta(BaseMeta):
    """
    Metadata for a team.
    """
    type: str = "team"
    brain_count: int = 2
    reusability: str = "D"
    
    def __post_init__(self):
        """Set default description if not provided."""
        if not self.description:
            self.description = f"{self.name} team"
    
    @classmethod
    def from_dict(cls, data: MetadataDict) -> 'TeamMeta':
        """
        Create metadata from a dictionary.
        
        Args:
            data: The dictionary representation of the metadata
            
        Returns:
            A TeamMeta instance
        """
        return cls(
            name=data.get("name"),
            type=data.get("type", "team"),
            class_path=data.get("class"),
            description=data.get("description"),
            brain_count=data.get("brain_count", 2),
            reusability=data.get("reusability", "D"),
            input_schema=data.get("input_schema"),
            output_schema=data.get("output_schema"),
            tags=data.get("tags"),
            path=data.get("path"),
        )


@dataclass
class AgentMeta(BaseMeta):
    """
    Metadata for an agent.
    """
    type: str = "agent"
    brain_count: int = 1
    reusability: str = "B"
    
    def __post_init__(self):
        """Set default description if not provided."""
        if not self.description:
            self.description = f"{self.name} agent"
    
    @classmethod
    def from_dict(cls, data: MetadataDict) -> 'AgentMeta':
        """
        Create metadata from a dictionary.
        
        Args:
            data: The dictionary representation of the metadata
            
        Returns:
            An AgentMeta instance
        """
        return cls(
            name=data.get("name"),
            type=data.get("type", "agent"),
            class_path=data.get("class"),
            description=data.get("description"),
            brain_count=data.get("brain_count", 1),
            reusability=data.get("reusability", "B"),
            input_schema=data.get("input_schema"),
            output_schema=data.get("output_schema"),
            tags=data.get("tags"),
            path=data.get("path"),
        )


@dataclass
class ToolMeta(BaseMeta):
    """
    Metadata for a tool.
    """
    type: str = "tool"
    brain_count: int = 0
    reusability: str = "A"
    
    def __post_init__(self):
        """Set default description if not provided."""
        if not self.description:
            self.description = f"{self.name} tool"
    
    @classmethod
    def from_dict(cls, data: MetadataDict) -> 'ToolMeta':
        """
        Create metadata from a dictionary.
        
        Args:
            data: The dictionary representation of the metadata
            
        Returns:
            A ToolMeta instance
        """
        return cls(
            name=data.get("name"),
            type=data.get("type", "tool"),
            class_path=data.get("class"),
            description=data.get("description"),
            brain_count=data.get("brain_count", 0),
            reusability=data.get("reusability", "A"),
            input_schema=data.get("input_schema"),
            output_schema=data.get("output_schema"),
            tags=data.get("tags"),
            path=data.get("path"),
        )