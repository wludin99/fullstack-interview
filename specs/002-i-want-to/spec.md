# Backend UV Package Management - Technical Specification

## Constitution Alignment
This specification implements the principles defined in constitution.md:
- ✅ Checklist App Alignment: Maintains core CRUD operations for questions/conditions
- ✅ LLM Accuracy & Context: Preserves optimized prompting for tender document analysis
- ✅ Timeboxing & Minimal Viability: UV setup is faster and more reliable than pip
- ✅ Error Handling & Documentation: UV provides better dependency resolution
- ✅ UI Usability: Backend changes don't affect frontend usability

## System Architecture Update

### Backend Package Management (UV-based)
- **Package Manager:** UV (ultra-fast Python package manager)
- **Virtual Environment:** UV-managed virtual environment
- **Dependency Resolution:** UV's advanced dependency resolver
- **Lock Files:** `uv.lock` for reproducible builds
- **Project Structure:** `pyproject.toml` for project configuration

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

## Project Configuration

### pyproject.toml
```toml
[project]
name = "tender-checklist-backend"
version = "0.1.0"
description = "Backend API for Tender Checklist App"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "anthropic>=0.7.0",
    "sqlalchemy>=2.0.0",
    "python-multipart>=0.0.6",
    "pydantic>=2.5.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.7.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
    "pytest>=7.4.0",
    "pytest-asyncio>=0.21.0",
    "black>=23.0.0",
    "isort>=5.12.0",
    "mypy>=1.7.0",
]
```

### UV Commands
```bash
# Initialize UV project
uv init tender-checklist-backend
cd tender-checklist-backend

# Install dependencies
uv sync

# Add new dependencies
uv add fastapi uvicorn anthropic sqlalchemy python-multipart

# Add development dependencies
uv add --dev pytest black isort mypy

# Run the application
uv run uvicorn main:app --reload --port 8000

# Run tests
uv run pytest

# Format code
uv run black .
uv run isort .

# Type checking
uv run mypy .
```

## Development Workflow

### Initial Setup
```bash
# Create UV project
uv init tender-checklist-backend
cd tender-checklist-backend

# Install all dependencies
uv sync

# Create environment file
echo "ANTHROPIC_API_KEY=your_api_key_here" > .env
echo "DATABASE_URL=sqlite:///./tender_checklist.db" >> .env
```

### Daily Development
```bash
# Activate UV environment
source .venv/bin/activate  # or use uv run

# Install new dependencies
uv add package-name

# Run development server
uv run uvicorn main:app --reload --port 8000

# Run tests
uv run pytest

# Code formatting
uv run black . && uv run isort .
```

### Production Deployment
```bash
# Install production dependencies only
uv sync --no-dev

# Run with production server
uv run gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## Benefits of UV over pip

### Performance
- **Faster Installation:** UV is 10-100x faster than pip
- **Parallel Downloads:** Concurrent package downloads
- **Better Caching:** Intelligent package caching
- **Dependency Resolution:** Advanced resolver with conflict detection

### Reliability
- **Lock Files:** Reproducible builds with `uv.lock`
- **Conflict Detection:** Better dependency conflict resolution
- **Version Pinning:** Automatic version pinning for stability
- **Cross-Platform:** Consistent behavior across platforms

### Developer Experience
- **Project Management:** Built-in project initialization
- **Virtual Environments:** Automatic venv management
- **Script Running:** `uv run` for executing commands in environment
- **Development Dependencies:** Separate dev/prod dependency management

## Migration from pip

### If Starting Fresh
```bash
# Remove any existing pip setup
rm -rf venv/ requirements.txt

# Initialize UV project
uv init tender-checklist-backend
cd tender-checklist-backend

# Add dependencies
uv add fastapi uvicorn anthropic sqlalchemy python-multipart
uv add --dev pytest black isort mypy
```

### If Migrating Existing Project
```bash
# Convert requirements.txt to pyproject.toml
uv init --no-readme
# Manually add dependencies from requirements.txt using uv add
```

## Error Handling Strategy
- **UV Installation Errors:** Clear error messages for dependency conflicts
- **Environment Issues:** UV handles virtual environment management
- **Dependency Resolution:** UV provides better conflict detection
- **Lock File Management:** Automatic lock file updates with `uv sync`

## Documentation Updates

### README.md Changes
```markdown
## Backend Setup (UV)

### Prerequisites
- Python 3.11+
- UV package manager

### Installation
```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone and setup project
git clone <repo-url>
cd tender-checklist-backend

# Install dependencies
uv sync

# Set environment variables
cp .env.example .env
# Edit .env with your API keys

# Run development server
uv run uvicorn main:app --reload --port 8000
```

### Development
```bash
# Add new dependencies
uv add package-name

# Run tests
uv run pytest

# Format code
uv run black . && uv run isort .
```
```

## Implementation Checklist
- [ ] Initialize UV project with `uv init`
- [ ] Create `pyproject.toml` with all dependencies
- [ ] Set up development dependencies
- [ ] Update README with UV commands
- [ ] Test installation and running
- [ ] Verify all existing functionality works
- [ ] Update CI/CD to use UV instead of pip