# UNNES Document Chat System - System Design

## 1. System Overview

### 1.1 Purpose
UNNES Document Chat System adalah aplikasi berbasis web yang memungkinkan pengguna untuk:
- Mengupload dokumen dalam berbagai format
- Melakukan chat dengan AI berdasarkan konten dokumen
- Mendapatkan ringkasan dokumen
- Mengelola dokumen dan riwayat chat

### 1.2 Key Features
- **Document Upload & Processing**: Upload dan pemrosesan dokumen dengan ekstraksi teks
- **RAG (Retrieval-Augmented Generation)**: Chat AI yang menggunakan konten dokumen sebagai konteks
- **User Management**: Autentikasi dengan password dan Google OAuth
- **Admin Panel**: Manajemen user, dokumen, dan monitoring aktivitas
- **Document Summarization**: Pembuatan ringkasan dokumen otomatis

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (HTML/JS)     │◄──►│   (FastAPI)     │◄──►│   Services      │
│                 │    │                 │    │                 │
│ - User Interface│    │ - API Endpoints │    │ - Ollama LLM    │
│ - Authentication│    │ - Business Logic│    │ - Google OAuth  │
│ - File Upload   │    │ - Data Processing│   │ - MySQL DB      │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   Data Layer    │
                    │                 │
                    │ - File Storage  │
                    │ - Vector Store  │
                    │ - Database      │
                    └─────────────────┘
```

### 2.2 Detailed Component Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                           Frontend Layer                          │
├──────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │   Login     │ │  Document   │ │    Chat     │ │   Admin     │ │
│ │  Component  │ │  Manager    │ │  Interface  │ │   Panel     │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                        API Gateway Layer                          │
├──────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │    Auth     │ │  Documents  │ │    Chat     │ │    Admin    │ │
│ │   Router    │ │   Router    │ │   Router    │ │   Router    │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                       Business Logic Layer                        │
├──────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │    Auth     │ │    RAG      │ │    Chat     │ │Summarization│ │
│ │   Service   │ │   Service   │ │   Service   │ │   Service   │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Data Access Layer                         │
├──────────────────────────────────────────────────────────────────┤
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │   MySQL     │ │    File     │ │   Vector    │ │   Session   │ │
│ │  Database   │ │   Storage   │ │   Store     │ │   Manager   │ │
│ │             │ │   (Local)   │ │   (FAISS)   │ │             │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## 3. Component Details

### 3.1 Frontend Components

#### 3.1.1 Technology Stack
- **HTML5**: Struktur halaman web
- **CSS3**: Styling dan responsive design
- **Vanilla JavaScript**: Interaksi user dan API calls
- **Google OAuth SDK**: Autentikasi Google

#### 3.1.2 Key Components
- **Authentication Manager**: Mengelola login/logout dan token management
- **Document Upload Interface**: Drag & drop file upload dengan progress indicator
- **Chat Interface**: Real-time chat dengan AI
- **Admin Dashboard**: Monitoring dan manajemen sistem

### 3.2 Backend Components

#### 3.2.1 Technology Stack
- **FastAPI**: Web framework untuk API development
- **Pydantic**: Data validation dan serialization
- **JWT**: Token-based authentication
- **Uvicorn**: ASGI server

#### 3.2.2 API Routers

**Authentication Router (`/api/v1/auth`)**
- User registration dan login
- Google OAuth integration
- JWT token management
- User profile management

**Documents Router (`/api/v1/documents`)**
- File upload dan processing
- Document metadata management
- File format validation

**Chat Router (`/api/v1/chat`)**
- Message processing
- RAG integration
- Chat history management

**Admin Router (`/api/v1/admin`)**
- User management
- System statistics
- Document management
- Activity monitoring

**Summarization Router (`/api/v1/summarization`)**
- Document summarization
- Length customization
- Multi-document summarization

### 3.3 Business Logic Services

#### 3.3.1 Authentication Service
```python
class AuthService:
    - authenticate_user(username, password)
    - authenticate_google_user(credential)
    - create_access_token(username)
    - register_user(username, email, password)
    - hash_password(password)
    - verify_password(password, hashed)
```

#### 3.3.2 RAG Service
```python
class RAGService:
    - load_documents(file_paths)
    - split_documents(documents)
    - create_embeddings(texts)
    - build_vector_store(embeddings)
    - similarity_search(query, k=5)
    - generate_response(query, context)
