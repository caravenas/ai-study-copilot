from fastapi import APIRouter
from app.api.routes import health, ingest, query, study, eval

api_router = APIRouter()

api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(ingest.router, prefix="/ingest", tags=["ingest"])
api_router.include_router(query.router, prefix="/query", tags=["query"])
api_router.include_router(study.router, prefix="/study", tags=["study"])
api_router.include_router(eval.router, prefix="/eval", tags=["eval"])
