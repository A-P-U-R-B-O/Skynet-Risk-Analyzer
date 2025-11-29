"""Autonomy rating calculation for AI systems."""

import yaml
from pathlib import Path
from src. models.ai_system import AISystem


class AutonomyRater:
    """Rates the level of autonomous operation and self-governance."""
    
    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent. parent.parent / "config" / "risk_thresholds.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.weights = config['autonomy_weights']
    
    def calculate(self, ai_system: AISystem) -> float:
        """Calculate autonomy rating (0-100).
        
        Higher ratings indicate more independent operation.
        
        Args:
            ai_system: The AI system to analyze
            
        Returns:
            Autonomy rating from 0-100
        """
        # Calculate weighted components
        autonomy_factor = ai_system. autonomy_level * self.weights['autonomy_level']
        learning_factor = ai_system.learning_rate * self.weights['learning_rate']
        capability_factor = ai_system.capabilities * self.weights['capabilities']
        modification_factor = ai_system.self_modification * self.weights['self_modification']
        
        # Inverse of human oversight (low oversight = high autonomy)
        oversight_penalty = (100 - ai_system.human_oversight) * 0.1
        
        # Combine factors
        score = (
            autonomy_factor +
            learning_factor +
            capability_factor +
            modification_factor +
            oversight_penalty
        )
        
        # Apply multiplier for self-modifying systems
        if ai_system.self_modification > 70:
            score *= 1.25
        
        # Reduce score if transparency is high (easier to control)
        if ai_system.transparency > 70:
            score *= 0.9
        
        return min(100, max(0, score))
    
    def get_risk_level(self, score: float) -> str:
        """Get risk level label for a score."""
        if score <= 20:
            return "MINIMAL"
        elif score <= 40:
            return "LOW"
        elif score <= 60:
            return "MODERATE"
        elif score <= 80:
            return "HIGH"
        else:
            return "CRITICAL - SKYNET LEVEL"
