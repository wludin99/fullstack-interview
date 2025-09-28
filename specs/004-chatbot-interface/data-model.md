# Chatbot Interface - Data Model

## Database Schema Extensions

### Core Chat Tables

#### Conversations Table
```sql
CREATE TABLE conversations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id VARCHAR(255) NOT NULL,
    title VARCHAR(500),
    status VARCHAR(50) DEFAULT 'active', -- active, archived, deleted
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_updated_at ON conversations(updated_at);
```

#### Messages Table
```sql
CREATE TABLE messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    conversation_id UUID NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    type VARCHAR(50) NOT NULL, -- user, system, file, status, result
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_type ON messages(type);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

#### Message Attachments Table
```sql
CREATE TABLE message_attachments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES messages(id) ON DELETE CASCADE,
    file_id UUID REFERENCES documents(id) ON DELETE SET NULL,
    file_name VARCHAR(255) NOT NULL,
    file_type VARCHAR(50) NOT NULL,
    file_size INTEGER,
    file_url VARCHAR(500),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_message_attachments_message_id ON message_attachments(message_id);
CREATE INDEX idx_message_attachments_file_id ON message_attachments(file_id);
```

### Enhanced Existing Tables

#### Documents Table Extensions
```sql
-- Add chat-specific fields to existing documents table
ALTER TABLE documents ADD COLUMN conversation_id UUID REFERENCES conversations(id);
ALTER TABLE documents ADD COLUMN message_id UUID REFERENCES messages(id);
ALTER TABLE documents ADD COLUMN chat_metadata JSONB DEFAULT '{}';

CREATE INDEX idx_documents_conversation_id ON documents(conversation_id);
```

#### Processing Results Extensions
```sql
-- Add chat context to processing results
ALTER TABLE processing_results ADD COLUMN conversation_id UUID REFERENCES conversations(id);
ALTER TABLE processing_results ADD COLUMN message_id UUID REFERENCES messages(id);
ALTER TABLE processing_results ADD COLUMN chat_context JSONB DEFAULT '{}';

CREATE INDEX idx_processing_results_conversation_id ON processing_results(conversation_id);
```

## TypeScript Interfaces

### Core Chat Interfaces

```typescript
// Base message interface
interface BaseMessage {
  id: string;
  conversationId: string;
  type: MessageType;
  content: string;
  metadata: Record<string, any>;
  createdAt: Date;
  updatedAt: Date;
}

// Message types
type MessageType = 'user' | 'system' | 'file' | 'status' | 'result' | 'error';

// User message
interface UserMessage extends BaseMessage {
  type: 'user';
  content: string;
}

// System message
interface SystemMessage extends BaseMessage {
  type: 'system';
  content: string;
}

// File message
interface FileMessage extends BaseMessage {
  type: 'file';
  content: string;
  metadata: {
    fileName: string;
    fileType: string;
    fileSize: number;
    fileUrl?: string;
    documentId?: string;
  };
}

// Status message
interface StatusMessage extends BaseMessage {
  type: 'status';
  content: string;
  metadata: {
    status: 'processing' | 'completed' | 'error';
    progress?: number;
    processingId?: string;
  };
}

// Result message
interface ResultMessage extends BaseMessage {
  type: 'result';
  content: string;
  metadata: {
    resultId: string;
    checklistId: string;
    documentId: string;
    answers: Array<{
      questionId: string;
      questionText: string;
      answer: string;
    }>;
    conditions: Array<{
      conditionId: string;
      conditionText: string;
      result: boolean;
    }>;
  };
}

// Union type for all messages
type ChatMessage = UserMessage | SystemMessage | FileMessage | StatusMessage | ResultMessage;

// Conversation interface
interface Conversation {
  id: string;
  userId: string;
  title: string;
  status: 'active' | 'archived' | 'deleted';
  messages: ChatMessage[];
  createdAt: Date;
  updatedAt: Date;
  metadata: Record<string, any>;
}
```

### Chat State Management

```typescript
// Chat state interface
interface ChatState {
  currentConversation: Conversation | null;
  conversations: Conversation[];
  messages: ChatMessage[];
  isTyping: boolean;
  isConnected: boolean;
  inputValue: string;
  attachments: File[];
  error: string | null;
}

// Chat actions
interface ChatActions {
  sendMessage: (content: string, attachments?: File[]) => Promise<void>;
  uploadFile: (file: File) => Promise<void>;
  createConversation: (title?: string) => Promise<Conversation>;
  loadConversation: (conversationId: string) => Promise<void>;
  deleteMessage: (messageId: string) => Promise<void>;
  editMessage: (messageId: string, content: string) => Promise<void>;
  clearError: () => void;
}
```

### WebSocket Events

```typescript
// WebSocket event types
type WebSocketEvent = 
  | 'message_sent'
  | 'message_received'
  | 'typing_start'
  | 'typing_stop'
  | 'processing_start'
  | 'processing_update'
  | 'processing_complete'
  | 'error_occurred'
  | 'connection_status';

