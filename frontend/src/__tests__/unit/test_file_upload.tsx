/** @jest-environment jsdom */
import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FileUpload } from '../../components/FileUpload';

// Mock the API service
jest.mock('../../services/api', () => ({
  api: {
    uploadDocument: jest.fn(),
  }
}));

describe('FileUpload', () => {
  const mockOnUpload = jest.fn();
  const mockOnError = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('should render file upload component', () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    expect(screen.getByText('📁 Choose File')).toBeInTheDocument();
    expect(screen.getByLabelText('file-input')).toBeInTheDocument();
  });

  it('should handle file selection', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText('📄 test.pdf')).toBeInTheDocument();
      expect(screen.getByText('Upload')).toBeInTheDocument();
    });
  });

  it('should validate file type', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith('Invalid file type. Please upload a PDF file.');
    });
  });

  it('should validate file size', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    // Create a large file (11MB)
    const largeFile = new File(['x'.repeat(11 * 1024 * 1024)], 'large.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [largeFile] } });

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith('File too large. Please upload a file smaller than 10MB.');
    });
  });

  it('should upload file when Upload button is clicked', async () => {
    const { api } = require('../../services/api');
    api.uploadDocument.mockResolvedValue({ id: '1', filename: 'test.pdf' });

    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      const uploadButton = screen.getByText('Upload');
      fireEvent.click(uploadButton);
    });

    await waitFor(() => {
      expect(api.uploadDocument).toHaveBeenCalledWith(file);
      expect(mockOnUpload).toHaveBeenCalledWith({ id: '1', filename: 'test.pdf' });
    });
  });

  it('should handle upload errors', async () => {
    const { api } = require('../../services/api');
    api.uploadDocument.mockRejectedValue(new Error('Upload failed'));

    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      const uploadButton = screen.getByText('Upload');
      fireEvent.click(uploadButton);
    });

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith('Upload failed. Please try again.');
    });
  });

  it('should show uploading state during upload', async () => {
    const { api } = require('../../services/api');
    api.uploadDocument.mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));

    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      const uploadButton = screen.getByText('Upload');
      fireEvent.click(uploadButton);
    });

    expect(screen.getByText('Uploading...')).toBeInTheDocument();
  });

  it('should reset form after successful upload', async () => {
    const { api } = require('../../services/api');
    api.uploadDocument.mockResolvedValue({ id: '1', filename: 'test.pdf' });

    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      const uploadButton = screen.getByText('Upload');
      fireEvent.click(uploadButton);
    });

    await waitFor(() => {
      expect(screen.queryByText('📄 test.pdf')).not.toBeInTheDocument();
      expect(screen.queryByText('Upload')).not.toBeInTheDocument();
    });
  });

  it('should handle multiple file selections', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file1 = new File(['test content 1'], 'test1.pdf', { type: 'application/pdf' });
    const file2 = new File(['test content 2'], 'test2.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    // First file
    fireEvent.change(input, { target: { files: [file1] } });

    await waitFor(() => {
      expect(screen.getByText('📄 test1.pdf')).toBeInTheDocument();
    });

    // Second file (should replace first)
    fireEvent.change(input, { target: { files: [file2] } });

    await waitFor(() => {
      expect(screen.getByText('📄 test2.pdf')).toBeInTheDocument();
      expect(screen.queryByText('📄 test1.pdf')).not.toBeInTheDocument();
    });
  });

  it('should handle empty file selection', () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const input = screen.getByLabelText('file-input');
    fireEvent.change(input, { target: { files: [] } });

    expect(screen.queryByText('📄')).not.toBeInTheDocument();
  });

  it('should handle German filenames', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'deutsche_ausschreibung.pdf', { type: 'application/pdf' });
    const input = screen.getByLabelText('file-input');
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText('📄 deutsche_ausschreibung.pdf')).toBeInTheDocument();
    });
  });
});
