import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { http, HttpResponse } from 'msw';
import { setupServer } from 'msw/node';
import { Home } from '../../pages/Home';

// Mock API server for German tender workflow
const server = setupServer(
  http.get('/api/checklists', () => {
    return HttpResponse.json([]);
  }),
  http.post('/api/checklists', () => {
    return HttpResponse.json({
      id: 'checklist-1',
      name: 'Deutsche Ausschreibung Checkliste',
      description: 'Standard-Checkliste für deutsche öffentliche Ausschreibungen',
      questions: [
        {
          id: 'q1',
            text: 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?',
            orderIndex: 1
          },
          {
            id: 'q2',
            text: 'Wann ist die Frist für die Einreichung von Bieterfragen?',
            orderIndex: 2
          }
        ],
        conditions: [
          {
            id: 'c1',
            text: 'Ist das Angebot vollständig und fristgerecht eingegangen?',
            orderIndex: 1
          }
        ]
      });
  }),
  http.post('/api/upload', () => {
    return HttpResponse.json({
      id: 'document-1',
      filename: 'Bewerbungsbedingungen.pdf',
      status: 'uploaded'
    }, { status: 201 });
  }),
  http.post('/api/process/:checklistId', () => {
    return HttpResponse.json({
      id: 'result-1',
      status: 'processing'
    }, { status: 202 });
  }),
  http.get('/api/results/:id', () => {
    return HttpResponse.json({
      id: 'result-1',
      status: 'completed',
      answers: [
        {
          questionId: 'q1',
          questionText: 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?',
          answer: 'Elektronisch über das Vergabeportal'
        },
        {
          questionId: 'q2',
          questionText: 'Wann ist die Frist für die Einreichung von Bieterfragen?',
          answer: 'Bis zum 15. März 2024, 12:00 Uhr'
        }
      ],
      conditions: [
        {
          conditionId: 'c1',
          conditionText: 'Ist das Angebot vollständig und fristgerecht eingegangen?',
          result: true
        }
      ]
    });
  })
);

beforeAll(() => server.listen());
afterEach(() => server.resetHandlers());
afterAll(() => server.close());

describe('Complete German Tender Workflow', () => {
  it('completes full German tender document processing workflow', async () => {
    render(<Home />);

    // Step 1: Create German tender checklist
    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'Deutsche Ausschreibung Checkliste' } });
    fireEvent.change(descriptionInput, { target: { value: 'Standard-Checkliste für deutsche öffentliche Ausschreibungen' } });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/deutsche ausschreibung checkliste/i)).toBeInTheDocument();
    });

    // Step 2: Upload German tender document
    const file = new File(['german tender content'], 'Bewerbungsbedingungen.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/choose file/i);
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/bewerbungsbedingungen.pdf/i)).toBeInTheDocument();
    });

    // Step 3: Process the German document
    const processButton = screen.getByText(/process document/i);
    fireEvent.click(processButton);

    await waitFor(() => {
      expect(screen.getByText(/processing/i)).toBeInTheDocument();
    });

    // Step 4: View German language results
    await waitFor(() => {
      expect(screen.getByText(/elektronisch über das vergabeportal/i)).toBeInTheDocument();
      expect(screen.getByText(/bis zum 15\. märz 2024/i)).toBeInTheDocument();
      expect(screen.getByText(/ist das angebot vollständig/i)).toBeInTheDocument();
    });
  });

  it('handles German tender terminology correctly', async () => {
    render(<Home />);

    // Create checklist with German terminology
    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    fireEvent.change(nameInput, { target: { value: 'Deutsche Ausschreibung' } });

    // Add German questions
    const addQuestionButton = screen.getByText(/add question/i);
    fireEvent.click(addQuestionButton);

    await waitFor(() => {
      const questionInput = screen.getByPlaceholderText(/enter question text/i);
      fireEvent.change(questionInput, { target: { value: 'Wer ist der Auftraggeber?' } });
    });

    // Add German conditions
    const addConditionButton = screen.getByText(/add condition/i);
    fireEvent.click(addConditionButton);

    await waitFor(() => {
      const conditionInput = screen.getByPlaceholderText(/enter condition text/i);
      fireEvent.change(conditionInput, { target: { value: 'Sind alle Eignungsnachweise vorhanden?' } });
    });

    const saveButton = screen.getByText(/save/i);
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/deutsche ausschreibung/i)).toBeInTheDocument();
    });
  });

  it('validates German document processing performance', async () => {
    const startTime = Date.now();
    
    render(<Home />);

    // Create checklist
    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'Performance Test' } });
    fireEvent.click(saveButton);

    // Upload document
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const fileInput = screen.getByLabelText(/choose file/i);
    fireEvent.change(fileInput, { target: { files: [file] } });

    // Process document
    const processButton = screen.getByText(/process document/i);
    fireEvent.click(processButton);

    const endTime = Date.now();
    const processingTime = endTime - startTime;

    // Should complete within reasonable time (30 seconds = 30000ms)
    expect(processingTime).toBeLessThan(30000);
  });

  it('handles German tender document errors gracefully', async () => {
    server.use(
      http.post('/api/upload', () => {
        return HttpResponse.json({ error: 'Invalid file format' }, { status: 400 });
      })
    );

    render(<Home />);

    const file = new File(['invalid content'], 'test.txt', { type: 'text/plain' });
    const fileInput = screen.getByLabelText(/choose file/i);
    fireEvent.change(fileInput, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/invalid file type/i)).toBeInTheDocument();
    });
  });

  it('processes multiple German tender documents', async () => {
    render(<Home />);

    // Create checklist
    const createButton = screen.getByText(/create checklist/i);
    fireEvent.click(createButton);

    const nameInput = screen.getByLabelText(/checklist name/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'Multi-Document Test' } });
    fireEvent.click(saveButton);

    // Upload multiple documents
    const file1 = new File(['content1'], 'Bewerbungsbedingungen.pdf', { type: 'application/pdf' });
    const file2 = new File(['content2'], 'Fragebogen.pdf', { type: 'application/pdf' });
    
    const fileInput = screen.getByLabelText(/choose file/i);
    fireEvent.change(fileInput, { target: { files: [file1, file2] } });

    await waitFor(() => {
      expect(screen.getByText(/bewerbungsbedingungen.pdf/i)).toBeInTheDocument();
      expect(screen.getByText(/fragebogen.pdf/i)).toBeInTheDocument();
    });
  });
});
