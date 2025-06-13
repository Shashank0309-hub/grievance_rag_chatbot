// Generate a random session ID that persists until page refresh
const sessionId = 'session-' + Math.random().toString(36).substr(2, 9);

// DOM Elements
const chatMessages = document.getElementById('chat-messages');
const userInput = document.getElementById('user-input');
const sendButton = document.getElementById('send-button');
const typingIndicator = document.getElementById('typing-indicator');

// Function to add a message to the chat
function addMessage(content, isUser = false) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${isUser ? 'user-message' : 'bot-message'}`;
    messageDiv.textContent = content;
    
    // Remove typing indicator if it's a bot message
    if (!isUser && typingIndicator.style.display === 'flex') {
        typingIndicator.style.display = 'none';
    }
    
    chatMessages.insertBefore(messageDiv, typingIndicator);
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to show typing indicator
function showTypingIndicator() {
    typingIndicator.style.display = 'flex';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

// Function to hide typing indicator
function hideTypingIndicator() {
    typingIndicator.style.display = 'none';
}

// Function to send message to the API
async function sendMessage() {
    const message = userInput.value.trim();
    if (!message) return;
    
    // Add user message to chat
    addMessage(message, true);
    userInput.value = '';
    
    // Show typing indicator
    showTypingIndicator();
    
    try {
        // Encode the message and session ID for URL
        const encodedMessage = encodeURIComponent(message);
        const encodedSessionId = encodeURIComponent(sessionId);
        
        // Make the GET request with query parameters
        const response = await fetch(`/v1/customer/chat?query=${encodedMessage}&session_id=${encodedSessionId}`, {
            method: 'GET',
            headers: {
                'Accept': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }
        
        const data = await response.json();
        
        // Add bot response to chat
        if (data.response) {
            addMessage(data.response);
        } else {
            addMessage("I'm sorry, I couldn't process your request.");
        }
    } catch (error) {
        console.error('Error:', error);
        addMessage("Sorry, there was an error processing your message. Please try again.");
    } finally {
        hideTypingIndicator();
    }
}

// Event Listeners
sendButton.addEventListener('click', sendMessage);

userInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        sendMessage();
    }
});

// Initial welcome message
setTimeout(() => {
    addMessage("Hi! I am your Grievance AI Chatbot. How can I assist you today?");
}, 500);