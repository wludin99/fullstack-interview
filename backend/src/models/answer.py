"""Answer model for the Tender Checklist App."""

from sqlalchemy import Column, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class Answer(Base):
    """Answer model."""
    
    __tablename__ = "answers"
    
    id = Column(String, primary_key=True, index=True)
    processing_result_id = Column(String, ForeignKey("processing_results.id"), nullable=False)
    question_id = Column(String, ForeignKey("questions.id"), nullable=False)
    answer_text = Column(Text, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    processing_result = relationship("ProcessingResult", back_populates="answers")
    question = relationship("Question", back_populates="answers")
