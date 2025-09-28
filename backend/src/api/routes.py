"""API routes for the Tender Checklist App."""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from src.database import get_db
from src.models.checklist import Checklist
from src.models.document import Document
from src.models.processing_result import ProcessingResult
from src.schemas.checklist import ChecklistCreate, ChecklistUpdate, ChecklistResponse
from src.schemas.document import DocumentResponse, DocumentUploadResponse
from src.schemas.processing import ProcessingRequest, ProcessingResponse, ResultsResponse, BatchProcessingRequest, BatchProcessingResponse
from src.services.checklist_service import ChecklistService
from src.services.document_service import DocumentService
from src.services.processing_service import ProcessingService
from src.services.batch_processing_service import BatchProcessingService
from src.services.template_service import TemplateService

router = APIRouter()

# Checklist endpoints
@router.post("/checklists", response_model=ChecklistResponse, status_code=201)
async def create_checklist(
    checklist: ChecklistCreate,
    db: Session = Depends(get_db)
):
    """Create a new checklist."""
    # Validate required fields
    if not checklist.name or not checklist.name.strip():
        raise HTTPException(status_code=422, detail="Name is required")
    
    service = ChecklistService(db)
    return service.create_checklist(checklist)

@router.get("/checklists", response_model=List[ChecklistResponse])
async def get_checklists(db: Session = Depends(get_db)):
    """Get all checklists."""
    service = ChecklistService(db)
    return service.get_checklists()

@router.get("/checklists/{checklist_id}", response_model=ChecklistResponse)
async def get_checklist(
    checklist_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific checklist."""
    service = ChecklistService(db)
    checklist = service.get_checklist(checklist_id)
    if not checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return checklist

@router.put("/checklists/{checklist_id}", response_model=ChecklistResponse)
async def update_checklist(
    checklist_id: str,
    checklist: ChecklistUpdate,
    db: Session = Depends(get_db)
):
    """Update a checklist."""
    service = ChecklistService(db)
    updated_checklist = service.update_checklist(checklist_id, checklist)
    if not updated_checklist:
        raise HTTPException(status_code=404, detail="Checklist not found")
    return updated_checklist

@router.delete("/checklists/{checklist_id}", status_code=204)
async def delete_checklist(
    checklist_id: str,
    db: Session = Depends(get_db)
):
    """Delete a checklist."""
    service = ChecklistService(db)
    if not service.delete_checklist(checklist_id):
        raise HTTPException(status_code=404, detail="Checklist not found")

# Document endpoints
@router.post("/upload", response_model=DocumentUploadResponse, status_code=201)
async def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload a document."""
    # Validate file type
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")
    
    # Validate file size (10MB limit)
    max_size = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if len(content) > max_size:
        raise HTTPException(status_code=413, detail="File too large. Maximum size is 10MB")
    
    # Reset file pointer
    await file.seek(0)
    
    service = DocumentService(db)
    return service.upload_document(file)

@router.get("/documents", response_model=List[DocumentResponse])
async def get_documents(db: Session = Depends(get_db)):
    """Get all documents."""
    service = DocumentService(db)
    return service.get_documents()

@router.get("/documents/{document_id}", response_model=DocumentResponse)
async def get_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific document."""
    service = DocumentService(db)
    document = service.get_document(document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return DocumentResponse(
        id=document.id,
        filename=document.filename,
        original_name=document.original_name,
        file_size=document.file_size,
        status=document.status,
        uploaded_at=document.uploaded_at
    )

@router.delete("/documents/{document_id}", status_code=204)
async def delete_document(
    document_id: str,
    db: Session = Depends(get_db)
):
    """Delete a document."""
    service = DocumentService(db)
    if not service.delete_document(document_id):
        raise HTTPException(status_code=404, detail="Document not found")

# Processing endpoints
@router.post("/process/{checklist_id}", response_model=ProcessingResponse, status_code=202)
async def process_documents(
    checklist_id: str,
    request: ProcessingRequest,
    db: Session = Depends(get_db)
):
    """Process documents with a checklist."""
    service = ProcessingService(db)
    result = service.process_documents(checklist_id, request.documentIds)
    
    # Check for errors and return appropriate status codes
    if result.status == "error":
        if "Checklist not found" in result.message:
            raise HTTPException(status_code=404, detail=result.message)
        elif "No documents found" in result.message:
            raise HTTPException(status_code=400, detail=result.message)
        else:
            raise HTTPException(status_code=400, detail=result.message)
    
    return result

@router.get("/results/{result_id}", response_model=ResultsResponse)
async def get_processing_results(
    result_id: str,
    db: Session = Depends(get_db)
):
    """Get processing results."""
    service = ProcessingService(db)
    result = service.get_processing_result(result_id)
    if not result:
        raise HTTPException(status_code=404, detail="Processing result not found")
    return result

# Batch processing endpoints
@router.post("/batch/process/{checklist_id}", response_model=BatchProcessingResponse, status_code=202)
async def batch_process_documents(
    checklist_id: str,
    request: BatchProcessingRequest,
    db: Session = Depends(get_db)
):
    """Process multiple documents with a checklist in batch."""
    service = BatchProcessingService(db)
    result = service.process_documents_batch(checklist_id, request.documentIds)
    
    # Check for errors and return appropriate status codes
    if result.status == "error":
        raise HTTPException(status_code=400, detail=result.message)
    
    return result

@router.get("/batch/status")
async def get_batch_processing_status(
    document_ids: str,  # Comma-separated list
    db: Session = Depends(get_db)
):
    """Get processing status for multiple documents."""
    service = BatchProcessingService(db)
    document_id_list = document_ids.split(',')
    status_map = service.get_processing_status(document_id_list)
    return {"statuses": status_map}

# Template management endpoints
@router.get("/templates", response_model=List[ChecklistResponse])
async def get_templates(db: Session = Depends(get_db)):
    """Get all template checklists."""
    service = TemplateService(db)
    return service.get_templates()

@router.get("/templates/{template_id}", response_model=ChecklistResponse)
async def get_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Get a specific template by ID."""
    service = TemplateService(db)
    template = service.get_template_by_id(template_id)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.put("/templates/{template_id}", response_model=ChecklistResponse)
async def update_template(
    template_id: str,
    template_data: ChecklistUpdate,
    db: Session = Depends(get_db)
):
    """Update a template checklist."""
    service = TemplateService(db)
    template = service.update_template(template_id, template_data)
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    return template

@router.delete("/templates/{template_id}", status_code=204)
async def delete_template(
    template_id: str,
    db: Session = Depends(get_db)
):
    """Delete a template checklist."""
    service = TemplateService(db)
    if not service.delete_template(template_id):
        raise HTTPException(status_code=404, detail="Template not found")

@router.post("/templates/{template_id}/create-custom", response_model=ChecklistResponse)
async def create_custom_from_template(
    template_id: str,
    custom_name: str,
    db: Session = Depends(get_db)
):
    """Create a custom checklist from a template."""
    service = TemplateService(db)
    custom_checklist = service.create_custom_checklist_from_template(template_id, custom_name)
    if not custom_checklist:
        raise HTTPException(status_code=404, detail="Template not found")
    return custom_checklist