import eventlet
eventlet.monkey_patch()

import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026'

# Cấu hình SocketIO cho Render
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # Nhận và gửi lại tin nhắn cho cả lớp
    emit('render_message', data, broadcast=True)

if __name__ == '__main__':
    # Lấy cổng do Render cấp
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
