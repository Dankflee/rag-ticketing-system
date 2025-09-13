from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.schemas import ChatRequest, ChatResponse, TicketListResponse
from app.router import classify_intent, create_ticket_from_message
from app.rag import answer_ticket_query, answer_knowledge_query, answer_general_query
from app.notify import notify_assignment
from app.storage import get_all_tickets, add_knowledge
import os

app = FastAPI(title="RAG Ticketing System", version="1.0.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the frontend"""
    return FileResponse("frontend/index.html")

@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """Main chat endpoint"""
    try:
        intent = classify_intent(req.message)
        
        if intent == "ticket_create":
            ticket_id, ticket = create_ticket_from_message(
                req.message, req.user_id, req.org
            )
            notify_assignment(ticket)
            response = f"✅ Created ticket **{ticket_id}** for **{ticket.assignee or 'unassigned'}** at priority **{ticket.priority}**.\n\nSummary: {ticket.summary}"
            return ChatResponse(
                response=response,
                ticket_id=ticket_id,
                intent=intent
            )
        
        elif intent == "ticket_query":
            answer = answer_ticket_query(req.message)
            return ChatResponse(response=answer, intent=intent)
        
        elif intent == "knowledge_query":
            answer = answer_knowledge_query(req.message)
            return ChatResponse(response=answer, intent=intent)
        
        else:
            answer = answer_general_query(req.message)
            return ChatResponse(response=answer, intent=intent)
            
    except Exception as e:
        return ChatResponse(
            response=f"Sorry, I encountered an error: {str(e)}",
            intent="error"
        )

@app.get("/tickets", response_model=TicketListResponse)
async def get_tickets():
    """Get all tickets"""
    try:
        tickets = get_all_tickets()
        return TicketListResponse(tickets=tickets, total=len(tickets))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.on_event("startup")
async def startup_event():
    """Initialize some sample knowledge"""
    try:
        # Add some sample knowledge documents
        add_knowledge(
            "sop-001",
            "To reset the staging database: 1) Stop all services 2) Run migration scripts 3) Restart services 4) Verify functionality",
            {"source": "SOP Database Management", "type": "procedure"}
        )
        add_knowledge(
            "sop-002", 
            "For API key rotation: 1) Generate new keys 2) Update applications 3) Test connectivity 4) Revoke old keys after 24h",
            {"source": "SOP Security", "type": "procedure"}
        )
        print("Sample knowledge initialized")
    except Exception as e:
        print(f"Startup error: {e}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
