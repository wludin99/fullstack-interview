import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FileUpload } from '../../components/FileUpload';

// Mock the API service
jest.mock('../../services/api', () => ({
  uploadDocument: jest.fn(),
}));

describe('FileUpload', () => {
  const mockOnUpload = jest.fn();
  const mockOnError = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders file upload component', () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    expect(screen.getByText(/choose file/i)).toBeInTheDocument();
    expect(screen.getByText(/choose file/i)).toBeInTheDocument();
  });

  it('handles file selection', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = document.querySelector('#file-input') as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(screen.getByText(/test.pdf/)).toBeInTheDocument();
    });
  });

  it('validates file type', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.txt', { type: 'text/plain' });
    const input = document.querySelector('#file-input') as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith(
        expect.stringContaining('Invalid file type')
      );
    });
  });

  it('validates file size', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    // Create a large file (simulate)
    const largeContent = new Array(11 * 1024 * 1024).fill('x').join('');
    const file = new File([largeContent], 'large.pdf', { type: 'application/pdf' });
    const input = document.querySelector('#file-input') as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });

    await waitFor(() => {
      expect(mockOnError).toHaveBeenCalledWith(
        expect.stringContaining('File too large')
      );
    });
  });

  it('shows upload progress', async () => {
    render(
      <FileUpload
        onUpload={mockOnUpload}
        onError={mockOnError}
      />
    );

    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    const input = document.querySelector('#file-input') as HTMLInputElement;
    
    fireEvent.change(input, { target: { files: [file] } });

    // Click the upload button
    const uploadButton = screen.getByText('Upload');
    fireEvent.click(uploadButton);

    await waitFor(() => {
      expect(screen.getByText(/uploading/i)).toBeInTheDocument();
    });
  });
});
