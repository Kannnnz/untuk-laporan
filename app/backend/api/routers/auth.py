from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from backend.schemas.user import UserCreate, Token, GoogleToken
from backend.api.deps import get_current_user
from backend.services.auth_service import AuthService

router = APIRouter()

@router.post("/token", response_model=Token, tags=["Authentication"])
def login_with_password(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = AuthService.authenticate_user(form_data.username, form_data.password)
    access_token = AuthService.create_access_token(user_db["username"])
    
    return {"access_token": access_token, "token_type": "bearer", "role": user_db["role"]}

@router.post("/google", response_model=Token, tags=["Authentication"])
def login_with_google(token_data: GoogleToken):
    user_data = AuthService.authenticate_google_user(token_data.credential)
    access_token = AuthService.create_access_token(user_data["username"])

    return {"access_token": access_token, "token_type": "bearer", "role": user_data["role"]}

@router.post("/register", status_code=status.HTTP_201_CREATED, tags=["Authentication"])
def register(user: UserCreate):
    AuthService.register_user(user.username, user.email, user.password)
    return {"message": "User registered successfully"}

@router.get("/profile", tags=["User"])
def get_user_profile(current_user: dict = Depends(get_current_user)):
    return current_user
