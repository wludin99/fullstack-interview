"""Unit tests for Checklist model validation."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
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

def test_checklist_creation(sample_checklist):
    """Test checklist creation with valid data."""
    assert sample_checklist.name == "Test Checklist"
    assert sample_checklist.description == "Test description"
    assert sample_checklist.id is not None

def test_checklist_name_validation():
    """Test checklist name validation."""
    # Test with None name (should work as model allows it)
    checklist = Checklist(
        id=str(uuid.uuid4()),
        name=None,
        description="Test description"
    )
    assert checklist.name is None

def test_checklist_relationships(db_session, sample_checklist):
    """Test checklist relationships with questions and conditions."""
    db_session.add(sample_checklist)
    db_session.flush()
    
    # Add questions
    question1 = Question(
        id=str(uuid.uuid4()),
        checklist_id=sample_checklist.id,
        text="Test question 1",
        order_index=1
    )
    question2 = Question(
        id=str(uuid.uuid4()),
        checklist_id=sample_checklist.id,
        text="Test question 2",
        order_index=2
    )
    
    # Add conditions
    condition1 = Condition(
        id=str(uuid.uuid4()),
        checklist_id=sample_checklist.id,
        text="Test condition 1",
        order_index=1
    )
    
    db_session.add_all([question1, question2, condition1])
    db_session.commit()
    
    # Test relationships
    assert len(sample_checklist.questions) == 2
    assert len(sample_checklist.conditions) == 1
    assert sample_checklist.questions[0].text == "Test question 1"
    assert sample_checklist.conditions[0].text == "Test condition 1"

def test_checklist_validation():
    """Test checklist field validation."""
    checklist = Checklist(
        id=str(uuid.uuid4()),
        name="Valid Name",
        description="Valid description"
    )
    
    assert checklist.name == "Valid Name"
    assert checklist.description == "Valid description"
    assert len(checklist.name) > 0
    assert len(checklist.description) > 0

def test_checklist_empty_name():
    """Test checklist with empty name."""
    checklist = Checklist(
        id=str(uuid.uuid4()),
        name="",
        description="Test description"
    )
    assert checklist.name == ""

def test_checklist_long_name():
    """Test checklist with very long name."""
    long_name = "A" * 1000
    checklist = Checklist(
        id=str(uuid.uuid4()),
        name=long_name,
        description="Test description"
    )
    assert checklist.name == long_name

def test_checklist_unicode_support():
    """Test checklist with unicode characters."""
    checklist = Checklist(
        id=str(uuid.uuid4()),
        name="Deutsche Ausschreibung - Test",
        description="Beschreibung mit Umlauten: äöü"
    )
    assert "äöü" in checklist.description
    assert "Deutsche" in checklist.name
