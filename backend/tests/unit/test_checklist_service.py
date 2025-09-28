"""Unit tests for checklist service validation."""

import pytest
from unittest.mock import Mock, patch
from src.services.checklist_service import ChecklistService
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
import uuid

@pytest.fixture
def mock_db_session():
    """Mock database session."""
    return Mock()

@pytest.fixture
def checklist_service(mock_db_session):
    """Checklist service with mocked database session."""
    return ChecklistService(mock_db_session)

@pytest.fixture
def sample_checklist_data():
    """Sample checklist data for testing."""
    return {
        "name": "Test Checklist",
        "description": "Test description",
        "questions": [
            {"text": "Test question 1?", "order_index": 1},
            {"text": "Test question 2?", "order_index": 2}
        ],
        "conditions": [
            {"text": "Test condition 1", "order_index": 1},
            {"text": "Test condition 2", "order_index": 2}
        ]
    }

def test_create_checklist_success(checklist_service, mock_db_session, sample_checklist_data):
    """Test successful checklist creation."""
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create checklist
    result = checklist_service.create_checklist(sample_checklist_data)
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
    assert mock_db_session.refresh.called
    
    # Verify result structure
    assert result is not None
    assert hasattr(result, 'name')
    assert hasattr(result, 'description')

def test_create_checklist_with_questions_and_conditions(checklist_service, mock_db_session, sample_checklist_data):
    """Test checklist creation with questions and conditions."""
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create checklist
    result = checklist_service.create_checklist(sample_checklist_data)
    
    # Verify that questions and conditions are added
    assert mock_db_session.add.call_count >= 3  # checklist + 2 questions + 2 conditions

def test_get_checklist_by_id_success(checklist_service, mock_db_session):
    """Test successful checklist retrieval by ID."""
    checklist_id = str(uuid.uuid4())
    mock_checklist = Mock()
    mock_checklist.id = checklist_id
    mock_checklist.name = "Test Checklist"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_checklist
    mock_db_session.query.return_value = mock_query
    
    # Get checklist
    result = checklist_service.get_checklist_by_id(checklist_id)
    
    # Verify result
    assert result is not None
    assert result.id == checklist_id
    assert result.name == "Test Checklist"

def test_get_checklist_by_id_not_found(checklist_service, mock_db_session):
    """Test checklist retrieval when not found."""
    checklist_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Get checklist
    result = checklist_service.get_checklist_by_id(checklist_id)
    
    # Verify result
    assert result is None

def test_get_all_checklists_success(checklist_service, mock_db_session):
    """Test successful retrieval of all checklists."""
    mock_checklists = [
        Mock(id=str(uuid.uuid4()), name="Checklist 1"),
        Mock(id=str(uuid.uuid4()), name="Checklist 2")
    ]
    
    # Mock database query
    mock_query = Mock()
    mock_query.all.return_value = mock_checklists
    mock_db_session.query.return_value = mock_query
    
    # Get all checklists
    result = checklist_service.get_all_checklists()
    
    # Verify result
    assert len(result) == 2
    assert result[0].name == "Checklist 1"
    assert result[1].name == "Checklist 2"

def test_update_checklist_success(checklist_service, mock_db_session):
    """Test successful checklist update."""
    checklist_id = str(uuid.uuid4())
    update_data = {
        "name": "Updated Checklist",
        "description": "Updated description"
    }
    
    mock_checklist = Mock()
    mock_checklist.id = checklist_id
    mock_checklist.name = "Original Name"
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_checklist
    mock_db_session.query.return_value = mock_query
    mock_db_session.commit = Mock()
    
    # Update checklist
    result = checklist_service.update_checklist(checklist_id, update_data)
    
    # Verify database operations
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is not None
    assert result.id == checklist_id

def test_update_checklist_not_found(checklist_service, mock_db_session):
    """Test checklist update when not found."""
    checklist_id = str(uuid.uuid4())
    update_data = {"name": "Updated Checklist"}
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Update checklist
    result = checklist_service.update_checklist(checklist_id, update_data)
    
    # Verify result
    assert result is None

def test_delete_checklist_success(checklist_service, mock_db_session):
    """Test successful checklist deletion."""
    checklist_id = str(uuid.uuid4())
    mock_checklist = Mock()
    mock_checklist.id = checklist_id
    
    # Mock database query
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = mock_checklist
    mock_db_session.query.return_value = mock_query
    mock_db_session.delete = Mock()
    mock_db_session.commit = Mock()
    
    # Delete checklist
    result = checklist_service.delete_checklist(checklist_id)
    
    # Verify database operations
    assert mock_db_session.delete.called
    assert mock_db_session.commit.called
    
    # Verify result
    assert result is True

def test_delete_checklist_not_found(checklist_service, mock_db_session):
    """Test checklist deletion when not found."""
    checklist_id = str(uuid.uuid4())
    
    # Mock database query to return None
    mock_query = Mock()
    mock_query.filter.return_value.first.return_value = None
    mock_db_session.query.return_value = mock_query
    
    # Delete checklist
    result = checklist_service.delete_checklist(checklist_id)
    
    # Verify result
    assert result is False

def test_checklist_service_error_handling(checklist_service, mock_db_session):
    """Test checklist service error handling."""
    # Mock database to raise exception
    mock_db_session.query.side_effect = Exception("Database error")
    
    # Test that service handles errors gracefully
    with pytest.raises(Exception):
        checklist_service.get_all_checklists()

def test_checklist_service_with_german_examples(checklist_service, mock_db_session):
    """Test checklist service with German tender examples."""
    german_checklist_data = {
        "name": "Deutsche Ausschreibung Checkliste",
        "description": "Checkliste für deutsche Vergabeverfahren",
        "questions": [
            {"text": "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?", "order_index": 1},
            {"text": "Wann ist die Frist für die Einreichung von Bieterfragen?", "order_index": 2}
        ],
        "conditions": [
            {"text": "Ist die Abgabefrist vor dem 31.12.2025?", "order_index": 1}
        ]
    }
    
    # Mock database operations
    mock_db_session.add = Mock()
    mock_db_session.commit = Mock()
    mock_db_session.refresh = Mock()
    
    # Create German checklist
    result = checklist_service.create_checklist(german_checklist_data)
    
    # Verify database operations
    assert mock_db_session.add.called
    assert mock_db_session.commit.called
