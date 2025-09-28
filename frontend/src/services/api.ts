const API_BASE_URL = 'http://localhost:8000/api';

export interface Checklist {
  id: string;
  name: string;
  description: string;
  questions: Question[];
  conditions: Condition[];
}

export interface Question {
  id: string;
  text: string;
  orderIndex: number;
}

export interface Condition {
  id: string;
  text: string;
  orderIndex: number;
}

export interface Document {
  id: string;
  filename: string;
  status: string;
}

export interface ProcessingResult {
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

export interface BatchProcessingRequest {
  documentIds: string[];
}

export interface BatchProcessingResult {
  id: string;
  document_id: string;
  status: string;
  error?: string;
}

export interface BatchProcessingResponse {
  id: string;
  status: string;
  message: string;
  results: BatchProcessingResult[];
}

export interface Template {
  id: string;
  name: string;
  description: string;
  questions: Question[];
  conditions: Condition[];
  created_at: string;
  updated_at: string;
}

export const api = {
  // Checklist endpoints
  async getChecklists(): Promise<Checklist[]> {
    const response = await fetch(`${API_BASE_URL}/checklists`);
    if (!response.ok) {
      throw new Error('Failed to fetch checklists');
    }
    return response.json();
  },

  async createChecklist(checklist: Omit<Checklist, 'id'>): Promise<Checklist> {
    const response = await fetch(`${API_BASE_URL}/checklists`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(checklist),
    });
    if (!response.ok) {
      throw new Error('Failed to create checklist');
    }
    return response.json();
  },

  async updateChecklist(id: string, checklist: Omit<Checklist, 'id'>): Promise<Checklist> {
    const response = await fetch(`${API_BASE_URL}/checklists/${id}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(checklist),
    });
    if (!response.ok) {
      throw new Error('Failed to update checklist');
    }
    return response.json();
  },

  async deleteChecklist(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/checklists/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete checklist');
    }
  },

  // Document endpoints
  async getDocuments(): Promise<Document[]> {
    const response = await fetch(`${API_BASE_URL}/documents`);
    if (!response.ok) {
      throw new Error('Failed to fetch documents');
    }
    return response.json();
  },

  async uploadDocument(file: File): Promise<Document> {
    const formData = new FormData();
    formData.append('file', file);

    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    if (!response.ok) {
      throw new Error('Failed to upload document');
    }
    return response.json();
  },

  async deleteDocument(id: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/documents/${id}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete document');
    }
  },

  // Processing endpoints
  async processDocuments(checklistId: string, documentIds: string[]): Promise<ProcessingResult> {
    const response = await fetch(`${API_BASE_URL}/process/${checklistId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ documentIds }),
    });
    if (!response.ok) {
      throw new Error('Failed to process documents');
    }
    return response.json();
  },

  async getResults(resultId: string): Promise<ProcessingResult> {
    const response = await fetch(`${API_BASE_URL}/results/${resultId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch results');
    }
    return response.json();
  },

  // Batch processing endpoints
  async batchProcessDocuments(checklistId: string, request: BatchProcessingRequest): Promise<BatchProcessingResponse> {
    const response = await fetch(`${API_BASE_URL}/batch/process/${checklistId}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(request),
    });
    if (!response.ok) {
      throw new Error('Failed to batch process documents');
    }
    return response.json();
  },

  async getBatchProcessingStatus(documentIds: string[]): Promise<Record<string, string>> {
    const response = await fetch(`${API_BASE_URL}/batch/status?document_ids=${documentIds.join(',')}`);
    if (!response.ok) {
      throw new Error('Failed to fetch batch processing status');
    }
    const data = await response.json();
    return data.statuses;
  },

  // Template management endpoints
  async getTemplates(): Promise<Template[]> {
    const response = await fetch(`${API_BASE_URL}/templates`);
    if (!response.ok) {
      throw new Error('Failed to fetch templates');
    }
    return response.json();
  },

  async getTemplate(templateId: string): Promise<Template> {
    const response = await fetch(`${API_BASE_URL}/templates/${templateId}`);
    if (!response.ok) {
      throw new Error('Failed to fetch template');
    }
    return response.json();
  },

  async updateTemplate(templateId: string, template: Omit<Template, 'id' | 'created_at' | 'updated_at'>): Promise<Template> {
    const response = await fetch(`${API_BASE_URL}/templates/${templateId}`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(template),
    });
    if (!response.ok) {
      throw new Error('Failed to update template');
    }
    return response.json();
  },

  async deleteTemplate(templateId: string): Promise<void> {
    const response = await fetch(`${API_BASE_URL}/templates/${templateId}`, {
      method: 'DELETE',
    });
    if (!response.ok) {
      throw new Error('Failed to delete template');
    }
  },

  async createCustomFromTemplate(templateId: string, customName: string): Promise<Checklist> {
    const response = await fetch(`${API_BASE_URL}/templates/${templateId}/create-custom?custom_name=${encodeURIComponent(customName)}`, {
      method: 'POST',
    });
    if (!response.ok) {
      throw new Error('Failed to create custom checklist from template');
    }
    return response.json();
  },

  // Enhanced batch operations
  async uploadMultipleDocuments(files: File[]): Promise<Document[]> {
    const uploadPromises = files.map(file => this.uploadDocument(file));
    return Promise.all(uploadPromises);
  },

  async processBatchWithProgress(
    checklistId: string, 
    documentIds: string[], 
    onProgress?: (progress: number) => void
  ): Promise<BatchProcessingResponse> {
    // Start batch processing
    const batchResponse = await this.batchProcessDocuments(checklistId, { documentIds });
    
    // Poll for status updates if processing is async
    if (batchResponse.status === 'processing') {
      const pollInterval = setInterval(async () => {
        try {
          const statuses = await this.getBatchProcessingStatus(documentIds);
          const completedCount = Object.values(statuses).filter(status => 
            status === 'completed' || status === 'error'
          ).length;
          const progress = (completedCount / documentIds.length) * 100;
          
          if (onProgress) {
            onProgress(progress);
          }
          
          if (completedCount === documentIds.length) {
            clearInterval(pollInterval);
          }
        } catch (error) {
          console.error('Error polling batch status:', error);
          clearInterval(pollInterval);
        }
      }, 1000);
    }
    
    return batchResponse;
  },

  // Export functionality
  async exportBatchResults(results: BatchProcessingResult[], documents: Document[]): Promise<void> {
    const csvContent = results.map(result => {
      const doc = documents.find(d => d.id === result.document_id);
      return {
        document: doc?.filename || 'Unknown',
        status: result.status,
        error: result.error || ''
      };
    });

    const csv = 'Document,Status,Error\n' + 
      csvContent.map(row => `"${row.document}","${row.status}","${row.error}"`).join('\n');
    
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `batch_results_${new Date().toISOString().split('T')[0]}.csv`;
    a.click();
    URL.revokeObjectURL(url);
  },
};
