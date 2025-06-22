from gevent import monkey
monkey.patch_all()

from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from flask_socketio import SocketIO, emit, join_room
import uuid
import json
import firebase_admin
from firebase_admin import credentials, firestore
from firebase_setup import initialize_firebase
import os
import random

# ✅ Initialize Flask App
app = Flask(__name__, template_folder='templates')
CORS(app)

# ✅ Load Firebase credentials from environment
firebase_creds = json.loads(os.environ['FIREBASE_CREDS_JSON'])
cred = credentials.Certificate(firebase_creds)
firebase_admin.initialize_app(cred)
initialize_firebase()
db = firestore.client()

# ✅ Initialize SocketIO (after app is created)
socketio = SocketIO(app, cors_allowed_origins="*", async_mode="gevent")

# ---------- ROUTES ----------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/rooms')
def rooms():
    return render_template('rooms.html')

@app.route('/meet/<room_id>')
def meet(room_id):
    user_name = request.args.get('username', 'Guest')
    doc = db.collection('rooms').document(room_id).get()
    room_name = doc.to_dict().get('name', 'Bubblemeet') if doc.exists else 'Bubblemeet'
    return render_template('meet.html', room_id=room_id, user_name=user_name, room_name=room_name)

@app.route('/api/create_room', methods=['POST'])
def create_room():
    data = request.get_json()
    room_name = data.get('room_name', 'Untitled Room')
    room_id = str(uuid.uuid4())[:8]
    emojis = ["📚", "✏️", "📝", "📖", "💡", "🎓", "🧠", "📊", "🔬", "📎"]
    emoji = random.choice(emojis)
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

# ---------- SOCKET.IO EVENTS ----------

@socketio.on('join-room')
def handle_join(data):
    print("JOIN-ROOM received:", data)
    room_id = data['roomId']
    join_room(room_id)
    emit('user-connected', {
        'peerId': data['peerId'],
        'userName': data['userName']
    }, room=room_id, include_self=False)

@socketio.on('disconnect')
def handle_disconnect():
    print('A user disconnected')

@socketio.on('chat-message')
def handle_chat(data):
    emit('chat-message', data, room=data['roomId'])

@socketio.on('send-reaction')
def handle_reaction(data):
    emit('receive-reaction', data, room=data.get('room'))

# ---------- RUN ----------

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    socketio.run(app, host='0.0.0.0', port=port)
