import React, { useState } from 'react';

interface Question {
  id: string;
  text: string;
  orderIndex: number;
}

interface Condition {
  id: string;
  text: string;
  orderIndex: number;
}

interface ChecklistData {
  name: string;
  description: string;
  questions: Question[];
  conditions: Condition[];
}

interface ChecklistEditorProps {
  onSave: (data: ChecklistData) => void;
  onCancel: () => void;
}

export const ChecklistEditor: React.FC<ChecklistEditorProps> = ({
  onSave,
  onCancel
}) => {
  const [name, setName] = useState('');
  const [description, setDescription] = useState('');
  const [questions, setQuestions] = useState<Question[]>([]);
  const [conditions, setConditions] = useState<Condition[]>([]);
  const [errors, setErrors] = useState<{ [key: string]: string }>({});

  const addQuestion = () => {
    const newQuestion: Question = {
      id: `q${Date.now()}`,
      text: '',
      orderIndex: questions.length + 1
    };
    setQuestions([...questions, newQuestion]);
  };

  const addCondition = () => {
    const newCondition: Condition = {
      id: `c${Date.now()}`,
      text: '',
      orderIndex: conditions.length + 1
    };
    setConditions([...conditions, newCondition]);
  };

  const updateQuestion = (id: string, text: string) => {
    setQuestions(questions.map(q => q.id === id ? { ...q, text } : q));
  };

  const updateCondition = (id: string, text: string) => {
    setConditions(conditions.map(c => c.id === id ? { ...c, text } : c));
  };

  const handleSave = () => {
    const newErrors: { [key: string]: string } = {};
    
    if (!name.trim()) {
      newErrors.name = 'Name is required';
    }

    if (Object.keys(newErrors).length > 0) {
      setErrors(newErrors);
      return;
    }

    onSave({
      name,
      description,
      questions,
      conditions
    });
  };

  return (
    <div className="checklist-editor">
      <h2>Create Checklist</h2>
      
      <div className="form-group">
        <label htmlFor="name">Checklist Name</label>
        <input
          id="name"
          type="text"
          value={name}
          onChange={(e) => setName(e.target.value)}
          placeholder="Enter checklist name"
        />
        {errors.name && <span className="error">{errors.name}</span>}
      </div>

      <div className="form-group">
        <label htmlFor="description">Description</label>
        <textarea
          id="description"
          value={description}
          onChange={(e) => setDescription(e.target.value)}
          placeholder="Enter description"
        />
      </div>

      <div className="questions-section">
        <h3>Questions</h3>
        <button type="button" onClick={addQuestion}>Add Question</button>
        {questions.map((question) => (
          <div key={question.id} className="question-item">
            <input
              type="text"
              value={question.text}
              onChange={(e) => updateQuestion(question.id, e.target.value)}
              placeholder="Enter question text"
            />
          </div>
        ))}
      </div>

      <div className="conditions-section">
        <h3>Conditions</h3>
        <button type="button" onClick={addCondition}>Add Condition</button>
        {conditions.map((condition) => (
          <div key={condition.id} className="condition-item">
            <input
              type="text"
              value={condition.text}
              onChange={(e) => updateCondition(condition.id, e.target.value)}
              placeholder="Enter condition text"
            />
          </div>
        ))}
      </div>

      <div className="actions">
        <button type="button" onClick={handleSave}>Save</button>
        <button type="button" onClick={onCancel}>Cancel</button>
      </div>
    </div>
  );
};
