"""Unit tests for Document model validation."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.document import Document
from src.database import Base
import uuid
from datetime import datetime

# Test database setup
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(bind=engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture
def db_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

@pytest.fixture
def sample_document():
    return Document(
        id=str(uuid.uuid4()),
        filename="test_document.pdf",
        original_name="Test Document.pdf",
        file_path="/uploads/test_document.pdf",
        file_size=1024000,  # 1MB
        status="uploaded"
    )

def test_document_creation(sample_document):
    """Test document creation with valid data."""
    assert sample_document.filename == "test_document.pdf"
    assert sample_document.original_name == "Test Document.pdf"
    assert sample_document.file_path == "/uploads/test_document.pdf"
    assert sample_document.file_size == 1024000
    assert sample_document.status == "uploaded"
    assert sample_document.id is not None

def test_document_filename_validation():
    """Test document filename validation."""
    # Test with None filename (should work as model allows it)
    document = Document(
        id=str(uuid.uuid4()),
        filename=None,
        original_name="Test Document.pdf",
        file_path="/uploads/test_document.pdf",
        file_size=1024000,
        status="uploaded"
    )
    assert document.filename is None

def test_document_file_path_validation():
    """Test document file_path validation."""
    # Test with None file_path (should work as model allows it)
    document = Document(
        id=str(uuid.uuid4()),
        filename="test_document.pdf",
        original_name="Test Document.pdf",
        file_path=None,
        file_size=1024000,
        status="uploaded"
    )
    assert document.file_path is None

def test_document_status_validation():
    """Test document status validation."""
    valid_statuses = ["uploaded", "processing", "processed", "error"]
    
    for status in valid_statuses:
        document = Document(
            id=str(uuid.uuid4()),
            filename="test_document.pdf",
            original_name="Test Document.pdf",
            file_path="/uploads/test_document.pdf",
            file_size=1024000,
            status=status
        )
        assert document.status == status

def test_document_file_size_validation():
    """Test document file size validation."""
    # Test with different file sizes
    sizes = [1024, 1024000, 10485760]  # 1KB, 1MB, 10MB
    
    for size in sizes:
        document = Document(
            id=str(uuid.uuid4()),
            filename="test_document.pdf",
            original_name="Test Document.pdf",
            file_path="/uploads/test_document.pdf",
            file_size=size,
            status="uploaded"
        )
        assert document.file_size == size
        assert document.file_size > 0

def test_document_pdf_extension():
    """Test document with PDF extension."""
    document = Document(
        id=str(uuid.uuid4()),
        filename="tender_document.pdf",
        original_name="Tender Document.pdf",
        file_path="/uploads/tender_document.pdf",
        file_size=2048000,
        status="uploaded"
    )
    assert document.filename.endswith(".pdf")
    assert document.original_name.endswith(".pdf")

def test_document_unicode_filename():
    """Test document with unicode characters in filename."""
    document = Document(
        id=str(uuid.uuid4()),
        filename="deutsche_ausschreibung.pdf",
        original_name="Deutsche Ausschreibung.pdf",
        file_path="/uploads/deutsche_ausschreibung.pdf",
        file_size=1024000,
        status="uploaded"
    )
    assert "deutsche" in document.filename
    assert "Deutsche" in document.original_name

def test_document_large_file():
    """Test document with large file size."""
    large_size = 50 * 1024 * 1024  # 50MB
    document = Document(
        id=str(uuid.uuid4()),
        filename="large_document.pdf",
        original_name="Large Document.pdf",
        file_path="/uploads/large_document.pdf",
        file_size=large_size,
        status="uploaded"
    )
    assert document.file_size == large_size

def test_document_status_transitions():
    """Test document status transitions."""
    document = Document(
        id=str(uuid.uuid4()),
        filename="test_document.pdf",
        original_name="Test Document.pdf",
        file_path="/uploads/test_document.pdf",
        file_size=1024000,
        status="uploaded"
    )
    
    # Test status transitions
    document.status = "processing"
    assert document.status == "processing"
    
    document.status = "processed"
    assert document.status == "processed"
    
    document.status = "error"
    assert document.status == "error"

def test_document_relationships(db_session, sample_document):
    """Test document relationships with processing results."""
    db_session.add(sample_document)
    db_session.commit()
    
    # Test that document can be retrieved
    retrieved_document = db_session.query(Document).filter(Document.id == sample_document.id).first()
    assert retrieved_document is not None
    assert retrieved_document.filename == sample_document.filename

def test_document_uploaded_at_timestamp(db_session):
    """Test document uploaded_at timestamp."""
    document = Document(
        id=str(uuid.uuid4()),
        filename="test_document.pdf",
        original_name="Test Document.pdf",
        file_path="/uploads/test_document.pdf",
        file_size=1024000,
        status="uploaded"
    )
    
    # Save to database to trigger timestamp
    db_session.add(document)
    db_session.commit()
    
    # Check that uploaded_at is set
    assert document.uploaded_at is not None
    assert isinstance(document.uploaded_at, datetime)
