"""
Continuous learning agent for system improvement.
"""
from typing import Dict, Any, List
from tdev.core.agent import Agent as BaseAgent
from tdev.core.registry import get_registry

class LearningAgent(BaseAgent):
    """Agent that learns from feedback and improves system performance."""
    
    def __init__(self):
        super().__init__()
        self.feedback_history: List[Dict[str, Any]] = []
        self.performance_metrics: Dict[str, float] = {}
        self.registry = get_registry()
    
    def run(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze feedback and suggest improvements."""
        action = input_data.get("action", "analyze")
        
        if action == "analyze":
            return self._analyze_feedback()
        elif action == "improve":
            return self._suggest_improvements()
        elif action == "update_metrics":
            return self._update_performance_metrics(input_data.get("metrics", {}))
        else:
            return {"error": f"Unknown action: {action}"}
    
    def _analyze_feedback(self) -> Dict[str, Any]:
        """Analyze collected feedback for patterns."""
        if not self.feedback_history:
            return {"analysis": "No feedback data available"}
        
        # Simple analysis - count positive/negative feedback
        positive = sum(1 for f in self.feedback_history if f.get("rating", 0) >= 4)
        negative = sum(1 for f in self.feedback_history if f.get("rating", 0) <= 2)
        total = len(self.feedback_history)
        
        satisfaction_rate = positive / total if total > 0 else 0
        
        return {
            "total_feedback": total,
            "satisfaction_rate": satisfaction_rate,
            "positive_feedback": positive,
            "negative_feedback": negative,
            "recommendations": self._generate_recommendations(satisfaction_rate)
        }
    
    def _suggest_improvements(self) -> Dict[str, Any]:
        """Suggest system improvements based on analysis."""
        analysis = self._analyze_feedback()
        
        improvements = []
        if analysis["satisfaction_rate"] < 0.7:
            improvements.append("Consider retraining agents with low ratings")
        
        if analysis["negative_feedback"] > analysis["positive_feedback"]:
            improvements.append("Review agent prompts and improve response quality")
        
        return {
            "improvements": improvements,
            "priority": "high" if analysis["satisfaction_rate"] < 0.5 else "medium"
        }
    
    def _update_performance_metrics(self, metrics: Dict[str, float]) -> Dict[str, Any]:
        """Update performance metrics."""
        self.performance_metrics.update(metrics)
        return {"status": "metrics_updated", "metrics": self.performance_metrics}
    
    def _generate_recommendations(self, satisfaction_rate: float) -> List[str]:
        """Generate recommendations based on satisfaction rate."""
        if satisfaction_rate >= 0.8:
            return ["System performing well", "Consider expanding capabilities"]
        elif satisfaction_rate >= 0.6:
            return ["Minor improvements needed", "Focus on user experience"]
        else:
            return ["Major improvements required", "Review core functionality"]
    
    def add_feedback(self, feedback: Dict[str, Any]) -> None:
        """Add feedback to history."""
        self.feedback_history.append(feedback)
        
        # Keep only recent feedback (last 100 entries)
        if len(self.feedback_history) > 100:
            self.feedback_history = self.feedback_history[-100:]