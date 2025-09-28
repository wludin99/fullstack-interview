# Modern Chatbot Interface - Quick Start Guide

## Overview

This guide will help you implement a modern ChatGPT-like interface for the Tender Checklist App. The chatbot interface provides a conversational way to interact with the system, upload documents, create checklists, and view processing results.

## Prerequisites

- Existing Tender Checklist App (backend and frontend)
- Node.js 18+ and npm
- Python 3.11+ with uv
- WebSocket support in your development environment

## Quick Setup

### 1. Backend Setup

#### Install Additional Dependencies
```bash
cd backend
uv add websockets fastapi-websocket python-multipart
uv add --dev pytest-websocket
```

#### Database Migration
```bash
# Create migration for chat tables
uv run alembic revision --autogenerate -m "Add chat interface tables"
uv run alembic upgrade head
```

#### Environment Variables
```bash
# Add to .env file
WEBSOCKET_ENABLED=true
CHAT_RATE_LIMIT=30
CHAT_MAX_MESSAGE_LENGTH=10000
```

### 2. Frontend Setup

#### Install Additional Dependencies
```bash
cd frontend
npm install @types/ws ws
npm install --save-dev @types/ws
```

#### WebSocket Configuration
```typescript
// src/config/websocket.ts
export const WEBSOCKET_CONFIG = {
  url: process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws/chat',
  reconnectInterval: 5000,
  maxReconnectAttempts: 5,
};
```

## Implementation Steps

### Phase 1: Basic Chat Interface

#### 1.1 Create Chat Components

**ChatContainer.tsx**
```typescript
import React, { useState, useEffect, useRef } from 'react';
import { ChatMessage } from '../types/chat';
import { MessageList } from './MessageList';
import { MessageInput } from './MessageInput';
import { useWebSocket } from '../hooks/useWebSocket';

export const ChatContainer: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isTyping, setIsTyping] = useState(false);
  const { sendMessage, isConnected } = useWebSocket();

  const handleSendMessage = async (content: string, attachments?: File[]) => {
    await sendMessage(content, attachments);
  };

  return (
    <div className="chat-container">
      <MessageList messages={messages} isTyping={isTyping} />
      <MessageInput onSendMessage={handleSendMessage} />
    </div>
  );
};
```

**MessageList.tsx**
```typescript
import React from 'react';
import { ChatMessage } from '../types/chat';
import { MessageBubble } from './MessageBubble';

interface MessageListProps {
  messages: ChatMessage[];
  isTyping: boolean;
}

export const MessageList: React.FC<MessageListProps> = ({ messages, isTyping }) => {
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  return (
    <div className="message-list">
      {messages.map((message) => (
        <MessageBubble key={message.id} message={message} />
      ))}
      {isTyping && <TypingIndicator />}
      <div ref={messagesEndRef} />
    </div>
  );
};
```

#### 1.2 WebSocket Hook

**useWebSocket.ts**
```typescript
import { useEffect, useRef, useState } from 'react';
import { WEBSOCKET_CONFIG } from '../config/websocket';

export const useWebSocket = () => {
  const [isConnected, setIsConnected] = useState(false);
  const wsRef = useRef<WebSocket | null>(null);
  const reconnectTimeoutRef = useRef<NodeJS.Timeout>();

  useEffect(() => {
    connect();
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
      if (reconnectTimeoutRef.current) {
        clearTimeout(reconnectTimeoutRef.current);
      }
    };
  }, []);

  const connect = () => {
    try {
      const ws = new WebSocket(WEBSOCKET_CONFIG.url);
      wsRef.current = ws;

      ws.onopen = () => {
        setIsConnected(true);
        console.log('WebSocket connected');
      };

      ws.onmessage = (event) => {
        const data = JSON.parse(event.data);
        handleMessage(data);
      };

      ws.onclose = () => {
        setIsConnected(false);
        reconnect();
      };

      ws.onerror = (error) => {
        console.error('WebSocket error:', error);
      };
    } catch (error) {
      console.error('Failed to connect WebSocket:', error);
      reconnect();
    }
  };

  const reconnect = () => {
    reconnectTimeoutRef.current = setTimeout(() => {
      connect();
    }, WEBSOCKET_CONFIG.reconnectInterval);
  };

  const sendMessage = (content: string, attachments?: File[]) => {
    if (wsRef.current?.readyState === WebSocket.OPEN) {
      wsRef.current.send(JSON.stringify({
        event: 'send_message',
        data: { content, attachments }
      }));
    }
  };

  return { isConnected, sendMessage };
};
```

### Phase 2: Backend WebSocket Implementation

#### 2.1 WebSocket Manager

**websocket_manager.py**
```python
from typing import Dict, Set
import json
import asyncio
from fastapi import WebSocket
from src.services.chat_service import ChatService

class WebSocketManager:
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.chat_service = ChatService()
    
    async def connect(self, websocket: WebSocket, conversation_id: str):
        await websocket.accept()
        if conversation_id not in self.active_connections:
            self.active_connections[conversation_id] = set()
        self.active_connections[conversation_id].add(websocket)
    
    async def disconnect(self, websocket: WebSocket, conversation_id: str):
        if conversation_id in self.active_connections:
            self.active_connections[conversation_id].discard(websocket)
    
    async def send_message(self, conversation_id: str, message: dict):
        if conversation_id in self.active_connections:
            for connection in self.active_connections[conversation_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    # Remove broken connections
                    self.active_connections[conversation_id].discard(connection)
    
    async def handle_message(self, websocket: WebSocket, data: dict):
        event = data.get('event')
        
        if event == 'send_message':
            await self.chat_service.process_user_message(data['data'])
        elif event == 'upload_file':
            await self.chat_service.process_file_upload(data['data'])
        elif event == 'typing_start':
            await self.broadcast_typing_indicator(data['data'])
```

