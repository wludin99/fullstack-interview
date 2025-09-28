import React, { useState, useEffect } from 'react';
import type { Checklist } from '../services/api';

interface EditChecklistDialogProps {
  isOpen: boolean;
  checklist: Checklist | null;
  onClose: () => void;
  onUpdateChecklist: (id: string, name: string, description: string, questions: string[], conditions: string[]) => void;
}

export const EditChecklistDialog: React.FC<EditChecklistDialogProps> = ({
  isOpen,
  checklist,
  onClose,
  onUpdateChecklist
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [questions, setQuestions] = useState<string[]>(['']);
  const [conditions, setConditions] = useState<string[]>(['']);

  // Populate form when checklist changes
  useEffect(() => {
    if (checklist) {
      setName(checklist.name);
      setDescription(checklist.description || '');
      setQuestions(checklist.questions.length > 0 ? checklist.questions.map(q => q.text) : ['']);
      setConditions(checklist.conditions.length > 0 ? checklist.conditions.map(c => c.text) : ['']);
    }
  }, [checklist]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!checklist) return;
    
    // Filter out empty questions and conditions
    const validQuestions = questions.filter(q => q.trim() !== '');
    const validConditions = conditions.filter(c => c.trim() !== '');
    
    if (name.trim() && validQuestions.length > 0) {
      onUpdateChecklist(checklist.id, name.trim(), description.trim(), validQuestions, validConditions);
      handleClose();
    }
  };

  const handleClose = () => {
    setName('');
    setDescription('');
    setQuestions(['']);
    setConditions(['']);
    onClose();
  };

  const addQuestion = () => {
    setQuestions([...questions, '']);
  };

  const removeQuestion = (index: number) => {
    if (questions.length > 1) {
      setQuestions(questions.filter((_, i) => i !== index));
    }
  };

  const updateQuestion = (index: number, value: string) => {
    const newQuestions = [...questions];
    newQuestions[index] = value;
    setQuestions(newQuestions);
  };

  const addCondition = () => {
    setConditions([...conditions, '']);
  };

  const removeCondition = (index: number) => {
    if (conditions.length > 1) {
      setConditions(conditions.filter((_, i) => i !== index));
    }
  };

  const updateCondition = (index: number, value: string) => {
    const newConditions = [...conditions];
    newConditions[index] = value;
    setConditions(newConditions);
  };

  if (!isOpen || !checklist) return null;

  return (
    <div className="create-checklist-dialog-overlay">
      <div className="create-checklist-dialog">
        <div className="dialog-header">
          <h3>Edit Checklist</h3>
          <button onClick={handleClose} className="close-button">×</button>
        </div>

        <form onSubmit={handleSubmit} className="dialog-form">
          <div className="form-group">
            <label htmlFor="checklist-name">Checklist Name *</label>
            <input
              id="checklist-name"
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Enter checklist name"
              required
              className="form-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="checklist-description">Description</label>
            <textarea
              id="checklist-description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              placeholder="Enter checklist description (optional)"
              className="form-textarea"
              rows={3}
            />
          </div>

          <div className="form-group">
            <label>Questions *</label>
            <div className="dynamic-list">
              {questions.map((question, index) => (
                <div key={index} className="list-item">
                  <input
                    type="text"
                    value={question}
                    onChange={(e) => updateQuestion(index, e.target.value)}
                    placeholder={`Question ${index + 1}`}
                    className="form-input"
                    required
                  />
                  {questions.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeQuestion(index)}
                      className="remove-button"
                      title="Remove question"
                    >
                      ×
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addQuestion}
                className="add-button"
              >
                + Add Question
              </button>
            </div>
          </div>

          <div className="form-group">
            <label>Conditions</label>
            <div className="dynamic-list">
              {conditions.map((condition, index) => (
                <div key={index} className="list-item">
                  <input
                    type="text"
                    value={condition}
                    onChange={(e) => updateCondition(index, e.target.value)}
                    placeholder={`Condition ${index + 1}`}
                    className="form-input"
                  />
                  {conditions.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeCondition(index)}
                      className="remove-button"
                      title="Remove condition"
                    >
                      ×
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addCondition}
                className="add-button"
              >
                + Add Condition
              </button>
            </div>
          </div>

          <div className="dialog-actions">
            <button type="button" onClick={handleClose} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Update Checklist
            </button>
          </div>
        </form>
      </div>
    </div>
  );
};
