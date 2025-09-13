import httpx
import os
from app.schemas import Ticket

SLACK_WEBHOOK = os.getenv("SLACK_WEBHOOK")

def notify_assignment(ticket: Ticket):
    """Send notification about ticket assignment"""
    if not SLACK_WEBHOOK:
        print(f"Notification: New ticket {ticket.id} created for {ticket.assignee or 'unassigned'}")
        return
    
    try:
        text = f"""New ticket created!
ID: {ticket.id}
Summary: {ticket.summary}
Assignee: {ticket.assignee or 'Unassigned'}
Priority: {ticket.priority}
Due: {ticket.due_date or 'Not set'}"""
        
        httpx.post(SLACK_WEBHOOK, json={"text": text}, timeout=5.0)
    except Exception as e:
        print(f"Notification failed: {e}")
