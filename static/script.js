let ws = new WebSocket("ws://localhost:8001/ws");
let chatBox = document.getElementById("chatBox");
let input = document.getElementById("messageInput");

ws.onmessage = function(event) {
    let messageElement = document.createElement("div");
    messageElement.classList.add("chat-message", "bot-message");
    messageElement.textContent = "Bot: " + event.data;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;
};

function sendMessage() {
    if (input.value.trim() === "") return;

    let userMessage = document.createElement("div");
    userMessage.classList.add("chat-message", "user-message");
    userMessage.textContent = "You: " + input.value;
    chatBox.appendChild(userMessage);
    chatBox.scrollTop = chatBox.scrollHeight;

    ws.send(input.value);
    input.value = '';
}

// Allow Enter key to send messages
input.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        event.preventDefault();
        sendMessage();
    }
});
