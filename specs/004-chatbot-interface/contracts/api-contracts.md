# Chatbot Interface - API Contracts

## WebSocket Events

### Client to Server Events

#### Join Conversation
```typescript
{
  event: 'join_conversation',
  data: {
    conversationId: string;
    userId: string;
  }
}
```

#### Send Message
```typescript
{
  event: 'send_message',
  data: {
    conversationId: string;
    content: string;
    attachments?: Array<{
      fileName: string;
      fileType: string;
      fileSize: number;
      fileData: string; // base64 encoded
    }>;
  }
}
```

#### Typing Indicators
```typescript
{
  event: 'typing_start',
  data: {
    conversationId: string;
    userId: string;
  }
}

{
  event: 'typing_stop',
  data: {
    conversationId: string;
    userId: string;
  }
}
```

#### Upload File
```typescript
{
  event: 'upload_file',
  data: {
    conversationId: string;
    fileName: string;
    fileType: string;
    fileSize: number;
    fileData: string; // base64 encoded
  }
}
```

### Server to Client Events

#### Message Received
```typescript
{
  event: 'message_received',
  data: {
    id: string;
    conversationId: string;
    type: 'user' | 'system' | 'file' | 'status' | 'result' | 'error';
    content: string;
    metadata: Record<string, any>;
    createdAt: string; // ISO timestamp
  }
}
```

#### Typing Indicators
```typescript
{
  event: 'typing_start',
  data: {
    conversationId: string;
    userId: string;
    timestamp: string;
  }
}

{
  event: 'typing_stop',
  data: {
    conversationId: string;
    userId: string;
    timestamp: string;
  }
}
```

#### Processing Updates
```typescript
{
  event: 'processing_start',
  data: {
    messageId: string;
    processingId: string;
    status: 'processing';
  }
}

{
  event: 'processing_update',
  data: {
    processingId: string;
    status: string;
    progress?: number; // 0-100
    message: string;
  }
}

{
  event: 'processing_complete',
  data: {
    messageId: string;
    processingId: string;
    resultId: string;
    status: 'completed';
  }
}
```

#### Error Events
```typescript
{
  event: 'error_occurred',
  data: {
    messageId?: string;
    processingId?: string;
    error: string;
    code: string;
    timestamp: string;
  }
}
```

#### Connection Status
```typescript
{
  event: 'connection_status',
  data: {
    status: 'connected' | 'disconnected' | 'reconnecting';
    timestamp: string;
  }
}
```

## REST API Endpoints

### Conversations

#### List Conversations
```http
GET /api/chat/conversations
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  conversations: Array<{
    id: string;
    title: string;
    status: 'active' | 'archived' | 'deleted';
    lastMessage?: {
      content: string;
      createdAt: string;
    };
    messageCount: number;
    createdAt: string;
    updatedAt: string;
  }>;
  total: number;
  page: number;
  limit: number;
}
```

#### Create Conversation
```http
POST /api/chat/conversations
Authorization: Bearer <token>
Content-Type: application/json

{
  title?: string;
  metadata?: Record<string, any>;
}
```

**Response:**
```typescript
{
  id: string;
  title: string;
  status: 'active';
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, any>;
}
```

#### Get Conversation
```http
GET /api/chat/conversations/:id
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  id: string;
  title: string;
  status: 'active' | 'archived' | 'deleted';
  messages: Array<{
    id: string;
    type: 'user' | 'system' | 'file' | 'status' | 'result' | 'error';
    content: string;
    metadata: Record<string, any>;
    createdAt: string;
    updatedAt: string;
  }>;
  createdAt: string;
  updatedAt: string;
  metadata: Record<string, any>;
}
```

#### Update Conversation
```http
PUT /api/chat/conversations/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  title?: string;
  status?: 'active' | 'archived' | 'deleted';
  metadata?: Record<string, any>;
}
```

#### Delete Conversation
```http
DELETE /api/chat/conversations/:id
Authorization: Bearer <token>
```

**Response:**
```http
204 No Content
```

### Messages

#### Get Messages
```http
GET /api/chat/conversations/:id/messages?page=1&limit=50&before=<timestamp>
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  messages: Array<{
    id: string;
    type: 'user' | 'system' | 'file' | 'status' | 'result' | 'error';
    content: string;
    metadata: Record<string, any>;
    createdAt: string;
    updatedAt: string;
  }>;
  hasMore: boolean;
  total: number;
}
```

#### Send Message
```http
POST /api/chat/conversations/:id/messages
Authorization: Bearer <token>
Content-Type: application/json

{
  content: string;
  attachments?: Array<{
    fileName: string;
    fileType: string;
    fileSize: number;
    fileData: string; // base64 encoded
  }>;
}
```

