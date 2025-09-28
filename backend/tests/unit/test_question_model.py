"""Unit tests for Question model validation."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.question import Question
from src.models.checklist import Checklist
from src.database import Base
import uuid

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
def sample_question(sample_checklist):
    return Question(
        id=str(uuid.uuid4()),
        checklist_id=sample_checklist.id,
        text="Test question?",
        order_index=1
    )

def test_question_creation(sample_question):
    """Test question creation with valid data."""
    assert sample_question.text == "Test question?"
    assert sample_question.order_index == 1
    assert sample_question.id is not None
    assert sample_question.checklist_id is not None

def test_question_text_validation():
    """Test question text validation."""
    # Test with None text (should work as model allows it)
    question = Question(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text=None,
        order_index=1
    )
    assert question.text is None

def test_question_order_index_validation():
    """Test question order index validation."""
    # Test with None order_index (should work as model allows it)
    question = Question(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="Test question",
        order_index=None
    )
    assert question.order_index is None

def test_question_checklist_relationship(db_session, sample_checklist, sample_question):
    """Test question relationship with checklist."""
    db_session.add(sample_checklist)
    db_session.add(sample_question)
    db_session.commit()
    
    # Test relationship
    assert sample_question.checklist_id == sample_checklist.id
    assert sample_question in sample_checklist.questions

def test_question_order_index_validation():
    """Test question order index validation."""
    question = Question(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="Test question",
        order_index=5
    )
    assert question.order_index == 5
    assert question.order_index > 0

def test_question_empty_text():
    """Test question with empty text."""
    question = Question(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="",
        order_index=1
    )
    assert question.text == ""

def test_question_long_text():
    """Test question with very long text."""
    long_text = "A" * 1000 + "?"
    question = Question(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text=long_text,
        order_index=1
    )
    assert question.text == long_text

def test_question_unicode_support():
    """Test question with unicode characters."""
    question = Question(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="Welche Art von Leistung wird ausgeschrieben?",
        order_index=1
    )
    assert "ausgeschrieben" in question.text
    assert "Leistung" in question.text

def test_question_german_examples():
    """Test question with German tender examples."""
    german_questions = [
        "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?",
        "Wann ist die Frist für die Einreichung von Bieterfragen?",
        "Welche Vergabeverfahren wird angewendet?"
    ]
    
    for i, text in enumerate(german_questions, 1):
        question = Question(
            id=str(uuid.uuid4()),
            checklist_id=str(uuid.uuid4()),
            text=text,
            order_index=i
        )
        assert question.text == text
        assert question.order_index == i
