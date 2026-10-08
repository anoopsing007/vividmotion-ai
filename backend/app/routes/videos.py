from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from sqlalchemy.orm import Session
import uuid

from app.database import get_db
from app.schemas import GenerateVideoRequest, VideoResponse, VideoListResponse
from app.models import Video, User
from app.services.security_service import SecurityService
from app.services.user_service import UserService
from app.services.video_service import VideoService
from app.services.ai_service import AIVideoGenerator

router = APIRouter(prefix="/videos", tags=["videos"])
security = HTTPBearer()
ai_generator = AIVideoGenerator()
video_service = VideoService()

def get_current_user(credentials: HTTPAuthCredentials = Depends(security), db: Session = Depends(get_db)) -> User:
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

@router.get("", response_model=VideoListResponse)
def list_videos(skip: int = 0, limit: int = 20, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    videos = db.query(Video).filter(Video.user_id == current_user.id).offset(skip).limit(limit).all()
    total = db.query(Video).filter(Video.user_id == current_user.id).count()
    return {"total": total, "videos": videos}

@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

@router.post("/generate", response_model=VideoResponse)
async def generate_video(payload: GenerateVideoRequest, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    # Check credits
    if current_user.credits_remaining < 1:
        raise HTTPException(status_code=400, detail="Insufficient credits. Please upgrade your plan.")
    
    # Deduct credits
    UserService.deduct_credits(db, current_user.id, 1)
    
    # Create video record
    video_id = str(uuid.uuid4())
    video = Video(
        id=video_id,
        user_id=current_user.id,
        prompt=payload.prompt,
        style=payload.style,
        duration=payload.duration,
        aspect_ratio=payload.aspect_ratio,
        status="processing"
    )
    db.add(video)
    db.commit()
    db.refresh(video)
    
    # Queue generation (async)
    import asyncio
    asyncio.create_task(ai_generator.generate_async(video_id, payload.prompt, payload.style, payload.duration, payload.aspect_ratio, db))
    
    return video

@router.delete("/{video_id}")
def delete_video(video_id: str, current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    
    db.delete(video)
    db.commit()
    return {"message": "Video deleted successfully"}
