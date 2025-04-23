from flask import Flask, render_template, request, redirect, session, g
import random  # Example to generate random room IDs

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for sessions (important for Flask sessions)

# Route to create a new room
@app.route('/create_room')
def create_room():
    room_id = random.randint(1000, 9999)  # Generate a random room ID
    if 'rooms' not in g:
        g.rooms = []  # Initialize rooms list if not already initialized
    g.rooms.append(room_id)  # Add the new room to the global list
    session['room_id'] = room_id  # Store the room ID in session for the current user
    return redirect(f'/room/{room_id}')  # Redirect user to the room

# Route to view available rooms
@app.route('/rooms')
def list_rooms():
    if 'rooms' not in g:
        g.rooms = []  # Initialize rooms list if not already initialized
    return render_template('rooms.html', rooms=g.rooms)

# Route to join an existing room
@app.route('/room/<room_id>')
def join_room(room_id):
    # Check if the room exists in the global list
    if room_id not in [str(r) for r in g.rooms]:
        return "Room not found", 404  # Return 404 if room doesn't exist
    return render_template('room.html', room_id=room_id)

# Home route
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/meet.html')
def meet():
    return render_template('meet.html')
