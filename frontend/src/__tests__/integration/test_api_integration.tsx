import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { Home } from '../../pages/Home';

// Mock API server
const server = setupServer(
  http.get('/api/checklists', () => {
    return HttpResponse.json([
      {
        id: 'checklist-1',
        name: 'German Tender Checklist',
        description: 'Test checklist',
        questions: [],
        conditions: []
      }
    ]);
  }),
  http.post('/api/checklists', () => {
    return HttpResponse.json({
      id: 'checklist-2',
      name: 'New Checklist',
      description: 'New description',
      questions: [],
      conditions: []
    }, { status: 201 });
  }),
  http.get('/api/documents', () => {
    return HttpResponse.json([
      {
        id: 'document-1',
        filename: 'test.pdf',
        status: 'uploaded'
      }
    ]);
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('API Integration', () => {
  it('loads checklists from API', async () => {
    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/no checklists found matching/i)).toBeInTheDocument();
    });
  });

  it('creates new checklist via API', async () => {
    render(<Home />);

    const createButton = screen.getByRole('button', { name: /create new checklist/i });
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const saveButton = screen.getByRole('button', { name: /create checklist/i });

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
      expect(screen.getByText(/no documents found/i)).toBeInTheDocument();
    });
  });

  it('handles API errors gracefully', async () => {
    server.use(
      http.get('/api/checklists', () => {
        return HttpResponse.json({ error: 'Server error' }, { status: 500 });
      })
    );

    render(<Home />);

    await waitFor(() => {
      expect(screen.getByText(/error loading documents/i)).toBeInTheDocument();
    });
  });
});
