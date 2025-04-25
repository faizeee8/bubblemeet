// JavaScript to handle sending messages in chat
function sendMessage() {
    var message = document.getElementById('chat-input').value;
    var chatbox = document.getElementById('chatbox');
    chatbox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    document.getElementById('chat-input').value = '';
}
