"""Question model for the Tender Checklist App."""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class Question(Base):
    """Question model."""
    
    __tablename__ = "questions"
    
    id = Column(String, primary_key=True, index=True)
    checklist_id = Column(String, ForeignKey("checklists.id"), nullable=False)
    text = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    checklist = relationship("Checklist", back_populates="questions")
    answers = relationship("Answer", back_populates="question", cascade="all, delete-orphan")
