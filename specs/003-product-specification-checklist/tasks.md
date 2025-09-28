# Tasks: Tender Checklist App

**Input**: Design documents from `/specs/003-product-specification-checklist/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/
**Tech Stack**: Python FastAPI + UV, React TypeScript + Vite, Anthropic API, SQLite

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → If not found: ERROR "No implementation plan found"
   → Extract: tech stack, libraries, structure
2. Load optional design documents:
   → data-model.md: Extract entities → model tasks
   → contracts/: Each file → contract test task
   → research.md: Extract decisions → setup tasks
3. Generate tasks by category:
   → Setup: project init, dependencies, linting
   → Tests: contract tests, integration tests
   → Core: models, services, API endpoints
   → Integration: DB, middleware, logging
   → Polish: unit tests, performance, docs
4. Apply task rules:
   → Different files = mark [P] for parallel
   → Same file = sequential (no [P])
   → Tests before implementation (TDD)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → All contracts have tests?
   → All entities have models?
   → All endpoints implemented?
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
- **Backend**: `backend/src/`, `backend/tests/`
- **Frontend**: `frontend/src/`, `frontend/tests/`
- Paths shown below assume full-stack structure

## Phase 3.1: Setup
- [x] T001 Create project structure per implementation plan
- [x] T002 Initialize backend Python project with UV and FastAPI dependencies
- [x] T003 Initialize frontend React project with TypeScript and Vite dependencies
- [x] T004 [P] Configure backend linting and formatting tools (black, isort, mypy)
- [x] T005 [P] Configure frontend linting and formatting tools (ESLint, Prettier)
- [x] T006 [P] Create configuration files for Anthropic API settings
- [x] T007 [P] Set up database schema and migrations with SQLAlchemy

## Phase 3.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 3.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [x] T008 [P] Contract test POST /api/checklists in backend/tests/contract/test_checklists_api.py
- [x] T009 [P] Contract test GET /api/checklists in backend/tests/contract/test_checklists_api.py
- [x] T010 [P] Contract test PUT /api/checklists/{id} in backend/tests/contract/test_checklists_api.py
- [x] T011 [P] Contract test DELETE /api/checklists/{id} in backend/tests/contract/test_checklists_api.py
- [x] T012 [P] Contract test POST /api/upload in backend/tests/contract/test_upload_api.py
- [x] T013 [P] Contract test GET /api/documents in backend/tests/contract/test_documents_api.py
- [x] T014 [P] Contract test POST /api/process/{checklist_id} in backend/tests/contract/test_processing_api.py
- [x] T015 [P] Contract test GET /api/results/{id} in backend/tests/contract/test_results_api.py
- [x] T016 [P] Integration test checklist CRUD workflow in backend/tests/integration/test_checklist_workflow.py
- [x] T017 [P] Integration test document upload and processing in backend/tests/integration/test_document_processing.py
- [x] T018 [P] Integration test LLM processing with Anthropic API in backend/tests/integration/test_llm_processing.py
- [x] T019 [P] Frontend component test ChecklistEditor in frontend/src/__tests__/components/test_checklist_editor.tsx
- [x] T020 [P] Frontend component test FileUpload in frontend/src/__tests__/components/test_file_upload.tsx
- [x] T021 [P] Frontend component test ResultsDisplay in frontend/src/__tests__/components/test_results_display.tsx
- [x] T022 [P] Frontend integration test API communication in frontend/src/__tests__/integration/test_api_integration.tsx
- [x] T023 [P] E2E test complete user workflow in frontend/src/__tests__/e2e/test_user_workflow.tsx

## Phase 3.3: Core Implementation (ONLY after tests are failing)
- [x] T024 [P] Checklist model in backend/src/models/checklist.py
- [x] T025 [P] Question model in backend/src/models/question.py
- [x] T026 [P] Condition model in backend/src/models/condition.py
- [x] T027 [P] Document model in backend/src/models/document.py
- [x] T028 [P] ProcessingResult model in backend/src/models/processing_result.py
- [x] T029 [P] Answer model in backend/src/models/answer.py
- [x] T030 [P] ConditionResult model in backend/src/models/condition_result.py
- [x] T031 [P] Checklist service in backend/src/services/checklist_service.py
- [x] T032 [P] Document service in backend/src/services/document_service.py
- [x] T033 [P] Anthropic LLM service in backend/src/services/llm_service.py
- [x] T034 [P] Processing service in backend/src/services/processing_service.py
- [x] T035 [P] ChecklistEditor component in frontend/src/components/ChecklistEditor.tsx
- [x] T036 [P] FileUpload component in frontend/src/components/FileUpload.tsx
- [x] T037 [P] ResultsDisplay component in frontend/src/components/ResultsDisplay.tsx
- [x] T038 [P] ErrorBoundary component in frontend/src/components/ErrorBoundary.tsx
- [x] T039 POST /api/checklists endpoint in backend/src/api/routes.py
- [x] T040 GET /api/checklists endpoint in backend/src/api/routes.py
- [x] T041 PUT /api/checklists/{id} endpoint in backend/src/api/routes.py
- [x] T042 DELETE /api/checklists/{id} endpoint in backend/src/api/routes.py
- [x] T043 POST /api/upload endpoint in backend/src/api/routes.py
- [x] T044 GET /api/documents endpoint in backend/src/api/routes.py
- [x] T045 DELETE /api/documents/{id} endpoint in backend/src/api/routes.py
- [x] T046 POST /api/process/{checklist_id} endpoint in backend/src/api/routes.py
- [x] T047 GET /api/results/{id} endpoint in backend/src/api/routes.py
- [x] T048 API service integration in frontend/src/services/api.ts
- [x] T049 Home page component in frontend/src/pages/Home.tsx
- [x] T050 Results page component in frontend/src/pages/Results.tsx

## Phase 3.4: Integration
- [x] T051 Connect checklist service to database
- [x] T052 Connect document service to Anthropic File API
- [x] T053 Connect LLM service to Anthropic API
- [x] T054 Connect processing service to LLM service
- [x] T055 Connect frontend to backend API
- [x] T056 Error handling and logging middleware
- [x] T057 CORS and security headers
- [x] T058 File upload handling and validation
- [x] T059 German tender template data seeding
- [x] T060 Database indexes and performance optimization

## Phase 3.5: Enhanced User Workflow (Batch Processing)
- [x] T061 [P] Batch document selection component in frontend/src/components/BatchDocumentSelector.tsx
- [x] T062 [P] Checklist selection dropdown component in frontend/src/components/ChecklistSelector.tsx
- [x] T063 [P] Template modification interface in frontend/src/components/TemplateEditor.tsx
- [x] T064 [P] Batch processing results display in frontend/src/components/BatchResultsDisplay.tsx
- [x] T065 [P] Enhanced Home page with batch workflow in frontend/src/pages/Home.tsx
- [x] T066 [P] Batch processing API endpoint in backend/src/api/routes.py
- [x] T067 [P] Template modification API endpoints in backend/src/api/routes.py
- [x] T068 [P] Batch processing service in backend/src/services/batch_processing_service.py
- [x] T069 [P] Template service in backend/src/services/template_service.py
- [x] T070 [P] Batch processing tests in backend/tests/contract/test_batch_processing_api.py
- [x] T071 [P] Template modification tests in backend/tests/contract/test_template_api.py
- [x] T072 [P] Frontend batch workflow tests in frontend/src/__tests__/integration/test_batch_workflow.tsx
- [x] T073 [P] Enhanced API service for batch operations in frontend/src/services/api.ts
- [x] T074 [P] Batch processing state management in frontend/src/context/BatchProcessingContext.tsx
- [x] T075 [P] Export results functionality in frontend/src/components/ExportResults.tsx

## Phase 3.5.1: Delete Functionality
- [x] T103 [P] Add delete document API endpoint in backend/src/api/routes.py
- [x] T104 [P] Add delete checklist API endpoint in backend/src/api/routes.py
- [x] T105 [P] Add delete document functionality to frontend API service in frontend/src/services/api.ts
- [x] T106 [P] Add delete checklist functionality to frontend API service in frontend/src/services/api.ts
- [x] T107 [P] Add delete buttons to document list in frontend/src/components/BatchDocumentSelector.tsx
- [x] T108 [P] Add delete buttons to checklist list in frontend/src/pages/Home.tsx
- [x] T109 [P] Add confirmation dialogs for delete operations in frontend/src/components/DeleteConfirmDialog.tsx
- [ ] T110 [P] Add delete functionality tests in backend/tests/contract/test_delete_api.py
- [ ] T111 [P] Add delete functionality tests in frontend/src/__tests__/integration/test_delete_workflow.tsx

## Phase 3.6: Polish & Testing
- [x] T076 [P] Unit tests for Checklist model validation in backend/tests/unit/test_checklist_model.py
- [x] T077 [P] Unit tests for Question model validation in backend/tests/unit/test_question_model.py
- [x] T078 [P] Unit tests for Condition model validation in backend/tests/unit/test_condition_model.py
- [x] T079 [P] Unit tests for Document model validation in backend/tests/unit/test_document_model.py
- [x] T080 [P] Unit tests for ProcessingResult model validation in backend/tests/unit/test_processing_result_model.py
- [x] T081 [P] Unit tests for checklist service in backend/tests/unit/test_checklist_service.py
- [x] T082 [P] Unit tests for document service in backend/tests/unit/test_document_service.py
- [x] T083 [P] Unit tests for LLM service in backend/tests/unit/test_llm_service.py
- [x] T084 [P] Unit tests for processing service in backend/tests/unit/test_processing_service.py
- [x] T085 [P] Frontend unit tests for API service in frontend/tests/unit/test_api_service.tsx
- [x] T086 [P] Frontend unit tests for ChecklistEditor in frontend/tests/unit/test_checklist_editor.tsx
- [x] T087 [P] Frontend unit tests for FileUpload in frontend/tests/unit/test_file_upload.tsx
- [x] T088 [P] Frontend unit tests for ResultsDisplay in frontend/tests/unit/test_results_display.tsx
- [ ] T089 Performance tests for document processing (<30s requirement)
- [x] T090 [P] Update backend documentation in backend/README.md
- [x] T091 [P] Update frontend documentation in frontend/README.md
- [ ] T092 [P] Create sample German tender documents and test data
- [x] T093 [P] Integration test with real German tender documents in backend/tests/integration/test_real_documents.py
- [x] T094 [P] Performance test with Tender_documents folder in backend/tests/performance/test_document_processing_performance.py
- [x] T095 [P] German language processing validation in backend/tests/integration/test_german_language_processing.py
- [x] T096 [P] End-to-end test with complete German tender workflow in frontend/src/__tests__/e2e/test_german_tender_workflow.tsx
- [ ] T097 [P] Style frontend components with CSS
- [ ] T098 [P] Add error boundaries and loading states
- [ ] T099 [P] Implement retry logic and exponential backoff
- [ ] T100 [P] Add comprehensive logging and monitoring
- [ ] T101 [P] Generate test coverage reports
- [ ] T102 [P] Create deployment documentation

## Dependencies
- Tests (T008-T023) before implementation (T024-T050)
- T024-T030 (models) before T031-T034 (services)
- T031-T034 (services) before T039-T047 (endpoints)
- T035-T038 (components) before T048 (API integration)
- T039-T047 (endpoints) before T051-T060 (integration)
- Implementation before polish (T061-T102)

## Batch Processing Workflow Dependencies
- T061-T065 (frontend components) before T066-T069 (backend services)
- T066-T069 (backend services) before T070-T071 (API tests)
- T070-T071 (API tests) before T072 (integration tests)
- T073-T075 (enhanced frontend) after T061-T065 (basic components)
- T076-T102 (polish) after T061-T075 (batch processing implementation)

## Parallel Example
```
# Launch T008-T015 together:
Task: "Contract test POST /api/checklists in backend/tests/contract/test_checklists_api.py"
Task: "Contract test GET /api/checklists in backend/tests/contract/test_checklists_api.py"
Task: "Contract test PUT /api/checklists/{id} in backend/tests/contract/test_checklists_api.py"
Task: "Contract test DELETE /api/checklists/{id} in backend/tests/contract/test_checklists_api.py"
Task: "Contract test POST /api/upload in backend/tests/contract/test_upload_api.py"
Task: "Contract test GET /api/documents in backend/tests/contract/test_documents_api.py"
Task: "Contract test POST /api/process/{checklist_id} in backend/tests/contract/test_processing_api.py"
Task: "Contract test GET /api/results/{id} in backend/tests/contract/test_results_api.py"
```

## Batch Processing Parallel Example
```
# Launch T061-T065 together (frontend components):
Task: "Batch document selection component in frontend/src/components/BatchDocumentSelector.tsx"
Task: "Checklist selection dropdown component in frontend/src/components/ChecklistSelector.tsx"
Task: "Template modification interface in frontend/src/components/TemplateEditor.tsx"
Task: "Batch processing results display in frontend/src/components/BatchResultsDisplay.tsx"
Task: "Enhanced Home page with batch workflow in frontend/src/pages/Home.tsx"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts
- Focus on TDD approach with failing tests first
- Ensure both frontend and backend components are properly integrated
- German tender focus with Anthropic API integration
- UV package management for Python dependencies

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**:
   - Each contract file → contract test task [P]
   - Each endpoint → implementation task
   
2. **From Data Model**:
   - Each entity → model creation task [P]
   - Relationships → service layer tasks
   
3. **From User Stories**:
   - Each story → integration test [P]
   - Quickstart scenarios → validation tasks

4. **Ordering**:
   - Setup → Tests → Models → Services → Endpoints → Integration → Polish
   - Dependencies block parallel execution

## Validation Checklist
*GATE: Checked by main() before returning*

- [ ] All contracts have corresponding tests
- [ ] All entities have model tasks
- [ ] All tests come before implementation
- [ ] Parallel tasks truly independent
- [ ] Each task specifies exact file path
- [ ] No task modifies same file as another [P] task
- [ ] Frontend and backend tasks are properly balanced
- [ ] Full-stack integration tasks are included
- [ ] German tender focus maintained throughout
- [ ] Anthropic API integration properly tested
