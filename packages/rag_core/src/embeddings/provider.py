import os
from openai import OpenAI

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def embed_texts(texts: list[str]) -> list[list[float]]:
    response = client.embeddings.create(
        model=EMBEDDINGS_MODEL,
        input=texts,
    )
    return [item.embedding for item in response.data]

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]