// JavaScript to handle sending messages in chat
function sendMessage() {
    var message = document.getElementById('chat-input').value;
    var chatbox = document.getElementById('chatbox');
    if (message.trim() !== "") {
        chatbox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
        document.getElementById('chat-input').value = '';
    }
}

// Camera and Microphone access
window.addEventListener('load', () => {
    const myVideo = document.getElementById('my-video');
    if (!myVideo) {
        console.error("Video element with id 'my-video' not found.");
        return;
    }

    navigator.mediaDevices.getUserMedia({ video: true, audio: true })
        .then(stream => {
            myVideo.srcObject = stream;
            myVideo.play();
        })
        .catch(error => {
            console.error("Error accessing camera/mic:", error);
            alert("Camera and microphone access is required. Please check browser permissions.");
        });
});
