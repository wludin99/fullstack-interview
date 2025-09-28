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
};
