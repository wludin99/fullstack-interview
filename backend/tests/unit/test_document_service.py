"""Unit tests for document service validation."""

import pytest
from unittest.mock import Mock, patch
from src.services.document_service import DocumentService
from src.models.document import Document
import uuid
import os

@pytest.fixture
def mock_db_session():
    """Mock database session."""
    return Mock()

@pytest.fixture
def document_service(mock_db_session):
    """Document service with mocked database session."""
    return DocumentService(mock_db_session)

@pytest.fixture
def sample_document_data():
    """Sample document data for testing."""
    return {
        "filename": "test_document.pdf",
        "original_name": "Test Document.pdf",
        "file_path": "/uploads/test_document.pdf",
        "file_size": 1024000,
        "status": "uploaded"
    }

def test_create_document_success(document_service, mock_db_session, sample_document_data):
    """Test successful document creation."""
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create document
    result = document_service.create_document(sample_document_data)
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    assert mock_db_session.refresh.called
    
    # Verify result structure
    assert result is not None
    assert hasattr(result, 'filename')
    assert hasattr(result, 'file_size')

def test_get_document_by_id_success(document_service, mock_db_session):
    """Test successful document retrieval by ID."""
    document_id = str(uuid.uuid4())
    mock_document = Mock()
    mock_document.id = document_id
    mock_document.filename = "test_document.pdf"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_document
    mock_db_session.query.return_value = mock_query
    
    # Get document
    result = document_service.get_document_by_id(document_id)
    
    # Verify result
    assert result is not None
    assert result.id == document_id
    assert result.filename == "test_document.pdf"

def test_get_document_by_id_not_found(document_service, mock_db_session):
    """Test document retrieval when not found."""
    document_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Get document
    result = document_service.get_document_by_id(document_id)
    
    # Verify result
    assert result is None

def test_get_all_documents_success(document_service, mock_db_session):
    """Test successful retrieval of all documents."""
    mock_documents = [
        Mock(id=str(uuid.uuid4()), filename="document1.pdf"),
        Mock(id=str(uuid.uuid4()), filename="document2.pdf")
    ]
    
    # Mock database query
    mock_query = Mock()
    mock_query.all.return_value = mock_documents
    mock_db_session.query.return_value = mock_query
    
    # Get all documents
    result = document_service.get_all_documents()
    
    # Verify result
    assert len(result) == 2
    assert result[0].filename == "document1.pdf"
    assert result[1].filename == "document2.pdf"

def test_update_document_status_success(document_service, mock_db_session):
    """Test successful document status update."""
    document_id = str(uuid.uuid4())
    new_status = "processed"
    
    mock_document = Mock()
    mock_document.id = document_id
    mock_document.status = "uploaded"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_document
    mock_db_session.query.return_value = mock_query
    mock_db_session.commit = Mock()
    
    # Update document status
    result = document_service.update_document_status(document_id, new_status)
    
    # Verify database operations
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is not None
    assert result.id == document_id

def test_update_document_status_not_found(document_service, mock_db_session):
    """Test document status update when not found."""
    document_id = str(uuid.uuid4())
    new_status = "processed"
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Update document status
    result = document_service.update_document_status(document_id, new_status)
    
    # Verify result
    assert result is None

def test_delete_document_success(document_service, mock_db_session):
    """Test successful document deletion."""
    document_id = str(uuid.uuid4())
    mock_document = Mock()
    mock_document.id = document_id
    mock_document.file_path = "/uploads/test_document.pdf"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_document
    mock_db_session.query.return_value = mock_query
    mock_db_session.delete = Mock()
    mock_db_session.commit = Mock()
    
    # Mock file system operations
    with patch('os.path.exists', return_value=True):
        with patch('os.remove') as mock_remove:
            # Delete document
            result = document_service.delete_document(document_id)
            
            # Verify database operations
            assert mock_db_session.delete.called
            assert mock_db_session.commit.called
            
            # Verify file system operations
            assert mock_remove.called
            
            # Verify result
            assert result is True

def test_delete_document_not_found(document_service, mock_db_session):
    """Test document deletion when not found."""
    document_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Delete document
    result = document_service.delete_document(document_id)
    
    # Verify result
    assert result is False

def test_validate_file_type_success(document_service):
    """Test successful file type validation."""
    # Test with valid PDF file
    result = document_service.validate_file_type("test_document.pdf")
    assert result is True
    
    # Test with valid PDF file (case insensitive)
    result = document_service.validate_file_type("test_document.PDF")
    assert result is True

def test_validate_file_type_failure(document_service):
    """Test file type validation failure."""
    # Test with invalid file types
    invalid_files = ["test_document.txt", "test_document.doc", "test_document.docx"]
    
    for filename in invalid_files:
        result = document_service.validate_file_type(filename)
        assert result is False

def test_validate_file_size_success(document_service):
    """Test successful file size validation."""
    # Test with valid file sizes (in bytes)
    valid_sizes = [1024, 1024000, 10485760]  # 1KB, 1MB, 10MB
    
    for size in valid_sizes:
        result = document_service.validate_file_size(size)
        assert result is True

def test_validate_file_size_failure(document_service):
    """Test file size validation failure."""
    # Test with invalid file sizes
    invalid_sizes = [0, -1, 50 * 1024 * 1024]  # 0 bytes, negative, 50MB
    
    for size in invalid_sizes:
        result = document_service.validate_file_size(size)
        assert result is False

def test_document_service_error_handling(document_service, mock_db_session):
    """Test document service error handling."""
    # Mock database to raise exception
    mock_db_session.query.side_effect = Exception("Database error")
    
    # Test that service handles errors gracefully
    with pytest.raises(Exception):
        document_service.get_all_documents()

def test_document_service_with_german_filenames(document_service, mock_db_session):
    """Test document service with German filenames."""
    german_document_data = {
        "filename": "deutsche_ausschreibung.pdf",
        "original_name": "Deutsche Ausschreibung.pdf",
        "file_path": "/uploads/deutsche_ausschreibung.pdf",
        "file_size": 2048000,
        "status": "uploaded"
    }
    
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create German document
    result = document_service.create_document(german_document_data)
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
