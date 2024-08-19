document.getElementById('send-button').addEventListener('click', postDB);

function postDB() {
    // URLを取得
    let url = new URL(window.location.href);
    // URLSearchParamsオブジェクトを取得
    let params = url.searchParams;
    const id = params.get('id')

    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    if (message.length == 0) {
        alert("メッセージを入力してください")
        return 0
    }

    fetch('/send_message', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            id: id,
            FromUser: false
        })
    })
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.error(data.error);
            } else {
                updateChatBox(data.messages);
                messageInput.value = '';  // メッセージ送信後に入力フィールドをクリア
            }
        })
        .catch(error => console.error('Error:', error));
}

function updateChatBox(messages) {
    const chatBox = document.getElementById('chat-box');
    chatBox.innerHTML = '';  // チャットボックスをクリア
    messages.forEach(message => {
        const messageElement = document.createElement('div');
        messageElement.classList.add("From_user_" + message[1]);
        messageElement.textContent = message[0];
        chatBox.appendChild(messageElement);
    });
}

function fetchMessages() {
    // URLを取得
    let url = new URL(window.location.href);
    // URLSearchParamsオブジェクトを取得
    let params = url.searchParams;
    const id = params.get('id')
    const messageInput = document.getElementById('message-input');
    const message = messageInput.value;
    fetch('/get_messages', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            message: message,
            id: id,
            FromUser: false
        })
    })
        .then(response => response.json())
        .then(data => {
            updateChatBox(data.messages);
        })
        .catch(error => console.error('Error:', error));
}

// 定期的にメッセージを取得して表示を更新
// setInterval(fetchMessages, 3000);

// 初期メッセージの取得
fetchMessages();

var socket = io();

socket.on('message', function (msg) {
    var messages = document.getElementById('chat-box');
    var message = document.createElement('div');
    message.classList.add('From_user_true');
    message.textContent = msg;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;
});

function sendMessage() {
    var input = document.getElementById('message-input');
    var msg = input.value;
    if (msg.trim() === '') return;

    // Add self message
    var messages = document.getElementById('chat-box');
    var message = document.createElement('div');
    message.classList.add('From_user_false');
    message.textContent = msg;
    messages.appendChild(message);
    messages.scrollTop = messages.scrollHeight;

    // Send message to server
    socket.emit('message', msg); // 修正: socket.sendからsocket.emitに変更
    // input.value = '';
}