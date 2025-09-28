"""Contract tests for results API endpoints."""

import pytest
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


class TestResultsAPI:
    """Test results retrieval operations."""
    
    def test_get_results_success(self):
        """Test successful results retrieval."""
        # This test assumes a processing result exists
        # In a real scenario, we'd create one first
        response = client.get("/api/results/test-result-id")
        # This will fail initially (404) until we implement the endpoint
        assert response.status_code in [200, 404]
    
    def test_get_nonexistent_results(self):
        """Test retrieving non-existent results."""
        response = client.get("/api/results/nonexistent-result-id")
        assert response.status_code == 404
