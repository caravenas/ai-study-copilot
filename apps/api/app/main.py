import sys
from pathlib import Path
from dotenv import load_dotenv

# Load .env from monorepo root before any other imports
_root = Path(__file__).resolve().parents[3]
load_dotenv(_root / ".env")

# Add monorepo root to path so `packages.*` imports resolve
sys.path.insert(0, str(_root))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.router import api_router
from app.core.config import settings

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.API_VERSION,
        description="API para el asistente de estudio",
        docs_url="/docs",
        redoc_url="/redoc"
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(api_router, prefix="/api")
    return app

app = create_app()
