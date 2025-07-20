# System Design Document
## UNNES Document Chat System

### 1. System Overview

UNNES Document Chat adalah sistem berbasis web yang memungkinkan mahasiswa dan staff UNNES untuk mengunggah dokumen dan berinteraksi dengan dokumen tersebut menggunakan teknologi AI (Large Language Model) melalui interface chat. Sistem ini menggunakan pendekatan RAG (Retrieval Augmented Generation) untuk memberikan respons yang akurat berdasarkan konten dokumen yang diunggah.

### 2. System Architecture

#### 2.1 High-Level Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (Web UI)      │◄──►│   (FastAPI)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ - HTML/CSS/JS   │    │ - REST API      │    │ - Ollama LLM    │
│ - Auth UI       │    │ - Auth Service  │    │ - Google OAuth  │
│ - Chat UI       │    │ - Chat Service  │    │                 │
│ - Upload UI     │    │ - RAG Service   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │    Database     │
                       │    (MySQL)      │
                       │                 │
                       │ - Users         │
                       │ - Documents     │
                       │ - Chat Sessions │
                       └─────────────────┘
```

#### 2.2 Technology Stack

**Frontend:**
- HTML5, CSS3, JavaScript (Vanilla)
- Responsive Design
- Google Identity Services

**Backend:**
- FastAPI (Python)
- Uvicorn ASGI Server
- Pydantic for data validation
- JWT for authentication

**Database:**
- MySQL
- Connection pooling

**AI/ML:**
- Ollama (Local LLM)
- LangChain framework
- FAISS vector store
- Document processing (PyPDF, docx2txt)

**Security:**
- JWT tokens
- Google OAuth2
- CORS middleware
- Password hashing (bcrypt)

### 3. System Components

#### 3.1 Frontend Components

**Authentication Module:**
- Login/Register forms
- Google OAuth integration
- Session management
- Role-based UI rendering

**Document Management:**
- File upload interface (drag & drop)
- Document listing
- File validation
- Progress indicators

**Chat Interface:**
- Real-time chat UI
- Document selection for chat context
- Message history
- Typing indicators

**Admin Panel:**
- User management
- System statistics
- Document oversight

#### 3.2 Backend Components

**API Layer (`/api/routers/`):**
- `auth.py` - Authentication endpoints
- `documents.py` - Document management
- `chat.py` - Chat functionality
- `admin.py` - Administrative functions

**Service Layer (`/services/`):**
- `auth_service.py` - Authentication logic
- `chat_service.py` - Chat processing
- `rag_service.py` - RAG implementation

**Core Layer (`/core/`):**
- `config.py` - Configuration management

**Data Layer (`/db/`):**
- `session.py` - Database connection management

**Schemas (`/schemas/`):**
- `user.py` - User data models
- `chat.py` - Chat data models
- `document.py` - Document data models

### 4. Database Design

#### 4.1 Entity Relationship Diagram
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│     Users       │    │   Documents     │    │  Chat_Sessions  │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ id (PK)         │    │ id (PK)         │    │ id (PK)         │
│ username        │    │ filename        │    │ user_id (FK)    │
│ email           │◄──►│ user_id (FK)    │◄──►│ document_ids    │
│ password        │    │ file_path       │    │ created_at      │
│ role            │    │ file_size       │    │ updated_at      │
│ created_at      │    │ file_type       │    └─────────────────┘
└─────────────────┘    │ created_at      │
                       └─────────────────┘
                                │
                                ▼
                       ┌─────────────────┐
                       │   Chat_Messages │
                       ├─────────────────┤
                       │ id (PK)         │
                       │ session_id (FK) │
                       │ message_type    │
                       │ content         │
                       │ timestamp       │
                       └─────────────────┘
```

#### 4.2 Table Specifications

**Users Table:**
- Primary authentication and user management
- Role-based access control (user/admin)
- UNNES email domain validation

**Documents Table:**
- File metadata storage
- User ownership tracking
- File type and size validation

**Chat_Sessions Table:**
- Chat context management
- Multi-document chat support
- Session persistence

**Chat_Messages Table:**
- Message history storage
- User and AI message differentiation
- Timestamp tracking

### 5. Security Design

#### 5.1 Authentication & Authorization

**Multi-factor Authentication:**
- Username/password authentication
- Google OAuth2 integration
- JWT token-based sessions

**Authorization Levels:**
- User: Document upload, chat, profile management
- Admin: User management, system oversight

