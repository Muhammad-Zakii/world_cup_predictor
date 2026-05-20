'use client';

import { useState, useEffect } from 'react';
import TeamGrid from '@/components/TeamGrid';
import PredictionResult from '@/components/PredictionResult';
import Header from '@/components/Header';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:5001';

export default function Home() {
  const [teams, setTeams] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTeam, setSelectedTeam] = useState<string | null>(null);
  const [prediction, setPrediction] = useState<any>(null);
  const [predicting, setPredicting] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    fetchTeams();
  }, []);

  const fetchTeams = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(`${API_URL}/api/teams`);
      if (!response.ok) throw new Error('Failed to fetch teams');
      const data = await response.json();
      console.log("Teams API response:", data);
      setTeams(Array.isArray(data) ? data : data.teams || []);
    } catch (err) {
      setError('Failed to load teams. Make sure the backend is running.');
      console.error('Error fetching teams:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleTeamSelect = async (teamName: string) => {
    setSelectedTeam(teamName);
    setPredicting(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/api/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ team: teamName }),
      });
      if (!response.ok) throw new Error('Failed to get prediction');
      const data = await response.json();
      setPrediction(data.prediction);
    } catch (err) {
      setError('Failed to get prediction. Please try again.');
      console.error('Error:', err);
    } finally {
      setPredicting(false);
    }
  };

  return (
    <main className="min-h-screen bg-gradient-to-br from-purple-600 via-blue-600 to-indigo-700">
      <Header />
      <div className="container">
        {error && <div className="error-message">{error}</div>}
        
        {loading ? (
          <div className="loading">
            <div className="text-2xl font-bold mb-4">Loading teams...</div>
            <div className="inline-block animate-spin">
              <svg className="w-12 h-12 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m0 0h6" />
              </svg>
            </div>
          </div>
        ) : (
          <>
            <TeamGrid 
              teams={teams}
              selectedTeam={selectedTeam}
              onTeamSelect={handleTeamSelect}
              loading={predicting}
            />
            {prediction && !predicting && (
              <PredictionResult prediction={prediction} />
            )}
          </>
        )}
      </div>
    </main>
  );
}
