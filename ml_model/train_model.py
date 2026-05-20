import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
import joblib
import os
import sys

# Add the ml_model directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from data.world_cup_data import WORLD_CUP_2026_TEAMS

os.makedirs(os.path.join(os.path.dirname(__file__), 'models'), exist_ok=True)

# Historical World Cup data
historical_data = [
    ('Brazil', 4, 5, 9, 1, 0.15),
    ('Argentina', 1, 3, 15, 1, 0.14),
    ('France', 2, 2, 0, 2, 0.12),
    ('Germany', 15, 4, 0, 2, 0.10),
    ('England', 5, 1, 0, 2, 0.08),
    ('Spain', 8, 1, 0, 2, 0.07),
    ('Italy', 10, 4, 0, 2, 0.06),
    ('Netherlands', 9, 0, 0, 2, 0.05),
    ('Belgium', 21, 0, 0, 2, 0.04),
    ('Portugal', 12, 0, 0, 2, 0.03),
    ('Uruguay', 27, 2, 15, 1, 0.05),
    ('Colombia', 20, 0, 0, 1, 0.02),
    ('Mexico', 13, 0, 3, 0, 0.02),
    ('USA', 16, 0, 2, 0, 0.02),
    ('Morocco', 11, 0, 1, 3, 0.03),
    ('Senegal', 18, 0, 1, 3, 0.02),
]

region_map = {'CONCACAF': 0, 'CONMEBOL': 1, 'UEFA': 2, 'CAF': 3, 'AFC': 4}

df = pd.DataFrame(historical_data, columns=['team', 'fifa_ranking', 'historical_wins', 'continental_titles', 'region_code', 'win_probability'])

X = df[['fifa_ranking', 'historical_wins', 'continental_titles', 'region_code']].values
y = df['win_probability'].values

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

model = GradientBoostingRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42)
model.fit(X_train_scaled, y_train)

train_score = model.score(X_train_scaled, y_train)
test_score = model.score(X_test_scaled, y_test)

print(f"Training R² Score: {train_score:.4f}")
print(f"Testing R² Score: {test_score:.4f}")

models_dir = os.path.join(os.path.dirname(__file__), 'models')
joblib.dump(model, os.path.join(models_dir, 'world_cup_model.joblib'))
joblib.dump(scaler, os.path.join(models_dir, 'scaler.joblib'))
joblib.dump(region_map, os.path.join(models_dir, 'region_map.joblib'))

print("Model trained and saved successfully!")
