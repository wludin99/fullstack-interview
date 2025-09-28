"""ProcessingResult model for the Tender Checklist App."""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class ProcessingResult(Base):
    """ProcessingResult model."""
    
    __tablename__ = "processing_results"
    
    id = Column(String, primary_key=True, index=True)
    checklist_id = Column(String, ForeignKey("checklists.id"), nullable=False)
    document_id = Column(String, ForeignKey("documents.id"), nullable=False)
    status = Column(String, default="processing")
    created_at = Column(DateTime, default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    checklist = relationship("Checklist", back_populates="processing_results")
    document = relationship("Document", back_populates="processing_results")
    answers = relationship("Answer", back_populates="processing_result", cascade="all, delete-orphan")
    condition_results = relationship("ConditionResult", back_populates="processing_result", cascade="all, delete-orphan")
