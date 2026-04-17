import os
from openai import OpenAI

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_BATCH_SIZE = 100

def embed_texts(texts: list[str]) -> list[list[float]]:
    all_embeddings: list[list[float]] = []
    for i in range(0, len(texts), EMBED_BATCH_SIZE):
        batch = texts[i : i + EMBED_BATCH_SIZE]
        response = client.embeddings.create(
            model=EMBEDDINGS_MODEL,
            input=batch,
        )
        all_embeddings.extend(item.embedding for item in response.data)
    return all_embeddings

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]