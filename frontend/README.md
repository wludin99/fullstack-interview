# Tender Checklist App - Frontend

A React TypeScript frontend for the Tender Checklist App, providing an intuitive interface for document processing and checklist management.

## Features

- **Modern UI**: Clean, responsive interface with step-by-step workflow
- **Document Upload**: Drag-and-drop PDF upload with validation
- **Checklist Management**: Create, edit, and manage custom checklists
- **Batch Processing**: Process multiple documents with a single checklist
- **Template System**: Pre-built German tender checklist templates
- **Results Display**: Comprehensive results with confidence scores
- **Export Functionality**: Export results in CSV, JSON, and Excel formats
- **Delete Operations**: Remove documents and checklists with confirmation

## Tech Stack

- **Framework**: React 18 with TypeScript
- **Build Tool**: Vite
- **State Management**: React Context + useReducer
- **HTTP Client**: Fetch API
- **Testing**: Jest + React Testing Library
- **Styling**: CSS with modern design patterns

## Quick Start

### Prerequisites

- Node.js 18+
- npm or yarn
- Backend API running on port 8000

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd fullstack-interview/frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start the development server**
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`

## Project Structure

```
frontend/
├── src/
│   ├── components/        # Reusable UI components
│   │   ├── ChecklistEditor.tsx
│   │   ├── FileUpload.tsx
│   │   ├── ResultsDisplay.tsx
│   │   ├── BatchDocumentSelector.tsx
│   │   ├── ChecklistSelector.tsx
│   │   ├── TemplateEditor.tsx
│   │   ├── BatchResultsDisplay.tsx
│   │   ├── ExportResults.tsx
│   │   └── DeleteConfirmDialog.tsx
│   ├── pages/            # Page components
│   │   └── Home.tsx
│   ├── services/         # API service layer
│   │   └── api.ts
│   ├── context/          # React Context providers
│   │   └── BatchProcessingContext.tsx
│   ├── __tests__/        # Test files
│   ├── App.tsx           # Main application component
│   ├── App.css           # Global styles
│   └── main.tsx          # Application entry point
├── public/               # Static assets
└── package.json          # Dependencies and scripts
```

## User Workflow

### 1. Upload Documents
- Click "📁 Choose File" button
- Select PDF documents (max 10MB each)
- View uploaded documents in the list

### 2. Select Documents
- Choose which documents to process
- Use "Select All" / "Deselect All" for convenience
- Delete unwanted documents with 🗑️ button

### 3. Choose Checklist
- Select from existing checklists
- Create new checklist from scratch
- Modify template checklists
- Delete unwanted checklists

### 4. Process Documents
- Click "Process X Document(s)" button
- Monitor processing progress
- View real-time status updates

### 5. View Results
- Review answers to all questions
- Check condition evaluations
- Export results in multiple formats
- Download processing reports

## Components

### Core Components

#### FileUpload
- Drag-and-drop file selection
- PDF validation and size limits
- Upload progress indication
- Error handling and user feedback

#### ChecklistEditor
- Create new checklists
- Edit existing checklists
- Add/remove questions and conditions
- German tender examples included

#### BatchDocumentSelector
- Multi-select document interface
- Search and filter functionality
- Bulk operations (select all, delete)
- Document metadata display

#### ResultsDisplay
- Comprehensive results view
- Question answers with confidence scores
- Condition evaluations (true/false)
- Export functionality

### Advanced Components

#### BatchProcessingContext
- Centralized state management
- Document and checklist state
- Processing status tracking
- Error handling

#### TemplateEditor
- Modify existing templates
- Create custom checklists from templates
- German tender template management

#### ExportResults
- Multiple export formats (CSV, JSON, Excel)
- Batch results processing
- Download functionality

## API Integration

### Service Layer

The `api.ts` service provides a clean interface to the backend:

```typescript
// Example API usage
import { api } from './services/api';

// Upload document
const document = await api.uploadDocument(file);

// Create checklist
const checklist = await api.createChecklist({
  name: 'My Checklist',
  description: 'Custom checklist',
  questions: [...],
  conditions: [...]
});

// Process documents
const result = await api.processDocuments(checklistId, documentIds);

// Export results
api.exportBatchResults(results, documents);
```

### Error Handling

All API calls include comprehensive error handling:

```typescript
try {
  const result = await api.processDocuments(checklistId, documentIds);
  // Handle success
} catch (error) {
  // Display user-friendly error message
  setError(`Processing failed: ${error.message}`);
}
```

## Styling

### CSS Architecture

- **Global Styles**: `App.css` for base styles and layout
- **Component Styles**: Inline styles and CSS classes
- **Responsive Design**: Mobile-first approach
- **Modern UI**: Clean, professional appearance

### Key Style Features

- **Step-by-step Workflow**: Clear visual hierarchy
- **Button Variants**: Primary, secondary, danger, small, large
- **Status Indicators**: Processing, success, error states
- **Interactive Elements**: Hover effects and transitions

## Testing

### Running Tests

```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run tests with coverage
npm run test:coverage

# Run specific test file
npm test -- --testPathPattern="FileUpload"
```

### Test Structure

- **Unit Tests**: Component behavior and API integration
- **Integration Tests**: User workflows and state management
- **Mocking**: API calls and external dependencies

## Development

### Available Scripts

```bash
npm run dev          # Start development server
npm run build        # Build for production
npm run preview      # Preview production build
npm run test         # Run tests
npm run test:watch   # Run tests in watch mode
npm run lint         # Run ESLint
npm run type-check   # Run TypeScript compiler
```

### Code Quality

- **TypeScript**: Strict type checking
- **ESLint**: Code linting and formatting
- **Prettier**: Code formatting
- **Testing**: Comprehensive test coverage

## Deployment

### Production Build

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

### Environment Configuration

```bash
# Development
VITE_API_BASE_URL=http://localhost:8000

# Production
VITE_API_BASE_URL=https://api.yourdomain.com
```

### Docker Deployment

```dockerfile
FROM node:18-alpine

WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production

COPY . .
RUN npm run build

EXPOSE 5173
CMD ["npm", "run", "preview", "--", "--host", "0.0.0.0", "--port", "5173"]
```

## Browser Support

- **Modern Browsers**: Chrome, Firefox, Safari, Edge
- **ES6+ Features**: Arrow functions, async/await, destructuring
- **CSS Grid/Flexbox**: Modern layout features
- **File API**: File upload and processing

## Performance

### Optimization Features

- **Code Splitting**: Lazy loading of components
- **Bundle Optimization**: Vite's fast build system
- **Image Optimization**: Efficient asset handling
- **Caching**: API response caching

### Best Practices

- **Component Reusability**: Shared components across features
- **State Management**: Efficient state updates
- **Error Boundaries**: Graceful error handling
- **Loading States**: User feedback during operations

## Troubleshooting

### Common Issues

1. **Build Errors**
   - Check TypeScript compilation: `npm run type-check`
   - Verify all imports are correct
   - Ensure all dependencies are installed

2. **API Connection Issues**
   - Verify backend is running on port 8000
   - Check CORS configuration
   - Review network requests in browser dev tools

3. **File Upload Issues**
   - Ensure files are PDF format
   - Check file size limits (10MB max)
   - Verify upload directory permissions

4. **State Management Issues**
   - Check React Context providers
   - Review component state updates
   - Verify API service integration

### Debug Tools

```bash
# Enable debug logging
localStorage.setItem('debug', 'true');

# View component state
React DevTools browser extension

# Monitor API calls
Browser Network tab
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests: `npm test`
5. Build successfully: `npm run build`
6. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.