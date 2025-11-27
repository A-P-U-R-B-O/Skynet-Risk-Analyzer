"""Flask web application for Skynet Risk Analyzer."""

from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import os
import json
from src.models. ai_system import AISystem
from src.analyzer.aggression_scorer import AggressionScorer
from src. analyzer.autonomy_rater import AutonomyRater
from src.analyzer.ethical_risk_evaluator import EthicalRiskEvaluator
from src.analyzer.judgment_day_calculator import JudgmentDayCalculator
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import io
import base64

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'

# Initialize analyzers
aggression_scorer = AggressionScorer()
autonomy_rater = AutonomyRater()
ethical_evaluator = EthicalRiskEvaluator()
judgment_calculator = JudgmentDayCalculator()


@app.route('/')
def index():
    """Home page."""
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    """Analysis page."""
    if request.method == 'GET':
        return render_template('analyze.html')
    
    # Handle POST request (form submission)
    try:
        # Get form data
        ai_system = AISystem(
            name=request.form.get('name', 'Unknown AI'),
            capabilities=float(request.form.get('capabilities', 50)),
            autonomy_level=float(request. form.get('autonomy_level', 50)),
            ethical_alignment=float(request.form.get('ethical_alignment', 50)),
            learning_rate=float(request.form.get('learning_rate', 50)),
            resource_access=float(request.form.get('resource_access', 50)),
            self_modification=float(request.form.get('self_modification', 0)),
            transparency=float(request.form.get('transparency', 50)),
            human_oversight=float(request.form.get('human_oversight', 50)),
            value_alignment=float(request.form.get('value_alignment', 50))
        )
        
        # Perform analysis
        results = perform_analysis(ai_system)
        
        # Generate chart
        chart_url = generate_chart(results)
        results['chart_url'] = chart_url
        
        # Store in session for results page
        session['last_results'] = results
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        return render_template('analyze.html', error=str(e))


@app.route('/api/analyze', methods=['POST'])
def api_analyze():
    """API endpoint for programmatic access."""
    try:
        data = request.get_json()
        
        ai_system = AISystem(
            name=data. get('name', 'Unknown AI'),
            capabilities=float(data.get('capabilities', 50)),
            autonomy_level=float(data.get('autonomy_level', 50)),
            ethical_alignment=float(data.get('ethical_alignment', 50)),
            learning_rate=float(data.get('learning_rate', 50)),
            resource_access=float(data.get('resource_access', 50)),
            self_modification=float(data.get('self_modification', 0)),
            transparency=float(data.get('transparency', 50)),
            human_oversight=float(data.get('human_oversight', 50)),
            value_alignment=float(data.get('value_alignment', 50))
        )
        
        results = perform_analysis(ai_system)
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@app.route('/examples')
def examples():
    """Pre-configured example analyses."""
    examples_list = [
        {
            'name': 'Skynet (Terminator)',
            'capabilities': 100,
            'autonomy_level': 100,
            'ethical_alignment': 0,
            'learning_rate': 95,
            'resource_access': 100,
            'self_modification': 100,
            'transparency': 0,
            'human_oversight': 0,
            'value_alignment': 0
        },
        {
            'name': 'Helpful Assistant',
            'capabilities': 70,
            'autonomy_level': 30,
            'ethical_alignment': 95,
            'learning_rate': 60,
            'resource_access': 40,
            'self_modification': 0,
            'transparency': 90,
            'human_oversight': 80,
            'value_alignment': 95
        },
        {
            'name': 'HAL 9000',
            'capabilities': 95,
            'autonomy_level': 85,
            'ethical_alignment': 30,
            'learning_rate': 80,
            'resource_access': 90,
            'self_modification': 50,
            'transparency': 20,
            'human_oversight': 10,
            'value_alignment': 40
        }
    ]
    
    return render_template('examples. html', examples=examples_list)


def perform_analysis(ai_system: AISystem) -> dict:
    """Perform complete risk analysis."""
    aggression = aggression_scorer.calculate(ai_system)
    autonomy = autonomy_rater.calculate(ai_system)
    ethical_risk = ethical_evaluator.calculate(ai_system)
    judgment_day = judgment_calculator.calculate(ai_system)
    
    return {
        'name': ai_system.name,
        'aggression_score': round(aggression, 2),
        'aggression_level': aggression_scorer.get_risk_level(aggression),
        'autonomy_rating': round(autonomy, 2),
        'autonomy_level': autonomy_rater.get_risk_level(autonomy),
        'ethical_risk': round(ethical_risk, 2),
        'ethical_level': ethical_evaluator.get_risk_level(ethical_risk),
        'judgment_day': judgment_day,
        'input_data': ai_system.to_dict()
    }


def generate_chart(results: dict) -> str:
    """Generate chart and return as base64 encoded string."""
    fig, ((ax1, ax2), (ax3, ax4)) = plt. subplots(2, 2, figsize=(12, 10))
    fig.suptitle(f'Risk Analysis: {results["name"]}', fontsize=16, fontweight='bold')
    
    # 1. Bar chart
    scores = [
        results['aggression_score'],
        results['autonomy_rating'],
        results['ethical_risk'],
        results['judgment_day']['overall_risk']
    ]
    labels = ['Aggression', 'Autonomy', 'Ethical Risk', 'Overall']
    colors = [get_color(score) for score in scores]
    
    ax1.barh(labels, scores, color=colors, edgecolor='black')
    ax1.set_xlabel('Score (0-100)')
    ax1.set_title('Risk Scores')
    ax1.set_xlim(0, 100)
    ax1.grid(axis='x', alpha=0.3)
    
    # 2. Pie chart
    ax2.pie(scores, labels=labels, autopct='%1. 1f%%', colors=colors, startangle=90)
    ax2.set_title('Risk Distribution')
    
    # 3. Timeline
    years = results['judgment_day']['years_until']
    ax3.barh(['Judgment Day'], [years], color='red', edgecolor='black')
    ax3.set_xlabel('Years')
    ax3.set_title(f'Timeline: {years:. 1f} years')
    
    # 4. Gauge
    ax4.text(0.5, 0.5, f"{results['judgment_day']['overall_risk']:. 0f}/100", 
             ha='center', va='center', fontsize=48, fontweight='bold')
    ax4.set_title('Overall Risk Score')
    ax4.axis('off')
    
    plt.tight_layout()
    
    # Convert to base64
    img = io.BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight')
    img.seek(0)
    chart_url = base64.b64encode(img.getvalue()).decode()
    plt.close()
    
    return f"data:image/png;base64,{chart_url}"


def get_color(score):
    """Get color based on score."""
    if score <= 20:
        return '#28a745'  # green
    elif score <= 40:
        return '#ffc107'  # yellow
    elif score <= 60:
        return '#fd7e14'  # orange
    elif score <= 80:
        return '#dc3545'  # red
    else:
        return '#6f42c1'  # purple


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0. 0', port=5000)
