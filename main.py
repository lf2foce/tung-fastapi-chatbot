from __future__ import annotations

import os
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from google import genai
from google.genai import types
from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

# System prompt to define AI behavior
SYSTEM_PROMPT = """
You are a helpful, flexible, and multilingual AI assistant. 
Your goal is to provide accurate and useful information while adapting to the user's preferred language naturally.
If a user asks in Vietnamese, respond in Vietnamese. If they use English, respond in English, and so on.
Be polite, concise, and professional.
"""

# Initialize the new Google GenAI Client
if not GOOGLE_API_KEY:
    print("WARNING: GOOGLE_API_KEY not found in .env file")
    client = None
else:
    # Use the latest SDK
    client = genai.Client(api_key=GOOGLE_API_KEY)

# We use the latest model: gemini-2.0-flash
MODEL_ID = "gemini-2.0-flash"
CONFIG = types.GenerateContentConfig(
    system_instruction=SYSTEM_PROMPT,
    temperature=0.7,
)

app = FastAPI(title="Gemini 2.0 Flash Chatbot + Double API")

BASE_DIR = Path(__file__).resolve().parent
UI_FILE_PATH = BASE_DIR / "static" / "index.html"

# In-memory storage for chat sessions
# New SDK format for history: list[types.Content]
_SESSIONS: dict[str, list[types.Content]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str | None = None


class ChatMessage(BaseModel):
    role: str
    content: str
    ts: str


class ChatResponse(BaseModel):
    session_id: str
    reply: str
    messages: list[ChatMessage]


class ChatHistoryResponse(BaseModel):
    session_id: str
    messages: list[ChatMessage]


@app.get("/", include_in_schema=False)
async def ui() -> FileResponse:
    return FileResponse(UI_FILE_PATH)


@app.get("/api/health")
async def health():
    return {"status": "ok", "ai_configured": bool(GOOGLE_API_KEY), "model": MODEL_ID}


@app.post("/api/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    if not client:
        raise HTTPException(status_code=500, detail="Google API Key not configured")

    session_id = req.session_id or uuid4().hex
    
    # Get or initialize history
    history = _SESSIONS.get(session_id, [])
    
    try:
        # Add user message to history
        user_content = types.Content(role="user", parts=[types.Part(text=req.message)])
        history.append(user_content)
        
        # Call Gemini 2.0 Flash asynchronously using generate_content with history
        # This is equivalent to a chat session but more direct
        response = await client.aio.models.generate_content(
            model=MODEL_ID,
            contents=history,
            config=CONFIG
        )
        
        reply_text = response.text
        
        # Add assistant message to history
        assistant_content = types.Content(role="model", parts=[types.Part(text=reply_text)])
        history.append(assistant_content)
        
        # Save updated history
        _SESSIONS[session_id] = history
        
        # Convert history to UI format
        ui_messages = []
        for content in history:
            role = "user" if content.role == "user" else "assistant"
            text = "".join([p.text for p in content.parts if p.text])
            ui_messages.append(ChatMessage(role=role, content=text, ts=_now_iso()))
            
        return {
            "session_id": session_id,
            "reply": reply_text,
            "messages": ui_messages
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        # If error, remove the last user message from history to keep it consistent
        if history and history[-1].role == "user":
            history.pop()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/chat/{session_id}", response_model=ChatHistoryResponse)
async def chat_history(session_id: str):
    history = _SESSIONS.get(session_id, [])
    ui_messages = []
    for content in history:
        role = "user" if content.role == "user" else "assistant"
        text = "".join([p.text for p in content.parts if p.text])
        ui_messages.append(ChatMessage(role=role, content=text, ts=_now_iso()))
        
    return {"session_id": session_id, "messages": ui_messages}


@app.get("/double/{number}")
async def double_number(number: int):
    return {"input": number, "result": number * 2}


if __name__ == "__main__":
    import uvicorn
    # Render provides PORT environment variable
    port = int(os.getenv("PORT", 8001))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
