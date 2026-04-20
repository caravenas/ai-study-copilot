from app.schemas.query import QueryRequest, QueryResponse
from app.services.study_service import StudyOrchestrator


def run_query(request: QueryRequest, orchestrator: StudyOrchestrator) -> QueryResponse:
    return orchestrator.run(request)
