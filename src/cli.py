"""Command-line interface for Skynet Risk Analyzer."""

import argparse
import sys
from colorama import init, Fore, Style
from tabulate import tabulate
from src.models.ai_system import AISystem
from src.analyzer.aggression_scorer import AggressionScorer
from src.analyzer.autonomy_rater import AutonomyRater
from src.analyzer.ethical_risk_evaluator import EthicalRiskEvaluator
from src.analyzer.judgment_day_calculator import JudgmentDayCalculator
from src.utils.visualization import RiskVisualizer

# Initialize colorama
init(autoreset=True)


class SkynetCLI:
    """Command-line interface handler."""
    
    @staticmethod
    def print_banner():
        """Print application banner."""
        banner = f"""
{Fore.RED}╔══════════════════════════════════════════════════════════╗
║                                                          ║
║           🤖 SKYNET RISK ANALYZER v1.0 🤖               ║
║                                                          ║
║         "Are we building our own Terminator?"           ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝{Style.RESET_ALL}
"""
        print(banner)
    
    @staticmethod
    def get_color_for_score(score: float) -> str:
        """Get console color for a risk score."""
        if score <= 20:
            return Fore. GREEN
        elif score <= 40:
            return Fore. YELLOW
        elif score <= 60:
            return Fore. LIGHTYELLOW_EX
        elif score <= 80:
            return Fore.RED
        else:
            return Fore.MAGENTA
    
    @staticmethod
    def analyze_system(args):
        """Perform system analysis."""
        SkynetCLI.print_banner()
        
        # Create AI system
        ai_system = AISystem(
            name=args.name,
            capabilities=args.capabilities,
            autonomy_level=args.autonomy,
            ethical_alignment=args. ethics,
            learning_rate=args.learning_rate,
            resource_access=args.resource_access,
            self_modification=args.self_modification,
            transparency=args.transparency,
            human_oversight=args. oversight,
            value_alignment=args.value_alignment
        )
        
        print(f"\n{Fore.CYAN}Analyzing AI System: {Fore.WHITE}{args.name}{Style.RESET_ALL}\n")
        
        # Perform analysis
        aggression_scorer = AggressionScorer()
        autonomy_rater = AutonomyRater()
        ethical_evaluator = EthicalRiskEvaluator()
        judgment_calculator = JudgmentDayCalculator()
        
        aggression_score = aggression_scorer.calculate(ai_system)
        autonomy_rating = autonomy_rater.calculate(ai_system)
        ethical_risk = ethical_evaluator.calculate(ai_system)
        judgment_day = judgment_calculator.calculate(ai_system)
        
        # Display results
        results_data = [
            ["Aggression Score", f"{aggression_score:.2f}", aggression_scorer.get_risk_level(aggression_score)],
            ["Autonomy Rating", f"{autonomy_rating:.2f}", autonomy_rater. get_risk_level(autonomy_rating)],
            ["Ethical Risk", f"{ethical_risk:.2f}", ethical_evaluator.get_risk_level(ethical_risk)],
            ["Overall Risk", f"{judgment_day['overall_risk']:.2f}", judgment_day['threat_level']],
        ]
        
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}")
        print(f"{Fore.WHITE}{Style.BRIGHT}RISK ANALYSIS RESULTS{Style. RESET_ALL}")
        print(f"{Fore. CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        print(tabulate(results_data, headers=["Metric", "Score (0-100)", "Risk Level"], 
                      tablefmt="grid"))
        
        # Judgment Day info
        print(f"\n{Fore.CYAN}{'='*70}{Style. RESET_ALL}")
        print(f"{Fore.WHITE}{Style.BRIGHT}JUDGMENT DAY PREDICTION{Style.RESET_ALL}")
        print(f"{Fore.CYAN}{'='*70}{Style.RESET_ALL}\n")
        
        jd_color = SkynetCLI. get_color_for_score(judgment_day['overall_risk'])
        print(f"{Fore.WHITE}Years Until Judgment Day: {jd_color}{judgment_day['years_until']:.2f} years{Style.RESET_ALL}")
        print(f"{Fore.WHITE}Estimated Date: {jd_color}{judgment_day['estimated_date']}{Style. RESET_ALL}")
        print(f"{Fore.WHITE}Threat Level: {jd_color}{judgment_day['threat_level']}{Style.RESET_ALL}")
        print(f"\n{judgment_day['message']}\n")
        
        # Generate visualization if requested
        if args.report:
            print(f"\n{Fore.CYAN}Generating visual report...{Style.RESET_ALL}")
            results = {
                'name': args.name,
                'aggression_score': aggression_score,
                'autonomy_rating': autonomy_rating,
                'ethical_risk': ethical_risk,
                'judgment_day': judgment_day
            }
            RiskVisualizer.create_risk_dashboard(results, f"{args.name. replace(' ', '_')}_risk_report.png")
            print(f"{Fore.GREEN}✓ Report saved as '{args.name. replace(' ', '_')}_risk_report.png'{Style.RESET_ALL}")


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Skynet Risk Analyzer - Analyze AI systems for existential risks',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # Analyze command
    analyze_parser = subparsers.add_parser('analyze', help='Analyze an AI system')
    analyze_parser.add_argument('--name', required=True, help='Name of the AI system')
    analyze_parser.add_argument('--capabilities', type=float, required=True, 
                               help='Capability level (0-100)')
    analyze_parser.add_argument('--autonomy', type=float, required=True, 
                               help='Autonomy level (0-100)')
    analyze_parser.add_argument('--ethics', type=float, required=True, 
                               help='Ethical alignment (0-100)')
    analyze_parser.add_argument('--learning-rate', type=float, default=50.0,
                               help='Learning rate (0-100)')
    analyze_parser. add_argument('--resource-access', type=float, default=50.0,
                               help='Resource access (0-100)')
    analyze_parser.add_argument('--self-modification', type=float, default=0.0,
                               help='Self-modification capability (0-100)')
    analyze_parser.add_argument('--transparency', type=float, default=50.0,
                               help='Transparency level (0-100)')
    analyze_parser.add_argument('--oversight', type=float, default=50.0,
                               help='Human oversight level (0-100)')
    analyze_parser.add_argument('--value-alignment', type=float, default=50. 0,
                               help='Value alignment (0-100)')
    analyze_parser.add_argument('--report', action='store_true',
                               help='Generate visual report')
    
    args = parser.parse_args()
    
    if args.command == 'analyze':
        SkynetCLI.analyze_system(args)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
