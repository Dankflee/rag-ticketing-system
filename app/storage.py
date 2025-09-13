import chromadb
from chromadb.utils import embedding_functions
import os
from app.schemas import Ticket
from typing import List, Optional

# Initialize ChromaDB client
client = chromadb.PersistentClient(path="./chroma_data")

embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# Create collections
tickets_collection = client.get_or_create_collection(
    name="tickets",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

knowledge_collection = client.get_or_create_collection(
    name="knowledge",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}
)

def sanitized_metadata(metadata):
    """Replace empty lists or unsupported types with strings or None"""
    new_meta = {}
    for k, v in metadata.items():
        if isinstance(v, list):
            if len(v) == 0:
                new_meta[k] = ""  # empty string instead of empty list
            else:
                new_meta[k] = ",".join(str(item) for item in v)  # join list items as comma-separated string
        elif isinstance(v, (str, int, float, bool)) or v is None:
            new_meta[k] = v if v is not None else ""
        else:
            new_meta[k] = str(v)
    return new_meta

def add_ticket(ticket: Ticket):
    """Add a ticket to ChromaDB"""
    doc_id = ticket.id
    text = f"{ticket.summary}\n{ticket.description}"
    metadata = ticket.model_dump()
    metadata = sanitized_metadata(metadata)  # Sanitize metadata for ChromaDB
    
    tickets_collection.add(
        ids=[doc_id], 
        documents=[text], 
        metadatas=[metadata]
    )

def search_tickets(query: str, k: int = 5, where: Optional[dict] = None) -> dict:
    """Search tickets in ChromaDB"""
    try:
        return tickets_collection.query(
            query_texts=[query], 
            n_results=k, 
            where=where or {}
        )
    except Exception as e:
        print(f"Search error: {e}")
        return {"ids": [[]], "documents": [[]], "metadatas": [[]]}

def get_all_tickets() -> List[Ticket]:
    """Get all tickets from ChromaDB"""
    try:
        results = tickets_collection.get()
        tickets = []
        if results["ids"]:
            for i, ticket_id in enumerate(results["ids"]):
                metadata = results["metadatas"][i]
                # Convert tags back to list if it's a string
                if "tags" in metadata and isinstance(metadata["tags"], str):
                    metadata["tags"] = metadata["tags"].split(",") if metadata["tags"] else []
                ticket = Ticket(**metadata)
                tickets.append(ticket)
        return tickets
    except Exception as e:
        print(f"Error getting tickets: {e}")
        return []

def add_knowledge(doc_id: str, text: str, metadata: dict):
    """Add knowledge document to ChromaDB"""
    metadata = sanitized_metadata(metadata)  # Sanitize metadata for ChromaDB
    knowledge_collection.add(
        ids=[doc_id], 
        documents=[text], 
        metadatas=[metadata]
    )

def search_knowledge(query: str, k: int = 5, where: Optional[dict] = None) -> dict:
    """Search knowledge in ChromaDB"""
    try:
        return knowledge_collection.query(
            query_texts=[query], 
            n_results=k, 
            where=where or {}
        )
    except Exception as e:
        print(f"Knowledge search error: {e}")
        return {"ids": [[]], "documents": [[]], "metadatas": [[]]}
