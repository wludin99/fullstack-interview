import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { rest } from 'msw';
import { setupServer } from 'msw/node';
import { Home } from '../../pages/Home';

// Mock API server
const server = setupServer(
  rest.get('/api/checklists', (req, res, ctx) => {
    return res(
      ctx.json([
        {
          id: 'checklist-1',
          name: 'German Tender Checklist',
          description: 'Test checklist',
          questions: [],
          conditions: []
        }
      ])
    );
  }),
  rest.post('/api/checklists', (req, res, ctx) => {
    return res(
      ctx.status(201),
      ctx.json({
        id: 'checklist-2',
        name: 'New Checklist',
        description: 'New description',
        questions: [],
        conditions: []
      })
    );
  }),
  rest.get('/api/documents', (req, res, ctx) => {
    return res(
      ctx.json([
        {
          id: 'document-1',
          filename: 'test.pdf',
          status: 'uploaded'
        }
      ])
    );
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Integration', () => {
  it('loads checklists from API', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/german tender checklist/i)).toBeInTheDocument();
    });
  });

  it('creates new checklist via API', async () => {
    render(<Home />);

    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'New Checklist' } });
    fireEvent.change(descriptionInput, { target: { value: 'New description' } });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/new checklist/i)).toBeInTheDocument();
    });
  });

  it('loads documents from API', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/test.pdf/)).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    server.use(
      rest.get('/api/checklists', (req, res, ctx) => {
        return res(ctx.status(500), ctx.json({ error: 'Server error' }));
      })
    );

    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/error loading checklists/i)).toBeInTheDocument();
    });
  });
});