#### 2.2 Chat Service

**chat_service.py**
```python
from typing import Dict, Any
from sqlalchemy.orm import Session
from src.models.conversation import Conversation
from src.models.message import Message
from src.services.llm_service import LLMService
from src.services.processing_service import ProcessingService

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.llm_service = LLMService()
        self.processing_service = ProcessingService(db)
    
    async def process_user_message(self, data: Dict[str, Any]):
        """Process user message and generate response"""
        conversation_id = data['conversationId']
        content = data['content']
        
        # Save user message
        user_message = Message(
            conversation_id=conversation_id,
            type='user',
            content=content
        )
        self.db.add(user_message)
        self.db.commit()
        
        # Generate AI response
        response = await self.generate_ai_response(conversation_id, content)
        
        # Save AI response
        ai_message = Message(
            conversation_id=conversation_id,
            type='system',
            content=response
        )
        self.db.add(ai_message)
        self.db.commit()
        
        return ai_message
    
    async def process_file_upload(self, data: Dict[str, Any]):
        """Process file upload in chat context"""
        # Handle file upload logic
        pass
    
    async def generate_ai_response(self, conversation_id: str, user_input: str) -> str:
        """Generate AI response based on user input"""
        # Get conversation context
        conversation = self.db.query(Conversation).filter(
            Conversation.id == conversation_id
        ).first()
        
        # Generate response using LLM
        response = await self.llm_service.generate_chat_response(
            user_input, 
            conversation.context
        )
        
        return response
```

### Phase 3: Advanced Features

#### 3.1 File Upload in Chat

**FileUpload.tsx**
```typescript
import React, { useCallback } from 'react';

interface FileUploadProps {
  onFileUpload: (file: File) => void;
  disabled?: boolean;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload, disabled }) => {
  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    const files = Array.from(e.dataTransfer.files);
    files.forEach(file => onFileUpload(file));
  }, [onFileUpload]);

  const handleFileSelect = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || []);
    files.forEach(file => onFileUpload(file));
  }, [onFileUpload]);

  return (
    <div 
      className="file-upload-area"
      onDrop={handleDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      <input
        type="file"
        multiple
        accept=".pdf"
        onChange={handleFileSelect}
        disabled={disabled}
        style={{ display: 'none' }}
      />
      <div className="upload-text">
        Drag and drop files here or click to select
      </div>
    </div>
  );
};
```

#### 3.2 Real-time Processing Updates

**ProcessingStatus.tsx**
```typescript
import React from 'react';

interface ProcessingStatusProps {
  status: 'processing' | 'completed' | 'error';
  progress?: number;
  message: string;
}

export const ProcessingStatus: React.FC<ProcessingStatusProps> = ({ 
  status, 
  progress, 
  message 
}) => {
  return (
    <div className="processing-status">
      <div className="status-indicator">
        {status === 'processing' && <div className="spinner" />}
        {status === 'completed' && <div className="checkmark" />}
        {status === 'error' && <div className="error-icon" />}
      </div>
      <div className="status-message">{message}</div>
      {progress !== undefined && (
        <div className="progress-bar">
          <div 
            className="progress-fill" 
            style={{ width: `${progress}%` }}
          />
        </div>
      )}
    </div>
  );
};
```

## Testing

### Frontend Tests

```bash
# Run chat component tests
npm test -- --testPathPattern="chat"

# Run WebSocket tests
npm test -- --testPathPattern="websocket"
```

### Backend Tests

```bash
# Run chat service tests
uv run python -m pytest tests/chat/ -v

# Run WebSocket tests
uv run python -m pytest tests/websocket/ -v
```

## Deployment

### Environment Variables

```bash
# Production environment
WEBSOCKET_ENABLED=true
CHAT_RATE_LIMIT=100
CHAT_MAX_MESSAGE_LENGTH=10000
REDIS_URL=redis://localhost:6379  # For production scaling
```

### Docker Configuration

```dockerfile
# Add to existing Dockerfile
EXPOSE 8000
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Troubleshooting

### Common Issues

1. **WebSocket Connection Failed**
   - Check if backend is running on correct port
   - Verify CORS settings allow WebSocket connections
   - Check firewall settings

2. **Messages Not Appearing**
   - Verify database connection
   - Check WebSocket event handling
   - Review browser console for errors

3. **File Upload Issues**
   - Check file size limits
   - Verify file type restrictions
   - Review upload endpoint configuration

### Debug Mode

```typescript
// Enable WebSocket debugging
localStorage.setItem('debug', 'websocket');
```

## Next Steps

1. **Implement Advanced Features**
   - Message search and filtering
   - Conversation export
   - Message reactions and replies

2. **Performance Optimization**
   - Message pagination
   - Virtual scrolling for large conversations
   - Message caching

3. **Mobile Optimization**
   - Touch gestures
   - Mobile-specific UI components
   - Offline message queuing

4. **Analytics and Monitoring**
   - Chat usage analytics
   - Performance monitoring
   - Error tracking
