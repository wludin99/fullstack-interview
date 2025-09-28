"""Batch processing service for handling multiple document processing."""

import uuid
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from src.models.checklist import Checklist
from src.models.document import Document
from src.models.processing_result import ProcessingResult
from src.services.processing_service import ProcessingService
from src.schemas.processing import BatchProcessingRequest, BatchProcessingResponse


class BatchProcessingService:
    """Service for batch document processing operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.processing_service = ProcessingService(db)
    
    def process_documents_batch(
        self, 
        checklist_id: str, 
        document_ids: List[str]
    ) -> BatchProcessingResponse:
        """Process multiple documents with a checklist in batch."""
        
        # Validate checklist exists
        checklist = self.db.query(Checklist).filter(Checklist.id == checklist_id).first()
        if not checklist:
            return BatchProcessingResponse(
                id="",
                status="error",
                message="Checklist not found",
                results=[]
            )
        
        # Validate documents exist
        documents = self.db.query(Document).filter(Document.id.in_(document_ids)).all()
        if not documents:
            return BatchProcessingResponse(
                id="",
                status="error",
                message="No documents found",
                results=[]
            )
        
        # Create batch processing result
        batch_id = str(uuid.uuid4())
        batch_results = []
        
        try:
            # Process each document
            for document in documents:
                # Create individual processing result
                processing_result = ProcessingResult(
                    id=str(uuid.uuid4()),
                    checklist_id=checklist_id,
                    document_id=document.id,
                    status="processing"
                )
                self.db.add(processing_result)
                self.db.flush()  # Get the ID
                
                # Process the document
                try:
                    # Get questions and conditions for this checklist
                    questions = [
                        {
                            "id": q.id,
                            "text": q.text,
                            "orderIndex": q.order_index
                        }
                        for q in checklist.questions
                    ]
                    
                    conditions = [
                        {
                            "id": c.id,
                            "text": c.text,
                            "orderIndex": c.order_index
                        }
                        for c in checklist.conditions
                    ]
                    
                    # Call LLM service for this document
                    llm_result = self.processing_service.llm_service.process_document_with_checklist(
                        document.file_path,
                        questions,
                        conditions
                    )
                    
                    # Update processing result with results
                    if "error" in llm_result:
                        processing_result.status = "error"
                        processing_result.error_message = llm_result["error"]
                    else:
                        processing_result.status = "completed"
                        # Save answers and condition results
                        self._save_processing_results(processing_result, llm_result)
                    
                    batch_results.append({
                        "id": processing_result.id,
                        "document_id": document.id,
                        "status": processing_result.status,
                        "error": processing_result.error_message
                    })
                    
                except Exception as e:
                    processing_result.status = "error"
                    processing_result.error_message = str(e)
                    print(f"Error processing document {document.id}: {str(e)}")  # Debug log
                    batch_results.append({
                        "id": processing_result.id,
                        "document_id": document.id,
                        "status": "error",
                        "error": str(e)
                    })
            
            # Commit all changes
            self.db.commit()
            
            # Determine overall batch status
            error_count = sum(1 for r in batch_results if r["status"] == "error")
            if error_count == 0:
                overall_status = "completed"
            elif error_count == len(batch_results):
                overall_status = "error"
            else:
                overall_status = "partial"
            
            return BatchProcessingResponse(
                id=batch_id,
                status=overall_status,
                message=f"Batch processing completed: {len(batch_results) - error_count} successful, {error_count} failed",
                results=batch_results
            )
            
        except Exception as e:
            self.db.rollback()
            return BatchProcessingResponse(
                id=batch_id,
                status="error",
                message=f"Batch processing failed: {str(e)}",
                results=[]
            )
    
    def _save_processing_results(self, processing_result: ProcessingResult, llm_result: Dict[str, Any]):
        """Save answers and condition results from LLM processing."""
        from src.models.answer import Answer
        from src.models.condition_result import ConditionResult
        
        # Save answers
        if "answers" in llm_result:
            for answer_data in llm_result["answers"]:
                answer = Answer(
                    id=str(uuid.uuid4()),
                    processing_result_id=processing_result.id,
                    question_id=answer_data.get("questionId", ""),
                    answer_text=answer_data.get("answer", "")
                )
                self.db.add(answer)
        
        # Save condition results
        if "condition_results" in llm_result:
            for condition_data in llm_result["condition_results"]:
                # Ensure result is always a boolean
                result_value = condition_data.get("result")
                if result_value is None:
                    result_value = False
                elif isinstance(result_value, str):
                    result_value = result_value.lower() in ['true', '1', 'yes', 'ja']
                else:
                    result_value = bool(result_value)
                
                condition_result = ConditionResult(
                    id=str(uuid.uuid4()),
                    processing_result_id=processing_result.id,
                    condition_id=condition_data.get("conditionId", ""),
                    result=result_value
                )
                self.db.add(condition_result)
    
    def get_batch_results(self, batch_id: str) -> List[Dict[str, Any]]:
        """Get results for a batch processing operation."""
        # This would typically query a batch_results table
        # For now, return empty list as we're using individual processing results
        return []
    
    def get_processing_status(self, document_ids: List[str]) -> Dict[str, str]:
        """Get processing status for multiple documents."""
        results = self.db.query(ProcessingResult).filter(
            ProcessingResult.document_id.in_(document_ids)
        ).all()
        
        status_map = {}
        for result in results:
            status_map[result.document_id] = result.status
        
        return status_map
