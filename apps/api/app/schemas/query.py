from pydantic import BaseModel, Field
from typing import List, Optional

class QueryRequest(BaseModel):
    question: str = Field(..., min_length=3)
    module: Optional[str] = None
    top_k: int = Field(default=5, ge=1, le=10)
    
    
class CitationItem(BaseModel):
    source_file: str
    page: Optional[int] = None
    chunk_id: str
    excerpt: str
    

class RelatedLab(BaseModel):
    title: str
    source_file: str
    section: Optional[str] = None
    

class QueryResponse(BaseModel):
    answer: str
    citations: List[CitationItem]
    related_labs: List[RelatedLab] = []
    confidence: float
