from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    module: Optional[str] = None
    difficulty: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=10)
    
    
class CitationItem(BaseModel):
    source_file: str
    page: Optional[int] = None
    chunk_id: str
    excerpt: str
    

class RelatedLab(BaseModel):
    source_file: str
    topics: list[str]
    preview: str
    

class QuizItem(BaseModel):
    question: str
    options: List[str]
    correct: str
    explanation: str


class QueryResponse(BaseModel):
    answer: str
    citations: List[CitationItem]
    related_labs: List[RelatedLab] = []
    confidence: float
    quiz_items: List[QuizItem] = []
