import os
import ast
import re
from pathlib import Path
from tdev.core.agent import Agent

class ClassifierAgent(Agent):
    """
    Agent responsible for classifying components as Tool, Agent, or Team.
    
    The ClassifierAgent analyzes code to determine its type based on
    the number of decision points (brains) and coordination presence.
    """
    
    def run(self, target_file: str):
        """
        Classify a file.
        
        Args:
            target_file: The path to the file to classify
            
        Returns:
            A dictionary with classification results
        """
        print(f"ClassifierAgent: Classifying {target_file}")
        
        # Read the file content
        try:
            with open(target_file, 'r') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading file: {e}")
            return self._default_classification(target_file)
        
        # Extract the file name without extension
        file_name = Path(target_file).stem
        
        # Check if it's a team (inherits from Team)
        if self._is_team(content):
            return {
                "type": "team",
                "name": self._extract_name(file_name, content, "team"),
                "brain_count": 2,
                "reusability": "D"
            }
        
        # Check if it's a tool (has @tool decorator or no decision logic)
        elif self._is_tool(content):
            return {
                "type": "tool",
                "name": self._extract_name(file_name, content, "tool"),
                "brain_count": 0,
                "reusability": "A"
            }
        
        # Default to agent
        else:
            return {
                "type": "agent",
                "name": self._extract_name(file_name, content, "agent"),
                "brain_count": 1,
                "reusability": "B"
            }
    
    def _is_team(self, content):
        """Check if the content defines a Team."""
        # Check for Team import and inheritance
        has_import = ("from tdev.core.team import Team" in content or "import Team" in content)
        has_class = ("class" in content and "(Team)" in content)
        return has_import and has_class
    
    def _is_tool(self, content):
        """Check if the content defines a Tool."""
        # Check for @tool decorator
        return "@tool" in content
    
    def _extract_name(self, file_name, content, component_type):
        """Extract the component name from the content."""
        if component_type == "team":
            # Try to find class NameTeam(Team):
            match = re.search(r'class\s+([A-Za-z0-9_]+)Team\s*\(\s*Team\s*\)', content)
            if match:
                return match.group(1)
        elif component_type == "agent":
            # Try to find class NameAgent(Agent):
            match = re.search(r'class\s+([A-Za-z0-9_]+)Agent\s*\(\s*Agent\s*\)', content)
            if match:
                return match.group(1)
        elif component_type == "tool":
            # Try to find @tool\ndef name_tool
            match = re.search(r'@tool\s*\n\s*def\s+([A-Za-z0-9_]+)', content)
            if match:
                return match.group(1)
        
        # Default to file name
        return file_name
    
    def _default_classification(self, target_file):
        """Provide a default classification based on file path."""
        if "team" in target_file:
            return {
                "type": "team",
                "name": Path(target_file).stem,
                "brain_count": 2,
                "reusability": "D"
            }
        elif "tool" in target_file:
            return {
                "type": "tool",
                "name": Path(target_file).stem,
                "brain_count": 0,
                "reusability": "A"
            }
        else:
            return {
                "type": "agent",
                "name": Path(target_file).stem,
                "brain_count": 1,
                "reusability": "B"
            }