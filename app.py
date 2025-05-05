from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import uuid

app = Flask(__name__)
CORS(app)

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
    return render_template('meet.html', room_id=room_id)

@app.route('/api/create_room', methods=['POST'])
def create_room():
    room_id = str(uuid.uuid4())[:8]  # short ID
    active_rooms[room_id] = {"name": f"Study Room {room_id}"}
    return jsonify({'room_id': room_id})

@app.route('/api/rooms', methods=['GET'])
def get_rooms():
    return jsonify({"rooms": active_rooms})

if __name__ == '__main__':
    app.run(debug=True)
