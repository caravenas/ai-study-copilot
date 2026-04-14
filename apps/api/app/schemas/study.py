from pydantic import BaseModel, Field
from typing import Optional

class StudyRequest(BaseModel):
    question: str = Field(..., min_length=3)
    level: str = Field(default="intermedio", description="Nivel: básico, intermedio, avanzado")
    module: Optional[str] = None
    difficulty: Optional[str] = None
