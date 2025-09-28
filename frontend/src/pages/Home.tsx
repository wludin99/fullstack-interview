import React, { useState, useEffect } from 'react';
import { ChecklistEditor } from '../components/ChecklistEditor';
import { FileUpload } from '../components/FileUpload';
// import { ResultsDisplay } from '../components/ResultsDisplay';
import { BatchDocumentSelector } from '../components/BatchDocumentSelector';
import { ChecklistSelector } from '../components/ChecklistSelector';
import { TemplateEditor } from '../components/TemplateEditor';
import { BatchResultsDisplay } from '../components/BatchResultsDisplay';
import { DeleteConfirmDialog } from '../components/DeleteConfirmDialog';
import { CreateChecklistDialog } from '../components/CreateChecklistDialog';
import { EditChecklistDialog } from '../components/EditChecklistDialog';

interface Checklist {
  id: string;
  name: string;
  description: string;
  questions: any[];
  conditions: any[];
}

interface Document {
  id: string;
  filename: string;
  original_name: string;
  file_path: string;
  file_size: number;
  status: string;
  uploaded_at: string;
}

interface Results {
  id: string;
  checklistId: string;
  documentId: string;
  status: 'processing' | 'completed' | 'error';
  answers: Array<{
    questionId: string;
    questionText: string;
    answer: string;
  }>;
  conditions: Array<{
    conditionId: string;
    conditionText: string;
    result: boolean;
  }>;
  createdAt: string;
  error?: string;
}

