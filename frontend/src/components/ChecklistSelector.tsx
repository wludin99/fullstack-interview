import React, { useState } from 'react';
import type { Checklist } from '../services/api';

interface ChecklistSelectorProps {
  checklists: Checklist[];
  selectedChecklistId: string | null;
  onChecklistSelect: (checklistId: string) => void;
  onTemplateSelect: (templateId: string) => void;
  onCreateChecklist: () => void;
  onEditChecklist: (checklistId: string) => void;
  onDeleteChecklist: (checklistId: string, checklistName: string) => void;
  loading?: boolean;
}

export const ChecklistSelector: React.FC<ChecklistSelectorProps> = ({
  checklists,
  selectedChecklistId,
  onChecklistSelect,
  onTemplateSelect,
  onCreateChecklist,
  onEditChecklist,
  onDeleteChecklist
}) => {
  const [filter, setFilter] = useState('');

  // Separate templates from custom checklists
  const templates = checklists.filter(c => c.name.includes('Template') || c.name.includes('Standard'));
  const customChecklists = checklists.filter(c => !c.name.includes('Template') && !c.name.includes('Standard'));

  const filteredTemplates = templates.filter(c =>
    c.name.toLowerCase().includes(filter.toLowerCase())
  );
  const filteredCustom = customChecklists.filter(c =>
    c.name.toLowerCase().includes(filter.toLowerCase())
  );

  const handleChecklistClick = (checklistId: string, isTemplate: boolean) => {
    onChecklistSelect(checklistId);
    if (isTemplate) {
      onTemplateSelect(checklistId);
    }
  };


  const allChecklists = [...filteredTemplates, ...filteredCustom];

  return (
    <div className="checklist-selector">
      <div className="selector-header">
        <h3>Choose Checklist for Processing</h3>
        <button 
          onClick={onCreateChecklist} 
          className="btn btn-secondary btn-small"
          style={{ marginTop: '1rem' }}
        >
          Create New Checklist
        </button>
      </div>

      <div className="filter-container">
        <input
          type="text"
          placeholder="Filter checklists..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="filter-input"
        />
        <div className="selection-count">
          {selectedChecklistId ? '1 selected' : '0 selected'}
        </div>
      </div>

      <div className="checklist-list">
        {allChecklists.map((checklist) => {
          const isSelected = selectedChecklistId === checklist.id;
          const isTemplate = checklist.name.includes('Template') || checklist.name.includes('Standard');
          
          return (
            <div
              key={checklist.id}
              className={`checklist-item ${isSelected ? 'selected' : ''}`}
              onClick={() => handleChecklistClick(checklist.id, isTemplate)}
            >
              <div className="checklist-checkbox">
                <input
                  type="radio"
                  name="checklist-selection"
                  checked={isSelected}
                  onChange={() => handleChecklistClick(checklist.id, isTemplate)}
                  onClick={(e) => e.stopPropagation()}
                />
              </div>
              <div className="checklist-info">
                <div className="checklist-name">{checklist.name}</div>
                <div className="checklist-description">{checklist.description}</div>
                <div className="checklist-meta">
                  {checklist.questions.length} questions, {checklist.conditions.length} conditions
                </div>
              </div>
              <div className="checklist-actions">
                {isTemplate && <div className="template-badge">Template</div>}
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    onEditChecklist(checklist.id);
                  }}
                  className="btn btn-secondary btn-small"
                  title="Edit checklist"
                >
                  Edit
                </button>
                <button 
                  onClick={(e) => {
                    e.stopPropagation();
                    onDeleteChecklist(checklist.id, checklist.name);
                  }}
                  className="btn btn-danger btn-small"
                  title="Delete checklist"
                >
                  🗑️
                </button>
              </div>
            </div>
          );
        })}
      </div>

      {allChecklists.length === 0 && (
        <div className="no-results">
          <p>No checklists found matching "{filter}"</p>
        </div>
      )}
    </div>
  );
};
