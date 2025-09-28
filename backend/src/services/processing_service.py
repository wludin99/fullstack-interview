"""Processing service for coordinating document processing with LLM."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.processing_result import ProcessingResult
from src.models.answer import Answer
from src.models.condition_result import ConditionResult
from src.models.checklist import Checklist
from src.models.document import Document
from src.services.llm_service import LLMService
from src.schemas.processing import ProcessingRequest, ProcessingResponse, ResultsResponse, AnswerResponse, ConditionResultResponse


class ProcessingService:
    """Service for document processing operations."""
    
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
    
    def process_documents(
        self, 
        checklist_id: str, 
        document_ids: List[str]
    ) -> ProcessingResponse:
        """Process documents with a checklist."""
        
        # Get checklist
        checklist = self.db.query(Checklist).filter(Checklist.id == checklist_id).first()
        if not checklist:
            return ProcessingResponse(
                id="",
                status="error",
                message="Checklist not found"
            )
        
        # Get documents
        documents = self.db.query(Document).filter(Document.id.in_(document_ids)).all()
        if not documents:
            return ProcessingResponse(
                id="",
                status="error",
                message="No documents found"
            )
        
        # Create processing result
        processing_id = str(uuid.uuid4())
        processing_result = ProcessingResult(
            id=processing_id,
            checklist_id=checklist_id,
            document_id=document_ids[0],  # For now, process first document
            status="processing"
        )
        self.db.add(processing_result)
        self.db.commit()
        
        # Return immediately with processing status
        # In a real implementation, you'd use a background task queue
        return ProcessingResponse(
            id=processing_id,
            status="processing",
            message="Processing started"
        )
    
    def _process_single_document(
        self, 
        processing_result: ProcessingResult, 
        checklist: Checklist, 
        document: Document
    ):
        """Process a single document with the checklist."""
        
        # Prepare questions and conditions for LLM
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
        
        # Call LLM service
        llm_result = self.llm_service.process_document_with_checklist(
            document.file_path,
            questions,
            conditions
        )
        
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
                condition_result = ConditionResult(
                    id=str(uuid.uuid4()),
                    processing_result_id=processing_result.id,
                    condition_id=condition_data.get("conditionId", ""),
                    result=condition_data.get("result", False)
                )
                self.db.add(condition_result)
        
        self.db.commit()
    
    def get_processing_result(self, result_id: str) -> Optional[ResultsResponse]:
        """Get processing results."""
        processing_result = self.db.query(ProcessingResult).filter(
            ProcessingResult.id == result_id
        ).first()
        
        if not processing_result:
            return None
        
        # Get answers
        answers = self.db.query(Answer).filter(
            Answer.processing_result_id == result_id
        ).all()
        
        # Get condition results
        condition_results = self.db.query(ConditionResult).filter(
            ConditionResult.processing_result_id == result_id
        ).all()
        
        # Build response
        answer_responses = [
            AnswerResponse(
                questionId=answer.question_id,
                questionText=answer.question.text if answer.question else "",
                answer=answer.answer_text
            )
            for answer in answers
        ]
        
        condition_result_responses = [
            ConditionResultResponse(
                conditionId=cr.condition_id,
                conditionText=cr.condition.text if cr.condition else "",
                result=cr.result
            )
            for cr in condition_results
        ]
        
        return ResultsResponse(
            id=processing_result.id,
            checklistId=processing_result.checklist_id,
            documentId=processing_result.document_id,
            status=processing_result.status,
            answers=answer_responses,
            conditions=condition_result_responses,
            createdAt=processing_result.created_at,
            error=None if processing_result.status != "error" else "Processing failed"
        )
    
    def get_processing_status(self, result_id: str) -> Optional[str]:
        """Get processing status."""
        processing_result = self.db.query(ProcessingResult).filter(
            ProcessingResult.id == result_id
        ).first()
        
        return processing_result.status if processing_result else None
