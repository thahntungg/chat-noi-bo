import os
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'chat8a_2026_secret'

# Cấu hình SocketIO cho môi trường Production (Render)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(data):
    # Nhận data: { 'text': '...', 'sender_name': '...' }
    # Gửi lại cho tất cả mọi người
    emit('render_message', data, broadcast=True)

if __name__ == '__main__':
    # Render sẽ cấp một cổng thông qua biến môi trường PORT
    port = int(os.environ.get('PORT', 5000))
    # Sử dụng socketio.run thay vì app.run
    socketio.run(app, host='0.0.0.0', port=port)
