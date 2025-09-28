"""Checklist service for managing checklists."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
from src.schemas.checklist import ChecklistCreate, ChecklistUpdate


class ChecklistService:
    """Service for checklist operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_checklist(self, checklist_data: ChecklistCreate) -> Checklist:
        """Create a new checklist."""
        checklist_id = str(uuid.uuid4())
        
        # Create checklist
        checklist = Checklist(
            id=checklist_id,
            name=checklist_data.name,
            description=checklist_data.description
        )
        self.db.add(checklist)
        
        # Create questions
        for question_data in checklist_data.questions:
            question = Question(
                id=str(uuid.uuid4()),
                checklist_id=checklist_id,
                text=question_data.text,
                order_index=question_data.orderIndex
            )
            self.db.add(question)
        
        # Create conditions
        for condition_data in checklist_data.conditions:
            condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=checklist_id,
                text=condition_data.text,
                order_index=condition_data.orderIndex
            )
            self.db.add(condition)
        
        self.db.commit()
        self.db.refresh(checklist)
        return checklist
    
    def get_checklists(self) -> List[Checklist]:
        """Get all checklists."""
        from sqlalchemy.orm import joinedload
        return self.db.query(Checklist).options(
            joinedload(Checklist.questions),
            joinedload(Checklist.conditions)
        ).all()
    
    def get_checklist(self, checklist_id: str) -> Optional[Checklist]:
        """Get a specific checklist."""
        from sqlalchemy.orm import joinedload
        return self.db.query(Checklist).options(
            joinedload(Checklist.questions),
            joinedload(Checklist.conditions)
        ).filter(Checklist.id == checklist_id).first()
    
    def update_checklist(self, checklist_id: str, checklist_data: ChecklistUpdate) -> Optional[Checklist]:
        """Update a checklist."""
        checklist = self.get_checklist(checklist_id)
        if not checklist:
            return None
        
        if checklist_data.name is not None:
            checklist.name = checklist_data.name
        if checklist_data.description is not None:
            checklist.description = checklist_data.description
        
        # Update questions if provided
        if checklist_data.questions is not None:
            # Delete existing questions
            self.db.query(Question).filter(Question.checklist_id == checklist_id).delete()
            
            # Add new questions
            for question_data in checklist_data.questions:
                question = Question(
                    id=str(uuid.uuid4()),
                    checklist_id=checklist_id,
                    text=question_data.text,
                    order_index=question_data.orderIndex
                )
                self.db.add(question)
        
        # Update conditions if provided
        if checklist_data.conditions is not None:
            # Delete existing conditions
            self.db.query(Condition).filter(Condition.checklist_id == checklist_id).delete()
            
            # Add new conditions
            for condition_data in checklist_data.conditions:
                condition = Condition(
                    id=str(uuid.uuid4()),
                    checklist_id=checklist_id,
                    text=condition_data.text,
                    order_index=condition_data.orderIndex
                )
                self.db.add(condition)
        
        self.db.commit()
        self.db.refresh(checklist)
        return checklist
    
    def delete_checklist(self, checklist_id: str) -> bool:
        """Delete a checklist and all related data."""
        checklist = self.get_checklist(checklist_id)
        if not checklist:
            return False
        
        try:
            # First, delete all related processing results
            from src.models.processing_result import ProcessingResult
            processing_results = self.db.query(ProcessingResult).filter(
                ProcessingResult.checklist_id == checklist_id
            ).all()
            
            for result in processing_results:
                # Delete related answers and condition results
                from src.models.answer import Answer
                from src.models.condition_result import ConditionResult
                
                # Delete answers
                answers = self.db.query(Answer).filter(
                    Answer.processing_result_id == result.id
                ).all()
                for answer in answers:
                    self.db.delete(answer)
                
                # Delete condition results
                condition_results = self.db.query(ConditionResult).filter(
                    ConditionResult.processing_result_id == result.id
                ).all()
                for condition_result in condition_results:
                    self.db.delete(condition_result)
                
                # Delete the processing result
                self.db.delete(result)
            
            # Delete all questions and conditions
            questions = self.db.query(Question).filter(
                Question.checklist_id == checklist_id
            ).all()
            for question in questions:
                self.db.delete(question)
            
            conditions = self.db.query(Condition).filter(
                Condition.checklist_id == checklist_id
            ).all()
            for condition in conditions:
                self.db.delete(condition)
            
            # Finally, delete the checklist itself
            self.db.delete(checklist)
            self.db.commit()
            return True
            
        except Exception as e:
            self.db.rollback()
            print(f"Error deleting checklist {checklist_id}: {str(e)}")
            return False
