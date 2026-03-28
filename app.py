import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'tung_secret_123'
# Cấu hình để nhận kết nối từ mọi nơi
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('message')
def handle_message(msg):
    # Nhận tin nhắn và phát lại cho tất cả mọi người
    send(msg, broadcast=True)

@socketio.on('troll_all')
def handle_troll():
    # Lệnh đặc biệt để gây ảnh hưởng đến tất cả máy đang xem
    emit('execute_troll', broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)

