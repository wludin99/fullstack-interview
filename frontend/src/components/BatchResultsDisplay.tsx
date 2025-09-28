import React, { useState } from 'react';
import type { ProcessingResult, Document } from '../services/api';

interface BatchResultsDisplayProps {
  results: ProcessingResult[];
  documents: Document[];
  onExport?: () => void;
  onReprocess?: (documentIds: string[]) => void;
}

export const BatchResultsDisplay: React.FC<BatchResultsDisplayProps> = ({
  results,
  documents,
  onExport,
  onReprocess
}) => {
  const [selectedTab, setSelectedTab] = useState<'overview' | 'details'>('details');
  const [filterStatus, setFilterStatus] = useState<'all' | 'completed' | 'error'>('all');

  const filteredResults = results.filter(result => {
    if (filterStatus === 'all') return true;
    if (filterStatus === 'completed') return result.status === 'completed';
    if (filterStatus === 'error') return result.status === 'error';
    return true;
  });

  const completedCount = results.filter(r => r.status === 'completed').length;
  const errorCount = results.filter(r => r.status === 'error').length;
  const totalCount = results.length;

  const getDocumentName = (documentId: string) => {
    const doc = documents.find(d => d.id === documentId);
    return doc ? doc.original_name : 'Unknown Document';
  };

  const getOverallStatus = () => {
    if (errorCount === 0) return 'completed';
    if (completedCount === 0) return 'error';
    return 'partial';
  };

  const overallStatus = getOverallStatus();

  return (
    <div className="batch-results-display">
      <div className="results-header">
        <div className="results-title">
          <h3>Batch Processing Results</h3>
          <div className={`overall-status status-${overallStatus}`}>
            {overallStatus === 'completed' && '✅ All Completed'}
            {overallStatus === 'error' && '❌ All Failed'}
            {overallStatus === 'partial' && '⚠️ Partial Success'}
          </div>
        </div>
        
        <div className="results-actions">
          {onExport && (
            <button onClick={onExport} className="btn btn-secondary">
              Export Results
            </button>
          )}
          {onReprocess && errorCount > 0 && (
            <button 
              onClick={() => {
                const errorDocumentIds = results
                  .filter(r => r.status === 'error')
                  .map(r => r.documentId);
                onReprocess(errorDocumentIds);
              }}
              className="btn btn-primary"
            >
              Reprocess Failed
            </button>
          )}
        </div>
      </div>

      <div className="results-summary">
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-label">Total Documents:</span>
            <span className="stat-value">{totalCount}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Completed:</span>
            <span className="stat-value success">{completedCount}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Failed:</span>
            <span className="stat-value error">{errorCount}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Success Rate:</span>
            <span className="stat-value">
              {totalCount > 0 ? Math.round((completedCount / totalCount) * 100) : 0}%
            </span>
          </div>
        </div>
      </div>

      <div className="results-controls">
        <div className="tab-controls">
          <button
            className={`tab-button ${selectedTab === 'overview' ? 'active' : ''}`}
            onClick={() => setSelectedTab('overview')}
          >
            Overview
          </button>
          <button
            className={`tab-button ${selectedTab === 'details' ? 'active' : ''}`}
            onClick={() => setSelectedTab('details')}
          >
            Details
          </button>
        </div>

        <div className="filter-controls">
          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value as any)}
            className="filter-select"
          >
            <option value="all">All Results</option>
            <option value="completed">Completed Only</option>
            <option value="error">Errors Only</option>
          </select>
        </div>
      </div>

      <div className="results-content">
        {selectedTab === 'overview' ? (
          <div className="overview-tab">
            <div className="results-list">
              {filteredResults.map((result) => (
                <div key={result.id} className={`result-item ${result.status}`}>
                  <div className="result-header">
                    <div className="result-document">
                      <span className="document-name">
                        {getDocumentName(result.documentId)}
                      </span>
                      <span className={`status-badge status-${result.status}`}>
                        {result.status}
                      </span>
                    </div>
                    <div className="result-meta">
                      <span className="answers-count">
                        {result.answers.length} answers
                      </span>
                      <span className="conditions-count">
                        {result.conditions.length} conditions
                      </span>
                    </div>
                  </div>
                  
                  {result.status === 'error' && result.error && (
                    <div className="error-details">
                      <strong>Error:</strong> {result.error}
                    </div>
                  )}
                  
                  {result.status === 'completed' && (
                    <div className="result-preview">
                      <div className="answers-preview">
                        <strong>📝 Sample Questions & Answers:</strong>
                        <ul>
                          {result.answers.slice(0, 2).map((answer, index) => (
                            <li key={index}>
                              <span className="question-text">Q{index + 1}: {answer.questionText}</span>
                              <div className="answer-text">{answer.answer}</div>
                            </li>
                          ))}
                          {result.answers.length > 2 && (
                            <li>... and {result.answers.length - 2} more questions</li>
                          )}
                        </ul>
                      </div>
                      
                      {result.conditions.length > 0 && (
                        <div className="conditions-preview">
                          <strong>🔍 Sample Conditions:</strong>
                          <ul>
                            {result.conditions.slice(0, 2).map((condition, index) => (
                              <li key={index}>
                                <span className="condition-text">C{index + 1}: {condition.conditionText}</span>
                                <div className={`condition-result ${condition.result ? 'true' : 'false'}`}>
                                  {condition.result ? '✅ True' : '❌ False'}
                                </div>
                              </li>
                            ))}
                            {result.conditions.length > 2 && (
                              <li>... and {result.conditions.length - 2} more conditions</li>
                            )}
                          </ul>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>
        ) : (
          <div className="details-tab">
            {filteredResults.length > 0 && (
              <div className="details-summary">
                <h4>📊 Processing Summary</h4>
                <div className="summary-grid">
                  <div className="summary-item">
                    <span className="summary-label">Total Documents:</span>
                    <span className="summary-value">{filteredResults.length}</span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Total Questions:</span>
                    <span className="summary-value">
                      {filteredResults.reduce((sum, r) => sum + r.answers.length, 0)}
                    </span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Total Conditions:</span>
                    <span className="summary-value">
                      {filteredResults.reduce((sum, r) => sum + r.conditions.length, 0)}
                    </span>
                  </div>
                  <div className="summary-item">
                    <span className="summary-label">Conditions Passed:</span>
                    <span className="summary-value">
                      {filteredResults.reduce((sum, r) => 
                        sum + r.conditions.filter(c => c.result).length, 0
                      )}
                    </span>
                  </div>
                </div>
              </div>
            )}
            
            {filteredResults.map((result) => (
              <div key={result.id} className="detailed-result">
                <div className="result-document-header">
                  <h4>{getDocumentName(result.documentId)}</h4>
                  <span className={`status-badge status-${result.status}`}>
                    {result.status}
                  </span>
                </div>

                {result.status === 'error' && result.error && (
                  <div className="error-section">
                    <h5>Error Details</h5>
                    <p className="error-message">{result.error}</p>
                  </div>
                )}

                {result.status === 'completed' && (
                  <>
                    <div className="answers-section">
                      <h5>📝 Questions & Answers ({result.answers.length})</h5>
                      <div className="answers-list">
                        {result.answers.map((answer, index) => (
                          <div key={index} className="answer-item">
                            <div className="question-header">
                              <span className="question-number">Q{index + 1}</span>
                              <div className="question-text">{answer.questionText}</div>
                            </div>
                            <div className="answer-content">
                              <span className="answer-label">Answer:</span>
                              <div className="answer-text">{answer.answer}</div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>

                    <div className="conditions-section">
                      <h5>🔍 Condition Evaluations ({result.conditions.length})</h5>
                      <div className="conditions-list">
                        {result.conditions.map((condition, index) => (
                          <div key={index} className="condition-item">
                            <div className="condition-header">
                              <span className="condition-number">C{index + 1}</span>
                              <div className="condition-text">{condition.conditionText}</div>
                            </div>
                            <div className="condition-result-container">
                              <span className="result-label">Result:</span>
                              <div className={`condition-result ${condition.result ? 'true' : 'false'}`}>
                                {condition.result ? '✅ True' : '❌ False'}
                              </div>
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  </>
                )}
              </div>
            ))}
          </div>
        )}
      </div>

      {filteredResults.length === 0 && (
        <div className="no-results">
          <p>No results found matching the current filter.</p>
        </div>
      )}
    </div>
  );
};