**Security Measures:**
- Password hashing with bcrypt
- JWT token expiration
- CORS protection
- Input validation and sanitization
- File type validation
- Email domain restriction (@students.unnes.ac.id, @mail.unnes.ac.id)

#### 5.2 Data Protection

**File Security:**
- User-isolated file storage
- File type validation
- Size limitations
- Secure file paths

**Database Security:**
- Connection pooling
- Prepared statements
- Error handling without information leakage

### 6. AI/RAG System Design

#### 6.1 RAG Architecture
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Document      │    │   Vector        │    │   LLM Query     │
│   Processing    │───►│   Store         │───►│   Processing    │
│                 │    │   (FAISS)       │    │   (Ollama)      │
│ - PDF parsing   │    │                 │    │                 │
│ - Text chunking │    │ - Embeddings    │    │ - Context       │
│ - Preprocessing │    │ - Similarity    │    │ - Generation    │
└─────────────────┘    │   search        │    │ - Response      │
                       └─────────────────┘    └─────────────────┘
```

#### 6.2 Document Processing Pipeline

1. **File Upload & Validation**
   - File type checking (PDF, DOCX, TXT)
   - Size validation
   - Virus scanning (if implemented)

2. **Text Extraction**
   - PDF: PyPDF library
   - DOCX: docx2txt library
   - TXT: Direct reading

3. **Text Preprocessing**
   - Text cleaning and normalization
   - Chunking (1000 characters, 200 overlap)
   - Metadata extraction

4. **Vector Embedding**
   - Text-to-vector conversion
   - FAISS index creation
   - Persistent storage

#### 6.3 Chat Processing Flow

1. **Query Processing**
   - User input validation
   - Context preparation
   - Document selection

2. **Retrieval**
   - Vector similarity search
   - Relevant chunk extraction
   - Context ranking

3. **Generation**
   - Prompt construction
   - LLM query (Ollama)
   - Response generation

4. **Response Delivery**
   - Answer formatting
   - Source attribution
   - Chat history update

### 7. API Design

#### 7.1 Authentication Endpoints
```
POST /api/v1/auth/token
POST /api/v1/auth/google
POST /api/v1/auth/register
GET  /api/v1/auth/profile
GET  /api/v1/auth/google-client-id
```

#### 7.2 Document Endpoints
```
POST /api/v1/documents/upload
GET  /api/v1/documents/
GET  /api/v1/documents/{document_id}
DELETE /api/v1/documents/{document_id}
```

#### 7.3 Chat Endpoints
```
POST /api/v1/chat/sessions
GET  /api/v1/chat/sessions
POST /api/v1/chat/sessions/{session_id}/messages
GET  /api/v1/chat/sessions/{session_id}/messages
DELETE /api/v1/chat/sessions/{session_id}
```

#### 7.4 Admin Endpoints
```
GET  /api/v1/admin/stats
GET  /api/v1/admin/users
DELETE /api/v1/admin/users/{user_id}
GET  /api/v1/admin/documents
```

### 8. Performance Considerations

#### 8.1 Scalability
- Database connection pooling
- Async request handling
- File storage optimization
- Vector search optimization

#### 8.2 Caching Strategy
- Vector embeddings caching
- Session data caching
- Static file caching

#### 8.3 Resource Management
- File size limitations
- Concurrent user handling
- Memory management for large documents
- LLM response timeout handling

### 9. Deployment Architecture

#### 9.1 Development Environment
- Local Ollama instance
- Local MySQL database
- Development server (Uvicorn)

#### 9.2 Production Considerations
- Reverse proxy (Nginx)
- SSL/TLS termination
- Database clustering
- Load balancing
- Monitoring and logging

### 10. Error Handling & Logging

#### 10.1 Error Categories
- Authentication errors
- File processing errors
- Database connection errors
- AI service errors
- Validation errors

#### 10.2 Logging Strategy
- Request/response logging
- Error tracking
- Performance monitoring
- Security event logging

### 11. Future Enhancements

#### 11.1 Potential Features
- Multi-language support
- Advanced document analytics
- Collaborative chat sessions
- Document versioning
- Advanced admin analytics

#### 11.2 Technical Improvements
- Microservices architecture
- Container deployment
- Advanced caching
- Real-time notifications
- Mobile application

This system design provides a comprehensive foundation for the UNNES Document Chat system, ensuring scalability, security, and maintainability while meeting the specific requirements of the UNNES academic environment.