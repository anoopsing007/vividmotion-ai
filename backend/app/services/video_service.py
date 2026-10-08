from typing import Any


class VideoService:
    def __init__(self) -> None:
        self._videos: list[dict[str, Any]] = []

    def generate_video(self, payload: Any) -> dict[str, Any]:
        video_id = f"video_{len(self._videos) + 1:04d}"
        result = {
            "id": video_id,
            "status": "completed",
            "prompt": payload.prompt,
            "image_url": payload.image_url or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518",
            "style": payload.style,
            "duration": payload.duration,
            "aspect_ratio": payload.aspect_ratio,
            "output_url": "https://example.com/generated-video.mp4",
            "model": "mock-video-model"
        }
        self._videos.append(result)
        return result

    def list_videos(self) -> list[dict[str, Any]]:
        return self._videos
