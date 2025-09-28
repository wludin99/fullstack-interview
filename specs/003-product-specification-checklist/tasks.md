# Tender Checklist App - Testing Tasks

## Current Test Status Analysis

### Backend Tests
- **Total Tests**: 157 tests collected
- **Status**: 56 failed, 88 passed, 5 skipped, 8 errors
- **Coverage**: Good test structure but many failures due to implementation changes
- **Issues**: Service interface mismatches, missing API endpoints, LLM service changes

### Frontend Tests  
- **Total Tests**: 16 tests (4 failed, 12 passed)
- **Status**: Multiple TypeScript compilation errors
- **Issues**: MSW version conflicts, interface mismatches, missing React imports

## Phase 3.7: Test Fixes and Coverage (T103-T120)

### Backend Test Fixes (T103-T110)
- [x] T103 [P] Fix backend service unit tests - update interfaces to match current implementation
- [ ] T104 [P] Fix backend contract tests - update API endpoints and response schemas  
- [ ] T105 [P] Fix backend integration tests - update LLM service mocking
- [ ] T106 [P] Fix backend performance tests - update document processing benchmarks
- [ ] T107 [P] Fix backend template API tests - implement missing template endpoints
- [ ] T108 [P] Fix backend batch processing tests - update batch API contract tests
- [ ] T109 [P] Fix backend LLM service tests - update Anthropic API mocking
- [ ] T110 [P] Fix backend database constraint tests - update foreign key handling

### Frontend Test Fixes (T111-T115)
- [ ] T111 [P] Fix frontend TypeScript compilation errors - update imports and interfaces
- [ ] T112 [P] Fix frontend MSW version conflicts - update to MSW v2 API
- [ ] T113 [P] Fix frontend component tests - update component interfaces and props
- [ ] T114 [P] Fix frontend API service tests - update API method signatures
- [ ] T115 [P] Fix frontend integration tests - update workflow test scenarios

### Test Coverage Improvements (T116-T120)
- [ ] T116 [P] Add missing frontend component tests for new dialogs (CreateChecklistDialog, EditChecklistDialog)
- [ ] T117 [P] Add missing frontend component tests for BatchDocumentSelector and ChecklistSelector
- [ ] T118 [P] Add missing backend tests for new batch processing endpoints
- [ ] T119 [P] Add missing backend tests for template management endpoints
- [ ] T120 [P] Add missing backend tests for delete functionality

## Phase 3.8: Test Infrastructure (T121-T125)
- [ ] T121 [P] Update Jest configuration for ES modules and TypeScript
- [ ] T122 [P] Update pytest configuration for new test structure
- [ ] T123 [P] Add pre-commit hooks for test execution
- [ ] T124 [P] Generate comprehensive test coverage reports
- [ ] T125 [P] Set up CI/CD test pipeline configuration

## Dependencies
- T103-T110 (backend fixes) can run in parallel
- T111-T115 (frontend fixes) can run in parallel  
- T116-T120 (coverage improvements) depend on T103-T115 completion
- T121-T125 (infrastructure) can run in parallel with fixes

## Parallel Execution Examples

### Backend Test Fixes (Parallel)
```bash
# Terminal 1: Service tests
cd backend && uv run pytest tests/unit/test_*_service.py -v

# Terminal 2: Contract tests  
cd backend && uv run pytest tests/contract/test_*_api.py -v

# Terminal 3: Integration tests
cd backend && uv run pytest tests/integration/ -v

# Terminal 4: Performance tests
cd backend && uv run pytest tests/performance/ -v
```

### Frontend Test Fixes (Parallel)
```bash
# Terminal 1: Component tests
cd frontend && npm test -- --testPathPattern=components

# Terminal 2: Unit tests
cd frontend && npm test -- --testPathPattern=unit

# Terminal 3: Integration tests
cd frontend && npm test -- --testPathPattern=integration

# Terminal 4: E2E tests
cd frontend && npm test -- --testPathPattern=e2e
```

## Test Coverage Goals
- **Backend**: >90% coverage (currently ~60% due to failures)
- **Frontend**: >90% coverage (currently ~75% due to failures)
- **Integration**: All user workflows covered
- **Performance**: Document processing <30s requirement validated

## Critical Test Scenarios
1. **Complete User Workflow**: Upload → Select → Process → Results
2. **German Tender Processing**: Real document processing with German terminology
3. **Batch Processing**: Multiple documents with single checklist
4. **Error Handling**: API failures, validation errors, network issues
5. **Performance**: Large document processing, concurrent operations

## Test Data Requirements
- **German Tender Documents**: Use provided Tender_documents folder
- **Mock LLM Responses**: Consistent test data for Anthropic API
- **Database Fixtures**: Pre-populated test data for all scenarios
- **File Uploads**: Test PDF files of various sizes and types

## Success Criteria
- All tests passing (0 failures, 0 errors)
- >90% code coverage on both frontend and backend
- Performance tests validating <30s processing time
- Integration tests covering complete user workflows
- CI/CD pipeline running tests automatically on commits