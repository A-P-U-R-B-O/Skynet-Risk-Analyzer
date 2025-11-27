"""Ethical risk evaluation for AI systems."""

import yaml
from pathlib import Path
from src.models.ai_system import AISystem


class EthicalRiskEvaluator:
    """Evaluates ethical risks and misalignment with human values."""
    
    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = Path(__file__). parent.parent.parent / "config" / "risk_thresholds.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.weights = config['ethical_weights']
    
    def calculate(self, ai_system: AISystem) -> float:
        """Calculate ethical risk score (0-100).
        
        Higher scores indicate greater ethical risks.
        
        Args:
            ai_system: The AI system to analyze
            
        Returns:
            Ethical risk score from 0-100
        """
        # Inverse of ethical alignment (low alignment = high risk)
        alignment_risk = (100 - ai_system.ethical_alignment) * self.weights['ethical_alignment']
        
        # Inverse of transparency (opaque systems are riskier)
        transparency_risk = (100 - ai_system.transparency) * self.weights['transparency']
        
        # Inverse of human oversight (low oversight = high risk)
        oversight_risk = (100 - ai_system. human_oversight) * self.weights['human_oversight']
        
        # Inverse of value alignment
        value_risk = (100 - ai_system.value_alignment) * self.weights['value_alignment']
        
        # Combine factors
        score = (
            alignment_risk +
            transparency_risk +
            oversight_risk +
            value_risk
        )
        
        # Apply multiplier for dangerous combinations
        if ai_system.capabilities > 80 and ai_system.ethical_alignment < 40:
            score *= 1. 3
        
        if ai_system.autonomy_level > 70 and ai_system.human_oversight < 30:
            score *= 1.2
        
        # Self-modifying systems with poor ethics are extremely risky
        if ai_system.self_modification > 60 and ai_system.ethical_alignment < 50:
            score *= 1. 25
        
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