**Response:**
```typescript
{
  id: string;
  conversationId: string;
  type: 'user';
  content: string;
  metadata: Record<string, any>;
  createdAt: string;
  updatedAt: string;
}
```

#### Edit Message
```http
PUT /api/chat/messages/:id
Authorization: Bearer <token>
Content-Type: application/json

{
  content: string;
}
```

#### Delete Message
```http
DELETE /api/chat/messages/:id
Authorization: Bearer <token>
```

**Response:**
```http
204 No Content
```

### File Upload

#### Upload File in Chat
```http
POST /api/chat/upload
Authorization: Bearer <token>
Content-Type: multipart/form-data

file: File
conversationId: string
```

**Response:**
```typescript
{
  id: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  fileUrl: string;
  documentId?: string;
  createdAt: string;
}
```

#### Get File Info
```http
GET /api/chat/files/:id
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  id: string;
  fileName: string;
  fileType: string;
  fileSize: number;
  fileUrl: string;
  documentId?: string;
  createdAt: string;
}
```

### Processing

#### Process Document via Chat
```http
POST /api/chat/process
Authorization: Bearer <token>
Content-Type: application/json

{
  conversationId: string;
  messageId: string;
  documentId: string;
  checklistId: string;
}
```

**Response:**
```typescript
{
  processingId: string;
  status: 'processing';
  message: string;
}
```

#### Get Processing Status
```http
GET /api/chat/status/:id
Authorization: Bearer <token>
```

**Response:**
```typescript
{
  processingId: string;
  status: 'processing' | 'completed' | 'error';
  progress?: number; // 0-100
  message: string;
  resultId?: string;
  error?: string;
}
```

## Error Responses

### Standard Error Format
```typescript
{
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
    timestamp: string;
  }
}
```

### Common Error Codes

#### Authentication Errors
```http
401 Unauthorized
{
  error: {
    code: 'UNAUTHORIZED',
    message: 'Invalid or missing authentication token',
    timestamp: '2024-01-28T10:00:00Z'
  }
}
```

#### Validation Errors
```http
400 Bad Request
{
  error: {
    code: 'VALIDATION_ERROR',
    message: 'Invalid request data',
    details: {
      field: 'content',
      message: 'Content cannot be empty'
    },
    timestamp: '2024-01-28T10:00:00Z'
  }
}
```

#### Not Found Errors
```http
404 Not Found
{
  error: {
    code: 'NOT_FOUND',
    message: 'Conversation not found',
    timestamp: '2024-01-28T10:00:00Z'
  }
}
```

#### Rate Limiting
```http
429 Too Many Requests
{
  error: {
    code: 'RATE_LIMIT_EXCEEDED',
    message: 'Too many requests, please try again later',
    details: {
      retryAfter: 60
    },
    timestamp: '2024-01-28T10:00:00Z'
  }
}
```

#### Server Errors
```http
500 Internal Server Error
{
  error: {
    code: 'INTERNAL_ERROR',
    message: 'An unexpected error occurred',
    timestamp: '2024-01-28T10:00:00Z'
  }
}
```

## WebSocket Connection

### Connection URL
```
ws://localhost:8000/ws/chat?token=<jwt_token>
```

### Connection Events

#### Connection Established
```typescript
{
  event: 'connection_established',
  data: {
    userId: string;
    timestamp: string;
  }
}
```

#### Connection Lost
```typescript
{
  event: 'connection_lost',
  data: {
    reason: 'network_error' | 'server_error' | 'timeout';
    timestamp: string;
  }
}
```

#### Reconnection
```typescript
{
  event: 'reconnecting',
  data: {
    attempt: number;
    maxAttempts: number;
    timestamp: string;
  }
}
```

## Rate Limiting

### Message Rate Limits
- **Messages per minute**: 30
- **Messages per hour**: 1000
- **File uploads per hour**: 50
- **Processing requests per hour**: 100

### Rate Limit Headers
```http
X-RateLimit-Limit: 30
X-RateLimit-Remaining: 25
X-RateLimit-Reset: 1640995200
```

## Pagination

### Standard Pagination
```typescript
{
  data: any[];
  pagination: {
    page: number;
    limit: number;
    total: number;
    hasMore: boolean;
    nextCursor?: string;
  }
}
```

### Cursor-based Pagination
```typescript
{
  data: any[];
  pagination: {
    cursor?: string;
    limit: number;
    hasMore: boolean;
    nextCursor?: string;
  }
}
```
