from fastapi import HTTPException, status

class AuthenticationError(HTTPException):
    """Custom exception for authentication errors"""
    def __init__(self, detail: str = "Could not validate credentials"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )

class AuthorizationError(HTTPException):
    """Custom exception for authorization errors"""
    def __init__(self, detail: str = "Access forbidden"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )

class DatabaseError(HTTPException):
    """Custom exception for database errors"""
    def __init__(self, detail: str = "Database service not available"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )

class RAGServiceError(HTTPException):
    """Custom exception for RAG service errors"""
    def __init__(self, detail: str = "RAG service not available"):
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=detail
        )