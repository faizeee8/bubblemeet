from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Initialize SocketIO
socketio = SocketIO(app)

# Store active rooms
active_rooms = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room')
def create_room():
    room_id = f"room-{random.randint(100000, 999999)}"
    if room_id not in active_rooms:
        active_rooms.append(room_id)
    session['room_id'] = room_id
    return redirect(f'/meet/{room_id}')

@app.route('/rooms')
def list_rooms():
    return render_template('rooms.html', rooms=active_rooms)

@app.route('/room/<room_id>')
def join_room_page(room_id):
    if room_id not in active_rooms:
        return "Room not found", 404
    return render_template('room.html', room_id=room_id)

@app.route('/meet/<room_name>')
def meet_dynamic(room_name):
    if room_name not in active_rooms:
        return "Room not found", 404
    return render_template('meet.html', room_name=room_name)

# Prevent caching issues
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# ✅ Socket.IO event handlers
@socketio.on('join-room')
def handle_join(data):
    room = data['room']
    username = data['username']
    join_room(room)
    emit('user-joined', {'username': username}, room=room)
    print(f"{username} joined room {room}")

@socketio.on('leave-room')
def handle_leave(data):
    room = data['room']
    username = data['username']
    leave_room(room)
    emit('user-left', {'username': username}, room=room)
    print(f"{username} left room {room}")

# ✅ Run with SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True)
