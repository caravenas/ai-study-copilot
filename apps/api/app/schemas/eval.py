from pydantic import BaseModel, Field
from typing import Optional

class EvalRequest(BaseModel):
    question: str = Field(..., min_length=3)
    expected_answer: str = Field(..., min_length=3, description="Respuesta de referencia (ground truth)")
    module: Optional[str] = None

class MetricScore(BaseModel):
    score: float          # 0.0 a 1.0
    reasoning: str        # Por qué ese puntaje

class EvalResponse(BaseModel):
    question: str
    generated_answer: str
    retrieval_score: MetricScore
    grounding_score: MetricScore
    answer_relevance: MetricScore
    overall_score: float  # Promedio de las 3 métricas
