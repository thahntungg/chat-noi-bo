import eventlet
eventlet.monkey_patch() # BẮT BUỘC: Phải nằm ở dòng số 1 và 2

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_secret_key_2026'

# Cấu hình SocketIO chuyên dụng cho Render
# - cors_allowed_origins="*": Cho phép mọi thiết bị truy cập
# - async_mode='eventlet': Chế độ chạy đa nhiệm ổn định nhất
# - ping_timeout/ping_interval: Giữ kết nối không bị ngắt giữa chừng
socketio = SocketIO(
    app, 
    cors_allowed_origins="*", 
    async_mode='eventlet',
    ping_timeout=60,
    ping_interval=25
)

@app.route('/')
def index():
    return render_template('index.html')

# Lắng nghe sự kiện 'message' từ file index.html
@socketio.on('message')
def handle_message(data):
    # Log để Tùng kiểm tra trong mục Logs của Render
    print(f">>> Đã nhận tin nhắn: {data}")
    
    if data and 'text' in data:
        # Xử lý Emoji
        clean_text = emoji.emojize(data['text'], language='alias')
        
        # Phản hồi lại cho TẤT CẢ mọi người (bao gồm cả người gửi)
        # Tên sự kiện gửi đi là 'render_message'
        emit('render_message', {
            'text': clean_text,
            'sender_name': data.get('sender_name', 'Thành viên 8A')
        }, broadcast=True)

if __name__ == '__main__':
    # Lấy Port từ Render cấp phát
    port = int(os.environ.get('PORT', 5000))
    # Chạy bằng socketio thay vì app
    socketio.run(app, host='0.0.0.0', port=port)
