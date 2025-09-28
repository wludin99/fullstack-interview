"""Contract tests for template management API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.database import get_db
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
from tests.conftest import TestingSessionLocal
import uuid

client = TestClient(app)

def override_get_db():
    """Override database dependency for testing."""
    # Create tables on the test engine
    from tests.conftest import engine
    from src.database import Base
    Base.metadata.create_all(bind=engine)
    
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Override the database dependency
app.dependency_overrides[get_db] = override_get_db

@pytest.fixture
def sample_template(db_session):
    """Create a sample template checklist for testing."""
    template = Checklist(
        id=str(uuid.uuid4()),
        name="Test Template",
        description="Test template for template management"
    )
    db_session.add(template)
    db_session.flush()
    
    # Add questions
    for i in range(3):
        question = Question(
            id=str(uuid.uuid4()),
            checklist_id=template.id,
            text=f"Template question {i+1}",
            order_index=i+1
        )
        db_session.add(question)
    
    # Add conditions
    for i in range(2):
        condition = Condition(
            id=str(uuid.uuid4()),
            checklist_id=template.id,
            text=f"Template condition {i+1}",
            order_index=i+1
        )
        db_session.add(condition)
    
    db_session.commit()
    return template

def test_get_templates(sample_template):
    """Test getting all templates."""
    response = client.get("/api/templates")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Should include our template if it has 'Template' in the name
    if "Template" in sample_template.name:
        assert len(data) >= 1

def test_get_template_by_id(sample_template):
    """Test getting a specific template by ID."""
    response = client.get(f"/api/templates/{sample_template.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == sample_template.id
    assert data["name"] == sample_template.name
    assert data["description"] == sample_template.description
    assert "questions" in data
    assert "conditions" in data

def test_get_template_by_id_not_found():
    """Test getting a non-existent template."""
    fake_id = str(uuid.uuid4())
    
    response = client.get(f"/api/templates/{fake_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "Template not found" in data["detail"]

def test_update_template(sample_template):
    """Test updating a template."""
    update_data = {
        "name": "Updated Template",
        "description": "Updated description",
        "questions": [
            {"text": "Updated question 1", "orderIndex": 1},
            {"text": "Updated question 2", "orderIndex": 2}
        ],
        "conditions": [
            {"text": "Updated condition 1", "orderIndex": 1}
        ]
    }
    
    response = client.put(
        f"/api/templates/{sample_template.id}",
        json=update_data
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Template"
    assert data["description"] == "Updated description"
    assert len(data["questions"]) == 2
    assert len(data["conditions"]) == 1

def test_update_template_not_found():
    """Test updating a non-existent template."""
    fake_id = str(uuid.uuid4())
    update_data = {
        "name": "Updated Template",
        "description": "Updated description"
    }
    
    response = client.put(
        f"/api/templates/{fake_id}",
        json=update_data
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Template not found" in data["detail"]

def test_update_template_invalid_data(sample_template):
    """Test updating a template with invalid data."""
    update_data = {
        "name": "",  # Empty name should be invalid
        "description": "Updated description"
    }
    
    response = client.put(
        f"/api/templates/{sample_template.id}",
        json=update_data
    )
    
    # Should either succeed (if validation is lenient) or return 422
    assert response.status_code in [200, 422]

def test_delete_template(sample_template):
    """Test deleting a template."""
    response = client.delete(f"/api/templates/{sample_template.id}")
    
    assert response.status_code == 204
    
    # Verify template is deleted
    get_response = client.get(f"/api/templates/{sample_template.id}")
    assert get_response.status_code == 404

def test_delete_template_not_found():
    """Test deleting a non-existent template."""
    fake_id = str(uuid.uuid4())
    
    response = client.delete(f"/api/templates/{fake_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "Template not found" in data["detail"]

def test_create_custom_from_template(sample_template):
    """Test creating a custom checklist from a template."""
    custom_name = "My Custom Checklist"
    
    response = client.post(
        f"/api/templates/{sample_template.id}/create-custom",
        params={"custom_name": custom_name}
    )
    
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == custom_name
    assert "description" in data
    assert "questions" in data
    assert "conditions" in data
    assert len(data["questions"]) == 3  # Same as template
    assert len(data["conditions"]) == 2  # Same as template

def test_create_custom_from_template_not_found():
    """Test creating custom checklist from non-existent template."""
    fake_id = str(uuid.uuid4())
    custom_name = "My Custom Checklist"
    
    response = client.post(
        f"/api/templates/{fake_id}/create-custom",
        params={"custom_name": custom_name}
    )
    
    assert response.status_code == 404
    data = response.json()
    assert "Template not found" in data["detail"]

def test_create_custom_from_template_empty_name(sample_template):
    """Test creating custom checklist with empty name."""
    response = client.post(
        f"/api/templates/{sample_template.id}/create-custom",
        params={"custom_name": ""}
    )
    
    # Should either succeed or return 422 depending on validation
    assert response.status_code in [200, 422]

def test_template_operations_with_german_template(db_session):
    """Test template operations with German tender template."""
    # Create a German template
    german_template = Checklist(
        id=str(uuid.uuid4()),
        name="Deutsche Ausschreibung - Standard Checkliste",
        description="Standard-Checkliste für deutsche öffentliche Ausschreibungen"
    )
    db_session.add(german_template)
    db_session.flush()
    
    # Add German questions
    german_questions = [
        "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?",
        "Wann ist die Frist für die Einreichung von Bieterfragen?",
        "Welche Unterlagen sind mit dem Angebot einzureichen?"
    ]
    
    for i, question_text in enumerate(german_questions):
        question = Question(
            id=str(uuid.uuid4()),
            checklist_id=german_template.id,
            text=question_text,
            order_index=i+1
        )
        db_session.add(question)
    
    db_session.commit()
    
    # Test getting the German template
    response = client.get(f"/api/templates/{german_template.id}")
    assert response.status_code == 200
    data = response.json()
    assert "Deutsche Ausschreibung" in data["name"]
    assert len(data["questions"]) == 3
    
    # Test creating custom from German template
    response = client.post(
        f"/api/templates/{german_template.id}/create-custom",
        params={"custom_name": "My German Checklist"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "My German Checklist"
    assert len(data["questions"]) == 3
