from flask import Flask, render_template, request, redirect, session, g
import random

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_room')
def create_room():
    room_id = random.randint(1000, 9999)
    if 'rooms' not in g:
        g.rooms = []
    g.rooms.append(room_id)
    session['room_id'] = room_id
    return redirect(f'/room/{room_id}')

@app.route('/rooms')
def list_rooms():
    if 'rooms' not in g:
        g.rooms = []
    return render_template('rooms.html', rooms=g.rooms)

@app.route('/room/<room_id>')
def join_room(room_id):
    if room_id not in [str(r) for r in g.rooms]:
        return "Room not found", 404
    return render_template('room.html', room_id=room_id)

@app.route('/meet.html')
def meet():
    return render_template('meet.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.before_request
def prevent_cache():
    response = app.make_response()
    response.headers['Cache-Control'] = 'no-store'
    return response

