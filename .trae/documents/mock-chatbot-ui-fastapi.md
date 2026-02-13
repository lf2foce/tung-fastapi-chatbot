## Mục tiêu
- Tạo UI chatbot dạng mock (HTML/CSS/JS) chạy được trên trình duyệt.
- Tạo mock backend FastAPI để UI gọi API và hiển thị hội thoại.

## Thiết kế API (FastAPI)
- Thêm các model Pydantic:
  - `ChatRequest`: `message: str`, `session_id: str | None`.
  - `ChatResponse`: `reply: str`, `session_id: str`, `messages: list` (tuỳ chọn trả về toàn bộ lịch sử).
- Tạo endpoints:
  - `GET /api/health`: trả `{status: "ok"}`.
  - `POST /api/chat`: nhận message, tạo/nhận `session_id`, trả reply mock.
  - `GET /api/chat/{session_id}`: trả lịch sử chat của session (để UI load lại).
- Lưu lịch sử hội thoại in-memory (dict theo `session_id`) để mock “có trạng thái”.

## Mock logic trả lời
- Quy tắc đơn giản (không dùng LLM):
  - Nếu message rỗng → trả nhắc nhập.
  - Nếu có từ khoá như “help”/“xin chào” → trả câu chào.
  - Mặc định → echo lại: `"Bạn nói: ..."` + 1 câu gợi ý.

## UI mock
- Tạo 1 trang chat đơn giản:
  - Khung chat (bubble trái/phải), thanh nhập tin nhắn, nút Send.
  - Trạng thái “Bot đang gõ…” khi chờ response.
  - Lưu `session_id` vào `localStorage` để refresh vẫn giữ lịch sử.
- UI gọi backend qua `fetch('/api/chat')` (cùng domain) để tránh CORS.

## Cách phục vụ UI từ FastAPI
- Thêm thư mục `static/` (hoặc `ui/`) chứa `index.html` (có thể tách `app.js`/`styles.css` nếu cần).
- Thêm endpoint `GET /` (hoặc `GET /chat`) trả file HTML (dùng `FileResponse`), và mount static nếu tách file.
- Giữ endpoint `/double/{number}` hiện tại (hoặc chuyển sang `/api/double/{number}` nếu bạn muốn tách rõ UI/API).

## Cập nhật tài liệu
- Cập nhật [README.md] để có:
  - Cách chạy server.
  - URL UI (`/` hoặc `/chat`) và `/docs`.
  - Ví dụ gọi `POST /api/chat`.

## Kiểm tra
- Test nhanh bằng curl:
  - `POST /api/chat` với JSON.
  - `GET /api/chat/{session_id}`.
- Mở UI trên trình duyệt và gửi vài message để thấy lịch sử hoạt động.

Nếu bạn xác nhận plan này, mình sẽ:
- Chỉnh [main.py] để thêm các endpoint mock chat + serve UI.
- Tạo file UI (HTML/CSS/JS) trong repo và cập nhật README.