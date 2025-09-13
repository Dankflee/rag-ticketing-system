RAG-based Ticketing System with ChromaDB
A complete Retrieval-Augmented Generation (RAG) ticketing and chat system that enables natural language ticket creation, semantic search, and knowledge query capabilities. Built with FastAPI, ChromaDB, and a responsive web frontend.

🚀 Features
Natural Language Processing: Create tickets with simple sentences like "Create a P1 ticket for John: fix the database bug"

Semantic Search: Search tickets and knowledge using vector embeddings powered by ChromaDB

RAG-powered Q&A: Ask questions about tickets and organizational knowledge with contextual responses

Real-time Chat Interface: Modern web UI with instant responses and ticket display

Automatic Field Extraction: Smart extraction of assignee, priority, due dates, and tags from natural language

Slack Integration: Optional notifications for ticket assignments

Docker Ready: Easy deployment with docker-compose

🏗️ System Architecture
![System Architecture](/ticketing-1.svg)

🔄 Query Processing Flow
text
![System Architecture](/ticketing-2.svg)

🛠️ Technology Stack
Backend: FastAPI, Python 3.11+

Vector Database: ChromaDB with persistent storage

Embeddings: SentenceTransformers (all-MiniLM-L6-v2)

Frontend: Vanilla HTML/CSS/JavaScript

Containerization: Docker & Docker Compose

Notifications: Slack Webhook (optional)

🚦 Quick Start
Prerequisites
Python 3.11+

Git

Installation & Setup
bash
# Clone the repository
git clone https://github.com/yourusername/rag-ticketing-system.git
cd rag-ticketing-system

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
Docker Deployment (Recommended)
bash
# Build and run with Docker Compose
docker-compose up --build

# Or run in detached mode
docker-compose up -d
Access the Application
Open your browser and navigate to: http://localhost:8000

📁 Project Structure
text
![System Architecture](/ticketing-3.svg)
💬 Usage Examples
Creating Tickets
text
"Create a P1 ticket for John: fix login bug due tomorrow"
"Assign a high priority task to Sarah: update the API documentation"
"New ticket for Vidina org: server maintenance this weekend"
Querying Tickets
text
"Show me all P1 tickets"
"List tickets assigned to John"
"Find all open tickets due this week"
"What tickets are assigned to the Vidina org?"
Knowledge Queries
text
"How do I reset the staging database?"
"What's the procedure for API key rotation?"
"Show me the SOP for server maintenance"
⚙️ Configuration
Environment Variables
Create a .env file in the project root:

bash
# Slack webhook for notifications (optional)
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL

# Additional configuration can be added here
Customizing the LLM
Replace the simulated LLM in app/router.py with your preferred provider:

python
# OpenAI Example
import openai

def llm(prompt: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=150
    )
    return response.choices[0].message.content
🔧 API Endpoints
Endpoint	Method	Description
/	GET	Serve frontend interface
/chat	POST	Main chat endpoint for all interactions
/tickets	GET	Retrieve all tickets
/static/*	GET	Serve static frontend assets
🐳 Docker Configuration
The project includes Docker support with multi-stage builds:

Development: Use docker-compose up for hot-reload development

Production: Built image includes all dependencies and optimizations

Persistence: ChromaDB data is stored in Docker volumes

🤝 Contributing
Fork the repository

Create a feature branch: git checkout -b feature-name

Make your changes and add tests

Commit your changes: git commit -am 'Add feature'

Push to the branch: git push origin feature-name

Submit a pull request

🔮 Future Enhancements
 User authentication and role-based access

 Integration with external ticketing systems (Jira, Linear)

 Advanced analytics and reporting dashboard

 Multi-tenant support

 Mobile app development

 Voice interface integration

📝 License
This project is licensed under the MIT License - see the LICENSE file for details.

🆘 Troubleshooting
Common Issues
NumPy Compatibility Error: Install compatible versions:

bash
pip install "numpy<2.0.0"
ChromaDB Metadata Error: Ensure all list fields are converted to strings in storage.py

Port Already in Use: Change the port in the uvicorn command:

bash
uvicorn app.main:app --port 8001
📞 Support
For questions, issues, or contributions:

Open an issue on GitHub

Check the troubleshooting section

Review the code comments for implementation details

Built with ❤️ using RAG technology and modern web standards