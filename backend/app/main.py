from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine
from app.routes import auth, videos
from app.config import settings

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="VividMotion AI", version="0.1.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(auth.router, prefix=settings.api_v1_prefix)
app.include_router(videos.router, prefix=settings.api_v1_prefix)

@app.get("/health")
def health():
    return {"status": "ok", "service": "vividmotion-ai"}
