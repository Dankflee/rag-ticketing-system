from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime

class ChatRequest(BaseModel):
    message: str
    user_id: str = "default_user"
    org: str = "vidina"

class Ticket(BaseModel):
    id: str
    summary: str
    description: Optional[str] = ""
    assignee: Optional[str] = None
    org: str = "vidina"
    priority: str = "P2"
    due_date: Optional[str] = None
    tags: List[str] = []
    status: str = "open"
    created_by: str
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())

class ChatResponse(BaseModel):
    response: str
    ticket_id: Optional[str] = None
    intent: Optional[str] = None

class TicketListResponse(BaseModel):
    tickets: List[Ticket]
    total: int
