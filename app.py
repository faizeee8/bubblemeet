from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, emit
import uuid

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory room store (for demo/testing)
active_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html', rooms=active_rooms)


@app.route('/meet/<room_id>')
def meet(room_id):
    user_name = request.args.get('user', 'Guest')
    return render_template('meet.html', room_id=room_id, user_name=user_name)

@app.route('/room/<room_id>')
def room_preview(room_id):
    if room_id not in active_rooms:
        return "Room not found", 404
    return render_template('room.html', room_id=room_id, rooms=active_rooms)

@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name', 'Untitled Room')
    room_id = str(uuid.uuid4())[:8]
    active_rooms[room_id] = {"name": room_name}
    return jsonify({'room_id': room_id, 'room_name': room_name})

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify({"rooms": active_rooms})


# --- Socket.IO Events ---
@socketio.on('join-room')
def handle_join(data):
    room_id = data['room']
    peer_id = data['peerId']
    join_room(room_id)
    emit('user-connected', peer_id, room=room_id, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')

# --- Run using socketio ---
if __name__ == '__main__':
    socketio.run(app, debug=True, port=5050)

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, leave_room, emit
import uuid

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# In-memory room store (for demo/testing)
active_rooms = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html', rooms=active_rooms)

@app.route('/meet/<room_id>')
def meet(room_id):
    user_name = request.args.get('user', 'Guest')
    return render_template('meet.html', room_id=room_id, user_name=user_name)

@app.route('/room/<room_id>')
def room_preview(room_id):
    if room_id not in active_rooms:
        return "Room not found", 404
    return render_template('room.html', room_id=room_id, rooms=active_rooms)

@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name', 'Untitled Room')
    room_id = str(uuid.uuid4())[:8]
    active_rooms[room_id] = {"name": room_name}
    return jsonify({'room_id': room_id, 'room_name': room_name})

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify({"rooms": active_rooms})


# --- Socket.IO Events ---
@socketio.on('join-room')
def handle_join(data):
    room_id = data['room']
    peer_id = data['peerId']
    join_room(room_id)
    emit('user-connected', peer_id, room=room_id, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')
