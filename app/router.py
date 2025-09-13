import re
import uuid
import json
from typing import Tuple
from app.storage import add_ticket, search_tickets, search_knowledge
from app.schemas import Ticket
from datetime import datetime, timedelta
import random

# Simple LLM simulation (replace with actual LLM)
def llm(prompt: str) -> str:
    """Simulated LLM response - replace with actual LLM call"""
    if "classify" in prompt.lower():
        # Simple keyword-based classification
        message = prompt.split("Message:")[-1].strip().lower()
        if any(word in message for word in ["create", "ticket", "assign"]):
            return "ticket_create"
        elif any(word in message for word in ["show", "list", "find", "search"]):
            return "ticket_query"
        elif any(word in message for word in ["help", "how", "what", "sop"]):
            return "knowledge_query"
        else:
            return "chit_chat"
    
    elif "extract json" in prompt.lower():
        # Simple field extraction simulation
        message = prompt.split("Message:")[-1].strip()
        
        # Extract assignee
        assignee = None
        for word in message.split():
            if word.lower() in ["priya", "john", "sarah", "mike", "vidina"]:
                assignee = word.capitalize()
                break
        
        # Extract priority
        priority = "P2"
        if "p0" in message.lower() or "urgent" in message.lower():
            priority = "P0"
        elif "p1" in message.lower() or "high" in message.lower():
            priority = "P1"
        elif "p3" in message.lower() or "low" in message.lower():
            priority = "P3"
        
        # Extract due date
        due_date = None
        if "tonight" in message.lower():
            due_date = (datetime.now() + timedelta(hours=8)).isoformat()
        elif "tomorrow" in message.lower():
            due_date = (datetime.now() + timedelta(days=1)).isoformat()
        elif "monday" in message.lower():
            due_date = (datetime.now() + timedelta(days=7)).isoformat()
        
        # Extract summary (first part of message)
        summary = message.split(":")[1] if ":" in message else message
        summary = summary.strip()[:100]
        
        result = {
            "summary": summary,
            "description": "",
            "assignee": assignee,
            "org": "vidina",
            "priority": priority,
            "due_date": due_date,
            "tags": []
        }
        
        return json.dumps(result)
    
    return "I'm a simulated LLM response."

def classify_intent(message: str) -> str:
    """Classify user intent"""
    prompt = f"""Classify the user message into one of:
    - ticket_create
    - ticket_update  
    - ticket_query
    - knowledge_query
    - chit_chat
    Return only the label.
    Message: {message}"""
    return llm(prompt).strip()

def extract_ticket_fields(message: str) -> dict:
    """Extract ticket fields from message"""
    prompt = f"""Extract JSON with fields:
    summary, description, assignee, org, priority (P0-P3), due_date (ISO8601 or null), tags (array).
    If not present, leave null or sensible default (priority=P2).
    Message: {message}"""
    try:
        txt = llm(prompt)
        return json.loads(txt)
    except:
        # Fallback parsing
        return {
            "summary": message[:100],
            "description": "",
            "assignee": None,
            "org": "vidina",
            "priority": "P2",
            "due_date": None,
            "tags": []
        }

def create_ticket_from_message(message: str, user_id: str, org: str = "vidina") -> Tuple[str, Ticket]:
    """Create ticket from natural language message"""
    fields = extract_ticket_fields(message)
    ticket = Ticket(
        id=f"ticket-{uuid.uuid4().hex[:8]}",
        summary=fields.get("summary") or message[:140],
        description=fields.get("description") or "",
        assignee=fields.get("assignee"),
        org=fields.get("org") or org,
        priority=fields.get("priority") or "P2",
        due_date=fields.get("due_date"),
        tags=fields.get("tags") or [],
        created_by=user_id
    )
    add_ticket(ticket)
    return ticket.id, ticket
