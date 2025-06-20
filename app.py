from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
import uuid

app = Flask(__name__, template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode='threading')

# In-memory store for active rooms
active_rooms = {}

# ----- Routes -----

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    # Firebase handles live room display, so no need to send room data from Flask
    return render_template('rooms.html')

@app.route('/meet/<room_id>')
def meet(room_id):
    user_name = request.args.get('username', 'Guest')
    room_name = active_rooms.get(room_id, {}).get('name', 'Bubblemeet')
    return render_template('meet.html', room_id=room_id, user_name=user_name, room_name=room_name)

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

# ----- Socket.IO Events -----

@socketio.on('join-room')
def handle_join(data):
    join_room(data['roomName'])
    emit('user-connected', {
        'peerId': data['peerId'],
        'userName': data['userName']
    }, room=data['roomName'], include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')

@socketio.on('chat-message')
def handle_chat(data):
    emit('chat-message', data, room=data['roomName'])

@socketio.on('send-reaction')
def handle_reaction(data):
    room = data.get('room')
    emit('receive-reaction', data, broadcast=True, include_self=False)


# ---- Run Server ----
if __name__ == '__main__':
    print("Server running at http://localhost:5050")
    socketio.run(app, debug=True, port=5050)