```

#### 3.3.3 Chat Service
```python
class ChatService:
    - process_message(message, document_ids, session_id, username)
    - get_relevant_documents(message, document_ids)
    - generate_ai_response(message, context)
    - save_chat_history(message, response, session_id, username)
```

#### 3.3.4 Summarization Service
```python
class SummarizationService:
    - summarize_documents(document_ids, length)
    - extract_document_content(document_ids)
    - generate_summary(content, length)
```

## 4. Data Architecture

### 4.1 Database Schema (MySQL)

#### 4.1.1 Users Table
```sql
CREATE TABLE users (
    username VARCHAR(50) PRIMARY KEY,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255),
    role ENUM('user', 'admin') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

#### 4.1.2 Documents Table
```sql
CREATE TABLE documents (
    id VARCHAR(36) PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    filename VARCHAR(255) NOT NULL,
    file_path VARCHAR(500) NOT NULL,
    file_size BIGINT,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);
```

#### 4.1.3 Chat History Table
```sql
CREATE TABLE chat_history (
    id INT AUTO_INCREMENT PRIMARY KEY,
    session_id VARCHAR(36) NOT NULL,
    username VARCHAR(50) NOT NULL,
    message TEXT NOT NULL,
    response TEXT NOT NULL,
    document_ids JSON,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE
);
```

### 4.2 File Storage Structure
```
uploads/
├── admin/
│   ├── document1.pdf
│   └── document2.docx
├── user1/
│   ├── file1.pdf
│   └── file2.txt
└── user2/
    └── presentation.pptx
```

### 4.3 Vector Store (FAISS)
```
vector_store/
├── unnes_docs.faiss    # FAISS index file
└── unnes_docs.pkl      # Metadata pickle file
```

## 5. Data Flow

### 5.1 Document Upload Flow
```
1. User selects files → Frontend validation
2. Files sent to /api/v1/documents/upload
3. Backend validates file types and sizes
4. Files saved to uploads/{username}/
5. Document metadata saved to database
6. Text extraction and chunking
7. Embeddings generation
8. Vector store update
9. Success response to frontend
```

### 5.2 Chat Processing Flow
```
1. User sends message → Frontend
2. Message sent to /api/v1/chat
3. Authentication validation
4. Relevant documents retrieval from vector store
5. Context preparation
6. LLM query to Ollama
7. Response generation
8. Chat history saved to database
9. Response sent to frontend
```

### 5.3 Authentication Flow
```
1. User login → Frontend
2. Credentials sent to /api/v1/auth/token
3. User validation against database
4. JWT token generation
5. Token sent to frontend
6. Token stored in localStorage
7. Token included in subsequent API calls
```

## 6. External Dependencies

### 6.1 Ollama LLM
- **Purpose**: Large Language Model untuk chat dan summarization
- **Default Model**: mistral:7b
- **Connection**: HTTP API ke localhost:11434
- **Fallback**: Error handling jika service tidak tersedia

### 6.2 Google OAuth
- **Purpose**: Alternative authentication method
- **Integration**: Google Identity Services
- **Configuration**: GOOGLE_CLIENT_ID environment variable

### 6.3 MySQL Database
- **Purpose**: Primary data storage
- **Connection**: Connection pooling untuk performance
- **Backup**: Regular backup strategy diperlukan

## 7. Security Architecture

### 7.1 Authentication & Authorization
- **JWT Tokens**: Stateless authentication
- **Password Hashing**: bcrypt untuk password security
- **Role-Based Access**: User dan Admin roles
- **Token Expiration**: 60 menit untuk security

### 7.2 Data Protection
- **Input Validation**: Pydantic schemas untuk semua input
- **File Type Validation**: Whitelist file extensions
- **SQL Injection Prevention**: Parameterized queries
- **XSS Prevention**: Input sanitization

### 7.3 Access Control
- **User Isolation**: Users hanya akses dokumen sendiri
- **Admin Privileges**: Full access dengan restrictions
- **File Access**: Path traversal prevention

## 8. Performance Considerations

### 8.1 Database Optimization
- **Indexing**: Primary keys dan foreign keys
- **Connection Pooling**: Efficient database connections
- **Query Optimization**: Efficient SQL queries

### 8.2 File Processing
- **Async Processing**: Non-blocking file uploads
- **Chunking Strategy**: Optimal chunk size (1000 chars)
- **Batch Processing**: Multiple files processing

