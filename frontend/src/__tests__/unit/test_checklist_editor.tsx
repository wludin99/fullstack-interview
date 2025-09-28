/** @jest-environment jsdom */
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ChecklistEditor } from '../../components/ChecklistEditor';

// Mock the API service
jest.mock('../../services/api', () => ({
  api: {
    createChecklist: jest.fn(),
    updateChecklist: jest.fn(),
  }
}));

describe('ChecklistEditor', () => {
  const mockOnSave = jest.fn();
  const mockOnCancel = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render checklist editor form', () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByText('Create Checklist')).toBeInTheDocument();
    expect(screen.getByLabelText('Checklist Name')).toBeInTheDocument();
    expect(screen.getByLabelText('Description')).toBeInTheDocument();
    expect(screen.getByText('Add Question')).toBeInTheDocument();
    expect(screen.getByText('Add Condition')).toBeInTheDocument();
  });

  it('should render with empty form initially', () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    expect(screen.getByPlaceholderText('Enter checklist name')).toBeInTheDocument();
    expect(screen.getByPlaceholderText('Enter description')).toBeInTheDocument();
  });

  it('should add new question when Add Question is clicked', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const addQuestionButton = screen.getByText('Add Question');
    fireEvent.click(addQuestionButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Enter question text')).toBeInTheDocument();
    });
  });

  it('should add new condition when Add Condition is clicked', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const addConditionButton = screen.getByText('Add Condition');
    fireEvent.click(addConditionButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Enter condition text')).toBeInTheDocument();
    });
  });

  it('should add and update question text', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    // Add a question first
    const addButton = screen.getByText('Add Question');
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Enter question text')).toBeInTheDocument();
    });

    // Update question text
    const questionInput = screen.getByPlaceholderText('Enter question text');
    fireEvent.change(questionInput, { target: { value: 'Test question?' } });

    expect(questionInput).toHaveValue('Test question?');
  });

  it('should add and update condition text', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    // Add a condition first
    const addButton = screen.getByText('Add Condition');
    fireEvent.click(addButton);

    await waitFor(() => {
      expect(screen.getByPlaceholderText('Enter condition text')).toBeInTheDocument();
    });

    // Update condition text
    const conditionInput = screen.getByPlaceholderText('Enter condition text');
    fireEvent.change(conditionInput, { target: { value: 'Test condition' } });

    expect(conditionInput).toHaveValue('Test condition');
  });

  it('should update question text when input changes', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    // Add a question first
    const addQuestionButton = screen.getByText('Add Question');
    fireEvent.click(addQuestionButton);

    await waitFor(() => {
      const questionInput = screen.getByPlaceholderText('Enter question text');
      fireEvent.change(questionInput, { target: { value: 'New question?' } });
      expect(questionInput).toHaveValue('New question?');
    });
  });

  it('should update condition text when input changes', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    // Add a condition first
    const addConditionButton = screen.getByText('Add Condition');
    fireEvent.click(addConditionButton);

    await waitFor(() => {
      const conditionInput = screen.getByPlaceholderText('Enter condition text');
      fireEvent.change(conditionInput, { target: { value: 'New condition' } });
      expect(conditionInput).toHaveValue('New condition');
    });
  });

  it('should call onSave with checklist data when Save is clicked', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    // Fill in the form
    const nameInput = screen.getByLabelText('Checklist Name');
    const descriptionInput = screen.getByLabelText('Description');
    
    fireEvent.change(nameInput, { target: { value: 'New Checklist' } });
    fireEvent.change(descriptionInput, { target: { value: 'New description' } });

    // Add a question
    const addQuestionButton = screen.getByText('Add Question');
    fireEvent.click(addQuestionButton);

    await waitFor(() => {
      const questionInput = screen.getByPlaceholderText('Enter question text');
      fireEvent.change(questionInput, { target: { value: 'New question?' } });
    });

    // Save
    const saveButton = screen.getByText('Save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(mockOnSave).toHaveBeenCalledWith(
        expect.objectContaining({
          name: 'New Checklist',
          description: 'New description',
          questions: expect.arrayContaining([
            expect.objectContaining({
              text: 'New question?'
            })
          ])
        })
      );
    });
  });

  it('should call onCancel when Cancel is clicked', () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const cancelButton = screen.getByText('Cancel');
    fireEvent.click(cancelButton);

    expect(mockOnCancel).toHaveBeenCalled();
  });

  it('should validate required fields', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    const saveButton = screen.getByText('Save');
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText('Name is required')).toBeInTheDocument();
    });
  });

  it('should handle German tender examples', async () => {
    render(
      <ChecklistEditor
        onSave={mockOnSave}
        onCancel={mockOnCancel}
      />
    );

    // Add German question
    const addQuestionButton = screen.getByText('Add Question');
    fireEvent.click(addQuestionButton);

    await waitFor(() => {
      const questionInput = screen.getByPlaceholderText('Enter question text');
      fireEvent.change(questionInput, { 
        target: { value: 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?' } 
      });
    });

    // Add German condition
    const addConditionButton = screen.getByText('Add Condition');
    fireEvent.click(addConditionButton);

    await waitFor(() => {
      const conditionInput = screen.getByPlaceholderText('Enter condition text');
      fireEvent.change(conditionInput, { 
        target: { value: 'Ist die Abgabefrist vor dem 31.12.2025?' } 
      });
    });

    expect(screen.getByDisplayValue('In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?')).toBeInTheDocument();
    expect(screen.getByDisplayValue('Ist die Abgabefrist vor dem 31.12.2025?')).toBeInTheDocument();
  });
});
