import eventlet
# DÒNG NÀY PHẢI ĐẶT TRÊN CÙNG - TRƯỚC TẤT CẢ CÁC IMPORT KHÁC
eventlet.monkey_patch()

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026_super_stable'

# Cấu hình SocketIO
# Chú ý: logger=True giúp Tùng xem lỗi gửi tin nhắn ngay trong Logs của Render
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet', logger=True, engineio_logger=True)

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # Kiểm tra dữ liệu đến trong log server
    print(f"Nhận tin nhắn: {data}")
    
    if data and 'text' in data:
        # Chuyển đổi emoji và gửi đi
        decoded_text = emoji.emojize(data['text'], language='alias')
        emit('render_message', {
            'text': decoded_text,
            'sender_name': data.get('sender_name', 'Ẩn danh')
        }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
    
