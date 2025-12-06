"""
api.py - FastAPI endpoints for the Human-in-the-Loop Agent

Save this file as: api.py
Run with: python api.py
Or: uvicorn api:app --reload
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid

# Import the agent from agent.py
from main import HITLAgent

# ===========================================================
# FastAPI App Setup
# ===========================================================
app = FastAPI(
    title="Human-in-the-Loop Agent API",
    description="API for interacting with a LangGraph agent that supports human clarifications",
    version="1.0.0"
)

# Add CORS middleware (for frontend integration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent
agent = HITLAgent()

# ===========================================================
# Request/Response Models
# ===========================================================
class QuestionRequest(BaseModel):
    """Request model for asking questions"""
    question: str
    thread_id: Optional[str] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "When was the Eiffel Tower built?",
                "thread_id": "user-123-session-1"
            }
        }


class ClarificationRequest(BaseModel):
    """Request model for providing clarifications"""
    clarification: str
    thread_id: str
    
    class Config:
        json_schema_extra = {
            "example": {
                "clarification": "I'm asking about the year it was built",
                "thread_id": "user-123-session-1"
            }
        }


class AgentResponse(BaseModel):
    """Response model for agent interactions"""
    status: str
    message: Optional[str] = None
    final_answer: Optional[str] = None
    thread_id: str


# ===========================================================
# API Endpoints
# ===========================================================
@app.get("/")
async def root():
    """Root endpoint - API information"""
    return {
        "status": "online",
        "service": "Human-in-the-Loop Agent API",
        "version": "1.0.0",
        "endpoints": {
            "GET /": "API information",
            "GET /health": "Health check",
            "GET /docs": "Interactive API documentation",
            "POST /ask": "Start a new conversation",
            "POST /clarify": "Provide clarification to continue conversation"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "Human-in-the-Loop Agent",
        "graph_initialized": agent.graph is not None
    }


@app.post("/ask", response_model=AgentResponse)
async def ask_question(request: QuestionRequest):
    """
    Start a new conversation with the agent
    
    **Parameters:**
    - **question**: The question to ask the agent
    - **thread_id**: Optional unique identifier for this conversation (auto-generated if not provided)
    
    **Returns:**
    - If the agent needs clarification: status="awaiting_clarification" with a message
    - If the agent has an answer: status="completed" with final_answer
    
    **Example:**
    ```json
    {
        "question": "When was the Eiffel Tower built?",
        "thread_id": "session-123"
    }
    ```
    """
    try:
        # Generate thread_id if not provided
        thread_id = request.thread_id or f"thread-{uuid.uuid4()}"
        
        print(f"\n📥 New question received")
        print(f"   Question: {request.question}")
        print(f"   Thread ID: {thread_id}")
        
        # Start conversation
        result = agent.start_conversation(request.question, thread_id)
        
        print(f"   Status: {result['status']}")
        
        return AgentResponse(
            status=result["status"],
            message=result.get("message"),
            final_answer=result.get("final_answer"),
            thread_id=result["thread_id"]
        )
    
    except Exception as e:
        print(f"❌ Error in /ask: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/clarify", response_model=AgentResponse)
async def provide_clarification(request: ClarificationRequest):
    """
    Provide clarification to continue an existing conversation
    
    **Parameters:**
    - **clarification**: Your clarification response
    - **thread_id**: The thread_id from the previous /ask request
    
    **Returns:**
    - The final answer after processing your clarification
    
    **Example:**
    ```json
    {
        "clarification": "I want to know the year it was built",
        "thread_id": "session-123"
    }
    ```
    """
    try:
        print(f"\n📥 Clarification received")
        print(f"   Clarification: {request.clarification}")
        print(f"   Thread ID: {request.thread_id}")
        
        # Continue conversation with clarification
        result = agent.continue_conversation(
            request.clarification,
            request.thread_id
        )
        
        print(f"   Status: {result['status']}")
        
        return AgentResponse(
            status=result["status"],
            message=result.get("message"),
            final_answer=result.get("final_answer"),
            thread_id=result["thread_id"]
        )
    
    except Exception as e:
        print(f"❌ Error in /clarify: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ===========================================================
# Run Server
# ===========================================================
if __name__ == "__main__":
    import uvicorn
    
    print("=" * 70)
    print("🚀 Starting Human-in-the-Loop Agent API Server")
    print("=" * 70)
    print("\n📍 Server will be available at:")
    print("   • http://localhost:8000")
    print("   • http://localhost:8000/docs (Interactive API docs)")
    print("\n🔗 Endpoints:")
    print("   • GET  /health")
    print("   • POST /ask")
    print("   • POST /clarify")
    print("\n" + "=" * 70 + "\n")
    
    uvicorn.run(
        app, 
        host="0.0.0.0", 
        port=8000,
        log_level="info"
    )