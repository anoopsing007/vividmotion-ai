import httpx
import asyncio
from datetime import datetime
from app.config import settings
from app.services.video_service import VideoService


class AIVideoGenerator:
    """
    Handles AI video generation using Replicate, Runway, or Stable Video Diffusion.
    Supports both sync and async generation with proper error handling.
    """
    
    def __init__(self):
        self.provider = settings.video_model_provider
        self.video_service = VideoService()
        
    async def generate_async(self, video_id: str, prompt: str, style: str, duration: int, aspect_ratio: str, image_url: str | None):
        """Generate video asynchronously (should be run as background task)"""
        try:
            # Enhance prompt with style instructions
            enhanced_prompt = self._enhance_prompt(prompt, style)
            
            # Call appropriate AI provider
            if self.provider == "replicate":
                result = await self._generate_with_replicate(enhanced_prompt, image_url, duration, aspect_ratio)
            elif self.provider == "runway":
                result = await self._generate_with_runway(enhanced_prompt, image_url, duration, aspect_ratio)
            elif self.provider == "stability":
                result = await self._generate_with_stability(enhanced_prompt, image_url, duration, aspect_ratio)
            else:
                result = await self._generate_mock(enhanced_prompt, image_url, duration, aspect_ratio)
            
            # Update video with result
            self.video_service.update_video_status(
                video_id=video_id,
                status="completed",
                output_url=result.get("output_url"),
                thumbnail_url=result.get("thumbnail_url")
            )
            
        except Exception as e:
            # Update video with error
            self.video_service.update_video_status(
                video_id=video_id,
                status="failed",
                error_message=str(e)
            )
    
    def _enhance_prompt(self, prompt: str, style: str) -> str:
        """Enhance user prompt with style-specific instructions"""
        style_instructions = {
            "cinematic": "Cinematic camera movement, professional color grading, soft lighting, 4K quality. ",
            "product": "Product commercial style, clean lighting, professional advertisement look, focus on details. ",
            "dreamy": "Dreamy aesthetic, soft focus, ethereal glow, warm colors, gentle motion. ",
            "ad": "Modern advertisement style, dynamic motion, trendy effects, high energy. ",
            "parallax": "Parallax background movement, depth effect, layered motion, modern parallax style. "
        }
        
        enhanced = style_instructions.get(style, "") + prompt
        return enhanced
    
    async def _generate_with_replicate(self, prompt: str, image_url: str | None, duration: int, aspect_ratio: str) -> dict:
        """
        Generate video using Replicate API
        Replicate supports: Stable Video Diffusion, Pika, Luma, etc.
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Token {settings.replicate_api_key}"}
                
                # Use Stable Video Diffusion model
                model = "stability-ai/stable-video-diffusion:a5b3d6f5ff2e"
                
                payload = {
                    "input": {
                        "image": image_url or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518",
                        "prompt": prompt,
                        "num_frames": duration * 30,  # 30fps
                        "num_inference_steps": 25,
                        "guidance_scale": 7.5
                    }
                }
                
                response = await client.post(
                    f"https://api.replicate.com/v1/predictions",
                    json=payload,
                    headers=headers
                )
                
                result = response.json()
                
                # Poll for completion (simplified)
                while result.get("status") in ["starting", "processing"]:
                    await asyncio.sleep(2)
                    response = await client.get(
                        f"https://api.replicate.com/v1/predictions/{result['id']}",
                        headers=headers
                    )
                    result = response.json()
                
                if result.get("status") == "succeeded":
                    output = result.get("output", [])
                    return {
                        "output_url": output[0] if output else None,
                        "thumbnail_url": output[0] if output else None
                    }
                else:
                    raise Exception(f"Generation failed: {result.get('error')}")
                    
        except Exception as e:
            raise Exception(f"Replicate error: {str(e)}")
    
    async def _generate_with_runway(self, prompt: str, image_url: str | None, duration: int, aspect_ratio: str) -> dict:
        """
        Generate video using Runway API
        Runway ML offers Gen-3, Avatars, and Motion Brush
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "Authorization": f"Bearer {settings.runway_api_key}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "prompt": prompt,
                    "model": "gen3",
                    "image": image_url or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518",
                    "duration": duration,
                    "aspect_ratio": aspect_ratio
                }
                
                response = await client.post(
                    "https://api.runwayml.com/v1/image_to_video",
                    json=payload,
                    headers=headers,
                    timeout=30.0
                )
                
                result = response.json()
                
                if response.status_code == 200:
                    return {
                        "output_url": result.get("video_url"),
                        "thumbnail_url": result.get("thumbnail_url")
                    }
                else:
                    raise Exception(f"Runway error: {result.get('error')}")
                    
        except Exception as e:
            raise Exception(f"Runway error: {str(e)}")
    
    async def _generate_with_stability(self, prompt: str, image_url: str | None, duration: int, aspect_ratio: str) -> dict:
        """
        Generate video using Stability AI (Stable Video Diffusion)
        """
        try:
            async with httpx.AsyncClient() as client:
                headers = {
                    "authorization": settings.stability_api_key,
                    "accept": "video/mp4"
                }
                
                # Read image from URL or upload
                files = {
                    "image": ("image.jpg", httpx.get(image_url or "https://images.unsplash.com/photo-1521572267360-ee0c2909d518").content, "image/jpeg")
                }
                
                data = {
                    "motion_bucket_id": 127,
                    "seed": 0,
                    "cfg_scale": 1.8,
                    "conditioning_scale": 1.1,
                }
                
                response = await client.post(
                    "https://api.stability.ai/v2beta/image-to-video",
                    files=files,
                    data=data,
                    headers=headers,
                    timeout=60.0
                )
                
                if response.status_code == 200:
                    video_url = f"https://videos.stability.ai/{response.headers.get('id')}.mp4"
                    return {
                        "output_url": video_url,
                        "thumbnail_url": None
                    }
                else:
                    raise Exception(f"Stability API error: {response.status_code}")
                    
        except Exception as e:
            raise Exception(f"Stability error: {str(e)}")
    
    async def _generate_mock(self, prompt: str, image_url: str | None, duration: int, aspect_ratio: str) -> dict:
        """
        Mock generation for development/testing
        """
        await asyncio.sleep(3)  # Simulate processing time
        
        return {
            "output_url": "https://media.giphy.com/media/l0HlQaQ6gWfllcjDO/giphy.mp4",
            "thumbnail_url": "https://media.giphy.com/media/l0HlQaQ6gWfllcjDO/giphy.gif"
        }
