"""Contract tests for batch processing API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db
from src.models.checklist import Checklist
from src.models.document import Document
from src.models.question import Question
from src.models.condition import Condition
import uuid

client = TestClient(app)

@pytest.fixture
def sample_checklist(client):
    """Create a sample checklist for testing."""
    checklist_data = {
        "name": "Test Checklist",
        "description": "Test checklist for batch processing",
        "questions": [
            {"text": "Test question 1", "orderIndex": 1},
            {"text": "Test question 2", "orderIndex": 2}
        ],
        "conditions": [
            {"text": "Test condition 1", "orderIndex": 1},
            {"text": "Test condition 2", "orderIndex": 2}
        ]
    }
    
    response = client.post("/api/checklists", json=checklist_data)
    assert response.status_code == 201
    return response.json()

@pytest.fixture
def sample_documents(client):
    """Create sample documents for testing."""
    documents = []
    for i in range(3):
        # Create a temporary file for testing
        import tempfile
        import os
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_file.write(b"fake pdf content")
        temp_file.close()
        
        with open(temp_file.name, 'rb') as f:
            response = client.post("/api/upload", files={"file": f})
            assert response.status_code == 201
            documents.append(response.json())
        
        # Clean up temp file
        os.unlink(temp_file.name)
    
    return documents

def test_batch_process_documents_success(sample_checklist, sample_documents):
    """Test successful batch processing of documents."""
    document_ids = [doc["id"] for doc in sample_documents]
    
    response = client.post(
        f"/api/batch/process/{sample_checklist['id']}",
        json={"documentIds": document_ids}
    )
    
    assert response.status_code == 202
    data = response.json()
    assert "id" in data
    assert data["status"] in ["completed", "partial", "error"]
    assert "message" in data
    assert "results" in data
    assert len(data["results"]) == len(document_ids)

def test_batch_process_documents_nonexistent_checklist(sample_documents):
    """Test batch processing with non-existent checklist."""
    document_ids = [doc["id"] for doc in sample_documents]
    fake_checklist_id = str(uuid.uuid4())
    
    response = client.post(
        f"/api/batch/process/{fake_checklist_id}",
        json={"documentIds": document_ids}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "Checklist not found" in data["detail"]

def test_batch_process_documents_no_documents(sample_checklist):
    """Test batch processing with no documents."""
    fake_document_ids = [str(uuid.uuid4()) for _ in range(3)]
    
    response = client.post(
        f"/api/batch/process/{sample_checklist['id']}",
        json={"documentIds": fake_document_ids}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "No documents found" in data["detail"]

def test_batch_process_documents_empty_list(sample_checklist):
    """Test batch processing with empty document list."""
    response = client.post(
        f"/api/batch/process/{sample_checklist['id']}",
        json={"documentIds": []}
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "No documents found" in data["detail"]

def test_batch_process_documents_invalid_json():
    """Test batch processing with invalid JSON."""
    fake_checklist_id = str(uuid.uuid4())
    
    response = client.post(
        f"/api/batch/process/{fake_checklist_id}",
        json={"invalid": "data"}
    )
    
    assert response.status_code == 422

def test_get_batch_processing_status(sample_documents):
    """Test getting batch processing status."""
    document_ids = [doc["id"] for doc in sample_documents]
    document_ids_str = ",".join(document_ids)
    
    response = client.get(f"/api/batch/status?document_ids={document_ids_str}")
    
    assert response.status_code == 200
    data = response.json()
    assert "statuses" in data
    assert isinstance(data["statuses"], dict)

def test_get_batch_processing_status_empty():
    """Test getting batch processing status with empty document list."""
    response = client.get("/api/batch/status?document_ids=")
    
    assert response.status_code == 200
    data = response.json()
    assert "statuses" in data
    assert data["statuses"] == {}

def test_batch_process_documents_mixed_documents(sample_checklist, sample_documents):
    """Test batch processing with mix of valid and invalid documents."""
    valid_document_ids = [doc["id"] for doc in sample_documents[:2]]
    invalid_document_ids = [str(uuid.uuid4()) for _ in range(2)]
    mixed_document_ids = valid_document_ids + invalid_document_ids
    
    response = client.post(
        f"/api/batch/process/{sample_checklist['id']}",
        json={"documentIds": mixed_document_ids}
    )
    
    assert response.status_code == 202
    data = response.json()
    assert "results" in data
    # Should have results for valid documents only
    assert len(data["results"]) == len(valid_document_ids)

def test_batch_process_documents_large_batch(sample_checklist, client):
    """Test batch processing with a large number of documents."""
    # Create many documents
    documents = []
    for i in range(5):  # Reduced from 10 to 5 for faster testing
        # Create a temporary file for testing
        import tempfile
        import os
        temp_file = tempfile.NamedTemporaryFile(suffix='.pdf', delete=False)
        temp_file.write(b"fake pdf content")
        temp_file.close()
        
        with open(temp_file.name, 'rb') as f:
            response = client.post("/api/upload", files={"file": f})
            assert response.status_code == 201
            documents.append(response.json())
        
        # Clean up temp file
        os.unlink(temp_file.name)
    
    document_ids = [doc["id"] for doc in documents]
    
    response = client.post(
        f"/api/batch/process/{sample_checklist['id']}",
        json={"documentIds": document_ids}
    )
    
    assert response.status_code == 202
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == len(document_ids)
