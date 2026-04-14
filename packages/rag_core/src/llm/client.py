import os
from openai import OpenAI

client = OpenAI(api_key=os.getenv("MINIMAX_API_KEY"), base_url="https://api.minimax.io/v1")

CHAT_MODEL = os.getenv("CHAT_MODEL")

def generate_answer(prompt: str, system_prompt: str | None = None) -> str:
    # Si no le pasan un prompt de sistema especial, usa el básico antiguo
    sys_msg = system_prompt if system_prompt else "Eres un tutor experto en inteligencia artificial."

    response = client.chat.completions.create(
        model=CHAT_MODEL,
        messages=[
            {"role": "system", "content": sys_msg},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2, # Baja creatividad, alta precisión-Importante para grounding en RAG
        
    )
    return response.choices[0].message.content
    
