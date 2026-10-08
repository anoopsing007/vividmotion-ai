from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPCredentials
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.models import User, Video
from app.schemas import GenerateVideoRequest, TokenResponse, UserLogin, UserRegister, UserResponse, VideoListResponse, VideoResponse
from app.services.ai_service import AIVideoGenerator
from app.services.security_service import SecurityService
from app.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()
ai_generator = AIVideoGenerator()


def get_current_user(credentials: HTTPCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
    try:
        payload = SecurityService.decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
        user = UserService.get_user_by_id(db, user_id)
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        return user
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired token")


@router.post("/register", response_model=TokenResponse)
def register(user_data: UserRegister, db: Session = Depends(get_db)):
    if UserService.get_user_by_email(db, user_data.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if UserService.get_user_by_username(db, user_data.username):
        raise HTTPException(status_code=400, detail="Username already taken")

    user = UserService.create_user(db, user_data)
    access_token = SecurityService.create_access_token({"sub": user.id})
    refresh_token = SecurityService.create_refresh_token({"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600,
    }


@router.post("/login", response_model=TokenResponse)
def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = UserService.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = SecurityService.create_access_token({"sub": user.id})
    refresh_token = SecurityService.create_refresh_token({"sub": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": 3600,
    }


@router.get("/me", response_model=UserResponse)
def me(current_user: User = Depends(get_current_user)):
    return current_user
