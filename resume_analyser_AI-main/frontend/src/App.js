import React, { useState } from 'react';
import FileUpload from './components/FileUpload';
import Dashboard from './components/Dashboard';
import './App.css';

function App() {
  const [currentAnalysis, setCurrentAnalysis] = useState(null);

  const handleAnalysisComplete = (analysis) => {
    setCurrentAnalysis(analysis);
  };

  const handleNewAnalysis = () => {
    setCurrentAnalysis(null);
  };

  return (
    <div className="App">
      <header className="app-header">
        <h1>HIRESENSE AI</h1>
        <p className="app-subtitle">Analyze & Optimize Your Professional Profile</p>
        {currentAnalysis && (
          <button onClick={handleNewAnalysis} className="new-analysis-btn">
            ← New Analysis
          </button>
        )}
      </header>

      <main className="main-container">
        {!currentAnalysis ? (
          <FileUpload onAnalysisComplete={handleAnalysisComplete} />
        ) : (
          <Dashboard analysis={currentAnalysis} />
        )}
      </main>
    </div>
  );
}

export default App;