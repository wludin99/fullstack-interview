"""Contract tests for document upload API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestUploadAPI:
    """Test document upload operations."""
    
    def test_upload_document_success(self):
        """Test successful document upload."""
        # Create a mock PDF file
        files = {
            "file": ("test_document.pdf", b"mock pdf content", "application/pdf")
        }
        
        response = client.post("/api/upload", files=files)
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert "filename" in data
        assert data["filename"].endswith(".pdf")
        assert data["status"] == "uploaded"
    
    def test_upload_invalid_file_type(self):
        """Test upload with invalid file type."""
        files = {
            "file": ("test.txt", b"text content", "text/plain")
        }
        
        response = client.post("/api/upload", files=files)
        assert response.status_code == 400
    
    def test_upload_file_too_large(self):
        """Test upload with file too large."""
        # Create a large file (simulate)
        large_content = b"x" * (11 * 1024 * 1024)  # 11MB
        files = {
            "file": ("large_document.pdf", large_content, "application/pdf")
        }
        
        response = client.post("/api/upload", files=files)
        assert response.status_code == 413
    
    def test_upload_no_file(self):
        """Test upload without file."""
        response = client.post("/api/upload")
        assert response.status_code == 422
