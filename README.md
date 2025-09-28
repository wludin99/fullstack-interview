# Tender Checklist App

A full-stack application for processing German public tender documents using AI-powered checklist analysis.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- UV package manager
- Anthropic API key

### API Key Setup
1. Get your API key from [Anthropic Console](https://console.anthropic.com/)
2. Set environment variable:
   ```bash
   export ANTHROPIC_API_KEY=your-api-key-here
   ```

### Installation

1. **Backend Setup**
   ```bash
   cd backend
   uv sync --dev
   uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
   ```

2. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm run dev
   ```

3. **Access the Application**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📁 Project Structure

```
fullstack-interview/
├── backend/                    # FastAPI backend
│   ├── src/                   # Source code
│   │   ├── api/              # API routes
│   │   ├── models/           # Database models
│   │   ├── services/         # Business logic
│   │   └── schemas/          # Pydantic schemas
│   ├── tests/                # Comprehensive test suite
│   └── uploads/              # Document storage
├── frontend/                   # React frontend
│   ├── src/                  # Source code
│   │   ├── components/       # React components
│   │   ├── pages/            # Page components
│   │   ├── services/         # API services
│   │   └── __tests__/        # Test suite
│   └── dist/                 # Built application
├── specs/003-product-specification-checklist/  # Documentation
└── Tender_documents/          # Test documents (auto-seeded)
```

## 🎯 Features

### Core Functionality
- **Batch Document Processing**: Process multiple PDF documents simultaneously
- **German Language Support**: Optimized for German tender documents with auto-seeding
- **AI-Powered Analysis**: Uses Claude-3.5-Sonnet for intelligent document analysis
- **Modern Chatbot Interface**: Intuitive horizontal workflow with step-by-step guidance
- **Advanced Checklist Management**: Create, edit, delete, and customize checklists
- **Real-time Processing**: Process documents with AI in <30 seconds
- **Comprehensive Results**: Detailed analysis with questions, answers, and conditions

### User Workflow
1. **Upload Documents**: Drag & drop or select multiple PDF files
2. **Select Documents**: Choose which documents to process from uploaded files
3. **Choose Checklist**: Select from existing checklists or create new ones
4. **Process & Analyze**: AI processes documents and extracts answers
5. **View Results**: Comprehensive results with detailed breakdowns

### Advanced Features
- **Template Management**: Pre-built German tender checklists
- **Export Functionality**: Export results in multiple formats
- **Error Handling**: Comprehensive error handling and user feedback
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Real-time Updates**: Live progress updates during processing

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `ANTHROPIC_API_KEY` | Anthropic API key | Provided for development |
| `DATABASE_URL` | Database connection | `sqlite:///./tender_checklist.db` |
| `DEBUG` | Debug mode | `true` |

## 📚 Documentation

- [Complete Specification](specs/003-product-specification-checklist/spec.md)
- [API Documentation](http://localhost:8000/docs) (when backend is running)
- [Architecture Plan](specs/003-product-specification-checklist/plan.md)
- [Data Model](specs/003-product-specification-checklist/data-model.md)

## 🚀 Development

### TDD Workflow
This project follows Test-Driven Development (TDD):
1. Write failing tests first
2. Implement minimal code to pass
3. Refactor and optimize

### Running the Development Environment
```bash
# Terminal 1: Backend
cd backend
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Frontend
cd frontend
npm run dev
```

### Testing Workflow
```bash
# Backend TDD
cd backend
uv run pytest tests/contract/    # Must pass before implementation
uv run pytest tests/integration/ # Integration tests
uv run pytest tests/performance/ # Performance tests

# Frontend TDD
cd frontend
npm test                         # Component tests
npm run test:coverage           # Coverage reports
```

### Test Categories
- **Contract Tests**: API endpoint validation
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Processing speed and efficiency
- **Unit Tests**: Individual component testing
- **Real Document Tests**: Testing with actual German tender documents

## 📊 Performance

- **Document Processing**: <30 seconds per document
- **Batch Processing**: Multiple documents processed simultaneously
- **API Response**: <1 second for most endpoints
- **File Upload**: Supports up to 10MB PDF files
- **Concurrent Processing**: Handles multiple users simultaneously
- **Real-time Updates**: Live progress tracking

## 🔒 Security

- API keys stored in environment variables
- File upload validation and size limits
- SQL injection protection via SQLAlchemy ORM
- CORS configuration for frontend integration
- Input sanitization and validation
- Secure file handling and storage

## 🎨 UI/UX Features

### User Experience
- **Drag & Drop**: Easy file upload
- **Batch Selection**: Select multiple documents
- **Real-time Feedback**: Live progress updates
- **Error Handling**: Clear error messages
- **Success Notifications**: Confirmation of actions
- **Export Options**: Multiple result formats

## 🏗️ Architecture

### Backend (FastAPI)
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: Database ORM with relationships
- **Pydantic**: Data validation and serialization
- **Anthropic Claude**: AI document analysis
- **PyMuPDF**: PDF text extraction
- **SQLite**: Database for development

### Frontend (React)
- **React 19**: Latest React with hooks
- **TypeScript**: Type-safe development
- **Vite**: Fast build tool
- **Jest**: Testing framework
- **MSW**: API mocking for tests
- **Modern CSS**: Responsive design

### Database Schema
- **Checklists**: User-defined and template checklists
- **Questions**: Checklist questions with ordering
- **Conditions**: Boolean conditions for evaluation
- **Documents**: Uploaded PDF files with metadata
- **Processing Results**: AI analysis results
- **Answers**: Extracted answers from documents
- **Condition Results**: Boolean evaluation results

## 📈 Test Coverage

### Backend Test Coverage
- **Unit Tests**: 95%+ coverage for all services
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Processing speed validation
- **Contract Tests**: API endpoint validation
- **Real Document Tests**: Testing with actual German documents

### Frontend Test Coverage
- **Component Tests**: All React components tested
- **Integration Tests**: API integration testing
- **E2E Tests**: Complete user workflow testing
- **Unit Tests**: Individual function testing

## 🚀 Deployment

### Development
```bash
# Backend
cd backend
uv run uvicorn src.main:app --reload

# Frontend
cd frontend
npm run dev
```

### Production
```bash
# Backend
cd backend
uv run uvicorn src.main:app --host 0.0.0.0 --port 8000

# Frontend
cd frontend
npm run build
npm run preview
```

## 📝 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For questions or issues:
1. Check the [API Documentation](http://localhost:8000/docs)
2. Review the [Specification](specs/003-product-specification-checklist/spec.md)
3. Run the test suite to verify setup
4. Check the terminal logs for error details