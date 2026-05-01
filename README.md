# Bubblemeet

Bubblemeet is a real-time video conferencing web application that allows users to create and join rooms for communication. It is designed as a lightweight browser-based alternative to traditional meeting platforms.

## Features

* Multi-user video conferencing using WebRTC
* Real-time chat system
* Notification indicator for new messages
* Dark mode toggle
* Fullscreen support with exit using ESC
* Responsive layout for different screen sizes
* Active rooms display using Firebase
* Chat minimize and maximize functionality

## Tech Stack

* HTML, CSS, JavaScript
* WebRTC (Peer-to-peer communication)
* Socket.IO (Signaling and messaging)
* Firebase Realtime Database

## Project Structure

* index.html: Landing page
* meet.html: Video conferencing interface
* Firebase configuration: Real-time room tracking
* WebRTC + Socket.IO: Communication layer

## How It Works

1. User creates or joins a room
2. Firebase updates and displays active rooms
3. WebRTC establishes peer-to-peer video connections
4. Socket.IO handles signaling and real-time messaging
5. Users interact through video and chat

## Purpose

* Enable real-time browser-based communication
* Demonstrate WebRTC and real-time systems
* Provide a simple and efficient meeting solution


## Future Improvements

* Screen sharing functionality
* Meeting recording
* User authentication system
* Scalable architecture using SFU
