# FastAPI Mock Chatbot + Double Number Service

Dự án này cung cấp:
- Một UI chatbot dạng mock (HTML/CSS/JS) nối được với backend FastAPI.
- Một API đơn giản để gấp đôi một số nguyên.

## Tính năng
- UI chatbot tại `/`.
- Mock Chat API:
  - `POST /api/chat`: gửi message và nhận reply (kèm `session_id`).
  - `GET /api/chat/{session_id}`: lấy lịch sử hội thoại theo session.
  - `GET /api/health`: health check.
- Double API:
  - `GET /double/{number}`: trả về kết quả gấp đôi.
- Tài liệu API tự động tại `/docs` (Swagger UI).

## Cách cài đặt và chạy

1. **Cài đặt thư viện cần thiết:**
   ```bash
   pip install fastapi uvicorn
   ```

2. **Chạy server:**
   ```bash
   uvicorn main:app --host 127.0.0.1 --port 8001 --reload
   ```

## Cách sử dụng

### 1. Mở UI chatbot
Mở trình duyệt tại:
`http://127.0.0.1:8001/`

UI sẽ lưu `session_id` vào `localStorage` để refresh vẫn giữ lịch sử.

### 2. Gọi Chat API

Gửi một message (ví dụ):
```bash
curl -X POST http://127.0.0.1:8001/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"xin chào"}'
```

Ví dụ response:
```json
{
  "session_id": "....",
  "reply": "Chào bạn! Bạn muốn mình giúp gì?",
  "messages": [
    {"role":"user","content":"xin chào","ts":"..."},
    {"role":"assistant","content":"Chào bạn! Bạn muốn mình giúp gì?","ts":"..."}
  ]
}
```

Lấy lịch sử theo session:
`http://127.0.0.1:8001/api/chat/<session_id>`

### 3. Gấp đôi một số
Truy cập đường dẫn sau (ví dụ với số 25):
`http://127.0.0.1:8001/double/25`

**Kết quả trả về:**
```json
{
  "input": 25,
  "result": 50
}
```

### 4. Xem tài liệu API (Swagger UI)
FastAPI tự động tạo tài liệu hướng dẫn tại:
`http://127.0.0.1:8001/docs`

Tại đây bạn có thể thử nghiệm trực tiếp các endpoint một cách trực quan.
