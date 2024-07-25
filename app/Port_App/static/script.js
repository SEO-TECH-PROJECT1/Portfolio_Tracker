function sendMessage() {
    const message = document.getElementById('userMessage').value;
    const chatlogs = document.getElementById('chatlogs');
    const userMessageElement = document.createElement('div');
    userMessageElement.textContent = 'You: ' + message;
    chatlogs.appendChild(userMessageElement);

    fetch('/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: new URLSearchParams({'message': message})
    })
    .then(response => response.json())
    .then(data => {
        const botMessageElement = document.createElement('div');
        botMessageElement.textContent = 'Bot: ' + data.response;
        chatlogs.appendChild(botMessageElement);
        document.getElementById('userMessage').value = '';
        chatlogs.scrollTop = chatlogs.scrollHeight;
    });
}

document.getElementById('minimize-btn').addEventListener('click', function() {
    const chatbox = document.getElementById('chatbox');
    const chatTitle = document.getElementById('chat-title');
    if (chatbox.classList.contains('minimized')) {
        chatbox.classList.remove('minimized');
        chatTitle.style.display = 'block';
        this.style.display = 'none';
    } else {
        chatbox.classList.add('minimized');
        chatTitle.style.display = 'none';
        this.style.display = 'flex';
    }
});