// WebSocket message interface
interface WebSocketMessage {
  event: WebSocketEvent;
  data: any;
  timestamp: Date;
  conversationId?: string;
  messageId?: string;
}

// Typing indicator interface
interface TypingIndicator {
  isTyping: boolean;
  userId?: string;
  conversationId: string;
  timestamp: Date;
}
```

## API Endpoints

### Chat API Endpoints

```typescript
// Conversation endpoints
GET    /api/chat/conversations           // List user conversations
POST   /api/chat/conversations           // Create new conversation
GET    /api/chat/conversations/:id       // Get specific conversation
PUT    /api/chat/conversations/:id       // Update conversation
DELETE /api/chat/conversations/:id       // Delete conversation

// Message endpoints
GET    /api/chat/conversations/:id/messages     // Get conversation messages
POST   /api/chat/conversations/:id/messages     // Send message
PUT    /api/chat/messages/:id                   // Edit message
DELETE /api/chat/messages/:id                   // Delete message

// File upload in chat
POST   /api/chat/upload                         // Upload file in chat context
GET    /api/chat/files/:id                     // Get file info

// Processing in chat
POST   /api/chat/process                       // Process document via chat
GET    /api/chat/status/:id                    // Get processing status
```

### WebSocket Events

```typescript
// Client to Server events
interface ClientEvents {
  'join_conversation': { conversationId: string };
  'leave_conversation': { conversationId: string };
  'send_message': { content: string; attachments?: File[] };
  'typing_start': { conversationId: string };
  'typing_stop': { conversationId: string };
  'upload_file': { file: File; conversationId: string };
}

// Server to Client events
interface ServerEvents {
  'message_received': ChatMessage;
  'typing_start': TypingIndicator;
  'typing_stop': TypingIndicator;
  'processing_start': { messageId: string; processingId: string };
  'processing_update': { processingId: string; status: string; progress?: number };
  'processing_complete': { messageId: string; resultId: string };
  'error_occurred': { messageId: string; error: string };
  'connection_status': { status: 'connected' | 'disconnected' | 'reconnecting' };
}
```

## Database Relationships

### Entity Relationship Diagram

```
Conversations (1) ←→ (N) Messages
Messages (1) ←→ (N) MessageAttachments
Messages (1) ←→ (1) Documents (via message_attachments)
Messages (1) ←→ (1) ProcessingResults (via metadata)

Conversations
├── id (UUID, PK)
├── user_id (VARCHAR)
├── title (VARCHAR)
├── status (VARCHAR)
├── created_at (TIMESTAMP)
├── updated_at (TIMESTAMP)
└── metadata (JSONB)

Messages
├── id (UUID, PK)
├── conversation_id (UUID, FK → Conversations.id)
├── type (VARCHAR)
├── content (TEXT)
├── metadata (JSONB)
├── created_at (TIMESTAMP)
└── updated_at (TIMESTAMP)

MessageAttachments
├── id (UUID, PK)
├── message_id (UUID, FK → Messages.id)
├── file_id (UUID, FK → Documents.id)
├── file_name (VARCHAR)
├── file_type (VARCHAR)
├── file_size (INTEGER)
├── file_url (VARCHAR)
└── created_at (TIMESTAMP)
```

## Data Validation

### Message Validation
```typescript
// Message content validation
const messageContentSchema = z.object({
  content: z.string().min(1).max(10000),
  type: z.enum(['user', 'system', 'file', 'status', 'result', 'error']),
  metadata: z.record(z.any()).optional(),
});

// File attachment validation
const fileAttachmentSchema = z.object({
  fileName: z.string().min(1).max(255),
  fileType: z.string().min(1).max(50),
  fileSize: z.number().positive().max(10 * 1024 * 1024), // 10MB max
  fileUrl: z.string().url().optional(),
});
```

### Database Constraints
```sql
-- Message content constraints
ALTER TABLE messages ADD CONSTRAINT check_message_content_length 
  CHECK (LENGTH(content) <= 10000);

-- File size constraints
ALTER TABLE message_attachments ADD CONSTRAINT check_file_size 
  CHECK (file_size <= 10485760); -- 10MB

-- Message type constraints
ALTER TABLE messages ADD CONSTRAINT check_message_type 
  CHECK (type IN ('user', 'system', 'file', 'status', 'result', 'error'));

-- Conversation status constraints
ALTER TABLE conversations ADD CONSTRAINT check_conversation_status 
  CHECK (status IN ('active', 'archived', 'deleted'));
```

## Migration Strategy

### Phase 1: Schema Creation
1. Create new chat tables
2. Add foreign key constraints
3. Create indexes for performance
4. Add validation constraints

### Phase 2: Data Migration
1. Migrate existing user data
2. Create default conversations for existing users
3. Preserve existing documents and processing results
4. Update existing API endpoints

### Phase 3: Feature Integration
1. Connect chat to existing functionality
2. Implement WebSocket communication
3. Add real-time processing updates
4. Test end-to-end chat functionality
