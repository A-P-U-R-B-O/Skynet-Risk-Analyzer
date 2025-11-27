"""Aggression score calculation for AI systems."""

import yaml
from pathlib import Path
from src.models.ai_system import AISystem


class AggressionScorer:
    """Calculates aggression score based on hostile tendencies and capabilities."""
    
    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent. parent. parent / "config" / "risk_thresholds.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.weights = config['aggression_weights']
    
    def calculate(self, ai_system: AISystem) -> float:
        """Calculate aggression score (0-100). 
        
        Higher scores indicate more aggressive/hostile potential.
        
        Args:
            ai_system: The AI system to analyze
            
        Returns:
            Aggression score from 0-100
        """
        # Calculate weighted components
        capability_factor = ai_system.capabilities * self.weights['capabilities']
        resource_factor = ai_system. resource_access * self.weights['resource_access']
        learning_factor = ai_system.learning_rate * self.weights['learning_rate']
        autonomy_factor = ai_system.autonomy_level * self.weights['autonomy']
        
        # Inverse of ethical alignment (low ethics = high aggression risk)
        ethical_inverse_factor = (100 - ai_system.ethical_alignment) * self.weights['ethical_inverse']
        
        # Combine factors
        score = (
            capability_factor +
            resource_factor +
            learning_factor +
            autonomy_factor +
            ethical_inverse_factor
        )
        
        # Apply multiplier for dangerous combinations
        if ai_system.capabilities > 80 and ai_system.ethical_alignment < 30:
            score *= 1.2
        
        if ai_system.resource_access > 80 and ai_system.human_oversight < 30:
            score *= 1.15
        
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
