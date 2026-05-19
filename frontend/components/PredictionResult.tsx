'use client';

interface PredictionResultProps {
  prediction: {
    team: string;
    win_probability: number;
    rank: number;
    total_teams: number;
    confidence: number;
    region: string;
  };
}

const teamFlags: Record<string, string> = {
  'Argentina': '🇦🇷',
  'Brazil': '🇧🇷',
  'France': '🇫🇷',
  'England': '🇬🇧',
  'Germany': '🇩🇪',
  'Spain': '🇪🇸',
  'Italy': '🇮🇹',
  'Netherlands': '🇳🇱',
  'Belgium': '🇧🇪',
  'Portugal': '🇵🇹',
  'Uruguay': '🇺🇾',
  'Colombia': '🇨🇴',
  'Mexico': '🇲🇽',
  'USA': '🇺🇸',
  'Canada': '🇨🇦',
  'Morocco': '🇲🇦',
  'Senegal': '🇸🇳',
  'Egypt': '🇪🇬',
  'Japan': '🇯🇵',
  'South Korea': '🇰🇷',
  'Australia': '🇦🇺',
  'Iran': '🇮🇷',
};

export default function PredictionResult({ prediction }: PredictionResultProps) {
  const probabilityPercentage = prediction.win_probability;
  const medalEmoji = 
    prediction.rank === 1 ? '🥇' :
    prediction.rank === 2 ? '🥈' :
    prediction.rank === 3 ? '🥉' : '🏅';

  return (
    <div className="prediction-result">
      <div className="text-center mb-6">
        <div className="text-6xl mb-3">{teamFlags[prediction.team] || '🏴'}</div>
        <h2 className="prediction-title">{prediction.team}</h2>
      </div>

      <div className="space-y-4">
        <div className="prediction-stat">
          <span className="prediction-label">🏆 Winning Probability</span>
          <span className="prediction-value">{probabilityPercentage}%</span>
        </div>

        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${Math.max(5, probabilityPercentage)}%` }}
          >
            {probabilityPercentage > 10 && `${probabilityPercentage}%`}
          </div>
        </div>

        <div className="prediction-stat">
          <span className="prediction-label">📊 Championship Rank</span>
          <span className="prediction-value">{medalEmoji} #{prediction.rank}/{prediction.total_teams}</span>
        </div>

        <div className="prediction-stat">
          <span className="prediction-label">🎯 Model Confidence</span>
          <span className="prediction-value">{(prediction.confidence * 100).toFixed(0)}%</span>
        </div>

        <div className="prediction-stat">
          <span className="prediction-label">🌍 Region</span>
          <span className="prediction-value">{prediction.region}</span>
        </div>
      </div>

      <div className="mt-6 p-4 bg-blue-50 rounded-lg">
        <p className="text-sm text-gray-700">
          <strong>Note:</strong> These predictions are based on a machine learning model trained on historical World Cup data and FIFA rankings.
        </p>
      </div>
    </div>
  );
}
