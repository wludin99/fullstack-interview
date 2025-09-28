# Tender Checklist App - Backend

A Python FastAPI backend for processing German tender documents with AI-powered checklist evaluation.

## Features

- **Document Management**: Upload and manage PDF documents
- **Checklist Management**: Create, edit, and manage custom checklists
- **AI Processing**: Use Anthropic's Claude API for document analysis
- **Batch Processing**: Process multiple documents with a single checklist
- **Template System**: Pre-built German tender checklist templates
- **Results Export**: Export processing results in multiple formats

## Tech Stack

- **Framework**: FastAPI
- **Database**: SQLite with SQLAlchemy ORM
- **Package Manager**: UV (not pip)
- **AI Integration**: Anthropic Claude API
- **File Storage**: Local filesystem + Anthropic File API

## Quick Start

### Prerequisites

- Python 3.11+
- UV package manager
- Anthropic API key

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fullstack-interview/backend
   ```

2. **Install dependencies with UV**
   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Anthropic API key
   ```

4. **Initialize the database**
   ```bash
   uv run python -m src.database
   ```

5. **Start the development server**
   ```bash
   uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

The API will be available at `http://localhost:8000`

## API Documentation

### Core Endpoints

#### Checklists
- `GET /api/checklists` - List all checklists
- `POST /api/checklists` - Create new checklist
- `GET /api/checklists/{id}` - Get checklist by ID
- `PUT /api/checklists/{id}` - Update checklist
- `DELETE /api/checklists/{id}` - Delete checklist

#### Documents
- `GET /api/documents` - List all documents
- `POST /api/upload` - Upload PDF document
- `DELETE /api/documents/{id}` - Delete document

#### Processing
- `POST /api/process/{checklist_id}` - Process document with checklist
- `GET /api/results/{id}` - Get processing results
- `POST /api/batch/process/{checklist_id}` - Batch process documents

#### Templates
- `GET /api/templates` - List available templates
- `GET /api/templates/{id}` - Get template by ID
- `POST /api/templates/{id}/create-custom` - Create custom checklist from template

### Example Usage

#### Upload a Document
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

#### Create a Checklist
```bash
curl -X POST "http://localhost:8000/api/checklists" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "German Tender Checklist",
    "description": "Checklist for German public tenders",
    "questions": [
      {"text": "In welcher Form sind die Angebote einzureichen?", "order_index": 1}
    ],
    "conditions": [
      {"text": "Ist die Abgabefrist vor dem 31.12.2025?", "order_index": 1}
    ]
  }'
```

#### Process Document
```bash
curl -X POST "http://localhost:8000/api/process/checklist-id" \
  -H "Content-Type: application/json" \
  -d '{"document_id": "document-id"}'
```

## Database Schema

### Core Models

#### Checklist
- `id`: Unique identifier
- `name`: Checklist name
- `description`: Optional description
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

#### Question
- `id`: Unique identifier
- `checklist_id`: Foreign key to checklist
- `text`: Question text
- `order_index`: Display order

#### Condition
- `id`: Unique identifier
- `checklist_id`: Foreign key to checklist
- `text`: Condition text
- `order_index`: Display order

#### Document
- `id`: Unique identifier
- `filename`: Stored filename
- `original_name`: Original filename
- `file_path`: Local file path
- `anthropic_file_id`: Anthropic File API ID
- `file_size`: File size in bytes
- `status`: Processing status
- `uploaded_at`: Upload timestamp

#### ProcessingResult
- `id`: Unique identifier
- `checklist_id`: Foreign key to checklist
- `document_id`: Foreign key to document
- `status`: Processing status
- `created_at`: Processing timestamp
- `completed_at`: Completion timestamp

## AI Integration

### Anthropic Claude API

The backend uses Anthropic's Claude API for document analysis:

1. **File Upload**: Documents are uploaded to Anthropic's File API
2. **Context Processing**: Claude analyzes the document content
3. **Question Answering**: Extracts answers to checklist questions
4. **Condition Evaluation**: Evaluates boolean conditions

### Configuration

Set your Anthropic API key in the environment:
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
```

### Supported Models

- **Primary**: Claude-3.5-Sonnet (claude-3-5-sonnet-20241022)
- **Fallback**: Claude-3-Haiku (claude-3-haiku-20240307)

## Development

### Project Structure

```
backend/
├── src/
│   ├── api/           # API routes and endpoints
│   ├── models/        # SQLAlchemy models
│   ├── schemas/       # Pydantic schemas
│   ├── services/      # Business logic services
│   ├── database.py    # Database configuration
│   └── main.py        # FastAPI application
├── tests/             # Test files
├── uploads/           # File upload directory
└── pyproject.toml     # UV project configuration
```

### Running Tests

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test file
uv run pytest tests/unit/test_checklist_service.py
```

### Code Quality

```bash
# Format code
uv run black src/
uv run isort src/

# Type checking
uv run mypy src/

# Linting
uv run flake8 src/
```

## Deployment

### Production Setup

1. **Environment Variables**
   ```bash
   export ANTHROPIC_API_KEY="your-api-key"
   export DATABASE_URL="sqlite:///./production.db"
   export ENVIRONMENT="production"
   ```

2. **Database Migration**
   ```bash
   uv run python -m src.database
   ```

3. **Start Server**
   ```bash
   uv run uvicorn src.main:app --host 0.0.0.0 --port 8000
   ```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install uv
RUN uv sync

EXPOSE 8000
CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **API Key Issues**
   - Ensure `ANTHROPIC_API_KEY` is set correctly
   - Check API key permissions and quotas

2. **Database Issues**
   - Verify SQLite database file permissions
   - Run database initialization: `uv run python -m src.database`

3. **File Upload Issues**
   - Check `uploads/` directory permissions
   - Verify file size limits (10MB max)

4. **Processing Errors**
   - Check Anthropic API status
   - Verify document format (PDF only)
   - Review error logs for specific issues

### Logs

```bash
# View application logs
uv run uvicorn src.main:app --log-level debug

# Check specific service logs
tail -f logs/llm_service.log
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `uv run pytest`
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.