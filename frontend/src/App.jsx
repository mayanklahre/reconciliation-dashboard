import React, { useState } from 'react';
import Dashboard from './components/Dashboard.jsx';
import ResultsTable from './components/ResultsTable.jsx';

function App() {
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleFileUpload = async (file) => {
    setLoading(true);
    setError(null);
    const formData = new FormData();
    formData.append('file', file);

    try {
      // Sending the file to your Python backend!
      const response = await fetch('http://localhost:8000/api/reconcile', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Upload failed");
      }

      const data = await response.json();
      setResults(data.data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  // This return statement is what actually draws the screen!
  return (
    <div className="min-h-screen bg-gray-50 p-8">
      <div className="max-w-6xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 text-gray-800">Valuation Reconciliation</h1>
        
        {error && (
          <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-8 shadow-sm">
            {error}
          </div>
        )}
        
        <Dashboard onUpload={handleFileUpload} loading={loading} />
        
        {results && <ResultsTable data={results} />}
      </div>
    </div>
  );
}

export default App;