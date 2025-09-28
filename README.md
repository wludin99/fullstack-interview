# Tender Checklist App

A full-stack application for processing German public tender documents using AI-powered checklist analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- UV package manager
- Anthropic API key

### API Key Setup

#### Option 1: Use Provided API Key (Development)
The project comes with a pre-configured API key for development and testing. No additional setup required.

#### Option 2: Use Your Own API Key
1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY=your-api-key-here
   ```
3. Or use the setup script:
   ```bash
   cd backend/tender-checklist-backend
   ./setup_env.sh your-api-key-here
   ```

### Installation

1. **Backend Setup**
   ```bash
   cd backend/tender-checklist-backend
   uv sync --dev
   ./setup_env.sh  # Uses provided API key by default
   uv run uvicorn src.main:app --reload
   ```

2. **Frontend Setup**
   ```bash
   cd frontend/tender-checklist-frontend
   npm install
   npm run dev
   ```

3. **Test with Real Documents**
   ```bash
   # Place German tender documents in ./Tender_documents/
   # Run integration tests
   cd backend/tender-checklist-backend
   uv run pytest tests/integration/test_real_documents.py -v
   ```

## 📁 Project Structure

```
fullstack-interview/
├── backend/tender-checklist-backend/     # FastAPI backend
├── frontend/tender-checklist-frontend/    # React frontend
├── specs/003-product-specification-checklist/  # Documentation
└── Tender_documents/                      # Test documents (add your PDFs here)
```

## 🧪 Testing

### Backend Tests
```bash
cd backend/tender-checklist-backend
uv run pytest                    # All tests
uv run pytest tests/contract/    # API contract tests
uv run pytest tests/integration/ # Integration tests
uv run pytest tests/performance/ # Performance tests
```

### Frontend Tests
```bash
cd frontend/tender-checklist-frontend
npm test                         # All tests
npm run test:coverage           # With coverage
```

### Test with Real German Documents
```bash
# Ensure German tender documents are in ./Tender_documents/
cd backend/tender-checklist-backend
uv run pytest tests/integration/test_real_documents.py -v
uv run pytest tests/performance/test_document_processing_performance.py -v
```

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | Provided for development |
| `DATABASE_URL` | Database connection | `sqlite:///./tender_checklist.db` |
| `DEBUG` | Debug mode | `true` |

### API Key Options

1. **Use provided key** (development): No setup needed
2. **Environment variable**: `export ANTHROPIC_API_KEY=your-key`
3. **Setup script**: `./setup_env.sh your-key`
4. **Manual .env**: Create `.env` file with your key

## 📚 Documentation

- [Complete Specification](specs/003-product-specification-checklist/spec.md)
- [API Documentation](http://localhost:8000/docs) (when backend is running)
- [Quickstart Guide](specs/003-product-specification-checklist/quickstart.md)
- [Backend README](backend/tender-checklist-backend/README.md)

## 🎯 Features

- **Document Processing**: Upload and analyze PDF documents
- **German Language Support**: Optimized for German tender documents
- **AI-Powered Analysis**: Uses Claude-3.5-Sonnet for document analysis
- **Checklist Management**: Create and manage custom checklists
- **Real-time Processing**: Process documents with AI in <30 seconds
- **Comprehensive Testing**: Full test suite with real document testing

## 🚀 Development

### TDD Workflow
This project follows Test-Driven Development (TDD):
1. Write failing tests first
2. Implement minimal code to pass
3. Refactor and optimize

### Running Tests
```bash
# Backend TDD
cd backend/tender-checklist-backend
uv run pytest tests/contract/    # Must pass before implementation
uv run pytest tests/integration/ # Integration tests
uv run pytest tests/performance/ # Performance tests

# Frontend TDD
cd frontend/tender-checklist-frontend
npm test                         # Component tests
npm run test:e2e                # End-to-end tests
```

## 📊 Performance

- **Document Processing**: <30 seconds per document
- **API Response**: <1 second for most endpoints
- **File Upload**: Supports up to 10MB PDF files
- **Concurrent Processing**: Multiple documents simultaneously

## 🔒 Security

- API keys are stored in environment variables
- File upload validation and size limits
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend integration

## 📝 License

This project is licensed under the MIT License.
