from __future__ import annotations

import re
from datetime import datetime, timezone
from pathlib import Path
from uuid import uuid4

from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

app = FastAPI(title="Mock Chatbot + Double API")

BASE_DIR = Path(__file__).resolve().parent
UI_FILE_PATH = BASE_DIR / "static" / "index.html"

_SESSIONS: dict[str, list[dict[str, str]]] = {}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def _mock_reply(message: str) -> str:
    text = message.strip()
    lowered = text.lower()

    if not text:
        return "Bạn hãy nhập một tin nhắn trước nhé."

    if any(token in lowered for token in ("xin chào", "chào", "hello", "hi")):
        return "Chào bạn! Bạn muốn mình giúp gì?"

    if "help" in lowered or "giúp" in lowered:
        return "Bạn có thể nhập câu hỏi bất kỳ. Đây là bot mock nên mình sẽ phản hồi theo rule đơn giản."

    if "double" in lowered or "gấp đôi" in lowered:
        match = re.search(r"-?\d+", lowered)
        if match:
            n = int(match.group(0))
            return f"Bạn muốn gấp đôi {n} → {n * 2}"

    return f"Bạn nói: {text} (mock reply)"


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
def ui() -> FileResponse:
    return FileResponse(UI_FILE_PATH)


@app.get("/api/health")
def health():
    return {"status": "ok"}


@app.post("/api/chat", response_model=ChatResponse)
def chat(req: ChatRequest):
    session_id = req.session_id or uuid4().hex
    messages = _SESSIONS.setdefault(session_id, [])

    messages.append({"role": "user", "content": req.message, "ts": _now_iso()})
    reply = _mock_reply(req.message)
    messages.append({"role": "assistant", "content": reply, "ts": _now_iso()})

    return {"session_id": session_id, "reply": reply, "messages": messages}


@app.get("/api/chat/{session_id}", response_model=ChatHistoryResponse)
def chat_history(session_id: str):
    return {"session_id": session_id, "messages": _SESSIONS.get(session_id, [])}


@app.get("/double/{number}")
def double_number(number: int):
    return {"input": number, "result": number * 2}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)
