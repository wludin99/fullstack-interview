"""Template service for managing checklist templates."""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session
from src.models.checklist import Checklist
from src.models.question import Question
from src.models.condition import Condition
from src.schemas.checklist import ChecklistResponse, ChecklistCreate, ChecklistUpdate


class TemplateService:
    """Service for template management operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_templates(self) -> List[ChecklistResponse]:
        """Get all template checklists."""
        templates = self.db.query(Checklist).filter(
            Checklist.name.contains('Template')
        ).all()
        
        return [
            ChecklistResponse(
                id=template.id,
                name=template.name,
                description=template.description,
                questions=[
                    {
                        "id": q.id,
                        "text": q.text,
                        "orderIndex": q.order_index,
                        "created_at": q.created_at
                    }
                    for q in template.questions
                ],
                conditions=[
                    {
                        "id": c.id,
                        "text": c.text,
                        "orderIndex": c.order_index,
                        "created_at": c.created_at
                    }
                    for c in template.conditions
                ],
                created_at=template.created_at,
                updated_at=template.updated_at
            )
            for template in templates
        ]
    
    def get_template_by_id(self, template_id: str) -> Optional[ChecklistResponse]:
        """Get a specific template by ID."""
        template = self.db.query(Checklist).filter(
            Checklist.id == template_id,
            Checklist.name.contains('Template')
        ).first()
        
        if not template:
            return None
        
        return ChecklistResponse(
            id=template.id,
            name=template.name,
            description=template.description,
            questions=[
                {
                    "id": q.id,
                    "text": q.text,
                    "orderIndex": q.order_index,
                    "created_at": q.created_at
                }
                for q in template.questions
            ],
            conditions=[
                {
                    "id": c.id,
                    "text": c.text,
                    "orderIndex": c.order_index,
                    "created_at": c.created_at
                }
                for c in template.conditions
            ],
            created_at=template.created_at,
            updated_at=template.updated_at
        )
    
    def create_template_from_checklist(
        self, 
        checklist_id: str, 
        template_name: str
    ) -> Optional[ChecklistResponse]:
        """Create a template from an existing checklist."""
        original_checklist = self.db.query(Checklist).filter(
            Checklist.id == checklist_id
        ).first()
        
        if not original_checklist:
            return None
        
        # Create new template checklist
        template = Checklist(
            id=str(uuid.uuid4()),
            name=f"{template_name} Template",
            description=f"Template based on {original_checklist.name}"
        )
        self.db.add(template)
        self.db.flush()
        
        # Copy questions
        for question in original_checklist.questions:
            new_question = Question(
                id=str(uuid.uuid4()),
                checklist_id=template.id,
                text=question.text,
                order_index=question.order_index
            )
            self.db.add(new_question)
        
        # Copy conditions
        for condition in original_checklist.conditions:
            new_condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=template.id,
                text=condition.text,
                order_index=condition.order_index
            )
            self.db.add(new_condition)
        
        self.db.commit()
        
        return self.get_template_by_id(template.id)
    
    def update_template(
        self, 
        template_id: str, 
        template_data: ChecklistUpdate
    ) -> Optional[ChecklistResponse]:
        """Update a template checklist."""
        template = self.db.query(Checklist).filter(
            Checklist.id == template_id,
            Checklist.name.contains('Template')
        ).first()
        
        if not template:
            return None
        
        # Update basic info
        template.name = template_data.name
        template.description = template_data.description
        
        # Update questions
        if template_data.questions:
            # Remove existing questions
            self.db.query(Question).filter(
                Question.checklist_id == template_id
            ).delete()
            
            # Add new questions
            for q_data in template_data.questions:
                question = Question(
                    id=str(uuid.uuid4()),
                    checklist_id=template_id,
                    text=q_data.text,
                    order_index=q_data.orderIndex
                )
                self.db.add(question)
        
        # Update conditions
        if template_data.conditions:
            # Remove existing conditions
            self.db.query(Condition).filter(
                Condition.checklist_id == template_id
            ).delete()
            
            # Add new conditions
            for c_data in template_data.conditions:
                condition = Condition(
                    id=str(uuid.uuid4()),
                    checklist_id=template_id,
                    text=c_data.text,
                    order_index=c_data.orderIndex
                )
                self.db.add(condition)
        
        self.db.commit()
        
        return self.get_template_by_id(template_id)
    
    def delete_template(self, template_id: str) -> bool:
        """Delete a template checklist."""
        template = self.db.query(Checklist).filter(
            Checklist.id == template_id,
            Checklist.name.contains('Template')
        ).first()
        
        if not template:
            return False
        
        # Delete associated questions and conditions (cascade)
        self.db.delete(template)
        self.db.commit()
        
        return True
    
    def get_german_tender_template(self) -> Optional[ChecklistResponse]:
        """Get the German tender template specifically."""
        template = self.db.query(Checklist).filter(
            Checklist.name.contains('Deutsche Ausschreibung')
        ).first()
        
        if not template:
            return None
        
        return self.get_template_by_id(template.id)
    
    def create_custom_checklist_from_template(
        self, 
        template_id: str, 
        custom_name: str
    ) -> Optional[ChecklistResponse]:
        """Create a custom checklist from a template."""
        template = self.db.query(Checklist).filter(
            Checklist.id == template_id
        ).first()
        
        if not template:
            return None
        
        # Create new custom checklist
        custom_checklist = Checklist(
            id=str(uuid.uuid4()),
            name=custom_name,
            description=f"Custom checklist based on {template.name}"
        )
        self.db.add(custom_checklist)
        self.db.flush()
        
        # Copy questions
        for question in template.questions:
            new_question = Question(
                id=str(uuid.uuid4()),
                checklist_id=custom_checklist.id,
                text=question.text,
                order_index=question.order_index
            )
            self.db.add(new_question)
        
        # Copy conditions
        for condition in template.conditions:
            new_condition = Condition(
                id=str(uuid.uuid4()),
                checklist_id=custom_checklist.id,
                text=condition.text,
                order_index=condition.order_index
            )
            self.db.add(new_condition)
        
        self.db.commit()
        
        return ChecklistResponse(
            id=custom_checklist.id,
            name=custom_checklist.name,
            description=custom_checklist.description,
            questions=[
                {
                    "id": q.id,
                    "text": q.text,
                    "orderIndex": q.order_index,
                    "created_at": q.created_at
                }
                for q in custom_checklist.questions
            ],
            conditions=[
                {
                    "id": c.id,
                    "text": c.text,
                    "orderIndex": c.order_index,
                    "created_at": c.created_at
                }
                for c in custom_checklist.conditions
            ],
            created_at=custom_checklist.created_at,
            updated_at=custom_checklist.updated_at
        )
