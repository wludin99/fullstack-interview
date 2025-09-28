"""ConditionResult model for the Tender Checklist App."""

from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class ConditionResult(Base):
    """ConditionResult model."""
    
    __tablename__ = "condition_results"
    
    id = Column(String, primary_key=True, index=True)
    processing_result_id = Column(String, ForeignKey("processing_results.id"), nullable=False)
    condition_id = Column(String, ForeignKey("conditions.id"), nullable=False)
    result = Column(Boolean, nullable=False)
    created_at = Column(DateTime, default=func.now())
    
    # Relationships
    processing_result = relationship("ProcessingResult", back_populates="condition_results")
    condition = relationship("Condition", back_populates="condition_results")
