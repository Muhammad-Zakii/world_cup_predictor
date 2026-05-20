'use client';

export default function Header() {
  return (
    <header className="bg-black bg-opacity-20 text-white py-8 px-4">
      <div className="container text-center">
        <h1 className="text-5xl font-bold mb-2">🏆 World Cup 2026 Predictor</h1>
        <p className="text-xl text-gray-200">AI-Powered Championship Winner Predictions</p>
        <p className="text-sm text-gray-300 mt-2">Click on any team's flag to see their winning probability</p>
      </div>
    </header>
  );
}
