"""Document model for the Tender Checklist App."""

from sqlalchemy import Column, String, Text, DateTime, Integer, ForeignKey, Index
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.base import Base


class Document(Base):
    """Document model."""
    
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    original_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    anthropic_file_id = Column(String, nullable=True)
    file_size = Column(Integer, nullable=False)
    status = Column(String, default="uploaded")
    uploaded_at = Column(DateTime, default=func.now())
    
    # Relationships
    processing_results = relationship("ProcessingResult", back_populates="document")
    
    # Indexes for performance
    __table_args__ = (
        Index('idx_document_status', 'status'),
        Index('idx_document_uploaded_at', 'uploaded_at'),
        Index('idx_document_anthropic_file_id', 'anthropic_file_id'),
    )
