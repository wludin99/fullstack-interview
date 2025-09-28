"""Pydantic schemas for processing operations."""

from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class ProcessingRequest(BaseModel):
    documentIds: List[str]


class ProcessingResponse(BaseModel):
    id: str
    status: str
    message: str


class AnswerResponse(BaseModel):
    questionId: str
    questionText: str
    answer: str


class ConditionResultResponse(BaseModel):
    conditionId: str
    conditionText: str
    result: bool


class ResultsResponse(BaseModel):
    id: str
    checklistId: str
    documentId: str
    status: str
    answers: List[AnswerResponse] = []
    conditions: List[ConditionResultResponse] = []
    createdAt: datetime
    error: Optional[str] = None


class BatchProcessingRequest(BaseModel):
    documentIds: List[str]


class BatchProcessingResult(BaseModel):
    id: str
    document_id: str
    status: str
    error: Optional[str] = None


class BatchProcessingResponse(BaseModel):
    id: str
    status: str
    message: str
    results: List[BatchProcessingResult] = []
