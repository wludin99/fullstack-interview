"""Integration tests with real German tender documents."""

import pytest
import os
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db, Base
from src.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_real_docs.db"
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


class TestRealGermanTenderDocuments:
    """Test with actual German tender documents from Tender_documents folder."""
    
    @pytest.fixture(autouse=True)
    def setup_documents(self):
        """Setup test documents from Tender_documents folder."""
        self.tender_docs_path = Path(__file__).parent.parent.parent.parent / "Tender_documents"
        self.test_documents = []
        
        if self.tender_docs_path.exists():
            for doc_file in self.tender_docs_path.glob("*.pdf"):
                self.test_documents.append(doc_file)
    
    def test_upload_real_german_tender_document(self, client):
        """Test uploading a real German tender document."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Use the first available document
        test_doc = self.test_documents[0]
        
        with open(test_doc, "rb") as f:
            files = {"file": (test_doc.name, f, "application/pdf")}
            response = client.post("/api/upload", files=files)
        
        assert response.status_code == 201
        data = response.json()
        assert "id" in data
        assert data["original_name"] == test_doc.name  # Check original_name instead of filename
        assert data["status"] == "uploaded"
    
    def test_process_real_german_tender_document(self, client):
        """Test processing a real German tender document with German checklist."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create a German tender checklist
        checklist_data = {
            "name": "Deutsche Ausschreibung Checkliste",
            "description": "Standard-Checkliste für deutsche öffentliche Ausschreibungen",
            "questions": [
                {
                    "text": "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?",
                    "orderIndex": 1
                },
                {
                    "text": "Wann ist die Frist für die Einreichung von Bieterfragen?",
                    "orderIndex": 2
                },
                {
                    "text": "Welche Unterlagen sind erforderlich?",
                    "orderIndex": 3
                }
            ],
            "conditions": [
                {
                    "text": "Ist das Angebot vollständig und fristgerecht eingegangen?",
                    "orderIndex": 1
                },
                {
                    "text": "Sind alle erforderlichen Unterlagen vorhanden?",
                    "orderIndex": 2
                }
            ]
        }
        
        # Create checklist
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
        checklist_id = checklist_response.json()["id"]
        
        # Upload real document
        test_doc = self.test_documents[0]
        with open(test_doc, "rb") as f:
            files = {"file": (test_doc.name, f, "application/pdf")}
            upload_response = client.post("/api/upload", files=files)
        
        assert upload_response.status_code == 201
        document_id = upload_response.json()["id"]
        
        # Process document with German checklist
        process_data = {
            "documentIds": [document_id]
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        assert process_response.status_code == 202
        processing_result = process_response.json()
        assert "id" in processing_result
        assert processing_result["status"] == "processing"
    
    def test_german_language_processing_accuracy(self, client):
        """Test that German language processing works correctly."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # This test will be implemented once LLM service is ready
        # It should validate that German text is processed correctly
        # and that German-specific terms are understood
        pass
    
    def test_performance_with_real_documents(self, client):
        """Test processing performance with real documents."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # This test will measure processing time for real documents
        # Should complete within 30 seconds as per requirements
        pass
    
    def test_multiple_document_processing(self, client):
        """Test processing multiple real German tender documents."""
        if len(self.test_documents) < 2:
            pytest.skip("Need at least 2 German tender documents for this test")
        
        # Create checklist
        checklist_data = {
            "name": "Multi-Document German Tender Checklist",
            "description": "Test processing multiple documents",
            "questions": [
                {
                    "text": "Welche Dokumente sind vorhanden?",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Sind alle Dokumente vollständig?",
                    "orderIndex": 1
                }
            ]
        }
        
        checklist_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = checklist_response.json()["id"]
        
        # Upload multiple documents
        document_ids = []
        for doc_file in self.test_documents[:2]:  # Use first 2 documents
            with open(doc_file, "rb") as f:
                files = {"file": (doc_file.name, f, "application/pdf")}
                upload_response = client.post("/api/upload", files=files)
                assert upload_response.status_code == 201
                document_ids.append(upload_response.json()["id"])
        
        # Process all documents
        process_data = {
            "documentIds": document_ids
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        assert process_response.status_code == 202
