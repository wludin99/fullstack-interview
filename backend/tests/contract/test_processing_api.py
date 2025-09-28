"""Contract tests for document processing API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestProcessingAPI:
    """Test document processing operations."""
    
    def test_process_documents_success(self):
        """Test successful document processing."""
        # First create a checklist
        checklist_data = {
            "name": "Test Checklist",
            "description": "Test description",
            "questions": [
                {
                    "text": "Test question?",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Test condition",
                    "orderIndex": 1
                }
            ]
        }
        checklist_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = checklist_response.json()["id"]
        
        # Upload a document
        files = {
            "file": ("test_document.pdf", b"mock pdf content", "application/pdf")
        }
        upload_response = client.post("/api/upload", files=files)
        document_id = upload_response.json()["id"]
        
        # Process the document
        process_data = {
            "documentIds": [document_id]
        }
        response = client.post(f"/api/process/{checklist_id}", json=process_data)
        assert response.status_code == 202
        data = response.json()
        assert "id" in data
        assert data["status"] == "processing"
    
    def test_process_nonexistent_checklist(self):
        """Test processing with non-existent checklist."""
        process_data = {
            "documentIds": ["document-id"]
        }
        response = client.post("/api/process/nonexistent-checklist", json=process_data)
        assert response.status_code == 404
    
    def test_process_invalid_document_ids(self):
        """Test processing with invalid document IDs."""
        # First create a checklist
        checklist_data = {
            "name": "Test Checklist",
            "description": "Test description",
            "questions": [],
            "conditions": []
        }
        checklist_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = checklist_response.json()["id"]
        
        # Process with invalid document IDs
        process_data = {
            "documentIds": ["nonexistent-document"]
        }
        response = client.post(f"/api/process/{checklist_id}", json=process_data)
        assert response.status_code == 400
