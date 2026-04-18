import os
from openai import OpenAI

EMBEDDINGS_MODEL = os.getenv("EMBEDDINGS_MODEL", "text-embedding-3-small")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

EMBED_BATCH_SIZE = 100
# text-embedding-3-small: max 8192 tokens. Worst case (dense numeric content): 1 char = 1 token.
# Using 7500 to guarantee we stay under the limit for any type of content.
MAX_CHARS_PER_CHUNK = 7_500

def embed_texts(texts: list[str]) -> list[list[float]]:
    safe_texts = [t[:MAX_CHARS_PER_CHUNK] for t in texts]
    all_embeddings: list[list[float]] = []
    for i in range(0, len(safe_texts), EMBED_BATCH_SIZE):
        batch = safe_texts[i : i + EMBED_BATCH_SIZE]
        response = client.embeddings.create(
            model=EMBEDDINGS_MODEL,
            input=batch,
        )
        all_embeddings.extend(item.embedding for item in response.data)
    return all_embeddings

def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]