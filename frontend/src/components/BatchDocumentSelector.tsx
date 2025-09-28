import React, { useState } from 'react';
import type { Document } from '../services/api';

interface BatchDocumentSelectorProps {
  documents: Document[];
  selectedDocuments: string[];
  onSelectionChange: (selectedIds: string[]) => void;
  onSelectAll: () => void;
  onDeselectAll: () => void;
  onDeleteDocument?: (documentId: string, documentName: string) => void;
}

export const BatchDocumentSelector: React.FC<BatchDocumentSelectorProps> = ({
  documents,
  selectedDocuments,
  onSelectionChange,
  onSelectAll,
  onDeselectAll,
  onDeleteDocument
}) => {
  const [filter, setFilter] = useState('');

  const filteredDocuments = documents.filter(doc =>
    doc.original_name.toLowerCase().includes(filter.toLowerCase())
  );

  const handleDocumentToggle = (documentId: string) => {
    const isSelected = selectedDocuments.includes(documentId);
    if (isSelected) {
      onSelectionChange(selectedDocuments.filter(id => id !== documentId));
    } else {
      onSelectionChange([...selectedDocuments, documentId]);
    }
  };

  // Remove duplicate delete handling - use parent's delete handler directly

  const allSelected = documents.length > 0 && selectedDocuments.length === documents.length;
  // const someSelected = selectedDocuments.length > 0 && selectedDocuments.length < documents.length;

  return (
    <div className="batch-document-selector">
      <div className="selector-header">
        <h3>Select Documents for Batch Processing</h3>
        <div className="selection-controls">
          <button
            onClick={onSelectAll}
            disabled={allSelected}
            className="btn btn-secondary"
          >
            Select All
          </button>
          <button
            onClick={onDeselectAll}
            disabled={selectedDocuments.length === 0}
            className="btn btn-secondary"
          >
            Deselect All
          </button>
        </div>
      </div>

      <div className="filter-container">
        <input
          type="text"
          placeholder="Filter documents..."
          value={filter}
          onChange={(e) => setFilter(e.target.value)}
          className="filter-input"
        />
        <span className="selection-count">
          {selectedDocuments.length} of {documents.length} selected
        </span>
      </div>

      <div className="document-list">
        {filteredDocuments.length === 0 ? (
          <div className="no-documents">
            <p>No documents found</p>
            {documents.length === 0 && (
              <p>Upload some documents first to get started.</p>
            )}
          </div>
        ) : (
          filteredDocuments.map((document) => {
            const isSelected = selectedDocuments.includes(document.id);
            return (
              <div
                key={document.id}
                className={`document-item ${isSelected ? 'selected' : ''}`}
                onClick={() => handleDocumentToggle(document.id)}
              >
                <div className="document-checkbox">
                  <input
                    type="checkbox"
                    checked={isSelected}
                    onChange={() => handleDocumentToggle(document.id)}
                  />
                </div>
                <div className="document-info">
                  <div className="document-name">{document.original_name}</div>
                  <div className="document-status">
                    <span className="status-badge">{document.status}</span>
                  </div>
                </div>
                {onDeleteDocument && (
                  <div className="document-actions">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        onDeleteDocument?.(document.id, document.original_name);
                      }}
                      className="btn btn-danger btn-small"
                      title="Delete document"
                    >
                      🗑️
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>

      {selectedDocuments.length > 0 && (
        <div className="selection-summary">
          <p>Ready to process {selectedDocuments.length} document(s)</p>
        </div>
      )}

    </div>
  );
};
