"""Unit tests for Condition model validation."""

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.condition import Condition
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
def sample_condition(sample_checklist):
    return Condition(
        id=str(uuid.uuid4()),
        checklist_id=sample_checklist.id,
        text="Test condition",
        order_index=1
    )

def test_condition_creation(sample_condition):
    """Test condition creation with valid data."""
    assert sample_condition.text == "Test condition"
    assert sample_condition.order_index == 1
    assert sample_condition.id is not None
    assert sample_condition.checklist_id is not None

def test_condition_text_validation():
    """Test condition text validation."""
    # Test with None text (should work as model allows it)
    condition = Condition(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text=None,
        order_index=1
    )
    assert condition.text is None

def test_condition_order_index_validation():
    """Test condition order index validation."""
    # Test with None order_index (should work as model allows it)
    condition = Condition(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="Test condition",
        order_index=None
    )
    assert condition.order_index is None

def test_condition_checklist_relationship(db_session, sample_checklist, sample_condition):
    """Test condition relationship with checklist."""
    db_session.add(sample_checklist)
    db_session.add(sample_condition)
    db_session.commit()
    
    # Test relationship
    assert sample_condition.checklist_id == sample_checklist.id
    assert sample_condition in sample_checklist.conditions

def test_condition_order_index_validation():
    """Test condition order index validation."""
    condition = Condition(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="Test condition",
        order_index=3
    )
    assert condition.order_index == 3
    assert condition.order_index > 0

def test_condition_empty_text():
    """Test condition with empty text."""
    condition = Condition(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="",
        order_index=1
    )
    assert condition.text == ""

def test_condition_long_text():
    """Test condition with very long text."""
    long_text = "A" * 1000
    condition = Condition(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text=long_text,
        order_index=1
    )
    assert condition.text == long_text

def test_condition_unicode_support():
    """Test condition with unicode characters."""
    condition = Condition(
        id=str(uuid.uuid4()),
        checklist_id=str(uuid.uuid4()),
        text="Die Ausschreibung entspricht den Vorgaben der Vergabeverordnung (VgV)",
        order_index=1
    )
    assert "Vergabeverordnung" in condition.text
    assert "VgV" in condition.text

def test_condition_german_examples():
    """Test condition with German tender examples."""
    german_conditions = [
        "Ist die Abgabefrist vor dem 31.12.2025?",
        "Sind alle erforderlichen Nachweise vollständig?",
        "Entspricht die Ausschreibung den Vorgaben der VgV?"
    ]
    
    for i, text in enumerate(german_conditions, 1):
        condition = Condition(
            id=str(uuid.uuid4()),
            checklist_id=str(uuid.uuid4()),
            text=text,
            order_index=i
        )
        assert condition.text == text
        assert condition.order_index == i

def test_condition_boolean_evaluation():
    """Test condition text that represents boolean evaluation."""
    boolean_conditions = [
        "Die Ausschreibung entspricht den Vorgaben der Vergabeverordnung (VgV)",
        "Alle erforderlichen Nachweise sind vollständig und gültig",
        "Die technischen Anforderungen sind erfüllt"
    ]
    
    for i, text in enumerate(boolean_conditions, 1):
        condition = Condition(
            id=str(uuid.uuid4()),
            checklist_id=str(uuid.uuid4()),
            text=text,
            order_index=i
        )
        assert condition.text == text
        # These should be evaluable as boolean conditions
        assert "entspricht" in condition.text or "vollständig" in condition.text or "erfüllt" in condition.text
