class SimpleChatBot {
    constructor() {
        this.apiUrl = 'http://localhost:8000/chat';
        this.messageInput = document.getElementById('messageInput');
        this.sendButton = document.getElementById('sendButton');
        this.chatBox = document.getElementById('chatBox');
        
        this.initEventListeners();
    }

    initEventListeners() {
        // Send message on button click
        this.sendButton.addEventListener('click', (e) => {
            e.preventDefault();
            this.sendMessage();
        });
        
        // Send message on Enter key press
        this.messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.sendMessage();
            }
        });
        
        // Auto-focus input
        this.messageInput.focus();
    }

    async sendMessage() {
        const message = this.messageInput.value.trim();
        
        if (!message) return;
        
        // Disable input while processing
        this.sendButton.disabled = true;
        this.messageInput.disabled = true;
        
        // Add user message to chat
        this.addMessage(message, 'user');
        
        // Clear input
        this.messageInput.value = '';
        
        try {
            // Send request to backend
            const response = await fetch(this.apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message: message })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Add bot response to chat
            this.addMessage(data.message, 'bot');
            
        } catch (error) {
            console.error('Error:', error);
            
            // Show error message
            let errorMessage = 'Sorry, I encountered an error. ';
            
            if (error.message.includes('Failed to fetch')) {
                errorMessage += 'Please make sure the backend server is running.';
            } else {
                errorMessage += 'Please try again later.';
            }
            
            this.addMessage(errorMessage, 'bot');
            
        } finally {
            // Re-enable input
            this.sendButton.disabled = false;
            this.messageInput.disabled = false;
            this.messageInput.focus();
        }
    }

    addMessage(text, sender) {
        const itemDiv = document.createElement('div');
        itemDiv.className = sender === 'user' ? 'item right' : 'item';
        
        const iconDiv = document.createElement('div');
        iconDiv.className = 'icon';
        iconDiv.innerHTML = sender === 'user' ? '<i class="fa fa-user"></i>' : '<i class="fa fa-robot"></i>';
        
        const msgDiv = document.createElement('div');
        msgDiv.className = 'msg';
        
        const p = document.createElement('p');
        p.textContent = text;
        msgDiv.appendChild(p);
        
        itemDiv.appendChild(iconDiv);
        itemDiv.appendChild(msgDiv);
        
        // Add line break
        const br = document.createElement('br');
        br.setAttribute('clear', 'both');
        
        this.chatBox.appendChild(itemDiv);
        this.chatBox.appendChild(br);
        
        // Scroll to bottom
        this.chatBox.scrollTop = this.chatBox.scrollHeight;
    }
}

// Initialize the chatbot when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new SimpleChatBot();
});