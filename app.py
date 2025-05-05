from flask import Flask, render_template, request, redirect, session, jsonify
from flask import Flask, render_template, request, redirect, session
from flask_socketio import SocketIO, join_room, leave_room, emit
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# ✅ Initialize SocketIO
socketio = SocketIO(app)

# Store active rooms and users
active_rooms = []
room_users = {}
sid_to_user = {}  # NEW: maps socket id to (room_name, user_id, username)

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

# ✅ Prevent caching issues
@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store'
    return response

# ✅ Handle join-room
@socketio.on('join-room')
def handle_join_room(data):
    room_name = data['roomName']
    user_id = data['peerId']
    username = data['userName']

    join_room(room_name)
    if room_name not in room_users:
        room_users[room_name] = {}
    room_users[room_name][user_id] = username

    sid_to_user[request.sid] = (room_name, user_id, username)  # Track socket

    emit('user-connected', {'peerId': user_id, 'userName': username}, room=room_name, include_self=False)
    print(f"{username} ({user_id}) joined room {room_name}")

# ✅ Handle disconnect
@socketio.on('disconnect')
def handle_disconnect():
    sid = request.sid
    if sid in sid_to_user:
        room_name, user_id, username = sid_to_user[sid]
        print(f"{username} ({user_id}) disconnected from {room_name}")
        
        # Remove from room_users
        if room_name in room_users and user_id in room_users[room_name]:
            del room_users[room_name][user_id]

        # Notify others
        emit('user-disconnected', user_id, room=room_name)

        # Clean up
        del sid_to_user[sid]

# ✅ Manual room leave (optional)
@socketio.on('leave-room')
def handle_leave_room(data):
    room = data['room']
    user_id = data['user_id']
    username = data['username']

    leave_room(room)
    if room in room_users and user_id in room_users[room]:
        del room_users[room][user_id]

    # Clean up sid_to_user
    for sid, value in list(sid_to_user.items()):
        if value == (room, user_id, username):
            del sid_to_user[sid]

    emit('user-disconnected', user_id, room=room)
    print(f"{username} ({user_id}) left room {room}")

# ✅ Run with SocketIO
if __name__ == '__main__':
    socketio.run(app, debug=True,port=5001)

@app.route('/meet/<room_id>')
def meet(room_id):
    return render_template('room.html', room_id=room_id)

@app.route('/api/create_room', methods=['POST'])
def api_create_room():
    room_id = f"room-{random.randint(100000, 999999)}"
    if room_id not in active_rooms:
        active_rooms.append(room_id)
    return jsonify({'room_id': room_id})
