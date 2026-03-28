import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026_super_stable'

# Tắt logging nếu Tùng muốn code chạy nhẹ hơn, hoặc để True để bắt bệnh
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # Log ra console của Render để Tùng theo dõi
    print(f"Server nhận tin nhắn: {data}")
    if data and 'text' in data:
        decoded_text = emoji.emojize(data['text'], language='alias')
        emit('render_message', {
            'text': decoded_text,
            'sender_name': data.get('sender_name', 'Ẩn danh')
        }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
