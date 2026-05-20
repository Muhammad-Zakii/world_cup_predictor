
import joblib
import numpy as np
import os
import sys

# Add the ml_model directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from ml_model.data.world_cup_data import WORLD_CUP_2026_TEAMS

class PredictionEngine:
    def __init__(self):
        try:
            model_path = os.path.join(os.path.dirname(__file__), 'models', 'world_cup_model.joblib')
            scaler_path = os.path.join(os.path.dirname(__file__), 'models', 'scaler.joblib')
            region_map_path = os.path.join(os.path.dirname(__file__), 'models', 'region_map.joblib')
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            self.region_map = joblib.load(region_map_path)
        except FileNotFoundError:
            print("Warning: Model files not found. Please train the model first.")
            self.model = None
            self.scaler = None
            self.region_map = None
    
    def get_all_teams(self):
        """Return all qualified teams with their data."""
        teams_list = []
        for team, data in WORLD_CUP_2026_TEAMS.items():
            teams_list.append({
                'name': team,
                'fifa_ranking': data['fifa_ranking'],
                'historical_wins': data['historical_wins'],
                'continental_titles': data['continental_titles'],
                'region': data['region']
            })
        return sorted(teams_list, key=lambda x: x['fifa_ranking'])
    
    def predict_team(self, team_name):
        """Predict the winning probability for a team."""
        if team_name not in WORLD_CUP_2026_TEAMS:
            return {'error': f'Team {team_name} not found'}
        
        if self.model is None:
            return {'error': 'Model not trained. Please train the model first.'}
        
        team_data = WORLD_CUP_2026_TEAMS[team_name]
        region_code = self.region_map.get(team_data['region'], 0)
        
        features = np.array([[
            team_data['fifa_ranking'],
            team_data['historical_wins'],
            team_data['continental_titles'],
            region_code
        ]])
        
        features_scaled = self.scaler.transform(features)
        prediction = self.model.predict(features_scaled)[0]
        prediction = max(0, min(1, prediction))
        
        # Get ranking
        all_predictions = []
        for t_name, t_data in WORLD_CUP_2026_TEAMS.items():
            t_region_code = self.region_map.get(t_data['region'], 0)
            t_features = np.array([[
                t_data['fifa_ranking'],
                t_data['historical_wins'],
                t_data['continental_titles'],
                t_region_code
            ]])
            t_features_scaled = self.scaler.transform(t_features)
            t_pred = max(0, min(1, self.model.predict(t_features_scaled)[0]))
            all_predictions.append((t_name, t_pred))
        
        all_predictions.sort(key=lambda x: x[1], reverse=True)
        rank = next(i for i, (t, _) in enumerate(all_predictions, 1) if t == team_name)
        
        return {
            'team': team_name,
            'win_probability': round(prediction * 100, 2),
            'rank': rank,
            'total_teams': len(WORLD_CUP_2026_TEAMS),
            'confidence': round(0.85 + (0.1 * (1 - team_data['fifa_ranking']/150)), 2),
            'region': team_data['region']
        }
    
    def get_top_predictions(self, n=10):
        """Get top N teams by prediction."""
        predictions = []
        for team_name in WORLD_CUP_2026_TEAMS.keys():
            result = self.predict_team(team_name)
            if 'error' not in result:
                predictions.append(result)
        
        return sorted(predictions, key=lambda x: x['win_probability'], reverse=True)[:n]
