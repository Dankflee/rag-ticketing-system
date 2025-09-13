class TicketingApp {
    constructor() {
        this.apiBase = '';
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadTickets();
        this.focusInput();
    }

    bindEvents() {
        const sendButton = document.getElementById('sendButton');
        const messageInput = document.getElementById('messageInput');
        const refreshButton = document.getElementById('refreshTickets');

        sendButton.addEventListener('click', () => this.sendMessage());
        messageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
        refreshButton.addEventListener('click', () => this.loadTickets());
    }

    focusInput() {
        document.getElementById('messageInput').focus();
    }

    async sendMessage() {
        const messageInput = document.getElementById('messageInput');
        const sendButton = document.getElementById('sendButton');
        const message = messageInput.value.trim();

        if (!message) return;

        // Disable input while processing
        messageInput.disabled = true;
        sendButton.disabled = true;
        this.setStatus('Processing...');

        // Add user message to chat
        this.addMessage(message, 'user');
        messageInput.value = '';

        try {
            const response = await fetch('/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    user_id: 'frontend_user',
                    org: 'vidina'
                })
            });

            const data = await response.json();
            
            if (response.ok) {
                this.addMessage(data.response, 'bot');
                
                // If a ticket was created, refresh the tickets list
                if (data.ticket_id) {
                    setTimeout(() => this.loadTickets(), 500);
                }
                
                this.setStatus('Ready');
            } else {
                throw new Error(data.detail || 'Request failed');
            }
        } catch (error) {
            console.error('Error:', error);
            this.addMessage(`Sorry, there was an error: ${error.message}`, 'bot');
            this.setStatus('Error');
        } finally {
            // Re-enable input
            messageInput.disabled = false;
            sendButton.disabled = false;
            messageInput.focus();
        }
    }

    addMessage(content, sender) {
        const chatMessages = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (sender === 'bot') {
            // Convert markdown-style formatting to HTML
            content = content
                .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
                .replace(/\*(.*?)\*/g, '<em>$1</em>')
                .replace(/\n/g, '<br>');
            contentDiv.innerHTML = `<strong>Assistant:</strong> ${content}`;
        } else {
            contentDiv.innerHTML = `<strong>You:</strong> ${content}`;
        }
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        
        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    async loadTickets() {
        const container = document.getElementById('ticketsContainer');
        container.innerHTML = '<div class="loading">Loading tickets...</div>';

        try {
            const response = await fetch('/tickets');
            const data = await response.json();

            if (response.ok) {
                this.renderTickets(data.tickets);
            } else {
                throw new Error(data.detail || 'Failed to load tickets');
            }
        } catch (error) {
            console.error('Error loading tickets:', error);
            container.innerHTML = `<div class="error">Error loading tickets: ${error.message}</div>`;
        }
    }

    renderTickets(tickets) {
        const container = document.getElementById('ticketsContainer');
        
        if (!tickets || tickets.length === 0) {
            container.innerHTML = '<div class="no-tickets">No tickets found. Create one by chatting!</div>';
            return;
        }

        // Sort tickets by creation date (newest first)
        tickets.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));

        const ticketsHtml = tickets.map(ticket => this.renderTicket(ticket)).join('');
        container.innerHTML = ticketsHtml;
    }

    renderTicket(ticket) {
        const createdDate = new Date(ticket.created_at).toLocaleDateString();
        const dueDate = ticket.due_date 
            ? new Date(ticket.due_date).toLocaleDateString()
            : 'Not set';

        return `
            <div class="ticket-item priority-${ticket.priority}">
                <div class="ticket-header">
                    <span class="ticket-id">${ticket.id}</span>
                    <span class="ticket-priority ${ticket.priority}">${ticket.priority}</span>
                </div>
                <div class="ticket-summary">${ticket.summary}</div>
                <div class="ticket-meta">
                    <div><span class="ticket-assignee">Assignee:</span> ${ticket.assignee || 'Unassigned'}</div>
                    <div>Status: ${ticket.status}</div>
                    <div>Created: ${createdDate}</div>
                    <div>Due: ${dueDate}</div>
                    <div>Tags: ${ticket.tags.length > 0 ? ticket.tags.join(', ') : 'None'}</div>
                </div>
            </div>
        `;
    }

    setStatus(status) {
        document.getElementById('status').textContent = status;
    }
}

// Initialize the app when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new TicketingApp();
});
