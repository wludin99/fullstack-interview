"""Unit tests for ProcessingResult model validation."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.processing_result import ProcessingResult
from src.models.answer import Answer
from src.models.condition_result import ConditionResult
from src.models.checklist import Checklist
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
def sample_checklist():
    return Checklist(
        id=str(uuid.uuid4()),
        name="Test Checklist",
        description="Test description"
    )

@pytest.fixture
def sample_document():
    return Document(
        id=str(uuid.uuid4()),
        filename="test_document.pdf",
        original_name="Test Document.pdf",
        file_path="/uploads/test_document.pdf",
        file_size=1024000,
        status="uploaded"
    )

@pytest.fixture
def sample_processing_result(sample_checklist, sample_document):
    return ProcessingResult(
        id=str(uuid.uuid4()),
        checklist_id=sample_checklist.id,
        document_id=sample_document.id,
        status="completed"
    )

def test_processing_result_creation(sample_processing_result):
    """Test processing result creation with valid data."""
    assert sample_processing_result.status == "completed"
    assert sample_processing_result.id is not None
    assert sample_processing_result.checklist_id is not None
    assert sample_processing_result.document_id is not None

def test_processing_result_status_validation():
    """Test processing result status validation."""
    valid_statuses = ["processing", "completed", "error"]
    
    for status in valid_statuses:
        result = ProcessingResult(
            id=str(uuid.uuid4()),
            checklist_id=str(uuid.uuid4()),
            document_id=str(uuid.uuid4()),
            status=status
        )
        assert result.status == status

def test_processing_result_required_fields():
    """Test that required fields are present."""
    result = ProcessingResult(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        document_id=str(uuid.uuid4()),
        status="completed"
    )
    
    assert result.checklist_id is not None
    assert result.document_id is not None
    assert result.status is not None

def test_processing_result_error_message():
    """Test processing result with error message."""
    result = ProcessingResult(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        document_id=str(uuid.uuid4()),
        status="error",
        error_message="Processing failed due to API error"
    )
    
    assert result.status == "error"
    assert result.error_message == "Processing failed due to API error"

def test_processing_result_relationships(db_session, sample_processing_result):
    """Test processing result relationships."""
    db_session.add(sample_processing_result)
    db_session.commit()
    
    # Test that processing result can be retrieved
    retrieved_result = db_session.query(ProcessingResult).filter(
        ProcessingResult.id == sample_processing_result.id
    ).first()
    assert retrieved_result is not None
    assert retrieved_result.status == sample_processing_result.status

def test_answer_creation():
    """Test answer creation with valid data."""
    answer = Answer(
        id=str(uuid.uuid4()),
        processing_result_id=str(uuid.uuid4()),
        question_id=str(uuid.uuid4()),
        answer_text="Test answer"
    )
    
    assert answer.answer_text == "Test answer"
    assert answer.id is not None

def test_answer_required_fields():
    """Test that answer required fields are present."""
    answer = Answer(
        id=str(uuid.uuid4()),
        processing_result_id=str(uuid.uuid4()),
        question_id=str(uuid.uuid4()),
        answer_text="Test answer"
    )
    
    assert answer.processing_result_id is not None
    assert answer.question_id is not None
    assert answer.answer_text is not None

def test_condition_result_creation():
    """Test condition result creation with valid data."""
    condition_result = ConditionResult(
        id=str(uuid.uuid4()),
        processing_result_id=str(uuid.uuid4()),
        condition_id=str(uuid.uuid4()),
        result=True
    )
    
    assert condition_result.result is True
    assert condition_result.id is not None

def test_condition_result_boolean_values():
    """Test condition result with different boolean values."""
    # Test True result
    true_result = ConditionResult(
        id=str(uuid.uuid4()),
        processing_result_id=str(uuid.uuid4()),
        condition_id=str(uuid.uuid4()),
        result=True
    )
    assert true_result.result is True
    
    # Test False result
    false_result = ConditionResult(
        id=str(uuid.uuid4()),
        processing_result_id=str(uuid.uuid4()),
        condition_id=str(uuid.uuid4()),
        result=False
    )
    assert false_result.result is False

def test_processing_result_with_answers_and_conditions(db_session, sample_processing_result):
    """Test processing result with associated answers and conditions."""
    db_session.add(sample_processing_result)
    db_session.flush()
    
    # Add answer
    answer = Answer(
        id=str(uuid.uuid4()),
        processing_result_id=sample_processing_result.id,
        question_id=str(uuid.uuid4()),
        answer_text="Test answer"
    )
    
    # Add condition result
    condition_result = ConditionResult(
        id=str(uuid.uuid4()),
        processing_result_id=sample_processing_result.id,
        condition_id=str(uuid.uuid4()),
        result=True
    )
    
    db_session.add_all([answer, condition_result])
    db_session.commit()
    
    # Test relationships
    assert len(sample_processing_result.answers) == 1
    assert len(sample_processing_result.condition_results) == 1
    assert sample_processing_result.answers[0].answer_text == "Test answer"
    assert sample_processing_result.condition_results[0].result is True

def test_processing_result_created_at_timestamp():
    """Test processing result created_at timestamp."""
    result = ProcessingResult(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        document_id=str(uuid.uuid4()),
        status="completed"
    )
    
    # Check that created_at is set
    assert result.created_at is not None
    assert isinstance(result.created_at, datetime)
