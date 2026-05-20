'use client';

interface TeamGridProps {
  teams: any[];
  selectedTeam: string | null;
  onTeamSelect: (teamName: string) => void;
  loading: boolean;
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
  'Saudi Arabia': '🇸🇦',
  'Serbia': '🇷🇸',
  'Switzerland': '🇨🇭',
  'Austria': '🇦🇹',
  'Poland': '🇵🇱',
  'Denmark': '🇩🇰',
  'Sweden': '🇸🇪',
  'Ukraine': '🇺🇦',
  'Greece': '🇬🇷',
  'Czech Republic': '🇨🇿',
  'Romania': '🇷🇴',
  'Hungary': '🇭🇺',
  'Slovakia': '🇸🇰',
  'Slovenia': '🇸🇮',
  'Cameroon': '🇨🇲',
  'Nigeria': '🇳🇬',
  'Ghana': '🇬🇭',
  'Tunisia': '🇹🇳',
  'China PR': '🇨🇳',
  'Ecuador': '🇪🇨',
  'Paraguay': '🇵🇾',
};

export default function TeamGrid({ teams, selectedTeam, onTeamSelect, loading }: TeamGridProps) {
  if (!teams.length) {
    return <div className="text-white text-center py-10">No teams loaded</div>;
  }

  return (
    <div className="py-10">
      <h2 className="text-3xl font-bold text-white mb-8 text-center">Qualified Teams (2026)</h2>
      <div className="team-grid">
        {teams.map((team) => (
          <div
            key={team.name}
            onClick={() => onTeamSelect(team.name)}
            className={`team-card ${
              selectedTeam === team.name ? 'ring-4 ring-yellow-400' : ''
            } ${loading && selectedTeam === team.name ? 'opacity-50' : ''}`}
          >
            <div className="team-flag">{teamFlags[team.name] || '🏴'}</div>
            <div className="team-name">{team.name}</div>
            <div className="text-xs text-gray-500">FIFA #{team.fifa_ranking}</div>
            {loading && selectedTeam === team.name && (
              <div className="text-xs text-blue-500 mt-2 animate-pulse">Predicting...</div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
