import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026_pro'

# Cấu hình SocketIO tối ưu cho môi trường Web
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # data: {'text': '...', 'sender_name': '...'}
    if data and 'text' in data:
        # Chuyển đổi emoji (ví dụ :smile: -> 😄)
        msg_unicode = emoji.emojize(data['text'], language='alias')
        
        emit('render_message', {
            'text': msg_unicode,
            'sender_name': data.get('sender_name', 'Thành viên 8A')
        }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
