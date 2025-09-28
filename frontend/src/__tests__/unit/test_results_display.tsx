/** @jest-environment jsdom */
import { render, screen } from '@testing-library/react';
import { ResultsDisplay } from '../../components/ResultsDisplay';

describe('ResultsDisplay', () => {
  const mockResults = {
    id: '1',
    checklistId: 'checklist1',
    documentId: 'document1',
    status: 'completed' as const,
    answers: [
      {
        questionId: 'question1',
        questionText: 'Test question 1?',
        answer: 'Test answer 1'
      },
      {
        questionId: 'question2',
        questionText: 'Test question 2?',
        answer: 'Test answer 2'
      }
    ],
    conditions: [
      {
        conditionId: 'condition1',
        conditionText: 'Test condition 1',
        result: true
      },
      {
        conditionId: 'condition2',
        conditionText: 'Test condition 2',
        result: false
      }
    ],
    createdAt: '2024-01-01T00:00:00Z'
  };


  it('should render results display with answers and conditions', () => {
    render(
      <ResultsDisplay
        results={mockResults}
      />
    );

    expect(screen.getByText('Processing Results')).toBeInTheDocument();
  });

  it('should display answers section', () => {
    render(
      <ResultsDisplay
        results={mockResults}
      />
    );

    expect(screen.getByText('Answers')).toBeInTheDocument();
    expect(screen.getByText('Test question 1?')).toBeInTheDocument();
    expect(screen.getByText('Test answer 1')).toBeInTheDocument();
    expect(screen.getByText('Test question 2?')).toBeInTheDocument();
    expect(screen.getByText('Test answer 2')).toBeInTheDocument();
  });

  it('should display conditions section', () => {
    render(
      <ResultsDisplay
        results={mockResults}
      />
    );

    expect(screen.getByText('Conditions')).toBeInTheDocument();
    expect(screen.getByText('Test condition 1')).toBeInTheDocument();
    expect(screen.getByText('Test condition 2')).toBeInTheDocument();
  });

  it('should display answers and conditions correctly', () => {
    render(
      <ResultsDisplay
        results={mockResults}
      />
    );

    expect(screen.getByText('Test question 1?')).toBeInTheDocument();
    expect(screen.getByText('Test answer 1')).toBeInTheDocument();
    expect(screen.getByText('Test question 2?')).toBeInTheDocument();
    expect(screen.getByText('Test answer 2')).toBeInTheDocument();
    expect(screen.getByText('Test condition 1')).toBeInTheDocument();
    expect(screen.getByText('Test condition 2')).toBeInTheDocument();
  });

  it('should display condition results with correct styling', () => {
    render(
      <ResultsDisplay
        results={mockResults}
      />
    );

    const trueResult = screen.getByText('Yes');
    const falseResult = screen.getByText('No');

    expect(trueResult).toBeInTheDocument();
    expect(falseResult).toBeInTheDocument();
  });

  it('should handle empty results', () => {
    const emptyResults = {
      id: '1',
      checklistId: 'checklist1',
      documentId: 'document1',
      status: 'completed' as const,
      answers: [],
      conditions: [],
      createdAt: '2024-01-01T00:00:00Z'
    };

    render(
      <ResultsDisplay
        results={emptyResults}
      />
    );

    expect(screen.getByText('No results available')).toBeInTheDocument();
  });

  it('should handle error status', () => {
    const errorResults = {
      id: '1',
      checklistId: 'checklist1',
      documentId: 'document1',
      status: 'error' as const,
      error: 'Processing failed',
      answers: [],
      conditions: [],
      createdAt: '2024-01-01T00:00:00Z'
    };

    render(
      <ResultsDisplay
        results={errorResults}
      />
    );

    expect(screen.getByText('Processing Results')).toBeInTheDocument();
    expect(screen.getByText('Error: Processing failed')).toBeInTheDocument();
  });

  it('should handle processing status', () => {
    const processingResults = {
      id: '1',
      checklistId: 'checklist1',
      documentId: 'document1',
      status: 'processing' as const,
      answers: [],
      conditions: [],
      createdAt: '2024-01-01T00:00:00Z'
    };

    render(
      <ResultsDisplay
        results={processingResults}
      />
    );

    expect(screen.getByText('Processing Results')).toBeInTheDocument();
    expect(screen.getByText('Processing...')).toBeInTheDocument();
  });

  it('should display German tender examples', () => {
    const germanResults = {
      id: '1',
      checklistId: 'checklist1',
      documentId: 'document1',
      status: 'completed' as const,
      answers: [
        {
          questionId: 'question1',
          questionText: 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?',
          answer: 'Die Angebote sind in elektronischer Form einzureichen'
        }
      ],
      conditions: [
        {
          conditionId: 'condition1',
          conditionText: 'Ist die Abgabefrist vor dem 31.12.2025?',
          result: true
        }
      ],
      createdAt: '2024-01-01T00:00:00Z'
    };

    render(
      <ResultsDisplay
        results={germanResults}
      />
    );

    expect(screen.getByText('In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?')).toBeInTheDocument();
    expect(screen.getByText('Die Angebote sind in elektronischer Form einzureichen')).toBeInTheDocument();
    expect(screen.getByText('Ist die Abgabefrist vor dem 31.12.2025?')).toBeInTheDocument();
  });

  it('should handle missing confidence scores', () => {
    const resultsWithoutConfidence = {
      id: '1',
      checklistId: 'checklist1',
      documentId: 'document1',
      status: 'completed' as const,
      answers: [
        {
          questionId: 'question1',
          questionText: 'Test question?',
          answer: 'Test answer'
        }
      ],
      conditions: [
        {
          conditionId: 'condition1',
          conditionText: 'Test condition',
          result: true
        }
      ],
      createdAt: '2024-01-01T00:00:00Z'
    };

    render(
      <ResultsDisplay
        results={resultsWithoutConfidence}
      />
    );

    expect(screen.getByText('Test question?')).toBeInTheDocument();
    expect(screen.getByText('Test answer')).toBeInTheDocument();
    expect(screen.getByText('Test condition')).toBeInTheDocument();
    expect(screen.getByText('Yes')).toBeInTheDocument();
  });

  it('should display document information correctly', () => {
    render(
      <ResultsDisplay
        results={mockResults}
      />
    );

    expect(screen.getByText('Document: test.pdf')).toBeInTheDocument();
    expect(screen.getByText('Original Name: Test Document.pdf')).toBeInTheDocument();
    expect(screen.getByText('File Size: 1.0 MB')).toBeInTheDocument();
  });

  it('should handle different file sizes', () => {
    const mockResultsWithLargeFile = {
      ...mockResults,
      documentId: 'document1',
      document: {
        id: 'document1',
        filename: 'test.pdf',
        original_name: 'Test Document.pdf',
        file_path: '/uploads/test.pdf',
        file_size: 50 * 1024 * 1024, // 50MB
        status: 'processed'
      }
    };

    render(
      <ResultsDisplay
        results={mockResultsWithLargeFile}
      />
    );

    expect(screen.getByText('File Size: 50.0 MB')).toBeInTheDocument();
  });

  it('should handle small file sizes', () => {
    const mockResultsWithSmallFile = {
      ...mockResults,
      documentId: 'document1',
      document: {
        id: 'document1',
        filename: 'test.pdf',
        original_name: 'Test Document.pdf',
        file_path: '/uploads/test.pdf',
        file_size: 512, // 512 bytes
        status: 'processed'
      }
    };

    render(
      <ResultsDisplay
        results={mockResultsWithSmallFile}
      />
    );

    expect(screen.getByText('File Size: 0.0 MB')).toBeInTheDocument();
  });
});
