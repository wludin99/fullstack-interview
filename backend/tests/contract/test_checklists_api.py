"""Contract tests for checklist API endpoints."""

import pytest


class TestChecklistAPI:
    """Test checklist CRUD operations."""
    
    def test_create_checklist_success(self, client):
        """Test successful checklist creation."""
        checklist_data = {
            "name": "German Tender Checklist",
            "description": "Standard checklist for German public tenders",
            "questions": [
                {
                    "text": "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Ist das Angebot vollständig?",
                    "orderIndex": 1
                }
            ]
        }
        
        response = client.post("/api/checklists", json=checklist_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "German Tender Checklist"
        assert "id" in data
        assert len(data["questions"]) == 1
        assert len(data["conditions"]) == 1
    
    def test_get_checklists_success(self, client):
        """Test successful checklist retrieval."""
        response = client.get("/api/checklists")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
    
    def test_get_checklist_by_id_success(self, client):
        """Test successful single checklist retrieval."""
        # First create a checklist
        checklist_data = {
            "name": "Test Checklist",
            "description": "Test description",
            "questions": [],
            "conditions": []
        }
        create_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = create_response.json()["id"]
        
        # Then retrieve it
        response = client.get(f"/api/checklists/{checklist_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == checklist_id
        assert data["name"] == "Test Checklist"
    
    def test_update_checklist_success(self, client):
        """Test successful checklist update."""
        # First create a checklist
        checklist_data = {
            "name": "Original Name",
            "description": "Original description",
            "questions": [],
            "conditions": []
        }
        create_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = create_response.json()["id"]
        
        # Then update it
        update_data = {
            "name": "Updated Name",
            "description": "Updated description",
            "questions": [],
            "conditions": []
        }
        response = client.put(f"/api/checklists/{checklist_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Name"
        assert data["description"] == "Updated description"
    
    def test_delete_checklist_success(self, client):
        """Test successful checklist deletion."""
        # First create a checklist
        checklist_data = {
            "name": "To Delete",
            "description": "This will be deleted",
            "questions": [],
            "conditions": []
        }
        create_response = client.post("/api/checklists", json=checklist_data)
        checklist_id = create_response.json()["id"]
        
        # Then delete it
        response = client.delete(f"/api/checklists/{checklist_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        get_response = client.get(f"/api/checklists/{checklist_id}")
        assert get_response.status_code == 404
    
    def test_create_checklist_validation_error(self, client):
        """Test checklist creation with invalid data."""
        invalid_data = {
            "name": "",  # Empty name should fail
            "description": "Test",
            "questions": [],
            "conditions": []
        }
        
        response = client.post("/api/checklists", json=invalid_data)
        assert response.status_code == 422
    
    def test_get_nonexistent_checklist(self, client):
        """Test retrieving non-existent checklist."""
        response = client.get("/api/checklists/nonexistent-id")
        assert response.status_code == 404
