import os
from flask import Flask, render_template
from flask_socketio import SocketIO, send
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
# Tạo file database tên là chat.db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///chat.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# Cấu trúc bảng lưu tin nhắn
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(500), nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

# Tạo database nếu chưa có
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    # Xóa tin nhắn cũ hơn 24h mỗi khi có người vào web
    time_limit = datetime.utcnow() - timedelta(days=1)
    Message.query.filter(Message.timestamp < time_limit).delete()
    db.session.commit()
    
    # Lấy 50 tin nhắn gần nhất để hiển thị
    history = Message.query.order_by(Message.timestamp.asc()).all()
    return render_template('index.html', history=history)

@socketio.on('message')
def handleMessage(msg):
    # Lưu tin nhắn mới vào database
    new_msg = Message(content=msg)
    db.session.add(new_msg)
    db.session.commit()
    send(msg, broadcast=True)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port)
