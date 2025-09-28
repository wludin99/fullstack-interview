# Tasks: Modern Chatbot Interface

**Input**: Design documents from `/specs/004-chatbot-interface/`
**Prerequisites**: plan.md (required), research.md, data-model.md, contracts/
**Tech Stack**: Python FastAPI + UV, React TypeScript + Vite, WebSockets, Anthropic API, SQLite
**Dependencies**: Existing Tender Checklist App (T001-T050 completed)

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

## Phase 4.1: Chatbot Foundation Setup
- [ ] T051 [P] Install WebSocket dependencies (websockets, fastapi-websocket) in backend
- [ ] T052 [P] Install WebSocket client dependencies (@types/ws, ws) in frontend
- [ ] T053 [P] Create conversations table with proper indexes in backend/src/models/conversation.py
- [ ] T054 [P] Create messages table with foreign key constraints in backend/src/models/message.py
- [ ] T055 [P] Create message_attachments table in backend/src/models/message_attachment.py
- [ ] T056 [P] Add chat fields to existing documents and processing_results tables
- [ ] T057 [P] Create database migration scripts for chat tables
- [ ] T058 [P] Add data validation constraints for chat models

## Phase 4.2: Tests First (TDD) ⚠️ MUST COMPLETE BEFORE 4.3
**CRITICAL: These tests MUST be written and MUST FAIL before ANY implementation**
- [ ] T059 [P] Contract test WebSocket connection in backend/tests/contract/test_websocket_api.py
- [ ] T060 [P] Contract test POST /api/chat/conversations in backend/tests/contract/test_chat_api.py
- [ ] T061 [P] Contract test GET /api/chat/conversations in backend/tests/contract/test_chat_api.py
- [ ] T062 [P] Contract test POST /api/chat/conversations/:id/messages in backend/tests/contract/test_chat_api.py
- [ ] T063 [P] Contract test WebSocket message events in backend/tests/contract/test_websocket_events.py
- [ ] T064 [P] Integration test chat workflow in backend/tests/integration/test_chat_workflow.py
- [ ] T065 [P] Integration test WebSocket real-time communication in backend/tests/integration/test_websocket_integration.py
- [ ] T066 [P] Frontend component test ChatContainer in frontend/src/__tests__/components/test_chat_container.tsx
- [ ] T067 [P] Frontend component test MessageList in frontend/src/__tests__/components/test_message_list.tsx
- [ ] T068 [P] Frontend component test MessageInput in frontend/src/__tests__/components/test_message_input.tsx
- [ ] T069 [P] Frontend integration test WebSocket communication in frontend/src/__tests__/integration/test_websocket_integration.tsx
- [ ] T070 [P] E2E test complete chat workflow in frontend/src/__tests__/e2e/test_chat_workflow.tsx

## Phase 4.3: Core Implementation (ONLY after tests are failing)
- [ ] T071 [P] Conversation model in backend/src/models/conversation.py
- [ ] T072 [P] Message model in backend/src/models/message.py
- [ ] T073 [P] MessageAttachment model in backend/src/models/message_attachment.py
- [ ] T074 [P] WebSocketManager class in backend/src/websocket/manager.py
- [ ] T075 [P] ChatService in backend/src/services/chat_service.py
- [ ] T076 [P] WebSocketService in backend/src/services/websocket_service.py
- [ ] T077 [P] ChatContainer component in frontend/src/components/ChatContainer.tsx
- [ ] T078 [P] MessageList component in frontend/src/components/MessageList.tsx
- [ ] T079 [P] MessageInput component in frontend/src/components/MessageInput.tsx
- [ ] T080 [P] MessageBubble component in frontend/src/components/MessageBubble.tsx
- [ ] T081 [P] useWebSocket hook in frontend/src/hooks/useWebSocket.ts
- [ ] T082 [P] WebSocket endpoint in backend/src/api/websocket.py
- [ ] T083 [P] Chat API endpoints in backend/src/api/chat_routes.py
- [ ] T084 [P] Chat page component in frontend/src/pages/Chat.tsx

## Phase 4.4: Integration
- [ ] T085 Connect chat service to database
- [ ] T086 Connect WebSocket service to chat service
- [ ] T087 Connect frontend WebSocket to backend
- [ ] T088 Integrate chat with existing document processing
- [ ] T089 Add real-time processing updates via WebSocket
- [ ] T090 Implement file upload in chat interface
- [ ] T091 Add conversation context management
- [ ] T092 Connect chat to existing checklist functionality
- [ ] T093 Add error handling and logging for chat
- [ ] T094 Implement chat authentication and security

## Phase 4.5: Polish
- [ ] T095 [P] Unit tests for Conversation model validation in backend/tests/unit/test_conversation_model.py
- [ ] T096 [P] Unit tests for Message model validation in backend/tests/unit/test_message_model.py
- [ ] T097 [P] Unit tests for ChatService in backend/tests/unit/test_chat_service.py
- [ ] T098 [P] Unit tests for WebSocketService in backend/tests/unit/test_websocket_service.py
- [ ] T099 [P] Frontend unit tests for ChatContainer in frontend/tests/unit/test_chat_container.tsx
- [ ] T100 [P] Frontend unit tests for MessageList in frontend/tests/unit/test_message_list.tsx
- [ ] T101 [P] Frontend unit tests for MessageInput in frontend/tests/unit/test_message_input.tsx
- [ ] T102 [P] Frontend unit tests for useWebSocket hook in frontend/tests/unit/test_use_websocket.tsx
- [ ] T103 Performance tests for WebSocket communication
- [ ] T104 [P] Update backend documentation for chat features in backend/README.md
- [ ] T105 [P] Update frontend documentation for chat features in frontend/README.md
- [ ] T106 [P] Style chat components with modern CSS
- [ ] T107 [P] Add error boundaries and loading states for chat
- [ ] T108 [P] Implement retry logic and exponential backoff for WebSocket
- [ ] T109 [P] Add comprehensive logging and monitoring for chat
- [ ] T110 [P] Generate test coverage reports for chat features
- [ ] T111 [P] Create deployment documentation for chat features

## Dependencies
- Tests (T059-T070) before implementation (T071-T084)
- T071-T073 (models) before T074-T076 (services)
- T074-T076 (services) before T082-T083 (endpoints)
- T077-T081 (components) before T084 (page integration)
- T082-T083 (endpoints) before T085-T094 (integration)
- Implementation before polish (T095-T111)

## Parallel Example
```
# Launch T059-T063 together:
Task: "Contract test WebSocket connection in backend/tests/contract/test_websocket_api.py"
Task: "Contract test POST /api/chat/conversations in backend/tests/contract/test_chat_api.py"
Task: "Contract test GET /api/chat/conversations in backend/tests/contract/test_chat_api.py"
Task: "Contract test POST /api/chat/conversations/:id/messages in backend/tests/contract/test_chat_api.py"
Task: "Contract test WebSocket message events in backend/tests/contract/test_websocket_events.py"
```

## Notes
- [P] tasks = different files, no dependencies
- Verify tests fail before implementing
- Commit after each task
- Avoid: vague tasks, same file conflicts
- Focus on TDD approach with failing tests first
- Ensure both frontend and backend components are properly integrated
- WebSocket real-time communication focus
- Build on existing Tender Checklist App foundation (T001-T050 completed)

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
- [ ] WebSocket integration tasks are included
- [ ] Chat interface focus maintained throughout
- [ ] Existing app integration properly planned
