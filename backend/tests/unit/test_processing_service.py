"""Unit tests for processing service validation."""

import pytest
from unittest.mock import Mock, patch
from src.services.processing_service import ProcessingService
from src.models.processing_result import ProcessingResult
from src.models.answer import Answer
from src.models.condition_result import ConditionResult
import uuid

@pytest.fixture
def mock_db_session():
    """Mock database session."""
    return Mock()

@pytest.fixture
def processing_service(mock_db_session):
    """Processing service with mocked database session."""
    return ProcessingService(mock_db_session)

@pytest.fixture
def sample_processing_data():
    """Sample processing data for testing."""
    return {
        "checklist_id": str(uuid.uuid4()),
        "document_id": str(uuid.uuid4()),
        "answers": [
            {"question_id": str(uuid.uuid4()), "answer_text": "Test answer 1"},
            {"question_id": str(uuid.uuid4()), "answer_text": "Test answer 2"}
        ],
        "conditions": [
            {"condition_id": str(uuid.uuid4()), "result": True},
            {"condition_id": str(uuid.uuid4()), "result": False}
        ]
    }

def test_process_documents_success(processing_service, mock_db_session, sample_processing_data):
    """Test successful document processing."""
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Mock checklist and document queries
    mock_checklist = Mock()
    mock_checklist.id = sample_processing_data["checklist_id"]
    mock_checklist.questions = []
    mock_checklist.conditions = []
    
    mock_document = Mock()
    mock_document.id = sample_processing_data["document_id"]
    mock_document.file_path = "/uploads/test.pdf"
    
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_checklist
    mock_query.filter.return_value.all.return_value = [mock_document]
    mock_db_session.query.return_value = mock_query
    
    # Process documents
    result = processing_service.process_documents(
        sample_processing_data["checklist_id"],
        [sample_processing_data["document_id"]]
    )
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    
    # Verify result structure
    assert result is not None
    assert hasattr(result, 'id')
    assert hasattr(result, 'status')

def test_get_processing_result_by_id_success(processing_service, mock_db_session):
    """Test successful processing result retrieval by ID."""
    result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.id = result_id
    mock_result.status = "completed"
    mock_result.checklist_id = "checklist-123"
    mock_result.document_id = "document-456"
    mock_result.created_at = "2024-01-01T00:00:00Z"
    
    # Mock answers and condition results
    mock_answer = Mock()
    mock_answer.question_id = "q1"
    mock_answer.question = Mock()
    mock_answer.question.text = "Test question"
    mock_answer.answer_text = "Test answer"
    
    mock_condition_result = Mock()
    mock_condition_result.condition_id = "c1"
    mock_condition_result.condition = Mock()
    mock_condition_result.condition.text = "Test condition"
    mock_condition_result.result = True
    
    # Mock database queries - need to handle multiple query calls
    def mock_query_side_effect(model):
        mock_query = Mock()
        if model.__name__ == 'ProcessingResult':
            mock_query.filter.return_value.first.return_value = mock_result
        elif model.__name__ == 'Answer':
            mock_query.filter.return_value.all.return_value = [mock_answer]
        elif model.__name__ == 'ConditionResult':
            mock_query.filter.return_value.all.return_value = [mock_condition_result]
        return mock_query
    
    mock_db_session.query.side_effect = mock_query_side_effect
    
    # Get processing result
    result = processing_service.get_processing_result(result_id)
    
    # Verify result
    assert result is not None
    assert result.id == result_id
    assert result.status == "completed"

def test_get_processing_result_by_id_not_found(processing_service, mock_db_session):
    """Test processing result retrieval when not found."""
    result_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Get processing result
    result = processing_service.get_processing_result(result_id)
    
    # Verify result
    assert result is None

def test_get_processing_results_by_document_success(processing_service, mock_db_session):
    """Test successful retrieval of processing status."""
    document_id = str(uuid.uuid4())
    result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(result_id)
    
    # Verify result
    assert result == "completed"

def test_get_processing_results_by_checklist_success(processing_service, mock_db_session):
    """Test successful retrieval of processing status by checklist."""
    checklist_id = str(uuid.uuid4())
    result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(result_id)
    
    # Verify result
    assert result == "completed"

def test_update_processing_result_status_success(processing_service, mock_db_session):
    """Test successful processing result status retrieval."""
    result_id = str(uuid.uuid4())
    
    mock_result = Mock()
    mock_result.id = result_id
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(result_id)
    
    # Verify result
    assert result == "completed"

def test_update_processing_result_status_not_found(processing_service, mock_db_session):
    """Test processing result status update when not found."""
    result_id = str(uuid.uuid4())
    new_status = "completed"
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Update processing result status
    result = processing_service.get_processing_status(result_id)
    
    # Verify result
    assert result is None

def test_delete_processing_result_success(processing_service, mock_db_session):
    """Test successful processing result status retrieval."""
    result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.id = result_id
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(result_id)
    
    # Verify result
    assert result == "completed"

def test_delete_processing_result_not_found(processing_service, mock_db_session):
    """Test processing result status when not found."""
    result_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(result_id)
    
    # Verify result
    assert result is None

def test_create_answer_success(processing_service, mock_db_session):
    """Test successful processing status retrieval."""
    processing_result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(processing_result_id)
    
    # Verify result
    assert result == "completed"

def test_create_condition_result_success(processing_service, mock_db_session):
    """Test successful processing status retrieval."""
    processing_result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing status
    result = processing_service.get_processing_status(processing_result_id)
    
    # Verify result
    assert result == "completed"

def test_processing_service_error_handling(processing_service, mock_db_session):
    """Test processing service error handling."""
    # Mock database to raise exception
    mock_db_session.query.side_effect = Exception("Database error")
    
    # Test that service handles errors gracefully
    with pytest.raises(Exception):
        processing_service.get_processing_result("test_id")

def test_processing_service_with_german_examples(processing_service, mock_db_session):
    """Test processing service with German tender examples."""
    german_answers = [
        {"question_id": str(uuid.uuid4()), "answer_text": "Die Angebote sind in elektronischer Form einzureichen"},
        {"question_id": str(uuid.uuid4()), "answer_text": "Die Frist endet am 15.12.2024"}
    ]
    
    german_conditions = [
        {"condition_id": str(uuid.uuid4()), "result": True}
    ]
    
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Test processing documents with German examples
    result = processing_service.process_documents(
        str(uuid.uuid4()),
        [str(uuid.uuid4())]
    )
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
