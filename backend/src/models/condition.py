"""Condition model for the Tender Checklist App."""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class Condition(Base):
    """Condition model."""
    
    __tablename__ = "conditions"
    
    id = Column(String, primary_key=True, index=True)
    checklist_id = Column(String, ForeignKey("checklists.id"), nullable=False)
    text = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    checklist = relationship("Checklist", back_populates="conditions")
    condition_results = relationship("ConditionResult", back_populates="condition", cascade="all, delete-orphan")