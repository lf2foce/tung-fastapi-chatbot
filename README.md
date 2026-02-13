# Gemini 2.0 Flash Chatbot Service

Dự án này cung cấp một giao diện Chatbot AI thực thụ sử dụng mô hình **Gemini 2.0 Flash** mới nhất và thư viện **google-genai** của Google.

## Tính năng
- **UI Chatbot**: Giao diện chat hiện đại tại `/`.
- **Gemini 2.0 Flash**: Phản hồi cực nhanh và thông minh từ AI mới nhất của Google.
- **Async Handling**: Xử lý bất đồng bộ (async/await) giúp server chịu tải tốt nhiều người dùng cùng lúc.
- **Session Management**: Lưu lịch sử chat theo `session_id` (in-memory).
- **Double API**: Endpoint `/double/{number}` vẫn được giữ nguyên.

## Cách cài đặt và chạy

1. **Cài đặt thư viện:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Cấu hình API Key:**
   Tạo file `.env` và thêm key của bạn:
   ```env
   GOOGLE_API_KEY=your_api_key_here
   ```

3. **Chạy server:**
   ```bash
   python main.py
   ```
   Server sẽ chạy tại `http://127.0.0.1:8001`.

## Cách sử dụng

### 1. Chat với AI
Truy cập `http://127.0.0.1:8001/` để mở giao diện chat.

### 2. API Endpoints
- **Chat API**: `POST /api/chat` với body `{"message": "nội dung", "session_id": "tùy chọn"}`.
- **Lịch sử**: `GET /api/chat/{session_id}`.
- **Gấp đôi số**: `GET /double/{number}`.
- **Tài liệu API**: `http://127.0.0.1:8001/docs`.
