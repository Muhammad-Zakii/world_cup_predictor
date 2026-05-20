import os
import sys
from flask import Flask, jsonify, request
from flask_cors import CORS

# Add parent directory to path to import ml_model
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from ml_model.prediction_engine import PredictionEngine

app = Flask(__name__)
CORS(app)

# Initialize prediction engine
prediction_engine = PredictionEngine()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'message': 'World Cup 2026 Predictor API is running',
        'model_loaded': prediction_engine.model is not None
    }), 200

@app.route('/api/teams', methods=['GET'])
def get_teams():
    """Get all 48 qualified teams."""
    try:
        teams = prediction_engine.get_all_teams()
        return jsonify({
            'success': True,
            'total_teams': len(teams),
            'teams': teams
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict', methods=['POST'])
def predict():
    """Predict winning probability for a team."""
    try:
        data = request.get_json()
        team_name = data.get('team')
        
        if not team_name:
            return jsonify({
                'success': False,
                'error': 'Team name is required'
            }), 400
        
        result = prediction_engine.predict_team(team_name)
        
        if 'error' in result:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 404
        
        return jsonify({
            'success': True,
            'prediction': result
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/top-predictions', methods=['GET'])
def get_top_predictions():
    """Get top N teams by winning probability."""
    try:
        n = request.args.get('n', 10, type=int)
        if n > 48:
            n = 48
        if n < 1:
            n = 10
        
        predictions = prediction_engine.get_top_predictions(n)
        return jsonify({
            'success': True,
            'total_returned': len(predictions),
            'predictions': predictions
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/api/predict-multiple', methods=['POST'])
def predict_multiple():
    """Predict for multiple teams."""
    try:
        data = request.get_json()
        teams = data.get('teams', [])
        
        if not teams or not isinstance(teams, list):
            return jsonify({
                'success': False,
                'error': 'Teams list is required'
            }), 400
        
        results = []
        for team in teams:
            result = prediction_engine.predict_team(team)
            results.append(result)
        
        return jsonify({
            'success': True,
            'total_predictions': len(results),
            'predictions': results
        }), 200
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'error': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'error': 'Internal server error'
    }), 500

if __name__ == '__main__':
    # Use port 5001 to avoid conflicts
    print("🏆 World Cup 2026 Predictor API")
    print("Starting on http://localhost:5001")
    app.run(debug=True, host='0.0.0.0', port=5001)
