/** @jest-environment jsdom */
import { api } from '../../services/api';

// Mock fetch globally
global.fetch = jest.fn();

describe('API Service', () => {
  beforeEach(() => {
    (fetch as jest.Mock).mockClear();
  });

  describe('getChecklists', () => {
    it('should fetch checklists successfully', async () => {
      const mockChecklists = [
        { id: '1', name: 'Test Checklist', description: 'Test description' }
      ];
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockChecklists,
      });

      const result = await api.getChecklists();
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/checklists');
      expect(result).toEqual(mockChecklists);
    });

    it('should handle fetch errors', async () => {
      (fetch as jest.Mock).mockRejectedValueOnce(new Error('Network error'));

      await expect(api.getChecklists()).rejects.toThrow('Network error');
    });
  });

  describe('createChecklist', () => {
    it('should create checklist successfully', async () => {
      const checklistData = {
        name: 'New Checklist',
        description: 'New description',
        questions: [],
        conditions: []
      };
      
      const mockResponse = { id: '1', ...checklistData };
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await api.createChecklist(checklistData);
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/checklists', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(checklistData),
      });
      expect(result).toEqual(mockResponse);
    });

    it('should handle creation errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
      });

      await expect(api.createChecklist({} as any)).rejects.toThrow('Failed to create checklist');
    });
  });

  describe('uploadDocument', () => {
    it('should upload document successfully', async () => {
      const mockFile = new File(['test'], 'test.pdf', { type: 'application/pdf' });
      const mockResponse = { id: '1', filename: 'test.pdf' };
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await api.uploadDocument(mockFile);
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/upload', {
        method: 'POST',
        body: expect.any(FormData),
      });
      expect(result).toEqual(mockResponse);
    });

    it('should handle upload errors', async () => {
      const mockFile = new File(['test'], 'test.pdf', { type: 'application/pdf' });
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 400,
      });

      await expect(api.uploadDocument(mockFile)).rejects.toThrow('Failed to upload document');
    });
  });

  describe('processDocument', () => {
    it('should process document successfully', async () => {
      const mockResponse = { id: '1', status: 'completed' };
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await api.processDocuments('checklist1', ['document1']);
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/process/checklist1', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ document_id: 'document1' }),
      });
      expect(result).toEqual(mockResponse);
    });

    it('should handle processing errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 500,
      });

      await expect(api.processDocuments('checklist1', ['document1'])).rejects.toThrow('Failed to process document');
    });
  });

  describe('getDocuments', () => {
    it('should fetch documents successfully', async () => {
      const mockDocuments = [
        { id: '1', filename: 'test1.pdf', status: 'uploaded' },
        { id: '2', filename: 'test2.pdf', status: 'processed' }
      ];
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockDocuments,
      });

      const result = await api.getDocuments();
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/documents');
      expect(result).toEqual(mockDocuments);
    });
  });

  describe('deleteDocument', () => {
    it('should delete document successfully', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
      });

      await api.deleteDocument('document1');
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/documents/document1', {
        method: 'DELETE',
      });
    });

    it('should handle delete errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      await expect(api.deleteDocument('document1')).rejects.toThrow('Failed to delete document');
    });
  });

  describe('deleteChecklist', () => {
    it('should delete checklist successfully', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
      });

      await api.deleteChecklist('checklist1');
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/checklists/checklist1', {
        method: 'DELETE',
      });
    });

    it('should handle delete errors', async () => {
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: false,
        status: 404,
      });

      await expect(api.deleteChecklist('checklist1')).rejects.toThrow('Failed to delete checklist');
    });
  });

  describe('batchProcessDocuments', () => {
    it('should batch process documents successfully', async () => {
      const mockResponse = {
        id: 'batch1',
        status: 'completed',
        message: 'Processing completed',
        results: [
          { id: '1', document_id: 'doc1', status: 'completed' },
          { id: '2', document_id: 'doc2', status: 'completed' }
        ]
      };
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockResponse,
      });

      const result = await api.batchProcessDocuments('checklist1', { documentIds: ['doc1', 'doc2'] });
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/batch/process/checklist1', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ documentIds: ['doc1', 'doc2'] }),
      });
      expect(result).toEqual(mockResponse);
    });
  });

  describe('getTemplates', () => {
    it('should fetch templates successfully', async () => {
      const mockTemplates = [
        { id: '1', name: 'German Tender Template', description: 'Template for German tenders' }
      ];
      
      (fetch as jest.Mock).mockResolvedValueOnce({
        ok: true,
        json: async () => mockTemplates,
      });

      const result = await api.getTemplates();
      
      expect(fetch).toHaveBeenCalledWith('http://localhost:8000/api/templates');
      expect(result).toEqual(mockTemplates);
    });
  });

  describe('exportBatchResults', () => {
    it('should export results as CSV', () => {
      const mockResults = [
        { id: '1', document_id: 'doc1', status: 'completed', error: undefined }
      ];
      const mockDocuments = [
        { 
          id: 'doc1', 
          filename: 'test.pdf',
          original_name: 'test.pdf',
          file_path: '/uploads/test.pdf',
          file_size: 1024000,
          status: 'uploaded',
          uploaded_at: '2024-01-01T00:00:00Z'
        }
      ];

      // Mock URL.createObjectURL and document.createElement
      global.URL.createObjectURL = jest.fn(() => 'mock-url');
      global.URL.revokeObjectURL = jest.fn();
      
      const mockAnchor = {
        href: '',
        download: '',
        click: jest.fn()
      };
      jest.spyOn(document, 'createElement').mockReturnValue(mockAnchor as any);

      api.exportBatchResults(mockResults, mockDocuments);

      expect(mockAnchor.download).toContain('batch_results_');
      expect(mockAnchor.click).toHaveBeenCalled();
    });
  });
});
