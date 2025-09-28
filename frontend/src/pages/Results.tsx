import React, { useState, useEffect } from 'react';
import { ResultsDisplay } from '../components/ResultsDisplay';
import { api } from '../services/api';

interface Results {
  id: string;
  checklistId: string;
  documentId: string;
  status: 'processing' | 'completed' | 'error';
  answers: Array<{
    questionId: string;
    questionText: string;
    answer: string;
  }>;
  conditions: Array<{
    conditionId: string;
    conditionText: string;
    result: boolean;
  }>;
  createdAt: string;
  error?: string;
}

interface ResultsPageProps {
  resultId: string;
}

export const Results: React.FC<ResultsPageProps> = ({ resultId }) => {
  const [results, setResults] = useState<Results | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadResults();
  }, [resultId]);

  const loadResults = async () => {
    try {
      setLoading(true);
      const data = await api.getResults(resultId);
      setResults(data);
    } catch (err) {
      setError('Failed to load results');
    } finally {
      setLoading(false);
    }
  };

  const handleRefresh = () => {
    loadResults();
  };

  const handleBack = () => {
    window.history.back();
  };

  if (loading) {
    return (
      <div className="results-page">
        <h1>Loading Results...</h1>
        <div className="loading">Please wait while we load your results.</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="results-page">
        <h1>Error</h1>
        <div className="error">{error}</div>
        <button onClick={handleRefresh}>Retry</button>
        <button onClick={handleBack}>Back</button>
      </div>
    );
  }

  if (!results) {
    return (
      <div className="results-page">
        <h1>Results Not Found</h1>
        <div className="not-found">The requested results could not be found.</div>
        <button onClick={handleBack}>Back</button>
      </div>
    );
  }

  return (
    <div className="results-page">
      <div className="results-header">
        <h1>Processing Results</h1>
        <div className="results-actions">
          <button onClick={handleRefresh}>Refresh</button>
          <button onClick={handleBack}>Back</button>
        </div>
      </div>

      <div className="results-info">
        <div className="result-id">Result ID: {results.id}</div>
        <div className="created-at">Created: {new Date(results.createdAt).toLocaleString()}</div>
        <div className="status">Status: {results.status}</div>
      </div>

      <ResultsDisplay results={results} />

      {results.status === 'processing' && (
        <div className="processing-note">
          <p>Your document is being processed. This may take a few minutes.</p>
          <p>You can refresh this page to check for updates.</p>
        </div>
      )}

      {results.status === 'error' && (
        <div className="error-note">
          <p>There was an error processing your document.</p>
          {results.error && <p>Error: {results.error}</p>}
          <p>Please try uploading your document again.</p>
        </div>
      )}
    </div>
  );
};
