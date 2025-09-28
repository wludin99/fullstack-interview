"""Checklist model for the Tender Checklist App."""

from sqlalchemy import Column, String, Text, DateTime, Integer, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class Checklist(Base):
    """Checklist model."""
    
    __tablename__ = "checklists"
    
    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relationships
    questions = relationship("Question", back_populates="checklist", cascade="all, delete-orphan")
    conditions = relationship("Condition", back_populates="checklist", cascade="all, delete-orphan")
    processing_results = relationship("ProcessingResult", back_populates="checklist")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_checklist_name', 'name'),
        Index('idx_checklist_created_at', 'created_at'),
    )
