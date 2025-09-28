import React from 'react';

interface Answer {
  questionId: string;
  questionText: string;
  answer: string;
}

interface Condition {
  conditionId: string;
  conditionText: string;
  result: boolean;
}

interface Results {
  id: string;
  checklistId: string;
  documentId: string;
  status: 'processing' | 'completed' | 'error';
  answers: Answer[];
  conditions: Condition[];
  createdAt: string;
  error?: string;
}

interface ResultsDisplayProps {
  results: Results;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results }) => {
  if (results.status === 'processing') {
    return (
      <div className="results-display">
        <h2>Processing Results</h2>
        <div className="status processing">Processing...</div>
      </div>
    );
  }

  if (results.status === 'error') {
    return (
      <div className="results-display">
        <h2>Processing Results</h2>
        <div className="status error">Error: {results.error}</div>
      </div>
    );
  }

  if (results.answers.length === 0 && results.conditions.length === 0) {
    return (
      <div className="results-display">
        <h2>Processing Results</h2>
        <div className="no-results">No results available</div>
      </div>
    );
  }

  return (
    <div className="results-display">
      <h2>Processing Results</h2>
      
      <div className="answers-section">
        <h3>Answers</h3>
        {results.answers.map((answer) => (
          <div key={answer.questionId} className="answer-item">
            <div className="question">{answer.questionText}</div>
            <div className="answer">{answer.answer}</div>
          </div>
        ))}
      </div>

      <div className="conditions-section">
        <h3>Conditions</h3>
        {results.conditions.map((condition) => (
          <div key={condition.conditionId} className="condition-item">
            <div className="condition-text">{condition.conditionText}</div>
            <div className={`condition-result condition-${condition.result}`}>
              {condition.result ? 'Yes' : 'No'}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
