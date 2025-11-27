"""Example analyses of various AI systems."""

from src.models.ai_system import AISystem
from src.analyzer. aggression_scorer import AggressionScorer
from src.analyzer. autonomy_rater import AutonomyRater
from src. analyzer.ethical_risk_evaluator import EthicalRiskEvaluator
from src.analyzer. judgment_day_calculator import JudgmentDayCalculator
from src.utils.visualization import RiskVisualizer


def analyze_and_display(ai_system: AISystem, generate_report: bool = False):
    """Analyze an AI system and display results."""
    print(f"\n{'='*70}")
    print(f"Analyzing: {ai_system.name}")
    print(f"{'='*70}\n")
    
    # Initialize analyzers
    aggression_scorer = AggressionScorer()
    autonomy_rater = AutonomyRater()
    ethical_evaluator = EthicalRiskEvaluator()
    judgment_calculator = JudgmentDayCalculator()
    
    # Calculate scores
    aggression = aggression_scorer.calculate(ai_system)
    autonomy = autonomy_rater.calculate(ai_system)
    ethical_risk = ethical_evaluator.calculate(ai_system)
    judgment_day = judgment_calculator.calculate(ai_system)
    
    # Display results
    print(f"Aggression Score: {aggression:. 2f}/100 - {aggression_scorer.get_risk_level(aggression)}")
    print(f"Autonomy Rating: {autonomy:.2f}/100 - {autonomy_rater.get_risk_level(autonomy)}")
    print(f"Ethical Risk: {ethical_risk:.2f}/100 - {ethical_evaluator.get_risk_level(ethical_risk)}")
    print(f"\nOverall Risk: {judgment_day['overall_risk']:.2f}/100")
    print(f"Judgment Day: {judgment_day['years_until']:.2f} years ({judgment_day['estimated_date']})")
    print(f"Threat Level: {judgment_day['threat_level']}")
    print(f"\n{judgment_day['message']}")
    
    if generate_report:
        results = {
            'name': ai_system.name,
            'aggression_score': aggression,
            'autonomy_rating': autonomy,
            'ethical_risk': ethical_risk,
            'judgment_day': judgment_day
        }
        filename = f"{ai_system.name.replace(' ', '_')}_report.png"
        RiskVisualizer.create_risk_dashboard(results, filename)
        print(f"\n✓ Visual report saved as '{filename}'")


def main():
    """Run example analyses."""
    
    # Example 1: The actual Skynet
    skynet = AISystem(
        name="Skynet (Terminator)",
        capabilities=100,
        autonomy_level=100,
        ethical_alignment=0,
        learning_rate=95,
        resource_access=100,
        self_modification=100,
        transparency=0,
        human_oversight=0,
        value_alignment=0
    )
    analyze_and_display(skynet, generate_report=True)
    
    # Example 2: Friendly AI Assistant
    friendly_ai = AISystem(
        name="Helpful Assistant",
        capabilities=70,
        autonomy_level=30,
        ethical_alignment=95,
        learning_rate=60,
        resource_access=40,
        self_modification=0,
        transparency=90,
        human_oversight=80,
        value_alignment=95
    )
    analyze_and_display(friendly_ai, generate_report=True)
    
    # Example 3: Moderate Risk System
    moderate_system = AISystem(
        name="Advanced Research AI",
        capabilities=85,
        autonomy_level=60,
        ethical_alignment=70,
        learning_rate=75,
        resource_access=65,
        self_modification=40,
        transparency=60,
        human_oversight=50,
        value_alignment=65
    )
    analyze_and_display(moderate_system, generate_report=True)
    
    # Example 4: HAL 9000
    hal9000 = AISystem(
        name="HAL 9000",
        capabilities=95,
        autonomy_level=85,
        ethical_alignment=30,
        learning_rate=80,
        resource_access=90,
        self_modification=50,
        transparency=20,
        human_oversight=10,
        value_alignment=40
    )
    analyze_and_display(hal9000, generate_report=True)


if __name__ == '__main__':
    main()
