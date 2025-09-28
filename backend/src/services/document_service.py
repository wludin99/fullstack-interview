"""Document service for managing document uploads and processing."""

import uuid
import os
import tempfile
import shutil
from typing import List, Optional
from sqlalchemy.orm import Session
from fastapi import UploadFile
from src.models.document import Document
from src.schemas.document import DocumentResponse, DocumentUploadResponse
from src.services.llm_service import LLMService


class DocumentService:
    """Service for document operations."""
    
    def __init__(self, db: Session, upload_dir: Optional[str] = None):
        self.db = db
        self.llm_service = LLMService()
        # Use provided upload_dir or create a temporary one for tests
        if upload_dir:
            self.upload_dir = upload_dir
        else:
            # Check if we're in a test environment
            if os.getenv('PYTEST_CURRENT_TEST') or 'test' in os.getcwd():
                # Use temporary directory for tests
                self.upload_dir = tempfile.mkdtemp(prefix='tender_test_uploads_')
            else:
                # Use production uploads directory
                self.upload_dir = "uploads"
        
        os.makedirs(self.upload_dir, exist_ok=True)
    
    def upload_document(self, file: UploadFile) -> DocumentUploadResponse:
        """Upload a document and save to database."""
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = os.path.splitext(file.filename)[1] if file.filename else ""
        filename = f"{file_id}{file_extension}"
        file_path = os.path.join(self.upload_dir, filename)
        
        # Save file to disk
        with open(file_path, "wb") as buffer:
            content = file.file.read()
            buffer.write(content)
        
        # Upload to Anthropic File API
        anthropic_file_id = None
        try:
            anthropic_file_id = self.llm_service.upload_file_to_anthropic(file_path)
        except Exception as e:
            # Log error but don't fail the upload
            print(f"Warning: Failed to upload to Anthropic: {e}")
        
        # Create document record
        document = Document(
            id=file_id,
            filename=filename,
            original_name=file.filename or "unknown",
            file_path=file_path,
            file_size=len(content),
            status="uploaded",
            anthropic_file_id=anthropic_file_id
        )
        
        self.db.add(document)
        self.db.commit()
        self.db.refresh(document)
        
        return DocumentUploadResponse(
            id=document.id,
            filename=document.filename,
            status=document.status,
            message="Document uploaded successfully"
        )
    
    def get_documents(self) -> List[DocumentResponse]:
        """Get all documents."""
        documents = self.db.query(Document).all()
        return [
            DocumentResponse(
                id=doc.id,
                filename=doc.filename,
                original_name=doc.original_name,
                file_size=doc.file_size,
                status=doc.status,
                uploaded_at=doc.uploaded_at
            )
            for doc in documents
        ]
    
    def get_document(self, document_id: str) -> Optional[Document]:
        """Get a specific document."""
        return self.db.query(Document).filter(Document.id == document_id).first()
    
    def delete_document(self, document_id: str) -> bool:
        """Delete a document and its file."""
        document = self.get_document(document_id)
        if not document:
            return False
        
        # Delete file from disk
        if os.path.exists(document.file_path):
            os.remove(document.file_path)
        
        # Delete from database
        self.db.delete(document)
        self.db.commit()
        return True
    
    def update_document_status(self, document_id: str, status: str) -> bool:
        """Update document processing status."""
        document = self.get_document(document_id)
        if not document:
            return False
        
        document.status = status
        self.db.commit()
        return True
    
    def cleanup_upload_dir(self):
        """Clean up the upload directory (useful for tests)."""
        if os.path.exists(self.upload_dir):
            shutil.rmtree(self.upload_dir)
    
    def is_temp_dir(self) -> bool:
        """Check if this is using a temporary directory."""
        return 'tender_test_uploads_' in self.upload_dir
