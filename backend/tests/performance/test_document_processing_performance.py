"""Performance tests for document processing with real German tender documents."""

import pytest
import time
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_performance.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Create test client with database setup."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


class TestDocumentProcessingPerformance:
    """Performance tests with real German tender documents."""
    
    @pytest.fixture(autouse=True)
    def setup_documents(self):
        """Setup test documents from Tender_documents folder."""
        # Get the project root directory (go up to fullstack-interview)
        current_file = Path(__file__).resolve()
        # Go up from backend/tests/performance/ to fullstack-interview/
        project_root = current_file.parent.parent.parent.parent
        self.tender_docs_path = project_root / "Tender_documents"
        self.test_documents = []
        
        if self.tender_docs_path.exists():
            for doc_file in self.tender_docs_path.glob("*.pdf"):
                self.test_documents.append(doc_file)
    
    def test_single_document_processing_time(self, client):
        """Test that single document processing completes within 30 seconds."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create a German tender checklist
        checklist_data = {
            "name": "Performance Test German Checklist",
            "description": "Test processing performance",
            "questions": [
                {
                    "text": "Test question for performance",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Test condition for performance",
                    "orderIndex": 1
                }
            ]
        }
        
        # Create checklist
        checklist_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = checklist_response.json()["id"]
        
        # Upload document
        test_doc = self.test_documents[0]
        with open(test_doc, "rb") as f:
            files = {"file": (test_doc.name, f, "application/pdf")}
            upload_response = client.post("/api/upload", files=files)
        
        document_id = upload_response.json()["id"]
        
        # Measure processing time
        start_time = time.time()
        
        process_data = {
            "documentIds": [document_id]
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within 30 seconds
        assert processing_time < 30, f"Processing took {processing_time:.2f} seconds, expected < 30 seconds"
        assert process_response.status_code == 202
    
    def test_large_document_processing_time(self, client):
        """Test processing time for the largest document in Tender_documents."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Find the largest document
        largest_doc = max(self.test_documents, key=lambda x: x.stat().st_size)
        
        checklist_data = {
            "name": "Large Document Performance Test",
            "description": "Test processing performance with largest document",
            "questions": [
                {
                    "text": "Test question for large document",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Test condition for large document",
                    "orderIndex": 1
                }
            ]
        }
        
        # Create checklist
        checklist_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = checklist_response.json()["id"]
        
        # Upload largest document
        with open(largest_doc, "rb") as f:
            files = {"file": (largest_doc.name, f, "application/pdf")}
            upload_response = client.post("/api/upload", files=files)
        
        document_id = upload_response.json()["id"]
        
        # Measure processing time
        start_time = time.time()
        
        process_data = {
            "documentIds": [document_id]
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within 30 seconds even for large documents
        assert processing_time < 30, f"Large document processing took {processing_time:.2f} seconds, expected < 30 seconds"
        assert process_response.status_code == 202
        
        print(f"Large document ({largest_doc.name}, {largest_doc.stat().st_size} bytes) processed in {processing_time:.2f} seconds")
    
    def test_concurrent_document_processing(self, client):
        """Test processing multiple documents concurrently."""
        if len(self.test_documents) < 2:
            pytest.skip("Need at least 2 documents for concurrent processing test")
        
        checklist_data = {
            "name": "Concurrent Processing Test",
            "description": "Test concurrent document processing",
            "questions": [
                {
                    "text": "Test concurrent question",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Test concurrent condition",
                    "orderIndex": 1
                }
            ]
        }
        
        # Create checklist
        checklist_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = checklist_response.json()["id"]
        
        # Upload multiple documents
        document_ids = []
        for doc_file in self.test_documents[:2]:  # Use first 2 documents
            with open(doc_file, "rb") as f:
                files = {"file": (doc_file.name, f, "application/pdf")}
                upload_response = client.post("/api/upload", files=files)
                document_ids.append(upload_response.json()["id"])
        
        # Measure concurrent processing time
        start_time = time.time()
        
        process_data = {
            "documentIds": document_ids
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Should complete within 30 seconds even for multiple documents
        assert processing_time < 30, f"Concurrent processing took {processing_time:.2f} seconds, expected < 30 seconds"
        assert process_response.status_code == 202
        
        print(f"Concurrent processing of {len(document_ids)} documents completed in {processing_time:.2f} seconds")
    
    def test_memory_usage_during_processing(self, client):
        """Test memory usage during document processing."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # This test would monitor memory usage during processing
        # Implementation depends on the specific memory monitoring requirements
        pass
    
    def test_api_response_times(self, client):
        """Test API response times for all endpoints."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Test checklist creation response time
        start_time = time.time()
        checklist_data = {
            "name": "API Response Time Test",
            "description": "Test API response times",
            "questions": [],
            "conditions": []
        }
        response = client.post("/api/checklists", json=checklist_data)
        end_time = time.time()
        
        assert response.status_code == 201
        assert (end_time - start_time) < 1.0, "Checklist creation should respond within 1 second"
        
        # Test document upload response time
        test_doc = self.test_documents[0]
        start_time = time.time()
        with open(test_doc, "rb") as f:
            files = {"file": (test_doc.name, f, "application/pdf")}
            response = client.post("/api/upload", files=files)
        end_time = time.time()
        
        assert response.status_code == 201
        assert (end_time - start_time) < 5.0, "Document upload should respond within 5 seconds"
