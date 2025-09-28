/** @jest-environment jsdom */
import React from 'react';
import { render, screen } from '@testing-library/react';
import { ResultsDisplay } from '../../components/ResultsDisplay';

describe('ResultsDisplay', () => {
  const mockResults = {
    id: '1',
    checklist_id: 'checklist1',
    document_id: 'document1',
    status: 'completed',
    answers: [
      {
        id: 'answer1',
        question_id: 'question1',
        question_text: 'Test question 1?',
        answer_text: 'Test answer 1',
        confidence: 0.95
      },
      {
        id: 'answer2',
        question_id: 'question2',
        question_text: 'Test question 2?',
        answer_text: 'Test answer 2',
        confidence: 0.88
      }
    ],
    condition_results: [
      {
        id: 'condition1',
        condition_id: 'condition1',
        condition_text: 'Test condition 1',
        result: true,
        confidence: 0.92
      },
      {
        id: 'condition2',
        condition_id: 'condition2',
        condition_text: 'Test condition 2',
        result: false,
        confidence: 0.85
      }
    ]
  };

  const mockDocument = {
    id: 'document1',
    filename: 'test.pdf',
    original_name: 'Test Document.pdf',
    file_path: '/uploads/test.pdf',
    file_size: 1024000,
    status: 'processed'
  };

  it('should render results display with answers and conditions', () => {
    render(
      <ResultsDisplay
        results={mockResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('Processing Results')).toBeInTheDocument();
    expect(screen.getByText('Document: test.pdf')).toBeInTheDocument();
    expect(screen.getByText('Status: completed')).toBeInTheDocument();
  });

  it('should display answers section', () => {
    render(
      <ResultsDisplay
        results={mockResults}
        document={mockDocument}
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
        document={mockDocument}
      />
    );

    expect(screen.getByText('Conditions')).toBeInTheDocument();
    expect(screen.getByText('Test condition 1')).toBeInTheDocument();
    expect(screen.getByText('Test condition 2')).toBeInTheDocument();
  });

  it('should display confidence scores when available', () => {
    render(
      <ResultsDisplay
        results={mockResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('95%')).toBeInTheDocument();
    expect(screen.getByText('88%')).toBeInTheDocument();
    expect(screen.getByText('92%')).toBeInTheDocument();
    expect(screen.getByText('85%')).toBeInTheDocument();
  });

  it('should display condition results with correct styling', () => {
    render(
      <ResultsDisplay
        results={mockResults}
        document={mockDocument}
      />
    );

    const trueResult = screen.getByText('✓');
    const falseResult = screen.getByText('✗');

    expect(trueResult).toBeInTheDocument();
    expect(falseResult).toBeInTheDocument();
  });

  it('should handle empty results', () => {
    const emptyResults = {
      id: '1',
      checklist_id: 'checklist1',
      document_id: 'document1',
      status: 'completed',
      answers: [],
      condition_results: []
    };

    render(
      <ResultsDisplay
        results={emptyResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('No answers found')).toBeInTheDocument();
    expect(screen.getByText('No conditions found')).toBeInTheDocument();
  });

  it('should handle error status', () => {
    const errorResults = {
      id: '1',
      checklist_id: 'checklist1',
      document_id: 'document1',
      status: 'error',
      error_message: 'Processing failed',
      answers: [],
      condition_results: []
    };

    render(
      <ResultsDisplay
        results={errorResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('Status: error')).toBeInTheDocument();
    expect(screen.getByText('Error: Processing failed')).toBeInTheDocument();
  });

  it('should handle processing status', () => {
    const processingResults = {
      id: '1',
      checklist_id: 'checklist1',
      document_id: 'document1',
      status: 'processing',
      answers: [],
      condition_results: []
    };

    render(
      <ResultsDisplay
        results={processingResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('Status: processing')).toBeInTheDocument();
    expect(screen.getByText('Processing in progress...')).toBeInTheDocument();
  });

  it('should display German tender examples', () => {
    const germanResults = {
      id: '1',
      checklist_id: 'checklist1',
      document_id: 'document1',
      status: 'completed',
      answers: [
        {
          id: 'answer1',
          question_id: 'question1',
          question_text: 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?',
          answer_text: 'Die Angebote sind in elektronischer Form einzureichen',
          confidence: 0.95
        }
      ],
      condition_results: [
        {
          id: 'condition1',
          condition_id: 'condition1',
          condition_text: 'Ist die Abgabefrist vor dem 31.12.2025?',
          result: true,
          confidence: 0.92
        }
      ]
    };

    render(
      <ResultsDisplay
        results={germanResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?')).toBeInTheDocument();
    expect(screen.getByText('Die Angebote sind in elektronischer Form einzureichen')).toBeInTheDocument();
    expect(screen.getByText('Ist die Abgabefrist vor dem 31.12.2025?')).toBeInTheDocument();
  });

  it('should handle missing confidence scores', () => {
    const resultsWithoutConfidence = {
      id: '1',
      checklist_id: 'checklist1',
      document_id: 'document1',
      status: 'completed',
      answers: [
        {
          id: 'answer1',
          question_id: 'question1',
          question_text: 'Test question?',
          answer_text: 'Test answer'
        }
      ],
      condition_results: [
        {
          id: 'condition1',
          condition_id: 'condition1',
          condition_text: 'Test condition',
          result: true
        }
      ]
    };

    render(
      <ResultsDisplay
        results={resultsWithoutConfidence}
        document={mockDocument}
      />
    );

    expect(screen.getByText('Test question?')).toBeInTheDocument();
    expect(screen.getByText('Test answer')).toBeInTheDocument();
    expect(screen.getByText('Test condition')).toBeInTheDocument();
    expect(screen.getByText('✓')).toBeInTheDocument();
  });

  it('should display document information correctly', () => {
    render(
      <ResultsDisplay
        results={mockResults}
        document={mockDocument}
      />
    );

    expect(screen.getByText('Document: test.pdf')).toBeInTheDocument();
    expect(screen.getByText('Original Name: Test Document.pdf')).toBeInTheDocument();
    expect(screen.getByText('File Size: 1.0 MB')).toBeInTheDocument();
  });

  it('should handle different file sizes', () => {
    const largeDocument = {
      ...mockDocument,
      file_size: 50 * 1024 * 1024 // 50MB
    };

    render(
      <ResultsDisplay
        results={mockResults}
        document={largeDocument}
      />
    );

    expect(screen.getByText('File Size: 50.0 MB')).toBeInTheDocument();
  });

  it('should handle small file sizes', () => {
    const smallDocument = {
      ...mockDocument,
      file_size: 512 // 512 bytes
    };

    render(
      <ResultsDisplay
        results={mockResults}
        document={smallDocument}
      />
    );

    expect(screen.getByText('File Size: 0.0 MB')).toBeInTheDocument();
  });
});
