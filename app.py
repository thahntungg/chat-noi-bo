import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026_tung'

# Cấu hình SocketIO đơn giản nhất để tránh lỗi RLock
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # data nhận được: { 'text': '...', 'sender_name': '...' }
    if data:
        emit('render_message', data, broadcast=True)

if __name__ == '__main__':
    # Render cấp port qua biến môi trường PORT
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
