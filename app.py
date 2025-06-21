from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, join_room, emit
import uuid
import json
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_setup import initialize_firebase
import os
import random

# Load Firebase service account from environment variable
firebase_creds = json.loads(os.environ['FIREBASE_CREDS_JSON'])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
initialize_firebase()
db = firestore.client()


app = Flask(__name__, template_folder='templates')
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")


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

    # Fetch room name from Firestore instead of active_rooms
    doc = db.collection('rooms').document(room_id).get()
    room_name = doc.to_dict().get('name', 'Bubblemeet') if doc.exists else 'Bubblemeet'

    return render_template('meet.html', room_id=room_id, user_name=user_name, room_name=room_name)


@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name', 'Untitled Room')
    room_id = str(uuid.uuid4())[:8]

    # 🎯 Pick a random emoji for the room
    emojis = ["📚", "✏️", "📝", "📖", "💡", "🎓", "🧠", "📊", "🔬", "📎"]
    emoji = random.choice(emojis)

    # ✅ Save to Firestore with name + emoji
    db.collection('rooms').document(room_id).set({
        'name': room_name,
        'emoji': emoji
    })

    return jsonify({'room_id': room_id, 'room_name': room_name, 'emoji': emoji})


@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    rooms_ref = db.collection('rooms').stream()
    rooms = {}
    for doc in rooms_ref:
        rooms[doc.id] = doc.to_dict()
    return jsonify({"rooms": rooms})


# ----- Socket.IO Events -----

@socketio.on('join-room')
def handle_join(data):
    join_room(data['roomId'])  # ✅ Use room ID!
    emit('user-connected', {
        'peerId': data['peerId'],
        'userName': data['userName']
    }, room=data['roomId'], include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')

@socketio.on('chat-message')
def handle_chat(data):
    emit('chat-message', data, room=data['roomId'])  # <- updated

@socketio.on('send-reaction')
def handle_reaction(data):
    room = data.get('room')
    emit('receive-reaction', data, broadcast=True, include_self=False)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
