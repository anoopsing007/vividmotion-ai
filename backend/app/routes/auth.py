from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from datetime import timedelta
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserRegister, UserLogin, UserResponse, TokenResponse
from app.services.user_service import UserService
from app.services.security_service import SecurityService
from app.config import settings

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    # Check if user already exists
    existing_user = UserService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    existing_username = UserService.get_user_by_username(db, user_data.username)
    if existing_username:
        raise HTTPException(status_code=400, detail="Username already taken")
    
    # Create user
    user = UserService.create_user(db, user_data)
    
    # Create tokens
    access_token = SecurityService.create_access_token({"sub": user.id, "email": user.email})
    refresh_token = SecurityService.create_refresh_token({"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60
    }

@router.post("/login", response_model=TokenResponse)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    user = UserService.verify_password(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    
    access_token = SecurityService.create_access_token({"sub": user.id, "email": user.email})
    refresh_token = SecurityService.create_refresh_token({"sub": user.id})
    
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.access_token_expire_minutes * 60
    }

@router.post("/refresh", response_model=TokenResponse)
def refresh_token(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = SecurityService.decode_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        access_token = SecurityService.create_access_token({"sub": user_id})
        refresh_token = SecurityService.create_refresh_token({"sub": user_id})
        
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer",
            "expires_in": settings.access_token_expire_minutes * 60
        }
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))

@router.get("/me", response_model=UserResponse)
def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)):
    try:
        payload = SecurityService.decode_token(credentials.credentials)
        user_id = payload.get("sub")
        
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        
        return user
    except Exception as e:
        raise HTTPException(status_code=401, detail=str(e))
