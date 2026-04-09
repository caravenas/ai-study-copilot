import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.io/v1")

CHAT_MODEL = os.getenv("CHAT_MODEL")

def generate_answer(prompt: str) -> str:
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": "Eres un tutor experto en inteligencia artificial."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2, # Baja creatividad, alta precisión-Importante para grounding en RAG
        
    )
    return response.choices[0].message.content
    