export const Home: React.FC = () => {
  const [checklists, setChecklists] = useState<Checklist[]>([]);
  const [documents, setDocuments] = useState<Document[]>([]);
  // const [results] = useState<Results | null>(null);
  const [showEditor, setShowEditor] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);
  
  // Batch processing state
  const [selectedDocuments, setSelectedDocuments] = useState<string[]>([]);
  const [selectedChecklistId, setSelectedChecklistId] = useState<string | null>(null);
  const [batchResults, setBatchResults] = useState<Results[]>([]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [showTemplateEditor, setShowTemplateEditor] = useState(false);
  const [editingTemplate, setEditingTemplate] = useState<Checklist | null>(null);
  const [showCreateDialog, setShowCreateDialog] = useState(false);
  const [showEditDialog, setShowEditDialog] = useState(false);
  const [editingChecklist, setEditingChecklist] = useState<Checklist | null>(null);
  
  // Delete functionality state
  const [deleteDialog, setDeleteDialog] = useState<{
    isOpen: boolean;
    type: 'checklist' | 'document';
    id: string;
    name: string;
  }>({
    isOpen: false,
    type: 'checklist',
    id: '',
    name: ''
  });
  const [isDeleting, setIsDeleting] = useState(false);

  useEffect(() => {
    loadChecklists();
    loadDocuments();
  }, []);

  const loadChecklists = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/checklists');
      if (!response.ok) {
        throw new Error('Failed to load checklists');
      }
      const data = await response.json();
      console.log('Loaded checklists:', data);
      setChecklists(data);
    } catch (err) {
      setError('Error loading checklists');
    }
  };

  const loadDocuments = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/documents');
      if (!response.ok) {
        throw new Error('Failed to load documents');
      }
      const data = await response.json();
      console.log('Loaded documents:', data);
      setDocuments(data);
    } catch (err) {
      setError('Error loading documents');
    }
  };

  const handleCreateChecklist = () => {
    setShowCreateDialog(true);
  };

  const handleEditChecklist = (checklistId: string) => {
    const checklist = checklists.find(c => c.id === checklistId);
    if (checklist) {
      setEditingChecklist(checklist);
      setShowEditDialog(true);
    }
  };

  const handleCreateChecklistSubmit = async (name: string, description: string, questions: string[], conditions: string[]) => {
    try {
      const response = await fetch('http://localhost:8000/api/checklists', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          description,
          questions: questions.map((q, index) => ({ text: q, orderIndex: index })),
          conditions: conditions.map((c, index) => ({ text: c, orderIndex: index }))
        }),
      });

      if (response.ok) {
        const newChecklist = await response.json();
        setChecklists(prev => [...prev, newChecklist]);
        setSuccessMessage('Checklist created successfully!');
        setTimeout(() => setSuccessMessage(''), 3000);
        setShowCreateDialog(false);
      } else {
        setError('Failed to create checklist');
      }
    } catch (err) {
      setError('Error creating checklist');
    }
  };

  const handleUpdateChecklist = async (id: string, name: string, description: string, questions: string[], conditions: string[]) => {
    try {
      const response = await fetch(`http://localhost:8000/api/checklists/${id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          name,
          description,
          questions: questions.map((q, index) => ({ text: q, orderIndex: index })),
          conditions: conditions.map((c, index) => ({ text: c, orderIndex: index }))
        }),
      });

      if (response.ok) {
        const updatedChecklist = await response.json();
        setChecklists(prev => prev.map(c => c.id === id ? updatedChecklist : c));
        setSuccessMessage('Checklist updated successfully!');
        setTimeout(() => setSuccessMessage(''), 3000);
        setShowEditDialog(false);
        setEditingChecklist(null);
      } else {
        setError('Failed to update checklist');
      }
    } catch (err) {
      setError('Error updating checklist');
    }
  };

  const handleSaveChecklist = async (checklistData: any) => {
    try {
      const response = await fetch('http://localhost:8000/api/checklists', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(checklistData),
      });

      if (!response.ok) {
        throw new Error('Failed to create checklist');
      }

      const newChecklist = await response.json();
      setChecklists([...checklists, newChecklist]);
      setShowEditor(false);
    } catch (err) {
      setError('Error creating checklist');
    }
  };

  const handleFileUpload = async (file: File) => {
    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await fetch('http://localhost:8000/api/upload', {
        method: 'POST',
        body: formData,
      });

      if (!response.ok) {
        throw new Error('Upload failed');
      }

      const uploadedFile = await response.json();
      setDocuments([...documents, uploadedFile]);
    } catch (err) {
      setError('Upload failed');
    }
  };

  // Batch processing functions
  const handleBatchProcess = async () => {
    if (!selectedChecklistId || selectedDocuments.length === 0) {
      setError('Please select a checklist and at least one document');
      return;
    }

    console.log('Starting batch process with:', { selectedChecklistId, selectedDocuments });
    setIsProcessing(true);
    try {
      const response = await fetch(`http://localhost:8000/api/batch/process/${selectedChecklistId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ documentIds: selectedDocuments }),
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Batch processing failed');
      }

      const result = await response.json();
      console.log('Batch processing result:', result);
      
      // Fetch detailed results for each processing result
      const processingResults = await Promise.all(
        result.results.map(async (res: any) => {
          if (res.status === 'completed') {
            try {
              const detailResponse = await fetch(`http://localhost:8000/api/results/${res.id}`);
              if (detailResponse.ok) {
                const detailResult = await detailResponse.json();
                return {
                  id: res.id,
                  checklistId: selectedChecklistId,
                  documentId: res.document_id,
                  status: res.status,
                  answers: detailResult.answers || [],
                  conditions: detailResult.conditions || [],
                  createdAt: detailResult.createdAt || new Date().toISOString(),
                  error: res.error
                };
              }
            } catch (err) {
              console.error('Failed to fetch detailed results:', err);
            }
          }
          
          // Fallback for error cases or when detail fetch fails
          return {
            id: res.id,
            checklistId: selectedChecklistId,
            documentId: res.document_id,
            status: res.status,
            answers: [],
            conditions: [],
            createdAt: new Date().toISOString(),
            error: res.error
          };
        })
      );
      
      setBatchResults(processingResults);
      setSuccessMessage(`Successfully processed ${result.results.length} document(s)!`);
      setError(null);
      
      // Auto-dismiss success message after 5 seconds
      setTimeout(() => setSuccessMessage(null), 5000);
    } catch (err: any) {
      setError(`Batch processing failed: ${err.message}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleTemplateEdit = (templateId: string) => {
    const template = checklists.find(c => c.id === templateId);
    if (template) {
      setEditingTemplate(template);
      setShowTemplateEditor(true);
    }
  };

  const handleTemplateSave = async (templateData: any) => {
    try {
      const response = await fetch(`/api/checklists/${editingTemplate?.id}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(templateData),
      });

      if (!response.ok) {
        throw new Error('Failed to update template');
      }

      const updatedTemplate = await response.json();
      setChecklists(checklists.map(c => c.id === updatedTemplate.id ? updatedTemplate : c));
      setShowTemplateEditor(false);
      setEditingTemplate(null);
    } catch (err) {
      setError('Error updating template');
    }
  };

  const handleExportResults = () => {
    const csvContent = batchResults.map(result => {
      const doc = documents.find(d => d.id === result.documentId);
      return {
        document: doc?.filename || 'Unknown',
        status: result.status,
        answers: result.answers.length,
        conditions: result.conditions.length
      };
    });

    const csv = 'Document,Status,Answers,Conditions\n' + 
      csvContent.map(row => `${row.document},${row.status},${row.answers},${row.conditions}`).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'batch_results.csv';
    a.click();
    URL.revokeObjectURL(url);
  };

  // Delete handlers
  const handleDeleteClick = (type: 'checklist' | 'document', id: string, name: string) => {
    setDeleteDialog({
      isOpen: true,
      type,
      id,
      name
    });
  };

  const handleDeleteConfirm = async () => {
    setIsDeleting(true);
    try {
      if (deleteDialog.type === 'checklist') {
        const response = await fetch(`http://localhost:8000/api/checklists/${deleteDialog.id}`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          throw new Error('Failed to delete checklist');
        }
        setChecklists(checklists.filter(c => c.id !== deleteDialog.id));
      } else if (deleteDialog.type === 'document') {
        const response = await fetch(`http://localhost:8000/api/documents/${deleteDialog.id}`, {
          method: 'DELETE',
        });
        if (!response.ok) {
          throw new Error('Failed to delete document');
        }
        setDocuments(documents.filter(d => d.id !== deleteDialog.id));
        // Remove from selected documents if it was selected
        setSelectedDocuments(selectedDocuments.filter(id => id !== deleteDialog.id));
      }
      setDeleteDialog({ isOpen: false, type: 'checklist', id: '', name: '' });
    } catch (err: any) {
      setError(`Delete failed: ${err.message}`);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleDeleteCancel = () => {
    setDeleteDialog({ isOpen: false, type: 'checklist', id: '', name: '' });
  };

  if (showEditor) {
    return (
      <ChecklistEditor
        onSave={handleSaveChecklist}
        onCancel={() => setShowEditor(false)}
      />
    );
  }

  if (showTemplateEditor && editingTemplate) {
    return (
      <TemplateEditor
        template={editingTemplate}
        onSave={handleTemplateSave}
        onCancel={() => {
          setShowTemplateEditor(false);
          setEditingTemplate(null);
        }}
      />
    );
  }

  return (
    <div className="home">
      <h1>Tender Checklist App</h1>
      
      {error && <div className="error-message">{error}</div>}
      
      {successMessage && <div className="success-message">{successMessage}</div>}

      {/* Batch Processing Workflow */}
      <div className="batch-workflow">
        <h2>Batch Document Processing</h2>
        
        {/* Horizontal Steps 1-3 */}
        <div className="workflow-steps-horizontal">
          <div className="step">
            <h2>Step 1: Upload Documents</h2>
            <FileUpload onUpload={handleFileUpload} onError={setError} />
            <div className="document-count">
              {documents.length} document(s) uploaded
            </div>
          </div>

          <div className="step">
            <h2>Step 2: Select Documents</h2>
            <BatchDocumentSelector
              documents={documents}
              selectedDocuments={selectedDocuments}
              onSelectionChange={setSelectedDocuments}
              onSelectAll={() => setSelectedDocuments(documents.map(d => d.id))}
              onDeselectAll={() => setSelectedDocuments([])}
              onDeleteDocument={(documentId, documentName) => handleDeleteClick('document', documentId, documentName)}
            />
          </div>

          <div className="step">
            <h2>Step 3: Choose Checklist</h2>
            <ChecklistSelector
              checklists={checklists}
              selectedChecklistId={selectedChecklistId}
              onChecklistSelect={setSelectedChecklistId}
              onTemplateSelect={handleTemplateEdit}
              onCreateChecklist={handleCreateChecklist}
              onEditChecklist={handleEditChecklist}
              onDeleteChecklist={(checklistId, checklistName) => handleDeleteClick('checklist', checklistId, checklistName)}
            />
            
          </div>
        </div>


        {/* Step 4: Process Documents */}
        <div className="step">
          <h2>Step 4: Process Documents</h2>
          <div className="process-controls">
            <button
              onClick={handleBatchProcess}
              disabled={!selectedChecklistId || selectedDocuments.length === 0 || isProcessing}
              className={`btn btn-primary btn-large ${isProcessing ? 'loading' : ''}`}
            >
              {isProcessing ? (
                <>
                  <span className="loading-spinner">⏳</span>
                  Processing {selectedDocuments.length} document(s)...
                </>
              ) : (
                `Process ${selectedDocuments.length} Document(s)`
              )}
            </button>
          </div>
        </div>

        {batchResults.length > 0 && (
          <div className="step">
            <h2>Step 5: View Results</h2>
            <BatchResultsDisplay
              results={batchResults}
              documents={documents}
              onExport={handleExportResults}
            />
          </div>
        )}
      </div>

      <DeleteConfirmDialog
        isOpen={deleteDialog.isOpen}
        title={`Delete ${deleteDialog.type === 'checklist' ? 'Checklist' : 'Document'}`}
        message={`Are you sure you want to delete this ${deleteDialog.type}?`}
        itemName={deleteDialog.name}
        onConfirm={handleDeleteConfirm}
        onCancel={handleDeleteCancel}
        isLoading={isDeleting}
      />

      <CreateChecklistDialog
        isOpen={showCreateDialog}
        onClose={() => setShowCreateDialog(false)}
        onCreateChecklist={handleCreateChecklistSubmit}
      />

      <EditChecklistDialog
        isOpen={showEditDialog}
        checklist={editingChecklist}
        onClose={() => {
          setShowEditDialog(false);
          setEditingChecklist(null);
        }}
        onUpdateChecklist={handleUpdateChecklist}
      />
    </div>
  );
};
