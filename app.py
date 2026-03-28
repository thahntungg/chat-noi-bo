import eventlet
eventlet.monkey_patch()  # Bắt buộc cho Render + SocketIO

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import emoji  # Thư viện xử lý emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_emoji_secure_2026'

# Cấu hình SocketIO cho production
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    """
    Nhận dữ liệu dạng JSON: { 'text': '...', 'sender_name': '...' }
    """
    if data and 'text' in data and 'sender_name' in data:
        # Giải mã emoji từ văn bản (ví dụ: chuyển :smile: thành 😄)
        # để đảm bảo hiển thị đúng trên mọi thiết bị.
        decoded_text = emoji.emojize(data['text'], language='alias')
        
        # Tạo dữ liệu mới bảo mật hơn
        refined_data = {
            'text': decoded_text,
            'sender_name': data['sender_name'][:20] # Giới hạn tên 20 ký tự
        }
        
        # Gửi lại tin nhắn cho tất cả mọi người (broadcast)
        emit('render_message', refined_data, broadcast=True)

if __name__ == '__main__':
    # Render cấp cổng qua biến môi trường
    port = int(os.environ.get('PORT', 5000))
    # Sử dụng socketio.run
    socketio.run(app, host='0.0.0.0', port=port)
