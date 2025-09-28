import React from 'react';

interface DeleteConfirmDialogProps {
  isOpen: boolean;
  title: string;
  message: string;
  itemName: string;
  onConfirm: () => void;
  onCancel: () => void;
  isLoading?: boolean;
}

export const DeleteConfirmDialog: React.FC<DeleteConfirmDialogProps> = ({
  isOpen,
  title,
  message,
  itemName,
  onConfirm,
  onCancel,
  isLoading = false
}) => {
  if (!isOpen) return null;

  return (
    <div className="delete-confirm-dialog-overlay">
      <div className="delete-confirm-dialog">
        <div className="dialog-header">
          <h3>{title}</h3>
        </div>
        
        <div className="dialog-body">
          <p>{message}</p>
          <div className="item-name">
            <strong>"{itemName}"</strong>
          </div>
          <p className="warning-text">
            ⚠️ This action cannot be undone.
          </p>
        </div>
        
        <div className="dialog-actions">
          <button
            onClick={onCancel}
            disabled={isLoading}
            className="btn btn-secondary"
          >
            Cancel
          </button>
          <button
            onClick={onConfirm}
            disabled={isLoading}
            className="btn btn-danger"
          >
            {isLoading ? 'Deleting...' : 'Delete'}
          </button>
        </div>
      </div>
    </div>
  );
};
