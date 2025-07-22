from typing import Dict, Any, List, Optional, Union

# Type aliases for clarity
MetadataDict = Dict[str, Any]
SchemaDict = Dict[str, str]

class AgentMeta:
    """
    Metadata for an agent.
    """
    
    def __init__(
        self,
        name: str,
        type: str = "agent",
        class_path: str = None,
        description: str = None,
        brain_count: int = 1,
        reusability: str = "B",
        input_schema: Optional[SchemaDict] = None,
        output_schema: Optional[SchemaDict] = None,
        tags: Optional[List[str]] = None,
        path: Optional[str] = None,
    ):
        """
        Initialize agent metadata.
        
        Args:
            name: The name of the agent
            type: The type of component ('agent')
            class_path: The import path to the agent class
            description: A description of the agent
            brain_count: The number of decision points (1 for agents)
            reusability: The reusability tier ('B' for agents)
            input_schema: Optional schema for input data
            output_schema: Optional schema for output data
            tags: Optional tags for categorization
            path: Optional path to the agent's code file
        """
        self.name = name
        self.type = type
        self.class_path = class_path
        self.description = description or f"{name} agent"
        self.brain_count = brain_count
        self.reusability = reusability
        self.input_schema = input_schema or {}
        self.output_schema = output_schema or {}
        self.tags = tags or []
        self.path = path
    
    def to_dict(self) -> MetadataDict:
        """
        Convert the metadata to a dictionary.
        
        Returns:
            A dictionary representation of the metadata
        """
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


class ToolMeta:
    """
    Metadata for a tool.
    """
    
    def __init__(
        self,
        name: str,
        type: str = "tool",
        class_path: str = None,
        description: str = None,
        brain_count: int = 0,
        reusability: str = "A",
        input_schema: Optional[SchemaDict] = None,
        output_schema: Optional[SchemaDict] = None,
        tags: Optional[List[str]] = None,
        path: Optional[str] = None,
    ):
        """
        Initialize tool metadata.
        
        Args:
            name: The name of the tool
            type: The type of component ('tool')
            class_path: The import path to the tool class or function
            description: A description of the tool
            brain_count: The number of decision points (0 for tools)
            reusability: The reusability tier ('A' for tools)
            input_schema: Optional schema for input data
            output_schema: Optional schema for output data
            tags: Optional tags for categorization
            path: Optional path to the tool's code file
        """
        self.name = name
        self.type = type
        self.class_path = class_path
        self.description = description or f"{name} tool"
        self.brain_count = brain_count
        self.reusability = reusability
        self.input_schema = input_schema or {}
        self.output_schema = output_schema or {}
        self.tags = tags or []
        self.path = path
    
    def to_dict(self) -> MetadataDict:
        """
        Convert the metadata to a dictionary.
        
        Returns:
            A dictionary representation of the metadata
        """
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