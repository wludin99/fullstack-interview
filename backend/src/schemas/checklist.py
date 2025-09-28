"""Pydantic schemas for checklist operations."""

from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime


class QuestionCreate(BaseModel):
    text: str
    orderIndex: int


class ConditionCreate(BaseModel):
    text: str
    orderIndex: int


class ChecklistCreate(BaseModel):
    name: str
    description: Optional[str] = None
    questions: List[QuestionCreate] = []
    conditions: List[ConditionCreate] = []


class ChecklistUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    questions: Optional[List[QuestionCreate]] = None
    conditions: Optional[List[ConditionCreate]] = None


class QuestionResponse(BaseModel):
    id: str
    text: str
    orderIndex: int = Field(alias="order_index")
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class ConditionResponse(BaseModel):
    id: str
    text: str
    orderIndex: int = Field(alias="order_index")
    created_at: datetime

    class Config:
        from_attributes = True
        populate_by_name = True


class ChecklistResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    questions: List[QuestionResponse] = []
    conditions: List[ConditionResponse] = []
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
