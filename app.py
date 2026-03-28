from gevent import monkey
monkey.patch_all() # Phải nằm trên cùng

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import emoji

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026_final'

# Cấu hình SocketIO dùng gevent
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='gevent')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    if data and 'text' in data:
        msg_unicode = emoji.emojize(data['text'], language='alias')
        # Gửi dữ liệu đi kèm tên người gửi
        emit('render_message', {
            'text': msg_unicode,
            'sender_name': data.get('sender_name', 'Bạn học 8A')
        }, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
