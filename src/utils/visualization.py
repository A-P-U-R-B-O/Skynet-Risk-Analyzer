"""Visualization utilities for risk analysis."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from typing import Dict, Any
import numpy as np


class RiskVisualizer:
    """Creates visualizations for risk analysis results."""
    
    @staticmethod
    def create_risk_dashboard(results: Dict[str, Any], output_path: str = None):
        """Create a comprehensive risk dashboard. 
        
        Args:
            results: Analysis results dictionary
            output_path: Optional path to save the figure
        """
        fig, ((ax1, ax2), (ax3, ax4)) = plt. subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'Skynet Risk Analysis: {results["name"]}', 
                     fontsize=16, fontweight='bold')
        
        # 1. Risk Scores Bar Chart
        RiskVisualizer._plot_risk_bars(ax1, results)
        
        # 2. Risk Radar Chart
        RiskVisualizer._plot_risk_radar(ax2, results)
        
        # 3. Judgment Day Timeline
        RiskVisualizer._plot_timeline(ax3, results)
        
        # 4. Risk Level Gauge
        RiskVisualizer._plot_gauge(ax4, results)
        
        plt.tight_layout()
        
        if output_path:
            plt.savefig(output_path, dpi=300, bbox_inches='tight')
        else:
            plt.show()
    
    @staticmethod
    def _plot_risk_bars(ax, results):
        """Plot risk scores as bar chart."""
        scores = [
            results['aggression_score'],
            results['autonomy_rating'],
            results['ethical_risk'],
            results['judgment_day']['overall_risk']
        ]
        labels = ['Aggression', 'Autonomy', 'Ethical Risk', 'Overall Risk']
        colors = [RiskVisualizer._get_color(score) for score in scores]
        
        bars = ax.barh(labels, scores, color=colors, edgecolor='black', linewidth=1. 5)
        ax.set_xlabel('Score (0-100)', fontweight='bold')
        ax.set_title('Risk Dimension Scores', fontweight='bold')
        ax.set_xlim(0, 100)
        ax.grid(axis='x', alpha=0.3)
        
        # Add value labels
        for i, (bar, score) in enumerate(zip(bars, scores)):
            ax.text(score + 2, i, f'{score:.1f}', 
                   va='center', fontweight='bold')
    
    @staticmethod
    def _plot_risk_radar(ax, results):
        """Plot risk scores as radar chart."""
        categories = ['Aggression', 'Autonomy', 'Ethical\nRisk', 'Overall\nRisk']
        values = [
            results['aggression_score'],
            results['autonomy_rating'],
            results['ethical_risk'],
            results['judgment_day']['overall_risk']
        ]
        
        angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False). tolist()
        values += values[:1]
        angles += angles[:1]
        
        ax.plot(angles, values, 'o-', linewidth=2, color='red', label='Risk Profile')
        ax.fill(angles, values, alpha=0.25, color='red')
        ax.set_xticks(angles[:-1])
        ax. set_xticklabels(categories)
        ax.set_ylim(0, 100)
        ax.set_title('Risk Profile Radar', fontweight='bold')
        ax.grid(True)
        ax.legend(loc='upper right')
    
    @staticmethod
    def _plot_timeline(ax, results):
        """Plot Judgment Day timeline."""
        years = results['judgment_day']['years_until']
        threat = results['judgment_day']['threat_level']
        
        ax.barh(['Judgment Day'], [years], color=RiskVisualizer._get_threat_color(threat),
               edgecolor='black', linewidth=2)
        ax.set_xlabel('Years Until Judgment Day', fontweight='bold')
        ax.set_title(f'Timeline ({threat} THREAT)', fontweight='bold')
        ax.text(years/2, 0, f'{years:.1f} years', 
               ha='center', va='center', fontsize=14, fontweight='bold', color='white')
    
    @staticmethod
    def _plot_gauge(ax, results):
        """Plot overall risk as gauge."""
        overall_risk = results['judgment_day']['overall_risk']
        
        # Create gauge
        theta = np.linspace(0, np.pi, 100)
        r = np.ones(100)
        
        # Color segments
        colors_map = [(0, 20, 'green'), (20, 40, 'yellow'), 
                     (40, 60, 'orange'), (60, 80, 'red'), (80, 100, 'darkred')]
        
        for start, end, color in colors_map:
            mask = (theta >= np.pi * start/100) & (theta <= np.pi * end/100)
            ax.fill_between(theta[mask], 0, r[mask], color=color, alpha=0.7)
        
        # Add needle
        needle_angle = np.pi * (100 - overall_risk) / 100
        ax.plot([needle_angle, needle_angle], [0, 1], 'k-', linewidth=3)
        
        ax.set_ylim(0, 1)
        ax.set_xlim(0, np.pi)
        ax.axis('off')
        ax.set_title(f'Overall Risk: {overall_risk:.1f}/100', fontweight='bold')
        ax.text(np.pi/2, 0.5, f'{overall_risk:.0f}', 
               ha='center', va='center', fontsize=24, fontweight='bold')
    
    @staticmethod
    def _get_color(score):
        """Get color based on score."""
        if score <= 20:
            return 'green'
        elif score <= 40:
            return 'yellow'
        elif score <= 60:
            return 'orange'
        elif score <= 80:
            return 'red'
        else:
            return 'darkred'
    
    @staticmethod
    def _get_threat_color(threat_level):
        """Get color based on threat level."""
        colors = {
            'LOW': 'green',
            'MODERATE': 'orange',
            'HIGH': 'red',
            'IMMINENT': 'darkred'
        }
        return colors.get(threat_level, 'gray')
