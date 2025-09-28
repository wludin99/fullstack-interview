"""Integration tests for German language processing with real documents."""

import pytest
from pathlib import Path
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_german_lang.db"
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


class TestGermanLanguageProcessing:
    """Test German language processing with real tender documents."""
    
    @pytest.fixture(autouse=True)
    def setup_documents(self):
        """Setup test documents from Tender_documents folder."""
        self.tender_docs_path = Path(__file__).parent.parent.parent.parent / "Tender_documents"
        self.test_documents = []
        
        if self.tender_docs_path.exists():
            for doc_file in self.tender_docs_path.glob("*.pdf"):
                self.test_documents.append(doc_file)
    
    def test_german_tender_terminology_recognition(self, client):
        """Test that German tender terminology is correctly recognized."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create a checklist with German tender-specific questions
        checklist_data = {
            "name": "Deutsche Ausschreibung Terminologie Test",
            "description": "Test recognition of German tender terminology",
            "questions": [
                {
                    "text": "Wer ist der Auftraggeber?",
                    "orderIndex": 1
                },
                {
                    "text": "Wann ist die Angebotsfrist?",
                    "orderIndex": 2
                },
                {
                    "text": "Welche Eignungskriterien sind zu erfüllen?",
                    "orderIndex": 3
                },
                {
                    "text": "Sind Nachunternehmer zulässig?",
                    "orderIndex": 4
                }
            ],
            "conditions": [
                {
                    "text": "Ist das Angebot fristgerecht eingegangen?",
                    "orderIndex": 1
                },
                {
                    "text": "Sind alle Eignungsnachweise vorhanden?",
                    "orderIndex": 2
                },
                {
                    "text": "Erfüllt das Angebot die Mindestanforderungen?",
                    "orderIndex": 3
                }
            ]
        }
        
        # Create checklist
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
        checklist_id = checklist_response.json()["id"]
        
        # Upload German document
        test_doc = self.test_documents[0]
        with open(test_doc, "rb") as f:
            files = {"file": (test_doc.name, f, "application/pdf")}
            upload_response = client.post("/api/upload", files=files)
        
        assert upload_response.status_code == 201
        document_id = upload_response.json()["id"]
        
        # Process document
        process_data = {
            "documentIds": [document_id]
        }
        
        process_response = client.post(f"/api/process/{checklist_id}", json=process_data)
        assert process_response.status_code == 202
        
        # This test will be enhanced once LLM service is implemented
        # It should validate that German terms like "Auftraggeber", "Angebotsfrist", 
        # "Eignungskriterien", "Nachunternehmer" are correctly understood
    
    def test_german_legal_terms_processing(self, client):
        """Test processing of German legal terms in tender documents."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create checklist with German legal terms
        checklist_data = {
            "name": "Deutsche Rechtsbegriffe Test",
            "description": "Test processing of German legal terminology",
            "questions": [
                {
                    "text": "Welche VOB/B-Vorschriften sind anzuwenden?",
                    "orderIndex": 1
                },
                {
                    "text": "Sind die Vergabevorschriften eingehalten?",
                    "orderIndex": 2
                },
                {
                    "text": "Welche Gewährleistungsfristen gelten?",
                    "orderIndex": 3
                }
            ],
            "conditions": [
                {
                    "text": "Sind alle rechtlichen Anforderungen erfüllt?",
                    "orderIndex": 1
                },
                {
                    "text": "Entspricht das Angebot den Vergabevorschriften?",
                    "orderIndex": 2
                }
            ]
        }
        
        # This test validates processing of German legal terms like:
        # - VOB/B (Verdingungsordnung für Bauleistungen)
        # - Vergabevorschriften (procurement regulations)
        # - Gewährleistungsfristen (warranty periods)
        # - Eignungsnachweise (suitability certificates)
        
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
    
    def test_german_date_format_processing(self, client):
        """Test processing of German date formats in documents."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create checklist with date-related questions
        checklist_data = {
            "name": "Deutsche Datumsformate Test",
            "description": "Test processing of German date formats",
            "questions": [
                {
                    "text": "Wann ist der Stichtag für die Angebotsabgabe?",
                    "orderIndex": 1
                },
                {
                    "text": "Bis wann können Bieterfragen gestellt werden?",
                    "orderIndex": 2
                },
                {
                    "text": "Wann beginnt die Ausführungsfrist?",
                    "orderIndex": 3
                }
            ],
            "conditions": [
                {
                    "text": "Ist das Angebot fristgerecht eingegangen?",
                    "orderIndex": 1
                }
            ]
        }
        
        # This test validates processing of German date formats like:
        # - DD.MM.YYYY (German date format)
        # - German month names (Januar, Februar, etc.)
        # - German time expressions (bis, ab, von...bis)
        
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
    
    def test_german_currency_and_numbers(self, client):
        """Test processing of German currency and number formats."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create checklist with currency-related questions
        checklist_data = {
            "name": "Deutsche Währungsformate Test",
            "description": "Test processing of German currency and number formats",
            "questions": [
                {
                    "text": "Wie hoch ist der geschätzte Auftragswert?",
                    "orderIndex": 1
                },
                {
                    "text": "Welche Sicherheitsleistung ist erforderlich?",
                    "orderIndex": 2
                },
                {
                    "text": "Wie werden die Preise kalkuliert?",
                    "orderIndex": 3
                }
            ],
            "conditions": [
                {
                    "text": "Ist der Preisangabe vollständig?",
                    "orderIndex": 1
                }
            ]
        }
        
        # This test validates processing of German formats like:
        # - Currency: € 1.000.000,00 (German number format with dots and commas)
        # - Numbers: 1.234.567,89 (German decimal format)
        # - Currency symbols: €, EUR
        
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
    
    def test_german_technical_terms_processing(self, client):
        """Test processing of German technical terms in tender documents."""
        if not self.test_documents:
            pytest.skip("No German tender documents found in Tender_documents folder")
        
        # Create checklist with technical terms
        checklist_data = {
            "name": "Deutsche Fachbegriffe Test",
            "description": "Test processing of German technical terminology",
            "questions": [
                {
                    "text": "Welche Bauleistungen sind zu erbringen?",
                    "orderIndex": 1
                },
                {
                    "text": "Sind besondere Qualifikationen erforderlich?",
                    "orderIndex": 2
                },
                {
                    "text": "Welche Normen und Standards sind einzuhalten?",
                    "orderIndex": 3
                }
            ],
            "conditions": [
                {
                    "text": "Erfüllt das Angebot alle technischen Anforderungen?",
                    "orderIndex": 1
                }
            ]
        }
        
        # This test validates processing of German technical terms like:
        # - Bauleistungen (construction services)
        # - Qualifikationen (qualifications)
        # - Normen (standards)
        # - DIN-Normen (German industrial standards)
        
        checklist_response = client.post("/api/checklists", json=checklist_data)
        assert checklist_response.status_code == 201
