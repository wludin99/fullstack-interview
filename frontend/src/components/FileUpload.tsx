import React, { useState } from 'react';

interface FileUploadProps {
  onUpload: (file: File) => void;
  onError: (error: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({
  onUpload,
  onError
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);

  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    // Validate file type
    if (file.type !== 'application/pdf') {
      onError('Invalid file type. Please upload a PDF file.');
      return;
    }

    // Validate file size (10MB limit)
    const maxSize = 10 * 1024 * 1024; // 10MB
    if (file.size > maxSize) {
      onError('File too large. Please upload a file smaller than 10MB.');
      return;
    }

    setSelectedFile(file);
  };

  const handleUpload = async () => {
    if (!selectedFile) return;

    setIsUploading(true);
    try {
      await onUpload(selectedFile);
      setSelectedFile(null);
    } catch (error) {
      onError('Upload failed. Please try again.');
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <div className="file-upload">
      <div className="upload-area">
        <input
          type="file"
          id="file-input"
          accept=".pdf"
          onChange={handleFileSelect}
          style={{ display: 'none' }}
        />
        <label htmlFor="file-input" className="btn btn-primary file-upload-button">
          📁 Choose File
        </label>
        
        {selectedFile && (
          <div className="selected-file">
            <span className="file-name">📄 {selectedFile.name}</span>
            <button 
              type="button" 
              onClick={handleUpload} 
              disabled={isUploading}
              className="btn btn-secondary"
            >
              {isUploading ? 'Uploading...' : 'Upload'}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
