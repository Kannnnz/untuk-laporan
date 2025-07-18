import jwt
from datetime import datetime, timedelta
from google.oauth2 import id_token
from google.auth.transport import requests
from fastapi import HTTPException, status

from backend.core import config
from backend.db.session import get_db_connection
from backend.utils.password_utils import hash_password, verify_password
from backend.exceptions.custom_exceptions import AuthenticationError, AuthorizationError

class AuthService:
    @staticmethod
    def authenticate_user(username: str, password: str) -> dict:
        """Authenticate user with username and password"""
        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, password, role FROM users WHERE username = %s", (username,))
            user_db = cursor.fetchone()
            cursor.close()

        if not user_db or not verify_password(password, user_db["password"]):
            raise AuthenticationError("Incorrect username or password")
        
        return user_db
    
    @staticmethod
    def authenticate_google_user(credential: str) -> dict:
        """Authenticate user with Google OAuth2"""
        if not config.GOOGLE_CLIENT_ID:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                detail="Google Client ID not configured on server."
            )
        
        try:
            idinfo = id_token.verify_oauth2_token(
                credential, requests.Request(), config.GOOGLE_CLIENT_ID
            )
            email = idinfo['email']
            username = email.split('@')[0]
            
        except ValueError:
            raise AuthenticationError("Could not validate Google credentials")
        
        if not (email.endswith('@students.unnes.ac.id') or email.endswith('@mail.unnes.ac.id')):
            raise AuthorizationError("Hanya akun Google UNNES yang diizinkan.")

        with get_db_connection() as conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT username, role FROM users WHERE email = %s", (email,))
            user_db = cursor.fetchone()

            if not user_db:
                print(f"User baru dari Google: {email}")
                role = 'user'
                new_password_hash = hash_password(f"google_sso_{datetime.now().timestamp()}")
                
                insert_query = "INSERT INTO users (username, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s)"
                cursor.execute(insert_query, (username, email, new_password_hash, role, datetime.now()))
                conn.commit()
                user_role = role
                user_username = username
            else:
                print(f"User lama dari Google: {email}")
                user_username = user_db['username']
                user_role = user_db['role']
            
            cursor.close()
        
        return {"username": user_username, "role": user_role}
    
    @staticmethod
    def create_access_token(username: str) -> str:
        """Create JWT access token"""
        expires_delta = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
        expire = datetime.utcnow() + expires_delta
        to_encode = {"sub": username, "exp": expire}
        access_token = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
        return access_token
    
    @staticmethod
    def register_user(username: str, email: str, password: str) -> None:
        """Register a new user"""
        hashed_pass = hash_password(password)
        role = 'user'
        
        with get_db_connection() as conn:
            cursor = conn.cursor()
            try:
                query = "INSERT INTO users (username, email, password, role, created_at) VALUES (%s, %s, %s, %s, %s)"
                values = (username, email, hashed_pass, role, datetime.now())
                cursor.execute(query, values)
                conn.commit()
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT, 
                    detail="Username or email already exists"
                )
            finally:
                cursor.close()