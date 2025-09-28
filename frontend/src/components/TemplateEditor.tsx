import React, { useState, useEffect } from 'react';
import type { Checklist, Question, Condition } from '../services/api';

interface TemplateEditorProps {
  template: Checklist | null;
  onSave: (checklist: {
    name: string;
    description: string;
    questions: Array<{ text: string; orderIndex: number }>;
    conditions: Array<{ text: string; expression?: string; orderIndex: number }>;
  }) => void;
  onCancel: () => void;
  loading?: boolean;
}

export const TemplateEditor: React.FC<TemplateEditorProps> = ({
  template,
  onSave,
  onCancel,
  loading = false
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [questions, setQuestions] = useState<Omit<Question, 'id' | 'checklistId' | 'createdAt'>[]>([]);
  const [conditions, setConditions] = useState<Omit<Condition, 'id' | 'checklistId' | 'createdAt'>[]>([]);

  useEffect(() => {
    if (template) {
      setName(template.name);
      setDescription(template.description || '');
      setQuestions(template.questions.map(q => ({
        text: q.text,
        orderIndex: q.orderIndex
      })));
      setConditions(template.conditions.map(c => ({
        text: c.text,
        orderIndex: c.orderIndex
      })));
    }
  }, [template]);

  const addQuestion = () => {
    const newQuestion = {
      text: '',
      orderIndex: questions.length + 1
    };
    setQuestions([...questions, newQuestion]);
  };

  const updateQuestion = (index: number, text: string) => {
    const updated = [...questions];
    updated[index] = { ...updated[index], text };
    setQuestions(updated);
  };

  const removeQuestion = (index: number) => {
    const updated = questions.filter((_, i) => i !== index);
    // Reorder indices
    updated.forEach((q, i) => {
      q.orderIndex = i + 1;
    });
    setQuestions(updated);
  };

  const addCondition = () => {
    const newCondition = {
      text: '',
      orderIndex: conditions.length + 1
    };
    setConditions([...conditions, newCondition]);
  };

  const updateCondition = (index: number, text: string) => {
    const updated = [...conditions];
    updated[index] = { ...updated[index], text };
    setConditions(updated);
  };

  const removeCondition = (index: number) => {
    const updated = conditions.filter((_, i) => i !== index);
    // Reorder indices
    updated.forEach((c, i) => {
      c.orderIndex = i + 1;
    });
    setConditions(updated);
  };

  const handleSave = () => {
    if (!name.trim()) {
      alert('Please enter a checklist name');
      return;
    }

    const validQuestions = questions.filter(q => q.text.trim());
    const validConditions = conditions.filter(c => c.text.trim());

    if (validQuestions.length === 0) {
      alert('Please add at least one question');
      return;
    }

    onSave({
      name: name.trim(),
      description: description.trim(),
      questions: validQuestions.map((q, index) => ({
        text: q.text,
        orderIndex: index + 1
      })),
      conditions: validConditions.map((c, index) => ({
        text: c.text,
        orderIndex: index + 1
      }))
    });
  };

  if (!template) {
    return (
      <div className="template-editor">
        <div className="no-template">
          <p>No template selected for editing</p>
        </div>
      </div>
    );
  }

  return (
    <div className="template-editor">
      <div className="editor-header">
        <h3>Edit Template: {template.name}</h3>
        <div className="editor-actions">
          <button onClick={onCancel} className="btn btn-secondary">
            Cancel
          </button>
          <button 
            onClick={handleSave} 
            className="btn btn-primary"
            disabled={loading}
          >
            {loading ? 'Saving...' : 'Save Changes'}
          </button>
        </div>
      </div>

      <div className="editor-form">
        <div className="form-section">
          <label htmlFor="checklist-name">Checklist Name</label>
          <input
            id="checklist-name"
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            placeholder="Enter checklist name"
            className="form-input"
          />
        </div>

        <div className="form-section">
          <label htmlFor="checklist-description">Description</label>
          <textarea
            id="checklist-description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            placeholder="Enter checklist description"
            className="form-textarea"
            rows={3}
          />
        </div>

        <div className="form-section">
          <div className="section-header">
            <h4>Questions ({questions.length})</h4>
            <button onClick={addQuestion} className="btn btn-small">
              Add Question
            </button>
          </div>
          <div className="items-list">
            {questions.map((question, index) => (
              <div key={index} className="item-editor">
                <div className="item-number">{index + 1}</div>
                <input
                  type="text"
                  value={question.text}
                  onChange={(e) => updateQuestion(index, e.target.value)}
                  placeholder="Enter question text"
                  className="form-input"
                />
                <button
                  onClick={() => removeQuestion(index)}
                  className="btn btn-small btn-danger"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>

        <div className="form-section">
          <div className="section-header">
            <h4>Conditions ({conditions.length})</h4>
            <button onClick={addCondition} className="btn btn-small">
              Add Condition
            </button>
          </div>
          <div className="items-list">
            {conditions.map((condition, index) => (
              <div key={index} className="item-editor">
                <div className="item-number">{index + 1}</div>
                <input
                  type="text"
                  value={condition.text}
                  onChange={(e) => updateCondition(index, e.target.value)}
                  placeholder="Enter condition text"
                  className="form-input"
                />
                <button
                  onClick={() => removeCondition(index)}
                  className="btn btn-small btn-danger"
                >
                  Remove
                </button>
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="editor-summary">
        <h4>Summary</h4>
        <div className="summary-stats">
          <div className="stat">
            <span className="stat-label">Questions:</span>
            <span className="stat-value">{questions.filter(q => q.text.trim()).length}</span>
          </div>
          <div className="stat">
            <span className="stat-label">Conditions:</span>
            <span className="stat-value">{conditions.filter(c => c.text.trim()).length}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
