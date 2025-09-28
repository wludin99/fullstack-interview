"""Test configuration and fixtures."""

import pytest
import tempfile
import shutil
import os
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.database import get_db, Base
from src.config import settings


# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client():
    """Create test client with database setup."""
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Override database dependency
    app.dependency_overrides[get_db] = override_get_db
    
    # Create test client
    with TestClient(app) as test_client:
        yield test_client
    
    # Clean up
    Base.metadata.drop_all(bind=engine)
    app.dependency_overrides.clear()


@pytest.fixture(autouse=True)
def cleanup_uploads():
    """Automatically clean up upload directories after each test."""
    yield
    
    # Clean up any temporary upload directories created during tests
    for root, dirs, files in os.walk("."):
        for dir_name in dirs:
            if 'tender_test_uploads_' in dir_name:
                full_path = os.path.join(root, dir_name)
                if os.path.exists(full_path):
                    shutil.rmtree(full_path)
    
    # Also clean up the main uploads directory if it exists and is empty
    uploads_dir = "uploads"
    if os.path.exists(uploads_dir):
        try:
            # Only remove if it's empty
            if not os.listdir(uploads_dir):
                os.rmdir(uploads_dir)
        except OSError:
            # Directory not empty or other error, leave it alone
            pass
