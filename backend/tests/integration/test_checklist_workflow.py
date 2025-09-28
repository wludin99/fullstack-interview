"""Integration tests for checklist CRUD workflow."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestChecklistWorkflow:
    """Test complete checklist workflow."""
    
    def test_complete_checklist_workflow(self):
        """Test complete checklist creation, update, and deletion workflow."""
        # 1. Create checklist
        checklist_data = {
            "name": "German Tender Checklist",
            "description": "Complete workflow test",
            "questions": [
                {
                    "text": "In welcher Form sind die Angebote einzureichen?",
                    "orderIndex": 1
                },
                {
                    "text": "Wann ist die Frist für Bieterfragen?",
                    "orderIndex": 2
                }
            ],
            "conditions": [
                {
                    "text": "Ist das Angebot vollständig?",
                    "orderIndex": 1
                }
            ]
        }
        
        create_response = client.post("/api/checklists", json=checklist_data)
        assert create_response.status_code == 201
        checklist_id = create_response.json()["id"]
        
        # 2. Retrieve checklist
        get_response = client.get(f"/api/checklists/{checklist_id}")
        assert get_response.status_code == 200
        retrieved_data = get_response.json()
        assert retrieved_data["name"] == "German Tender Checklist"
        assert len(retrieved_data["questions"]) == 2
        assert len(retrieved_data["conditions"]) == 1
        
        # 3. Update checklist
        update_data = {
            "name": "Updated German Tender Checklist",
            "description": "Updated description",
            "questions": [
                {
                    "text": "Updated question?",
                    "orderIndex": 1
                }
            ],
            "conditions": [
                {
                    "text": "Updated condition",
                    "orderIndex": 1
                }
            ]
        }
        
        update_response = client.put(f"/api/checklists/{checklist_id}", json=update_data)
        assert update_response.status_code == 200
        updated_data = update_response.json()
        assert updated_data["name"] == "Updated German Tender Checklist"
        
        # 4. List all checklists
        list_response = client.get("/api/checklists")
        assert list_response.status_code == 200
        checklists = list_response.json()
        assert len(checklists) >= 1
        
        # 5. Delete checklist
        delete_response = client.delete(f"/api/checklists/{checklist_id}")
        assert delete_response.status_code == 204
        
        # 6. Verify deletion
        final_get_response = client.get(f"/api/checklists/{checklist_id}")
        assert final_get_response.status_code == 404
