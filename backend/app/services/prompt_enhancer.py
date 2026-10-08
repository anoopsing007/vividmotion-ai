import httpx
from datetime import datetime


class PromptEnhancer:
    """Enhance user prompts with AI to improve video quality"""
    
    def __init__(self, openai_api_key: str):
        self.openai_api_key = openai_api_key
    
    async def enhance(self, user_prompt: str, style: str) -> str:
        """Use OpenAI to enhance the prompt"""
        try:
            async with httpx.AsyncClient() as client:
                headers = {"Authorization": f"Bearer {self.openai_api_key}"}
                
                system_prompt = f"""You are a professional video director. 
Enhance this video generation prompt to be more detailed and cinematic. 
Style: {style}
Make it 1-2 sentences, vivid and actionable for AI video generation.
Return ONLY the enhanced prompt, nothing else."""
                
                payload = {
                    "model": "gpt-4-turbo-preview",
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    "max_tokens": 150,
                    "temperature": 0.7
                }
                
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    json=payload,
                    headers=headers
                )
                
                result = response.json()
                return result["choices"][0]["message"]["content"].strip()
                
        except Exception as e:
            # If enhancement fails, return original prompt
            return user_prompt
