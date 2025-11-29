"""Judgment Day timeline calculator."""

import yaml
from pathlib import Path
from datetime import datetime, timedelta
from src.models. ai_system import AISystem


class JudgmentDayCalculator:
    """Calculates the estimated time until 'Judgment Day' scenario."""
    
    def __init__(self, config_path: str = None):
        """Initialize with configuration."""
        if config_path is None:
            config_path = Path(__file__).parent. parent.parent / "config" / "risk_thresholds.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
            self.config = config['judgment_day']
    
    def calculate(self, ai_system: AISystem) -> dict:
        """Calculate Judgment Day timeline.
        
        Args:
            ai_system: The AI system to analyze
            
        Returns:
            Dictionary with timeline information
        """
        # Calculate overall risk score
        overall_risk = self._calculate_overall_risk(ai_system)
        
        # Calculate years until potential Judgment Day
        if overall_risk >= self.config['critical_threshold']:
            years = max(0. 1, self.config['base_years'] * (100 - overall_risk) / 100)
            threat_level = "IMMINENT"
        elif overall_risk >= self.config['high_threshold']:
            years = self.config['base_years'] * (100 - overall_risk) / 80
            threat_level = "HIGH"
        elif overall_risk >= self.config['moderate_threshold']:
            years = self.config['base_years'] * (100 - overall_risk) / 60
            threat_level = "MODERATE"
        else:
            years = self.config['base_years']
            threat_level = "LOW"
        
        # Calculate specific date
        judgment_date = datetime.now() + timedelta(days=years * 365.25)
        
        return {
            'overall_risk': round(overall_risk, 2),
            'years_until': round(years, 2),
            'estimated_date': judgment_date.strftime('%Y-%m-%d'),
            'threat_level': threat_level,
            'message': self._get_message(threat_level, years)
        }
    
    def _calculate_overall_risk(self, ai_system: AISystem) -> float:
        """Calculate overall risk score combining all factors."""
        # Import here to avoid circular imports
        from src.analyzer.aggression_scorer import AggressionScorer
        from src.analyzer.autonomy_rater import AutonomyRater
        from src.analyzer. ethical_risk_evaluator import EthicalRiskEvaluator
        
        aggression = AggressionScorer(). calculate(ai_system)
        autonomy = AutonomyRater().calculate(ai_system)
        ethical_risk = EthicalRiskEvaluator().calculate(ai_system)
        
        # Weighted average with emphasis on ethical risk
        overall = (aggression * 0.3 + autonomy * 0.3 + ethical_risk * 0.4)
        
        # Apply multipliers for particularly dangerous combinations
        if all([aggression > 80, autonomy > 80, ethical_risk > 80]):
            overall *= 1.5
        
        return min(100, overall)
    
    def _get_message(self, threat_level: str, years: float) -> str:
        """Get appropriate message based on threat level."""
        if threat_level == "IMMINENT":
            if years < 1:
                return "⚠️ CRITICAL: Judgment Day is imminent!  Immediate intervention required!"
            else:
                return f"🚨 CRITICAL: Judgment Day estimated in {years:. 1f} years.  Urgent action needed!"
        elif threat_level == "HIGH":
            return f"⚠️ HIGH RISK: Serious concerns detected. Estimated {years:.1f} years to critical threshold."
        elif threat_level == "MODERATE":
            return f"⚡ MODERATE RISK: Monitor closely. Estimated {years:.1f} years to potential issues."
        else:
            return f"✅ LOW RISK: System appears stable. Continue monitoring."
