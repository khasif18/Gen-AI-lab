const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const suggestedQuestions = document.getElementById('suggested-questions');

let conversationHistory = [];
let isWaiting = false;

// Format response nicely (bolding and lists)
function formatResponse(text) {
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
    formattedText = formattedText.replace(/\n\s*-\s/g, '<br>• ');
    formattedText = formattedText.replace(/\n\d\.\s/g, (match) => `<br>${match.trim()} `);
    formattedText = formattedText.replace(/\n/g, '<br>');
    return formattedText;
}

function scrollToBottom() {
    chatBox.scrollTop = chatBox.scrollHeight;
}

function appendMessage(sender, text, isError = false) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message');
    
    if (sender === 'user') {
        msgDiv.classList.add('user-message');
    } else {
        msgDiv.classList.add('assistant-message');
        if (isError) {
            msgDiv.classList.add('message-error');
        }
    }
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    
    if (sender === 'assistant' && !isError) {
        contentDiv.innerHTML = formatResponse(text);
    } else {
        contentDiv.textContent = text;
    }
    
    msgDiv.appendChild(contentDiv);
    chatBox.appendChild(msgDiv);
    scrollToBottom();
}

function appendLoadingIndicator() {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', 'assistant-message');
    msgDiv.id = 'loading-indicator';
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content', 'loading');
    contentDiv.innerHTML = '<span></span><span></span><span></span>';
    
    msgDiv.appendChild(contentDiv);
    chatBox.appendChild(msgDiv);
    scrollToBottom();
}

function removeLoadingIndicator() {
    const loading = document.getElementById('loading-indicator');
    if (loading) {
        loading.remove();
    }
}

async function sendMessage(message) {
    if (!message || isWaiting) return;
    
    // UI Update
    isWaiting = true;
    userInput.value = '';
    userInput.disabled = true;
    sendBtn.disabled = true;
    
    // Add user message to UI and history
    appendMessage('user', message);
    conversationHistory.push({"role": "user", "content": message});
    
    appendLoadingIndicator();
    
    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                history: conversationHistory.slice(-5) // Send last 5 messages for context
            })
        });
        
        const data = await response.json();
        removeLoadingIndicator();
        
        if (response.ok) {
            appendMessage('assistant', data.response);
            conversationHistory.push({"role": "assistant", "content": data.response});
        } else {
            appendMessage('assistant', `Error: ${data.error}`, true);
            // Remove the failed user message from history
            conversationHistory.pop(); 
        }
    } catch (error) {
        removeLoadingIndicator();
        appendMessage('assistant', `Network Error: Unable to reach the server.`, true);
        conversationHistory.pop();
    } finally {
        isWaiting = false;
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
    }
}

// Handle send button click
sendBtn.addEventListener('click', () => {
    const msg = userInput.value.trim();
    if (msg) sendMessage(msg);
});

// Handle enter key press
userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const msg = userInput.value.trim();
        if (msg) sendMessage(msg);
    }
});

// Exposed globally for suggested buttons in HTML
window.sendSuggested = function(msg) {
    sendMessage(msg);
    // Hide suggested questions after first interaction to free up space
    if (suggestedQuestions.style.display !== 'none') {
        // suggestedQuestions.style.display = 'none'; // Optional: hide after first use
    }
};

// Initial focus
userInput.focus();
