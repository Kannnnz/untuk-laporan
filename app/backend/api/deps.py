from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from typing import Dict

from backend.core import config
from backend.db.session import get_db_connection
from backend.exceptions.custom_exceptions import AuthenticationError, AuthorizationError

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/token")

def get_current_user(token: str = Depends(oauth2_scheme)) -> Dict:
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise AuthenticationError()
    except jwt.PyJWTError:
        raise AuthenticationError()
    
    with get_db_connection() as conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT username, email, role FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        cursor.close()
    
    if user is None:
        raise AuthenticationError()
    return user

def require_admin(current_user: Dict = Depends(get_current_user)) -> Dict:
    if current_user.get('role') != 'admin':
        raise AuthorizationError("Admin access required")
    return current_user