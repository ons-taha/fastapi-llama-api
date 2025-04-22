# main.py
from fastapi import FastAPI
from pydantic import BaseModel
import requests

app = FastAPI()

SCOUT_MODEL_ID = "meta-llama/llama-4-scout"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = "your_key_here"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

context = "Qi Card is a financial e-payment company."

class UserInput(BaseModel):
    question: str

@app.post("/ask")
async def ask_ai(user_input: UserInput):
    messages = [
        {"role": "system", "content": (
            "You are a professional, friendly Iraqi banking assistant..."
        )},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{user_input.question}"}
    ]

    payload = {
        "model": SCOUT_MODEL_ID,
        "messages": messages
    }

    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload)
    return response.json()
