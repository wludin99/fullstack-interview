import { render, screen } from '@testing-library/react';
import { ResultsDisplay } from '../../components/ResultsDisplay';

describe('ResultsDisplay', () => {
  const mockResults = {
    id: 'result-123',
    checklistId: 'checklist-123',
    documentId: 'document-123',
    status: 'completed' as const,
    answers: [
      {
        questionId: 'q1',
        questionText: 'What is the deadline?',
        answer: 'December 31, 2024'
      }
    ],
    conditions: [
      {
        conditionId: 'c1',
        conditionText: 'Is the document complete?',
        result: true
      }
    ],
    createdAt: '2024-01-28T10:00:00Z'
  };

  it('renders results display', () => {
    render(<ResultsDisplay results={mockResults} />);

    expect(screen.getByText(/processing results/i)).toBeInTheDocument();
    expect(screen.getByText(/what is the deadline/i)).toBeInTheDocument();
    expect(screen.getByText(/december 31, 2024/i)).toBeInTheDocument();
    expect(screen.getByText(/is the document complete/i)).toBeInTheDocument();
  });

  it('shows processing status', () => {
    const processingResults = {
      ...mockResults,
      status: 'processing' as const
    };

    render(<ResultsDisplay results={processingResults} />);

    expect(screen.getByText(/processing/i)).toBeInTheDocument();
  });

  it('shows error status', () => {
    const errorResults = {
      ...mockResults,
      status: 'error' as const,
      error: 'Processing failed'
    };

    render(<ResultsDisplay results={errorResults} />);

    expect(screen.getByText(/error/i)).toBeInTheDocument();
    expect(screen.getByText(/processing failed/i)).toBeInTheDocument();
  });

  it('displays condition results correctly', () => {
    render(<ResultsDisplay results={mockResults} />);

    const conditionResult = screen.getByText(/is the document complete/i).closest('div');
    expect(conditionResult).toHaveClass('condition-true'); // Assuming CSS class for styling
  });

  it('handles empty results', () => {
    const emptyResults = {
      ...mockResults,
      answers: [],
      conditions: []
    };

    render(<ResultsDisplay results={emptyResults} />);

    expect(screen.getByText(/no results available/i)).toBeInTheDocument();
  });
});
