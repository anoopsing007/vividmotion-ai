from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.services.video_service import VideoService

router = APIRouter(prefix="/videos", tags=["videos"])
video_service = VideoService()


class GenerateVideoRequest(BaseModel):
    prompt: str = Field(..., min_length=2, max_length=500)
    image_url: str | None = None
    style: str = "cinematic"
    duration: int = 5
    aspect_ratio: str = "9:16"


@router.get("")
def list_videos():
    return {"videos": video_service.list_videos()}


@router.post("/generate")
def generate_video(payload: GenerateVideoRequest):
    if not payload.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")

    result = video_service.generate_video(payload)
    return result
