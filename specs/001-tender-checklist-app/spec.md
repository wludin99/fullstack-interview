# Tender Checklist App - Technical Specification

## Constitution Alignment
This specification implements the principles defined in constitution.md:
- ✅ Checklist App Alignment: Core CRUD operations for questions/conditions
- ✅ LLM Accuracy & Context: Optimized prompting for tender document analysis
- ✅ Timeboxing & Minimal Viability: Minimal feature set for 3-hour implementation
- ✅ Error Handling & Documentation: Comprehensive error states and user feedback
- ✅ UI Usability: Clear React components for checklist management and results

## System Architecture

### Backend API (Python FastAPI with UV)
```
POST /api/checklists          # Create checklist
GET /api/checklists           # List checklists
PUT /api/checklists/:id       # Update checklist
DELETE /api/checklists/:id    # Delete checklist

POST /api/upload              # Upload PDF file
POST /api/process/:checklistId # Process PDF against checklist
GET /api/results/:id          # Get processing results
```

### Frontend Components (React + TypeScript)
- `ChecklistEditor`: Create/edit questions and conditions
- `FileUpload`: Drag-and-drop PDF upload with progress indication
- `ResultsDisplay`: Show evaluation results and document status
- `ErrorBoundary`: Handle and display errors gracefully

### LLM Integration
- **Model:** Anthropic Claude API
- **File API:** Upload PDFs to Anthropic for context ingestion
- **Prompting Strategy:** Structured prompts with examples for tender analysis
- **Context Management:** Full document text + specific question focus
- **Response Parsing:** JSON format for structured answers

## Data Models

### Checklist
```typescript
interface Checklist {
  id: string;
  name: string;
  questions: Question[];
  conditions: Condition[];
  createdAt: Date;
  updatedAt: Date;
}

interface Question {
  id: string;
  text: string;
  type: 'text';
}

interface Condition {
  id: string;
  expression: string; // Boolean expression
  description: string;
}
```

### Document
```typescript
interface Document {
  id: string;
  filename: string;
  originalName: string;
  anthropicFileId: string; // Anthropic File API ID
  uploadedAt: Date;
  size: number;
}
```

### Processing Result
```typescript
interface ProcessingResult {
  id: string;
  checklistId: string;
  documentId: string;
  documentName: string;
  answers: Answer[];
  conditions: ConditionResult[];
  processedAt: Date;
  status: 'success' | 'error';
  error?: string;
}

interface Answer {
  questionId: string;
  questionText: string;
  answer: string;
  confidence?: number;
}

interface ConditionResult {
  conditionId: string;
  conditionText: string;
  result: boolean;
  confidence?: number;
}
```

## Functional Requirements

### Document Ingestion
- **Upload Interface:** Drag-and-drop or file selection for PDF uploads
- **Storage:** SQLite database with file metadata + Anthropic File API for content
- **File Management:** List uploaded documents with metadata (name, size, date)
- **Validation:** PDF format validation, size limits (max 10MB per file)

### Checklist Creation
- **Questions:** Free-text questions with German examples:
  - "In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?"
  - "Wann ist die Frist für die Einreichung von Bieterfragen?"
- **Conditions:** Boolean expressions with German examples:
  - "Ist die Abgabefrist vor dem 31.12.2025?"
- **Default Templates:** Pre-loaded checklist templates for common tender types

### Information Extraction & Evaluation
- **LLM Processing:** For each document, query Claude with:
  - All checklist questions
  - All condition evaluations
- **Structured Responses:** JSON format with answers and boolean results
- **Confidence Scoring:** Optional confidence levels for answers
- **Error Handling:** Graceful handling of missing or unclear information

## Technical Requirements

### Backend Stack
- **Framework:** Python FastAPI
- **Package Manager:** UV (not pip)
- **Database:** SQLite with SQLAlchemy ORM
- **File Storage:** Local filesystem + Anthropic File API
- **API Client:** Anthropic Python SDK

### Frontend Stack
- **Framework:** React 18+ with TypeScript
- **Build Tool:** Vite
- **UI Components:** Basic HTML/CSS (no external UI library for timeboxing)
- **State Management:** React Context + useReducer
- **HTTP Client:** Fetch API

### API Integration
- **Anthropic API:** Claude-3.5-Sonnet for document analysis
- **File Upload:** Anthropic File API for PDF context
- **Authentication:** API key from environment variables
- **Rate Limiting:** Basic retry logic for API failures

## UI Requirements

### File Upload Section
- **Interface:** Drag-and-drop zone with file selection fallback
- **Progress:** Upload progress indicators
- **File List:** Table showing uploaded documents with metadata
- **Actions:** Delete, reprocess options

### Checklist Editor
- **Questions:** Add/edit/delete text questions
- **Conditions:** Add/edit/delete boolean conditions
- **Templates:** Load default German tender checklist
- **Validation:** Required field validation

### Results Display
- **Question Results:** Table format:
  - Question | Answer | Document(s) | Confidence
- **Condition Results:** Table format:
  - Condition | True/False | Document(s) | Confidence
- **Document Status:** Processing status and error messages
- **Export:** Optional CSV export of results

## Error Handling Strategy
- **File Upload Errors:** Invalid file type, size limits, upload failures
- **LLM Processing Errors:** API failures, parsing errors, timeout handling
- **Validation Errors:** Invalid checklist data, missing required fields
- **User Feedback:** Clear error messages, retry mechanisms, fallback states

## Setup & Deployment

### Development Setup
```bash
# Backend (Python with UV)
uv venv
uv pip install fastapi uvicorn anthropic sqlalchemy python-multipart

# Frontend (React with TypeScript)
npm create vite@latest frontend -- --template react-ts
cd frontend && npm install
```

### Environment Variables
```bash
ANTHROPIC_API_KEY=your_api_key_here
DATABASE_URL=sqlite:///./tender_checklist.db
```

### Local Development
```bash
# Backend
uvicorn main:app --reload --port 8000

# Frontend
npm run dev -- --port 3000
```

## Deliverables
- **Source Code:** Complete React + FastAPI implementation
- **README:** Setup instructions, API documentation, screenshots
- **Database:** SQLite schema with sample data
- **Documentation:** API endpoints, data models, error handling
- **Screenshots:** Demo results with sample tender documents