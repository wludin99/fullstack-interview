"""Pydantic schemas for document operations."""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class DocumentResponse(BaseModel):
    id: str
    filename: str
    original_name: str
    file_path: str
    file_size: int
    status: str
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResponse(BaseModel):
    id: str
    filename: str
    status: str
    message: str
