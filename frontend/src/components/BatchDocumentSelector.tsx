import React, { useState } from 'react';
import type { Document } from '../services/api';
import { DeleteConfirmDialog } from './DeleteConfirmDialog';

interface BatchDocumentSelectorProps {
  documents: Document[];
  selectedDocuments: string[];
  onSelectionChange: (selectedIds: string[]) => void;
  onSelectAll: () => void;
  onDeselectAll: () => void;
  onDeleteDocument?: (documentId: string) => void;
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
  const [deleteDialog, setDeleteDialog] = useState<{
    isOpen: boolean;
    documentId: string;
    documentName: string;
  }>({
    isOpen: false,
    documentId: '',
    documentName: ''
  });
  const [isDeleting, setIsDeleting] = useState(false);

  const filteredDocuments = documents.filter(doc =>
    doc.filename.toLowerCase().includes(filter.toLowerCase())
  );

  const handleDocumentToggle = (documentId: string) => {
    const isSelected = selectedDocuments.includes(documentId);
    if (isSelected) {
      onSelectionChange(selectedDocuments.filter(id => id !== documentId));
    } else {
      onSelectionChange([...selectedDocuments, documentId]);
    }
  };

  const handleDeleteClick = (documentId: string, documentName: string) => {
    setDeleteDialog({
      isOpen: true,
      documentId,
      documentName
    });
  };

  const handleDeleteConfirm = async () => {
    if (!onDeleteDocument) return;
    
    setIsDeleting(true);
    try {
      await onDeleteDocument(deleteDialog.documentId);
      setDeleteDialog({ isOpen: false, documentId: '', documentName: '' });
    } catch (error) {
      console.error('Error deleting document:', error);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialog({ isOpen: false, documentId: '', documentName: '' });
  };

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

      <div className="filter-section">
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
                  <div className="document-name">{document.filename}</div>
                  <div className="document-status">
                    Status: <span className={`status-${document.status}`}>{document.status}</span>
                  </div>
                </div>
                {onDeleteDocument && (
                  <div className="document-actions">
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handleDeleteClick(document.id, document.filename);
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

      <DeleteConfirmDialog
        isOpen={deleteDialog.isOpen}
        title="Delete Document"
        message="Are you sure you want to delete this document?"
        itemName={deleteDialog.documentName}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
        isLoading={isDeleting}
      />
    </div>
  );
};
