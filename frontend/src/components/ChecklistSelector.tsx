import React, { useState } from 'react';
import type { Checklist } from '../services/api';

interface ChecklistSelectorProps {
  checklists: Checklist[];
  selectedChecklistId: string | null;
  onChecklistSelect: (checklistId: string) => void;
  onTemplateSelect: (templateId: string) => void;
  loading?: boolean;
}

export const ChecklistSelector: React.FC<ChecklistSelectorProps> = ({
  checklists,
  selectedChecklistId,
  onChecklistSelect,
  onTemplateSelect,
  loading = false
}) => {
  const [isOpen, setIsOpen] = useState(false);
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

  const selectedChecklist = checklists.find(c => c.id === selectedChecklistId);

  const handleChecklistClick = (checklistId: string, isTemplate: boolean) => {
    onChecklistSelect(checklistId);
    if (isTemplate) {
      onTemplateSelect(checklistId);
    }
    setIsOpen(false);
  };

  return (
    <div className="checklist-selector">
      <div className="selector-header">
        <h3>Choose Checklist for Processing</h3>
        <div className="selected-checklist">
          {selectedChecklist ? (
            <div className="selected-info">
              <span className="checklist-name">{selectedChecklist.name}</span>
              <span className="checklist-meta">
                {selectedChecklist.questions.length} questions, {selectedChecklist.conditions.length} conditions
              </span>
            </div>
          ) : (
            <span className="no-selection">No checklist selected</span>
          )}
        </div>
      </div>

      <div className="dropdown-container">
        <button
          className="dropdown-trigger"
          onClick={() => setIsOpen(!isOpen)}
          disabled={loading}
        >
          {selectedChecklist ? selectedChecklist.name : 'Select a checklist...'}
          <span className="dropdown-arrow">{isOpen ? '▲' : '▼'}</span>
        </button>

        {isOpen && (
          <div className="dropdown-menu">
            <div className="filter-section">
              <input
                type="text"
                placeholder="Filter checklists..."
                value={filter}
                onChange={(e) => setFilter(e.target.value)}
                className="filter-input"
              />
            </div>

            <div className="checklist-sections">
              {filteredTemplates.length > 0 && (
                <div className="section">
                  <h4 className="section-title">Templates</h4>
                  <div className="checklist-list">
                    {filteredTemplates.map((checklist) => (
                      <div
                        key={checklist.id}
                        className={`checklist-item template ${selectedChecklistId === checklist.id ? 'selected' : ''}`}
                        onClick={() => handleChecklistClick(checklist.id, true)}
                      >
                        <div className="checklist-info">
                          <div className="checklist-name">{checklist.name}</div>
                          <div className="checklist-description">{checklist.description}</div>
                          <div className="checklist-meta">
                            {checklist.questions.length} questions, {checklist.conditions.length} conditions
                          </div>
                        </div>
                        <div className="template-badge">Template</div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {filteredCustom.length > 0 && (
                <div className="section">
                  <h4 className="section-title">Custom Checklists</h4>
                  <div className="checklist-list">
                    {filteredCustom.map((checklist) => (
                      <div
                        key={checklist.id}
                        className={`checklist-item custom ${selectedChecklistId === checklist.id ? 'selected' : ''}`}
                        onClick={() => handleChecklistClick(checklist.id, false)}
                      >
                        <div className="checklist-info">
                          <div className="checklist-name">{checklist.name}</div>
                          <div className="checklist-description">{checklist.description}</div>
                          <div className="checklist-meta">
                            {checklist.questions.length} questions, {checklist.conditions.length} conditions
                          </div>
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {filteredTemplates.length === 0 && filteredCustom.length === 0 && (
                <div className="no-results">
                  <p>No checklists found matching "{filter}"</p>
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {selectedChecklist && (
        <div className="checklist-preview">
          <h4>Preview</h4>
          <div className="preview-content">
            <div className="questions-preview">
              <strong>Questions ({selectedChecklist.questions.length}):</strong>
              <ul>
                {selectedChecklist.questions.slice(0, 3).map((q, index) => (
                  <li key={index}>{q.text}</li>
                ))}
                {selectedChecklist.questions.length > 3 && (
                  <li>... and {selectedChecklist.questions.length - 3} more</li>
                )}
              </ul>
            </div>
            <div className="conditions-preview">
              <strong>Conditions ({selectedChecklist.conditions.length}):</strong>
              <ul>
                {selectedChecklist.conditions.slice(0, 3).map((c, index) => (
                  <li key={index}>{c.text}</li>
                ))}
                {selectedChecklist.conditions.length > 3 && (
                  <li>... and {selectedChecklist.conditions.length - 3} more</li>
                )}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
