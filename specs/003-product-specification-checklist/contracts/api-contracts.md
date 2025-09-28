# API Contracts - Tender Checklist App (Complete Product Specification)

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
    },
    {
      "text": "Wann ist die Frist für die Einreichung von Bieterfragen?",
      "orderIndex": 2
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
    },
    {
      "id": "q_987654321",
      "checklistId": "cl_123456789",
      "text": "Wann ist die Frist für die Einreichung von Bieterfragen?",
      "orderIndex": 2,
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
      "questionCount": 2,
      "conditionCount": 1,
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
      },
      {
        "id": "a_987654321",
        "questionId": "q_987654321",
        "answerText": "15. März 2025",
        "confidence": 0.88
      }
    ],
    "conditionResults": [
      {
        "id": "cr_123456789",
        "conditionId": "c_123456789",
        "result": true,
        "confidence": 0.92
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

### Anthropic API Error
```json
{
  "error": "AnthropicAPIError",
  "message": "Failed to process document with Anthropic API",
  "details": {
    "documentId": "doc_123456789",
    "anthropicFileId": "file-abc123def456",
    "reason": "API rate limit exceeded"
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

## Anthropic API Integration
- **File Upload**: Documents uploaded to Anthropic File API for context ingestion
- **Structured Prompting**: JSON format responses for consistent parsing
- **German Language Support**: Optimized prompts for German tender documents
- **Error Handling**: Graceful handling of API failures and parsing errors
- **Confidence Scoring**: Optional confidence levels for answers and condition results

## Test Scenarios

### Unit Test Scenarios
```python
# Test checklist creation
def test_create_checklist_success():
    response = client.post("/api/checklists", json=valid_checklist_data)
    assert response.status_code == 201
    assert response.json()["name"] == "Test Checklist"

# Test checklist validation
def test_create_checklist_validation_error():
    response = client.post("/api/checklists", json=invalid_checklist_data)
    assert response.status_code == 422
    assert "validation error" in response.json()["error"]

# Test document upload
def test_upload_document_success():
    with open("test_document.pdf", "rb") as f:
        response = client.post("/api/upload", files={"file": f})
    assert response.status_code == 201
    assert response.json()["status"] == "uploaded"
```

### Integration Test Scenarios
```python
# Test complete workflow
def test_complete_workflow():
    # Create checklist
    checklist = create_test_checklist()
    
    # Upload document
    document = upload_test_document()
    
    # Process document
    result = process_document(checklist.id, document.id)
    
    # Verify results
    assert result.status == "success"
    assert len(result.answers) > 0
    assert len(result.condition_results) > 0

# Test LLM integration
def test_llm_processing():
    # Mock Anthropic API response
    with patch('anthropic.Anthropic') as mock_client:
        mock_client.return_value.messages.create.return_value = mock_llm_response
        
        result = process_document_with_llm(test_checklist, test_document)
        
        assert result.answers[0].answer_text == "Expected answer"
        assert result.condition_results[0].result is True
```

### API Contract Tests
```python
# Test API response format
def test_checklist_response_format():
    response = client.get("/api/checklists")
    data = response.json()
    
    assert "checklists" in data
    assert isinstance(data["checklists"], list)
    
    if data["checklists"]:
        checklist = data["checklists"][0]
        assert "id" in checklist
        assert "name" in checklist
        assert "createdAt" in checklist

# Test error response format
def test_error_response_format():
    response = client.get("/api/checklists/nonexistent")
    data = response.json()
    
    assert "error" in data
    assert "message" in data
    assert data["error"] == "NotFoundError"
```

### Frontend Test Scenarios
```typescript
// Component tests
describe('ChecklistEditor', () => {
  it('should create checklist with valid data', async () => {
    render(<ChecklistEditor />);
    
    fireEvent.change(screen.getByLabelText('Name'), { target: { value: 'Test Checklist' } });
    fireEvent.click(screen.getByText('Save'));
    
    await waitFor(() => {
      expect(mockCreateChecklist).toHaveBeenCalledWith({
        name: 'Test Checklist',
        questions: [],
        conditions: []
      });
    });
  });
});

// Integration tests
describe('File Upload Flow', () => {
  it('should upload and process document', async () => {
    render(<App />);
    
    // Upload file
    const file = new File(['test content'], 'test.pdf', { type: 'application/pdf' });
    fireEvent.change(screen.getByLabelText('Upload PDF'), { target: { files: [file] } });
    
    // Wait for upload
    await waitFor(() => {
      expect(screen.getByText('Upload successful')).toBeInTheDocument();
    });
    
    // Process document
    fireEvent.click(screen.getByText('Process Document'));
    
    // Wait for results
    await waitFor(() => {
      expect(screen.getByText('Processing complete')).toBeInTheDocument();
    });
  });
});
```
