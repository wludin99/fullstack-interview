# Data Model - Tender Checklist App

## Database Schema (SQLite)

### Core Entities

#### Checklists Table
```sql
CREATE TABLE checklists (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### Questions Table
```sql
CREATE TABLE questions (
    id TEXT PRIMARY KEY,
    checklist_id TEXT NOT NULL,
    text TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE
);
```

#### Conditions Table
```sql
CREATE TABLE conditions (
    id TEXT PRIMARY KEY,
    checklist_id TEXT NOT NULL,
    description TEXT NOT NULL,
    expression TEXT NOT NULL,
    order_index INTEGER NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE
);
```

#### Documents Table
```sql
CREATE TABLE documents (
    id TEXT PRIMARY KEY,
    filename TEXT NOT NULL,
    original_name TEXT NOT NULL,
    anthropic_file_id TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    uploaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status TEXT DEFAULT 'uploaded' CHECK (status IN ('uploaded', 'processing', 'processed', 'error'))
);
```

#### Processing Results Table
```sql
CREATE TABLE processing_results (
    id TEXT PRIMARY KEY,
    checklist_id TEXT NOT NULL,
    document_id TEXT NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('success', 'error')),
    processed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    error_message TEXT,
    FOREIGN KEY (checklist_id) REFERENCES checklists(id) ON DELETE CASCADE,
    FOREIGN KEY (document_id) REFERENCES documents(id) ON DELETE CASCADE
);
```

#### Answers Table
```sql
CREATE TABLE answers (
    id TEXT PRIMARY KEY,
    processing_result_id TEXT NOT NULL,
    question_id TEXT NOT NULL,
    answer_text TEXT NOT NULL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (processing_result_id) REFERENCES processing_results(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES questions(id) ON DELETE CASCADE
);
```

#### Condition Results Table
```sql
CREATE TABLE condition_results (
    id TEXT PRIMARY KEY,
    processing_result_id TEXT NOT NULL,
    condition_id TEXT NOT NULL,
    result BOOLEAN NOT NULL,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (processing_result_id) REFERENCES processing_results(id) ON DELETE CASCADE,
    FOREIGN KEY (condition_id) REFERENCES conditions(id) ON DELETE CASCADE
);
```

## TypeScript Interfaces

### Core Models
```typescript
interface Checklist {
  id: string;
  name: string;
  description?: string;
  questions: Question[];
  conditions: Condition[];
  createdAt: Date;
  updatedAt: Date;
}

interface Question {
  id: string;
  checklistId: string;
  text: string;
  orderIndex: number;
  createdAt: Date;
}

interface Condition {
  id: string;
  checklistId: string;
  description: string;
  expression: string;
  orderIndex: number;
  createdAt: Date;
}

interface Document {
  id: string;
  filename: string;
  originalName: string;
  anthropicFileId: string;
  fileSize: number;
  uploadedAt: Date;
  status: 'uploaded' | 'processing' | 'processed' | 'error';
}

interface ProcessingResult {
  id: string;
  checklistId: string;
  documentId: string;
  status: 'success' | 'error';
  processedAt: Date;
  errorMessage?: string;
  answers: Answer[];
  conditionResults: ConditionResult[];
}

interface Answer {
  id: string;
  processingResultId: string;
  questionId: string;
  answerText: string;
  confidence?: number;
  createdAt: Date;
}

interface ConditionResult {
  id: string;
  processingResultId: string;
  conditionId: string;
  result: boolean;
  confidence?: number;
  createdAt: Date;
}
```

### API Request/Response Models
```typescript
// Checklist Management
interface CreateChecklistRequest {
  name: string;
  description?: string;
  questions: Omit<Question, 'id' | 'checklistId' | 'createdAt'>[];
  conditions: Omit<Condition, 'id' | 'checklistId' | 'createdAt'>[];
}

interface UpdateChecklistRequest {
  name?: string;
  description?: string;
  questions?: Omit<Question, 'id' | 'checklistId' | 'createdAt'>[];
  conditions?: Omit<Condition, 'id' | 'checklistId' | 'createdAt'>[];
}

// Document Upload
interface UploadDocumentRequest {
  file: File;
}

interface UploadDocumentResponse {
  documentId: string;
  filename: string;
  anthropicFileId: string;
  status: string;
}

// Processing
interface ProcessDocumentRequest {
  checklistId: string;
  documentId: string;
}

interface ProcessDocumentResponse {
  processingResultId: string;
  status: 'success' | 'error';
  errorMessage?: string;
}

// Results
interface GetResultsResponse {
  processingResult: ProcessingResult;
  document: Document;
  checklist: Checklist;
}
```

## Database Indexes
```sql
-- Performance indexes
CREATE INDEX idx_questions_checklist_id ON questions(checklist_id);
CREATE INDEX idx_conditions_checklist_id ON conditions(checklist_id);
CREATE INDEX idx_answers_processing_result_id ON answers(processing_result_id);
CREATE INDEX idx_condition_results_processing_result_id ON condition_results(processing_result_id);
CREATE INDEX idx_processing_results_checklist_id ON processing_results(checklist_id);
CREATE INDEX idx_processing_results_document_id ON processing_results(document_id);
```

## Default Data

### Sample Checklist Template
```sql
-- Insert default German tender checklist
INSERT INTO checklists (id, name, description) VALUES 
('default-tender-checklist', 'Standard German Tender Checklist', 'Default checklist for German public tenders');

-- Insert default questions
INSERT INTO questions (id, checklist_id, text, order_index) VALUES 
('q1', 'default-tender-checklist', 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?', 1),
('q2', 'default-tender-checklist', 'Wann ist die Frist für die Einreichung von Bieterfragen?', 2),
('q3', 'default-tender-checklist', 'Welche Unterlagen sind erforderlich?', 3);

-- Insert default conditions
INSERT INTO conditions (id, checklist_id, description, expression, order_index) VALUES 
('c1', 'default-tender-checklist', 'Ist die Abgabefrist vor dem 31.12.2025?', 'deadline_before_2025', 1),
('c2', 'default-tender-checklist', 'Ist eine elektronische Einreichung möglich?', 'electronic_submission_available', 2);
```

## Data Validation Rules
- **Checklist Name**: Required, max 255 characters
- **Question Text**: Required, max 1000 characters
- **Condition Expression**: Required, max 500 characters
- **Document File Size**: Max 10MB per file
- **File Types**: Only PDF files allowed
- **Processing Status**: Must be one of: uploaded, processing, processed, error
- **Confidence Scores**: Must be between 0.0 and 1.0 if provided
