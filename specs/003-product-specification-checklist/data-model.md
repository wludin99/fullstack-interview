# Data Model - Tender Checklist App (Complete Product Specification)

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

### Sample Checklist Template (German Tender Focus)
```sql
-- Insert default German tender checklist
INSERT INTO checklists (id, name, description) VALUES 
('default-german-tender-checklist', 'Standard German Tender Checklist', 'Default checklist for German public tenders with example questions and conditions');

-- Insert default German questions
INSERT INTO questions (id, checklist_id, text, order_index) VALUES 
('q1', 'default-german-tender-checklist', 'In welcher Form sind die Angebote/Teilnahmeanträge einzureichen?', 1),
('q2', 'default-german-tender-checklist', 'Wann ist die Frist für die Einreichung von Bieterfragen?', 2),
('q3', 'default-german-tender-checklist', 'Welche Unterlagen sind erforderlich?', 3),
('q4', 'default-german-tender-checklist', 'Wie hoch ist der geschätzte Auftragswert?', 4);

-- Insert default German conditions
INSERT INTO conditions (id, checklist_id, description, expression, order_index) VALUES 
('c1', 'default-german-tender-checklist', 'Ist die Abgabefrist vor dem 31.12.2025?', 'deadline_before_2025', 1),
('c2', 'default-german-tender-checklist', 'Ist eine elektronische Einreichung möglich?', 'electronic_submission_available', 2),
('c3', 'default-german-tender-checklist', 'Ist der Auftragswert über 100.000 Euro?', 'contract_value_over_100k', 3);
```

## Data Validation Rules
- **Checklist Name**: Required, max 255 characters
- **Question Text**: Required, max 1000 characters
- **Condition Expression**: Required, max 500 characters
- **Document File Size**: Max 10MB per file
- **File Types**: Only PDF files allowed
- **Processing Status**: Must be one of: uploaded, processing, processed, error
- **Confidence Scores**: Must be between 0.0 and 1.0 if provided

## Anthropic API Integration
- **File Upload**: Documents uploaded to Anthropic File API for context ingestion
- **Structured Prompting**: JSON format responses for consistent parsing
- **German Language Support**: Optimized prompts for German tender documents
- **Error Handling**: Graceful handling of API failures and parsing errors
- **Confidence Scoring**: Optional confidence levels for answers and condition results

## Performance Optimization
- **Database Indexing**: Optimized queries for document processing and results retrieval
- **File Storage**: Efficient storage of PDF metadata and Anthropic file IDs
- **Caching**: Optional caching of processing results for repeated queries
- **Batch Processing**: Support for processing multiple documents simultaneously

## Test Data Models

### Test Factories (Factory-Boy)
```python
class ChecklistFactory(factory.Factory):
    class Meta:
        model = Checklist
    
    id = factory.Faker('uuid4')
    name = factory.Faker('sentence', nb_words=3)
    description = factory.Faker('text', max_nb_chars=200)
    created_at = factory.Faker('date_time_this_year')
    updated_at = factory.LazyFunction(datetime.now)

class QuestionFactory(factory.Factory):
    class Meta:
        model = Question
    
    id = factory.Faker('uuid4')
    checklist_id = factory.SubFactory(ChecklistFactory)
    text = factory.Faker('sentence', nb_words=8)
    order_index = factory.Sequence(lambda n: n)
    created_at = factory.Faker('date_time_this_year')

class DocumentFactory(factory.Factory):
    class Meta:
        model = Document
    
    id = factory.Faker('uuid4')
    filename = factory.Faker('file_name', extension='pdf')
    original_name = factory.Faker('file_name', extension='pdf')
    anthropic_file_id = factory.Faker('uuid4')
    file_size = factory.Faker('random_int', min=1000, max=10000000)
    uploaded_at = factory.Faker('date_time_this_year')
    status = factory.Iterator(['uploaded', 'processing', 'processed', 'error'])
```

### Test Fixtures
```python
@pytest.fixture
def test_checklist():
    return ChecklistFactory()

@pytest.fixture
def test_questions():
    checklist = ChecklistFactory()
    return QuestionFactory.create_batch(3, checklist_id=checklist.id)

@pytest.fixture
def test_document():
    return DocumentFactory()

@pytest.fixture
def test_processing_result():
    checklist = ChecklistFactory()
    document = DocumentFactory()
    return ProcessingResultFactory(
        checklist_id=checklist.id,
        document_id=document.id
    )
```

### Test Database Setup
```python
@pytest.fixture(scope="session")
def test_db():
    # Create test database
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)
    
    # Create session
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    # Cleanup
    session.close()
    engine.dispose()
```
