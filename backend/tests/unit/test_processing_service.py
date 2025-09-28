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

def test_create_processing_result_success(processing_service, mock_db_session, sample_processing_data):
    """Test successful processing result creation."""
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create processing result
    result = processing_service.create_processing_result(
        sample_processing_data["checklist_id"],
        sample_processing_data["document_id"],
        sample_processing_data["answers"],
        sample_processing_data["conditions"]
    )
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    assert mock_db_session.refresh.called
    
    # Verify result structure
    assert result is not None
    assert hasattr(result, 'checklist_id')
    assert hasattr(result, 'document_id')

def test_get_processing_result_by_id_success(processing_service, mock_db_session):
    """Test successful processing result retrieval by ID."""
    result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.id = result_id
    mock_result.status = "completed"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    
    # Get processing result
    result = processing_service.get_processing_result_by_id(result_id)
    
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
    result = processing_service.get_processing_result_by_id(result_id)
    
    # Verify result
    assert result is None

def test_get_processing_results_by_document_success(processing_service, mock_db_session):
    """Test successful retrieval of processing results by document."""
    document_id = str(uuid.uuid4())
    mock_results = [
        Mock(id=str(uuid.uuid4()), document_id=document_id),
        Mock(id=str(uuid.uuid4()), document_id=document_id)
    ]
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.all.return_value = mock_results
    mock_db_session.query.return_value = mock_query
    
    # Get processing results
    result = processing_service.get_processing_results_by_document(document_id)
    
    # Verify result
    assert len(result) == 2
    assert result[0].document_id == document_id
    assert result[1].document_id == document_id

def test_get_processing_results_by_checklist_success(processing_service, mock_db_session):
    """Test successful retrieval of processing results by checklist."""
    checklist_id = str(uuid.uuid4())
    mock_results = [
        Mock(id=str(uuid.uuid4()), checklist_id=checklist_id),
        Mock(id=str(uuid.uuid4()), checklist_id=checklist_id)
    ]
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.all.return_value = mock_results
    mock_db_session.query.return_value = mock_query
    
    # Get processing results
    result = processing_service.get_processing_results_by_checklist(checklist_id)
    
    # Verify result
    assert len(result) == 2
    assert result[0].checklist_id == checklist_id
    assert result[1].checklist_id == checklist_id

def test_update_processing_result_status_success(processing_service, mock_db_session):
    """Test successful processing result status update."""
    result_id = str(uuid.uuid4())
    new_status = "completed"
    
    mock_result = Mock()
    mock_result.id = result_id
    mock_result.status = "processing"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    mock_db_session.commit = Mock()
    
    # Update processing result status
    result = processing_service.update_processing_result_status(result_id, new_status)
    
    # Verify database operations
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is not None
    assert result.id == result_id

def test_update_processing_result_status_not_found(processing_service, mock_db_session):
    """Test processing result status update when not found."""
    result_id = str(uuid.uuid4())
    new_status = "completed"
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Update processing result status
    result = processing_service.update_processing_result_status(result_id, new_status)
    
    # Verify result
    assert result is None

def test_delete_processing_result_success(processing_service, mock_db_session):
    """Test successful processing result deletion."""
    result_id = str(uuid.uuid4())
    mock_result = Mock()
    mock_result.id = result_id
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_result
    mock_db_session.query.return_value = mock_query
    mock_db_session.delete = Mock()
    mock_db_session.commit = Mock()
    
    # Delete processing result
    result = processing_service.delete_processing_result(result_id)
    
    # Verify database operations
    assert mock_db_session.delete.called
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is True

def test_delete_processing_result_not_found(processing_service, mock_db_session):
    """Test processing result deletion when not found."""
    result_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Delete processing result
    result = processing_service.delete_processing_result(result_id)
    
    # Verify result
    assert result is False

def test_create_answer_success(processing_service, mock_db_session):
    """Test successful answer creation."""
    processing_result_id = str(uuid.uuid4())
    question_id = str(uuid.uuid4())
    answer_text = "Test answer"
    
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create answer
    result = processing_service.create_answer(processing_result_id, question_id, answer_text)
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is not None
    assert result.processing_result_id == processing_result_id
    assert result.question_id == question_id
    assert result.answer_text == answer_text

def test_create_condition_result_success(processing_service, mock_db_session):
    """Test successful condition result creation."""
    processing_result_id = str(uuid.uuid4())
    condition_id = str(uuid.uuid4())
    result_value = True
    
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create condition result
    result = processing_service.create_condition_result(processing_result_id, condition_id, result_value)
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is not None
    assert result.processing_result_id == processing_result_id
    assert result.condition_id == condition_id
    assert result.result == result_value

def test_processing_service_error_handling(processing_service, mock_db_session):
    """Test processing service error handling."""
    # Mock database to raise exception
    mock_db_session.query.side_effect = Exception("Database error")
    
    # Test that service handles errors gracefully
    with pytest.raises(Exception):
        processing_service.get_processing_result_by_id("test_id")

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
    
    # Create processing result with German examples
    result = processing_service.create_processing_result(
        str(uuid.uuid4()),
        str(uuid.uuid4()),
        german_answers,
        german_conditions
    )
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
