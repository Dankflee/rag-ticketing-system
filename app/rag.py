from app.storage import search_tickets, search_knowledge

def answer_ticket_query(message: str) -> str:
    """Answer queries about tickets using RAG"""
    res = search_tickets(message, k=5)
    
    if not res["ids"][0]:
        return "No tickets found matching your query."
    
    context = []
    for i in range(len(res["ids"])):
        md = res["metadatas"][i]
        doc = res["documents"][i]
        context.append(
            f"- Ticket {md['id']} [{md['status']} {md['priority']} assignee:{md.get('assignee', 'unassigned')}]: {doc}"
        )
    
    # Simple response generation (replace with actual LLM)
    response = f"Found {len(context)} relevant tickets:\n\n" + "\n".join(context)
    return response

def answer_knowledge_query(message: str) -> str:
    """Answer knowledge queries using RAG"""
    res = search_knowledge(message, k=5)
    
    if not res["ids"]:
        return "No knowledge documents found. Try asking about ticket management or general help."
    
    context = []
    for i in range(len(res["ids"])):
        md = res["metadatas"][i] 
        doc = res["documents"][i]
        context.append(f"- {md.get('source', 'Document')}: {doc}")
    
    response = f"Here's what I found:\n\n" + "\n".join(context)
    return response

def answer_general_query(message: str) -> str:
    """Handle general queries"""
    help_text = """I can help you with:

1. **Create tickets**: "Create a ticket for John: fix the login bug, priority P1"
2. **Search tickets**: "Show me all P1 tickets" or "Find tickets assigned to Sarah"
3. **General help**: Ask about procedures, SOPs, or how things work

Try asking me something!"""
    
    return help_text
