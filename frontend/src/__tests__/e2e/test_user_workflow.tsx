import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { Home } from '../../pages/Home';

// Mock API server for E2E workflow
const server = setupServer(
  rest.get('/api/checklists', (req, res, ctx) => {
    return res(ctx.json([]));
  }),
  rest.post('/api/checklists', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 'checklist-1',
        name: 'German Tender Checklist',
        description: 'Test checklist',
        questions: [
          {
            id: 'q1',
            text: 'What is the deadline?',
            orderIndex: 1
          }
        ],
        conditions: [
          {
            id: 'c1',
            text: 'Is the document complete?',
            orderIndex: 1
          }
        ]
      })
    );
  }),
  rest.post('/api/upload', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 'document-1',
        filename: 'tender.pdf',
        status: 'uploaded'
      })
    );
  }),
  rest.post('/api/process/:checklistId', (req, res, ctx) => {
    return res(
      ctx.status(202),
      ctx.json({
        id: 'result-1',
        status: 'processing'
      })
    );
  }),
  rest.get('/api/results/:id', (req, res, ctx) => {
    return res(
      ctx.json({
        id: 'result-1',
        status: 'completed',
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
        ]
      })
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Complete User Workflow', () => {
  it('completes full user workflow: create checklist, upload document, process, view results', async () => {
    render(<Home />);

    // Step 1: Create a checklist
    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'German Tender Checklist' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test checklist' } });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/german tender checklist/i)).toBeInTheDocument();
    });

    // Step 2: Upload a document
    const file = new File(['test content'], 'tender.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/choose file/i);
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/tender.pdf/)).toBeInTheDocument();
    });

    // Step 3: Process the document
    const processButton = screen.getByText(/process document/i);
    fireEvent.click(processButton);

    await waitFor(() => {
      expect(screen.getByText(/processing/i)).toBeInTheDocument();
    });

    // Step 4: View results
    await waitFor(() => {
      expect(screen.getByText(/december 31, 2024/i)).toBeInTheDocument();
      expect(screen.getByText(/is the document complete/i)).toBeInTheDocument();
    });
  });

  it('handles workflow errors gracefully', async () => {
    server.use(
      rest.post('/api/checklists', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Server error' }));
      })
    );

    render(<Home />);

    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'Test Checklist' } });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/error creating checklist/i)).toBeInTheDocument();
    });
  });
});
