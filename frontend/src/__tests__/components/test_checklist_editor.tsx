import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChecklistEditor } from '../../components/ChecklistEditor';

// Mock the API service
jest.mock('../../services/api', () => ({
  createChecklist: jest.fn(),
  updateChecklist: jest.fn(),
}));

describe('ChecklistEditor', () => {
  const mockOnSave = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders checklist editor form', () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByLabelText(/checklist name/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/description/i)).toBeInTheDocument();
    expect(screen.getByText(/add question/i)).toBeInTheDocument();
    expect(screen.getByText(/add condition/i)).toBeInTheDocument();
  });

  it('allows adding questions', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const addQuestionButton = screen.getByText(/add question/i);
    fireEvent.click(addQuestionButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/enter question text/i)).toBeInTheDocument();
    });
  });

  it('allows adding conditions', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const addConditionButton = screen.getByText(/add condition/i);
    fireEvent.click(addConditionButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/enter condition text/i)).toBeInTheDocument();
    });
  });

  it('validates required fields', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const saveButton = screen.getByText(/save/i);
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/name is required/i)).toBeInTheDocument();
    });
  });

  it('calls onSave with form data', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const nameInput = screen.getByLabelText(/checklist name/i);
    const descriptionInput = screen.getByLabelText(/description/i);
    const saveButton = screen.getByText(/save/i);

    fireEvent.change(nameInput, { target: { value: 'Test Checklist' } });
    fireEvent.change(descriptionInput, { target: { value: 'Test Description' } });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockOnSave).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'Test Checklist',
          description: 'Test Description',
          questions: [],
          conditions: []
        })
      );
    });
  });

  it('calls onCancel when cancel button is clicked', () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const cancelButton = screen.getByText(/cancel/i);
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
  });
});
