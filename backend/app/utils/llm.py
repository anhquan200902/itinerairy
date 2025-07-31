import os
import httpx
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

GROQ_API_KEY = os.getenv('GROQ_API_KEY')
OPENROUTER_API_KEY = os.getenv('OPENROUTER_API_KEY')
groq_client = Groq(api_key=GROQ_API_KEY)

def call_groq(prompt: str) -> str:
    completion = groq_client.chat.completions.create(
        model = 'llama-3.1-8b-instant',
        messages= [
            {
                'role': 'system',
                'content': (
                    "You are a travel planning expert. "
                    "Return only valid JSON matching the exact schema provided. "
                    "Do not include any explanatory text."
                )
            },
            {
                'role': 'user',
                'content': prompt
            }
        ],
        temperature=0.1, response_format={'type': 'json_object'}
    )
    return completion.choices[0].message.content

async def call_openrouter(prompt: str) -> str:
    url = 'https://api.openrouter.ai/v1/chat/completions'
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {OPENROUTER_API_KEY}',
    }
    payload = {
        'model': 'z-ai/glm-4.5-air:free',
        'temperature': 0.1,
        'messages': [
            {
                'role': 'system',
                'content': (
                    "You are a travel planning expert. "
                    "Return only valid JSON matching the exact schema provided. "
                    "Do not include any explanatory text."
                    )
            },
            {
                'role': 'user',
                'content': prompt
            }
        ]
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, headers=headers, json=payload, timeout=30)
        response.raise_for_status()
        data = response.json()
        return data['choices'][0]['message']['content']
    
async def call_api_with_fallback(prompt: str) -> str:
    try:
        return call_groq(prompt)
    except Exception as groq_error:
        print("[WARNING] Groq API call failed: ", groq_error)
        if OPENROUTER_API_KEY:
            try:
                return await call_openrouter(prompt)
            except Exception as openrouter_error:
                print("[ERROR] OpenRouter API call also failed: ", openrouter_error)
                raise groq_error
        raise groq_error