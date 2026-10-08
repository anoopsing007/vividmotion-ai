import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPCredentials
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import User, Video
from app.routes.auth import get_current_user
from app.schemas import GenerateVideoRequest, VideoListResponse, VideoResponse
from app.services.ai_service import AIVideoGenerator
from app.services.user_service import UserService

router = APIRouter(prefix="/videos", tags=["videos"])
security = HTTPBearer()
ai_generator = AIVideoGenerator()


@router.get("", response_model=VideoListResponse)
def list_videos(
    skip: int = 0,
    limit: int = 20,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    videos = db.query(Video).filter(Video.user_id == current_user.id).offset(skip).limit(limit).all()
    total = db.query(Video).filter(Video.user_id == current_user.id).count()
    return {"total": total, "videos": videos}


@router.post("/generate", response_model=VideoResponse)
async def generate_video(
    payload: GenerateVideoRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.credits_remaining <= 0:
        raise HTTPException(status_code=400, detail="No credits remaining. Upgrade your plan.")

    if not UserService.deduct_credits(db, current_user.id, 1):
        raise HTTPException(status_code=400, detail="Unable to deduct credits")

    import uuid
    video = Video(
        id=str(uuid.uuid4()),
        user_id=current_user.id,
        prompt=payload.prompt,
        style=payload.style,
        duration=payload.duration,
        aspect_ratio=payload.aspect_ratio,
        status="processing",
        model_name="mock-video-model",
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    asyncio.create_task(ai_generator.generate_async(video.id, payload.prompt, payload.style, payload.duration, payload.aspect_ratio, db))

    return video


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(
    video_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    video = db.query(Video).filter(Video.id == video_id, Video.user_id == current_user.id).first()
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video
