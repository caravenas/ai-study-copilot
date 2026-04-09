from pydantic import BaseModel

class IngestRequest(BaseModel):
    file_path: str

class IngestResponse(BaseModel):
    status: str
    chunks_indexed: int
    file_path: str
