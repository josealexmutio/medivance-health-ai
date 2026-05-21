from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from openai import OpenAI
import os

app = FastAPI()

# ✅ FIX: Proper CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

class Req(BaseModel):
    symptoms: str

@app.post("/analyze")
def analyze(data: Req):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a medical assistant. Do not diagnose, only explain possibilities."},
            {"role": "user", "content": data.symptoms}
        ]
    )

    return {"result": response.choices[0].message.content}
