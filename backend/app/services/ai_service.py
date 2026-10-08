import asyncio
from datetime import datetime

from sqlalchemy.orm import Session

from app.models import Video


class AIVideoGenerator:
    def __init__(self):
        self.provider = "mock"

    async def generate_async(self, video_id: str, prompt: str, style: str, duration: int, aspect_ratio: str, db: Session):
        try:
            await asyncio.sleep(3)
            output_url = "https://media.giphy.com/media/l0HlQaQ6gWfllcjDO/giphy.mp4"
            thumbnail_url = "https://media.giphy.com/media/l0HlQaQ6gWfllcjDO/giphy.gif"

            video = db.query(Video).filter(Video.id == video_id).first()
            if not video:
                return

            video.status = "completed"
            video.output_url = output_url
            video.thumbnail_url = thumbnail_url
            video.completed_at = datetime.utcnow()
            db.commit()
        except Exception as e:
            video = db.query(Video).filter(Video.id == video_id).first()
            if video:
                video.status = "failed"
                video.error_message = str(e)
                db.commit()
