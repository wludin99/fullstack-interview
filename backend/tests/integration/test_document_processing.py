"""Integration tests for document upload and processing."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestDocumentProcessing:
    """Test document upload and processing workflow."""
    
    def test_document_upload_and_processing_workflow(self):
        """Test complete document upload and processing workflow."""
        # 1. Create checklist
        checklist_data = {
            "name": "Test Processing Checklist",
            "description": "For document processing test",
            "questions": [
                {
                    "text": "What is the submission deadline?",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Is the document complete?",
                    "orderIndex": 1
                }
            ]
        }
        
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
        checklist_id = checklist_response.json()["id"]
        
        # 2. Upload document
        files = {
            "file": ("test_tender.pdf", b"mock pdf content for tender", "application/pdf")
        }
        
        upload_response = client.post("/api/upload", files=files)
        assert upload_response.status_code == 201
        document_id = upload_response.json()["id"]
        
        # 3. List documents
        documents_response = client.get("/api/documents")
        assert documents_response.status_code == 200
        documents = documents_response.json()
        assert len(documents) >= 1
        
        # 4. Process document
        process_data = {
            "documentIds": [document_id]
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        assert process_response.status_code == 202
        processing_result = process_response.json()
        assert "id" in processing_result
        assert processing_result["status"] == "processing"
        
        # 5. Clean up - delete document
        delete_response = client.delete(f"/api/documents/{document_id}")
        assert delete_response.status_code == 204
