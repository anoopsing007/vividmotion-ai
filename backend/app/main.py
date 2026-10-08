from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes import videos

app = FastAPI(title="VividMotion AI API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(videos.router, prefix="/api")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "vividmotion-ai"}
