from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel, Field
from datetime import datetime
import uuid

from app.services.video_service import VideoService
from app.services.ai_service import AIVideoGenerator

router = APIRouter(prefix="/videos", tags=["videos"])
video_service = VideoService()
ai_generator = AIVideoGenerator()


class GenerateVideoRequest(BaseModel):
    prompt: str = Field(..., min_length=5, max_length=500, description="Creative prompt for video generation")
    style: str = Field(default="cinematic", description="Video style: cinematic, product, dreamy, ad, parallax")
    duration: int = Field(default=5, ge=3, le=10, description="Video duration in seconds")
    aspect_ratio: str = Field(default="9:16", description="Aspect ratio: 9:16, 1:1, 16:9")
    image_url: str | None = Field(None, description="URL to image or base64 encoded image")


class VideoResponse(BaseModel):
    id: str
    user_id: str | None
    prompt: str
    style: str
    duration: int
    aspect_ratio: str
    status: str
    output_url: str | None
    thumbnail_url: str | None
    model_name: str
    created_at: datetime
    completed_at: datetime | None


@router.get("", response_model=list[VideoResponse])
def list_videos(skip: int = 0, limit: int = 20):
    """List all generated videos"""
    return video_service.list_videos(skip=skip, limit=limit)


@router.get("/{video_id}", response_model=VideoResponse)
def get_video(video_id: str):
    """Get video details by ID"""
    video = video_service.get_video(video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


@router.post("/generate", response_model=VideoResponse)
async def generate_video(payload: GenerateVideoRequest):
    """Generate a video from image and prompt"""
    if not payload.prompt or len(payload.prompt.strip()) < 5:
        raise HTTPException(status_code=400, detail="Prompt must be at least 5 characters")

    video_id = str(uuid.uuid4())
    
    # Validate inputs
    valid_styles = ["cinematic", "product", "dreamy", "ad", "parallax"]
    if payload.style not in valid_styles:
        raise HTTPException(status_code=400, detail=f"Style must be one of: {', '.join(valid_styles)}")
    
    valid_ratios = ["9:16", "1:1", "16:9"]
    if payload.aspect_ratio not in valid_ratios:
        raise HTTPException(status_code=400, detail=f"Aspect ratio must be one of: {', '.join(valid_ratios)}")

    try:
        # Create video record
        video = video_service.create_video(
            video_id=video_id,
            prompt=payload.prompt,
            style=payload.style,
            duration=payload.duration,
            aspect_ratio=payload.aspect_ratio,
            image_url=payload.image_url
        )
        
        # Queue generation task
        # In production, this would be a Celery/RQ task
        await ai_generator.generate_async(
            video_id=video_id,
            prompt=payload.prompt,
            style=payload.style,
            duration=payload.duration,
            aspect_ratio=payload.aspect_ratio,
            image_url=payload.image_url
        )
        
        return video
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Generation error: {str(e)}")


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """Upload an image for video generation"""
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Upload to S3/Supabase
    image_url = await video_service.upload_image(file)
    return {"image_url": image_url, "file_name": file.filename}


@router.delete("/{video_id}")
def delete_video(video_id: str):
    """Delete a generated video"""
    success = video_service.delete_video(video_id)
    if not success:
        raise HTTPException(status_code=404, detail="Video not found")
    return {"message": "Video deleted successfully"}
