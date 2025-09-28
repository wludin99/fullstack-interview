# Quickstart Guide - Tender Checklist App

## Prerequisites
- Python 3.11+
- Node.js 18+
- UV package manager
- Anthropic API key

## Installation

### 1. Install UV (if not already installed)
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### 2. Clone and Setup Project
```bash
git clone <repository-url>
cd fullstack-interview
```

### 3. Backend Setup (UV)
```bash
cd backend

# Initialize UV project
uv init tender-checklist-backend
cd tender-checklist-backend

# Install dependencies
uv add fastapi uvicorn anthropic sqlalchemy python-multipart pydantic python-dotenv
uv add --dev pytest black isort mypy

# Create environment file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
echo "DATABASE_URL=sqlite:///./tender_checklist.db" >> .env

# Run database migrations (if any)
uv run python -c "from app.database import init_db; init_db()"

# Start backend server
uv run uvicorn app.main:app --reload --port 8000
```

### 4. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev -- --port 3000
```

## Usage

### 1. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### 2. Create a Checklist
1. Click "Create New Checklist"
2. Enter checklist name and description
3. Add questions (e.g., "In welcher Form sind die Angebote einzureichen?")
4. Add conditions (e.g., "Ist die Abgabefrist vor dem 31.12.2025?")
5. Save checklist

### 3. Upload Documents
1. Drag and drop PDF files or click "Select Files"
2. Wait for upload to complete
3. Verify documents appear in the list

### 4. Process Documents
1. Select a checklist from the dropdown
2. Select documents to process
3. Click "Process Documents"
4. Wait for LLM analysis to complete

### 5. View Results
1. Navigate to "Results" tab
2. View answers to questions
3. View condition evaluations
4. Export results if needed

## Development Commands

### Backend Development
```bash
# Run with auto-reload
uv run uvicorn app.main:app --reload --port 8000

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .

# Add new dependency
uv add package-name

# Add development dependency
uv add --dev package-name
```

### Frontend Development
```bash
# Start development server
npm run dev

# Build for production
npm run build

# Run tests
npm run test

# Lint code
npm run lint

# Add new dependency
npm install package-name
```

## Environment Variables

### Backend (.env)
```bash
ANTHROPIC_API_KEY=your_anthropic_api_key
DATABASE_URL=sqlite:///./tender_checklist.db
LOG_LEVEL=INFO
```

### Frontend (.env.local)
```bash
VITE_API_BASE_URL=http://localhost:8000/api
VITE_APP_NAME=Tender Checklist App
```

## Troubleshooting

### Common Issues

#### 1. UV Installation Fails
```bash
# Try alternative installation method
pip install uv
```

#### 2. Anthropic API Errors
- Verify API key is correct
- Check API key has sufficient credits
- Ensure network connectivity

#### 3. Database Connection Issues
```bash
# Reset database
rm tender_checklist.db
uv run python -c "from app.database import init_db; init_db()"
```

#### 4. Frontend Build Errors
```bash
# Clear cache and reinstall
rm -rf node_modules package-lock.json
npm install
```

#### 5. Port Already in Use
```bash
# Backend - use different port
uv run uvicorn app.main:app --reload --port 8001

# Frontend - use different port
npm run dev -- --port 3001
```

## Testing

### Backend Tests
```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=app

# Run specific test file
uv run pytest tests/test_checklists.py
```

### Frontend Tests
```bash
# Run all tests
npm run test

# Run with coverage
npm run test:coverage

# Run specific test file
npm run test -- tests/ChecklistEditor.test.tsx
```

## Production Deployment

### Backend
```bash
# Install production dependencies only
uv sync --no-dev

# Run with production server
uv run gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

### Frontend
```bash
# Build for production
npm run build

# Serve static files
npx serve -s dist -l 3000
```

## API Testing

### Using curl
```bash
# Create checklist
curl -X POST http://localhost:8000/api/checklists \
  -H "Content-Type: application/json" \
  -d '{"name": "Test Checklist", "questions": [], "conditions": []}'

# Upload document
curl -X POST http://localhost:8000/api/upload \
  -F "file=@document.pdf"

# Process document
curl -X POST http://localhost:8000/api/process/cl_123456789 \
  -H "Content-Type: application/json" \
  -d '{"documentId": "doc_123456789"}'
```

### Using the API Documentation
1. Navigate to http://localhost:8000/docs
2. Use the interactive Swagger UI
3. Test endpoints directly in the browser

## Next Steps
1. **Customize Checklists**: Add your own questions and conditions
2. **Upload Sample Documents**: Test with German tender PDFs
3. **Review Results**: Analyze LLM accuracy and adjust prompts
4. **Extend Functionality**: Add new features as needed
5. **Deploy**: Set up production deployment when ready