### 8.3 Vector Store Optimization
- **FAISS Index**: Efficient similarity search
- **Incremental Updates**: Add/remove documents efficiently
- **Memory Management**: Optimal embedding storage

## 9. Scalability Architecture

### 9.1 Horizontal Scaling Options
- **Load Balancer**: Multiple FastAPI instances
- **Database Clustering**: MySQL master-slave setup
- **File Storage**: Distributed file system (future)
- **Vector Store**: Distributed vector databases (future)

### 9.2 Caching Strategy
- **Redis Integration**: Session dan response caching
- **Embedding Cache**: Frequently accessed embeddings
- **Static File Caching**: Frontend assets

## 10. Monitoring & Logging

### 10.1 Application Monitoring
- **Health Checks**: /health endpoint untuk monitoring
- **Performance Metrics**: Response time tracking
- **Error Tracking**: Comprehensive error logging

### 10.2 Business Metrics
- **User Activity**: Login frequency, document uploads
- **System Usage**: Chat volume, document processing
- **Admin Dashboard**: Real-time system statistics

## 11. Deployment Architecture

### 11.1 Development Environment
```
┌─────────────────┐
│   Local Dev     │
├─────────────────┤
│ - FastAPI       │
│ - MySQL Local   │
│ - Ollama Local  │
│ - File Storage  │
└─────────────────┘
```

### 11.2 Production Environment (Recommended)
```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Web Server    │    │   App Server    │    │   Database      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ - Nginx         │◄──►│ - FastAPI       │◄──►│ - MySQL         │
│ - SSL/TLS       │    │ - Gunicorn      │    │ - Backup        │
│ - Static Files  │    │ - Workers       │    │ - Replication   │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                    ┌─────────────────┐
                    │   AI Services   │
                    ├─────────────────┤
                    │ - Ollama        │
                    │ - GPU Support   │
                    │ - Model Cache   │
                    └─────────────────┘
```

## 12. Configuration Management

### 12.1 Environment Variables
```env
# Application
APP_SECRET_KEY=secure_secret_key
ENVIRONMENT=production

# Database
DB_HOST=localhost
DB_USER=app_user
DB_PASSWORD=secure_password
DB_NAME=unnes_chat_db

# AI Services
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=mistral:7b

# External Services
GOOGLE_CLIENT_ID=google_oauth_client_id

# Admin
DEFAULT_ADMIN_PASSWORD=secure_admin_password
```

### 12.2 Configuration Validation
- **Startup Checks**: Validate all required configurations
- **Service Health**: Check external service availability
- **Security Validation**: Ensure secure configurations

## 13. Error Handling Strategy

### 13.1 Error Categories
- **Authentication Errors**: 401 Unauthorized
- **Authorization Errors**: 403 Forbidden
- **Validation Errors**: 422 Unprocessable Entity
- **Service Errors**: 503 Service Unavailable
- **System Errors**: 500 Internal Server Error

### 13.2 Error Response Format
```json
{
  "detail": "Error description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2024-01-01T00:00:00Z",
  "path": "/api/v1/endpoint"
}
```

## 14. Testing Strategy

### 14.1 Unit Testing
- **Service Layer**: Business logic testing
- **API Endpoints**: Request/response testing
- **Data Models**: Validation testing

### 14.2 Integration Testing
- **Database Integration**: CRUD operations
- **External Services**: Ollama dan Google OAuth
- **File Processing**: Upload dan processing pipeline

### 14.3 End-to-End Testing
- **User Workflows**: Complete user journeys
- **Admin Functions**: Administrative operations
- **Error Scenarios**: Error handling validation

## 15. Future Enhancements

### 15.1 Technical Improvements
- **Microservices Architecture**: Service decomposition
- **Container Orchestration**: Docker dan Kubernetes
- **Message Queue**: Async processing dengan Redis/RabbitMQ
- **CDN Integration**: Static file delivery optimization

### 15.2 Feature Enhancements
- **Multi-language Support**: Internationalization
- **Advanced Analytics**: User behavior tracking
- **Mobile Application**: React Native atau Flutter
- **Real-time Collaboration**: WebSocket integration

### 15.3 AI/ML Improvements
- **Model Fine-tuning**: Domain-specific model training
- **Multi-modal Support**: Image dan video processing
- **Advanced RAG**: Graph-based retrieval
- **Personalization**: User-specific recommendations

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Architecture Type**: Monolithic with Microservice-ready design  
**Target Scale**: Small to Medium Enterprise
