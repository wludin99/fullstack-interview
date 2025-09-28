"""Contract tests for documents API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestDocumentsAPI:
    """Test document management operations."""
    
    def test_get_documents_success(self):
        """Test successful document list retrieval."""
        response = client.get("/api/documents")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_document_by_id_success(self):
        """Test successful single document retrieval."""
        # First upload a document
        files = {
            "file": ("test_document.pdf", b"mock pdf content", "application/pdf")
        }
        upload_response = client.post("/api/upload", files=files)
        document_id = upload_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/documents/{document_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == document_id
        assert data["filename"].endswith(".pdf")
    
    def test_delete_document_success(self):
        """Test successful document deletion."""
        # First upload a document
        files = {
            "file": ("test_document.pdf", b"mock pdf content", "application/pdf")
        }
        upload_response = client.post("/api/upload", files=files)
        document_id = upload_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/documents/{document_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/documents/{document_id}")
        assert get_response.status_code == 404
    
    def test_get_nonexistent_document(self):
        """Test retrieving non-existent document."""
        response = client.get("/api/documents/nonexistent-id")
        assert response.status_code == 404
