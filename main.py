

from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os  



app = FastAPI()
@app.get("/")
def home():
    return {"message": "Welcome to the Qi Card AI Chatbot API. Use POST /ask to chat."}


SCOUT_MODEL_ID = "meta-llama/llama-4-scout"
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

API_KEY = os.getenv("OPENROUTER_API_KEY")

HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

context = "Qi Card is a financial e-payment company."

class ChatRequest(BaseModel):
    question: str

@app.post("/ask")
async def ask_question(data: ChatRequest):
    messages = [
        {"role": "system", "content": (
            "You are a professional, friendly banking assistant. "
            "Only use the provided CONTEXT to answer questions. "
            "If unsure, reply with: 'Please contact a human representative.'"
        )},
        {"role": "user", "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{data.question}"}
    ]

    payload = {
        "model": SCOUT_MODEL_ID,
        "messages": messages
    }
    
    response = requests.post(OPENROUTER_URL, headers=HEADERS, json=payload)


    return response.json()
