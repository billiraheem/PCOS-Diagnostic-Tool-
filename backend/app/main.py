from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.routers.auth import router as auth_router
from app.routers.diagnosis import router as diagnosis_router


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered PCOS diagnostic support tool with explainable predictions",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth_router)
app.include_router(diagnosis_router)

@app.get("/")
async def root():
    return {
        "message": "PCOS Diagnostic Tool API",
        "version": settings.APP_VERSION,
        "status": "healthy"
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "database": "connected",  # Add actual check later
        "ml_model": "loaded"      # Add actual check later
    }