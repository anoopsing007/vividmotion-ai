from typing import Any
from datetime import datetime
import uuid


class VideoService:
    def __init__(self) -> None:
        # In production, this would be a database
        self._videos: dict[str, dict[str, Any]] = {}

    def create_video(self, video_id: str, prompt: str, style: str, duration: int, aspect_ratio: str, image_url: str | None) -> dict[str, Any]:
        """Create a new video record"""
        video = {
            "id": video_id,
            "user_id": None,
            "prompt": prompt,
            "style": style,
            "duration": duration,
            "aspect_ratio": aspect_ratio,
            "image_url": image_url,
            "status": "processing",
            "output_url": None,
            "thumbnail_url": None,
            "model_name": "stable-video-diffusion",
            "created_at": datetime.now(),
            "completed_at": None,
            "error_message": None
        }
        self._videos[video_id] = video
        return video

    def get_video(self, video_id: str) -> dict[str, Any] | None:
        """Get video by ID"""
        return self._videos.get(video_id)

    def update_video_status(self, video_id: str, status: str, output_url: str | None = None, thumbnail_url: str | None = None, error_message: str | None = None) -> dict[str, Any] | None:
        """Update video status after generation"""
        if video_id not in self._videos:
            return None
        
        video = self._videos[video_id]
        video["status"] = status
        if output_url:
            video["output_url"] = output_url
        if thumbnail_url:
            video["thumbnail_url"] = thumbnail_url
        if error_message:
            video["error_message"] = error_message
        if status == "completed":
            video["completed_at"] = datetime.now()
        
        return video

    def list_videos(self, skip: int = 0, limit: int = 20) -> list[dict[str, Any]]:
        """List all videos with pagination"""
        videos_list = list(self._videos.values())
        return sorted(videos_list, key=lambda x: x["created_at"], reverse=True)[skip : skip + limit]

    def delete_video(self, video_id: str) -> bool:
        """Delete a video"""
        if video_id in self._videos:
            del self._videos[video_id]
            return True
        return False

    async def upload_image(self, file) -> str:
        """Upload image to storage (S3/Supabase)"""
        # In production, upload to S3 or Supabase
        # For now, return a mock URL
        filename = f"{uuid.uuid4()}_{file.filename}"
        return f"https://storage.example.com/uploads/{filename}"
