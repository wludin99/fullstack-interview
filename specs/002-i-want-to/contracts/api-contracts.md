# API Contracts - Tender Checklist App

## Base URL
```
http://localhost:8000/api
```

## Authentication
All endpoints require API key authentication via header:
```
Authorization: Bearer <api_key>
```

## Checklist Management

### Create Checklist
```http
POST /api/checklists
Content-Type: application/json

{
  "name": "German Tender Checklist",
  "description": "Standard checklist for German public tenders",
  "questions": [
    {
      "text": "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?",
      "orderIndex": 1
    }
  ],
  "conditions": [
    {
      "description": "Ist die Abgabefrist vor dem 31.12.2025?",
      "expression": "deadline_before_2025",
      "orderIndex": 1
    }
  ]
}
```

**Response:**
```json
{
  "id": "cl_123456789",
  "name": "German Tender Checklist",
  "description": "Standard checklist for German public tenders",
  "questions": [
    {
      "id": "q_123456789",
      "checklistId": "cl_123456789",
      "text": "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?",
      "orderIndex": 1,
      "createdAt": "2025-01-28T10:00:00Z"
    }
  ],
  "conditions": [
    {
      "id": "c_123456789",
      "checklistId": "cl_123456789",
      "description": "Ist die Abgabefrist vor dem 31.12.2025?",
      "expression": "deadline_before_2025",
      "orderIndex": 1,
      "createdAt": "2025-01-28T10:00:00Z"
    }
  ],
  "createdAt": "2025-01-28T10:00:00Z",
  "updatedAt": "2025-01-28T10:00:00Z"
}
```

### Get All Checklists
```http
GET /api/checklists
```

**Response:**
```json
{
  "checklists": [
    {
      "id": "cl_123456789",
      "name": "German Tender Checklist",
      "description": "Standard checklist for German public tenders",
      "questionCount": 3,
      "conditionCount": 2,
      "createdAt": "2025-01-28T10:00:00Z",
      "updatedAt": "2025-01-28T10:00:00Z"
    }
  ]
}
```

### Get Checklist by ID
```http
GET /api/checklists/{checklist_id}
```

**Response:**
```json
{
  "id": "cl_123456789",
  "name": "German Tender Checklist",
  "description": "Standard checklist for German public tenders",
  "questions": [...],
  "conditions": [...],
  "createdAt": "2025-01-28T10:00:00Z",
  "updatedAt": "2025-01-28T10:00:00Z"
}
```

### Update Checklist
```http
PUT /api/checklists/{checklist_id}
Content-Type: application/json

{
  "name": "Updated German Tender Checklist",
  "questions": [...],
  "conditions": [...]
}
```

### Delete Checklist
```http
DELETE /api/checklists/{checklist_id}
```

**Response:**
```json
{
  "message": "Checklist deleted successfully"
}
```

## Document Management

### Upload Document
```http
POST /api/upload
Content-Type: multipart/form-data

file: <PDF file>
```

**Response:**
```json
{
  "documentId": "doc_123456789",
  "filename": "tender_document.pdf",
  "anthropicFileId": "file-abc123def456",
  "fileSize": 2048576,
  "status": "uploaded",
  "uploadedAt": "2025-01-28T10:00:00Z"
}
```

### Get All Documents
```http
GET /api/documents
```

**Response:**
```json
{
  "documents": [
    {
      "id": "doc_123456789",
      "filename": "tender_document.pdf",
      "originalName": "tender_document.pdf",
      "fileSize": 2048576,
      "status": "uploaded",
      "uploadedAt": "2025-01-28T10:00:00Z"
    }
  ]
}
```

### Delete Document
```http
DELETE /api/documents/{document_id}
```

**Response:**
```json
{
  "message": "Document deleted successfully"
}
```

## Document Processing

### Process Document
```http
POST /api/process/{checklist_id}
Content-Type: application/json

{
  "documentId": "doc_123456789"
}
```

**Response:**
```json
{
  "processingResultId": "pr_123456789",
  "status": "success",
  "processedAt": "2025-01-28T10:00:00Z"
}
```

### Get Processing Results
```http
GET /api/results/{processing_result_id}
```

**Response:**
```json
{
  "processingResult": {
    "id": "pr_123456789",
    "checklistId": "cl_123456789",
    "documentId": "doc_123456789",
    "status": "success",
    "processedAt": "2025-01-28T10:00:00Z",
    "answers": [
      {
        "id": "a_123456789",
        "questionId": "q_123456789",
        "answerText": "Elektronisch über das Vergabeportal",
        "confidence": 0.95
      }
    ],
    "conditionResults": [
      {
        "id": "cr_123456789",
        "conditionId": "c_123456789",
        "result": true,
        "confidence": 0.88
      }
    ]
  },
  "document": {
    "id": "doc_123456789",
    "filename": "tender_document.pdf",
    "originalName": "tender_document.pdf",
    "fileSize": 2048576,
    "status": "processed",
    "uploadedAt": "2025-01-28T10:00:00Z"
  },
  "checklist": {
    "id": "cl_123456789",
    "name": "German Tender Checklist",
    "description": "Standard checklist for German public tenders",
    "questions": [...],
    "conditions": [...]
  }
}
```

## Error Responses

### Validation Error
```json
{
  "error": "ValidationError",
  "message": "Invalid request data",
  "details": {
    "field": "name",
    "message": "Name is required"
  }
}
```

### Not Found Error
```json
{
  "error": "NotFoundError",
  "message": "Checklist not found",
  "details": {
    "id": "cl_123456789"
  }
}
```

### Processing Error
```json
{
  "error": "ProcessingError",
  "message": "Failed to process document",
  "details": {
    "documentId": "doc_123456789",
    "reason": "LLM API timeout"
  }
}
```

### File Upload Error
```json
{
  "error": "FileUploadError",
  "message": "Invalid file type",
  "details": {
    "allowedTypes": ["application/pdf"],
    "receivedType": "text/plain"
  }
}
```

## Rate Limiting
- **Upload**: 10 requests per minute
- **Processing**: 5 requests per minute
- **General API**: 100 requests per minute

## Response Headers
```
Content-Type: application/json
X-Rate-Limit-Remaining: 99
X-Rate-Limit-Reset: 1640995200
```
