import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { setupServer } from 'msw/node';
import { http, HttpResponse } from 'msw';
import { Home } from '../../pages/Home';

// Mock API responses
const server = setupServer(
  // Mock checklists endpoint
  http.get('/api/checklists', () => {
    return HttpResponse.json([
      {
        id: '1',
        name: 'German Tender Template',
        description: 'Standard German tender checklist',
        questions: [
          { id: 'q1', text: 'Question 1', orderIndex: 1 },
          { id: 'q2', text: 'Question 2', orderIndex: 2 }
        ],
        conditions: [
          { id: 'c1', text: 'Condition 1', orderIndex: 1 }
        ]
      }
    ]);
  }),

  // Mock documents endpoint
  http.get('/api/documents', () => {
    return HttpResponse.json([
      {
        id: 'doc1',
        filename: 'document1.pdf',
        status: 'uploaded'
      },
      {
        id: 'doc2',
        filename: 'document2.pdf',
        status: 'uploaded'
      }
    ]);
  }),

  // Mock file upload endpoint
  http.post('/api/upload', () => {
    return HttpResponse.json({
      id: 'new-doc',
      filename: 'new-document.pdf',
      status: 'uploaded',
      message: 'Document uploaded successfully'
    });
  }),

  // Mock batch processing endpoint
  http.post('/api/batch/process/:checklistId', () => {
    return HttpResponse.json({
      id: 'batch-1',
      status: 'completed',
      message: 'Batch processing completed: 2 successful, 0 failed',
      results: [
        {
          id: 'result1',
          document_id: 'doc1',
          status: 'completed',
          error: null
        },
        {
          id: 'result2',
          document_id: 'doc2',
          status: 'completed',
          error: null
        }
      ]
    });
  })
);

// Setup and teardown
beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Batch Workflow Integration', () => {
  it('completes full batch processing workflow', async () => {
    render(<Home />);

    // Wait for initial data to load
    await waitFor(() => {
      expect(screen.getByText('Batch Document Processing')).toBeInTheDocument();
    });

    // Step 1: Upload documents (simulate file upload)
    const fileInput = screen.getByLabelText(/choose file/i);
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText('1 document(s) uploaded')).toBeInTheDocument();
    });

    // Step 2: Select documents for batch processing
    const selectAllButton = screen.getByText('Select All');
    fireEvent.click(selectAllButton);

    await waitFor(() => {
      expect(screen.getByText('Ready to process 1 document(s)')).toBeInTheDocument();
    });

    // Step 3: Choose checklist
    const checklistDropdown = screen.getByText('Select a checklist...');
    fireEvent.click(checklistDropdown);

    await waitFor(() => {
      expect(screen.getByText('German Tender Template')).toBeInTheDocument();
    });

    const checklistOption = screen.getByText('German Tender Template');
    fireEvent.click(checklistOption);

    // Step 4: Process documents
    const processButton = screen.getByText(/Process 1 Document\(s\)/);
    fireEvent.click(processButton);

    // Wait for processing to complete
    await waitFor(() => {
      expect(screen.getByText('Batch processing completed: 2 successful, 0 failed')).toBeInTheDocument();
    }, { timeout: 5000 });
  });

  it('handles batch processing errors gracefully', async () => {
    // Mock error response
    server.use(
      http.post('/api/batch/process/:checklistId', () => {
        return HttpResponse.json({
          id: 'batch-error',
          status: 'error',
          message: 'Batch processing failed: API error',
          results: []
        }, { status: 400 });
      })
    );

    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Batch Document Processing')).toBeInTheDocument();
    });

    // Complete workflow setup
    const fileInput = screen.getByLabelText(/choose file/i);
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      const selectAllButton = screen.getByText('Select All');
      fireEvent.click(selectAllButton);
    });

    await waitFor(() => {
      const checklistDropdown = screen.getByText('Select a checklist...');
      fireEvent.click(checklistDropdown);
    });

    await waitFor(() => {
      const checklistOption = screen.getByText('German Tender Template');
      fireEvent.click(checklistOption);
    });

    // Attempt processing
    const processButton = screen.getByText(/Process 1 Document\(s\)/);
    fireEvent.click(processButton);

    // Should show error message
    await waitFor(() => {
      expect(screen.getByText(/Batch processing failed/)).toBeInTheDocument();
    });
  });

  it('allows template modification during workflow', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Batch Document Processing')).toBeInTheDocument();
    });

    // Select checklist
    const checklistDropdown = screen.getByText('Select a checklist...');
    fireEvent.click(checklistDropdown);

    await waitFor(() => {
      const checklistOption = screen.getByText('German Tender Template');
      fireEvent.click(checklistOption);
    });

    // Should show template editor option
    await waitFor(() => {
      expect(screen.getByText('Edit')).toBeInTheDocument();
    });

    // Click edit to modify template
    const editButton = screen.getByText('Edit');
    fireEvent.click(editButton);

    // Should show template editor
    await waitFor(() => {
      expect(screen.getByText('Edit Template: German Tender Template')).toBeInTheDocument();
    });
  });

  it('displays batch results with export functionality', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Batch Document Processing')).toBeInTheDocument();
    });

    // Complete workflow
    const fileInput = screen.getByLabelText(/choose file/i);
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      const selectAllButton = screen.getByText('Select All');
      fireEvent.click(selectAllButton);
    });

    await waitFor(() => {
      const checklistDropdown = screen.getByText('Select a checklist...');
      fireEvent.click(checklistDropdown);
    });

    await waitFor(() => {
      const checklistOption = screen.getByText('German Tender Template');
      fireEvent.click(checklistOption);
    });

    const processButton = screen.getByText(/Process 1 Document\(s\)/);
    fireEvent.click(processButton);

    // Wait for results
    await waitFor(() => {
      expect(screen.getByText('Batch processing completed: 2 successful, 0 failed')).toBeInTheDocument();
    });

    // Should show export button
    await waitFor(() => {
      expect(screen.getByText('Export Results')).toBeInTheDocument();
    });
  });

  it('handles multiple document selection and filtering', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText('Batch Document Processing')).toBeInTheDocument();
    });

    // Should show document list
    await waitFor(() => {
      expect(screen.getByText('document1.pdf')).toBeInTheDocument();
      expect(screen.getByText('document2.pdf')).toBeInTheDocument();
    });

    // Test filtering
    const filterInput = screen.getByPlaceholderText('Filter documents...');
    fireEvent.change(filterInput, { target: { value: 'document1' } });

    await waitFor(() => {
      expect(screen.getByText('document1.pdf')).toBeInTheDocument();
      expect(screen.queryByText('document2.pdf')).not.toBeInTheDocument();
    });

    // Test individual selection
    const documentCheckbox = screen.getByLabelText(/document1\.pdf/);
    fireEvent.click(documentCheckbox);

    await waitFor(() => {
      expect(screen.getByText('1 of 2 selected')).toBeInTheDocument();
    });
  });
});
