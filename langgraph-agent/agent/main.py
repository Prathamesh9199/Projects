"""
agent.py - Modular Human-in-the-Loop LangGraph Agent
"""
import os
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

# ===========================================================
# Setup
# ===========================================================
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


# ===========================================================
# Agent State
# ===========================================================
class AgentState(BaseModel):
    question: str
    context: str = ""
    clarify_questions: List[str] = []
    clarify_answers: List[str] = []
    final_answer: Optional[str] = None


# ===========================================================
# Node Functions
# ===========================================================
def retrieve_context_node(state: AgentState):
    """Retrieve context based on question and clarifications"""
    print("🧠 Retrieving context (RAG simulation)...")

    base_context = (
        "The Eiffel Tower is a famous landmark located in Paris, France. "
        "It attracts millions of tourists each year."
    )

    if state.clarify_answers:
        print("➕ Incorporating human clarification into context...")
        base_context += "\nAdditional clarification: " + " ".join(state.clarify_answers)

    return {"context": base_context}


def analyze_context_node(state: AgentState):
    """Analyze if context is sufficient to answer the question"""
    print("🔍 Analyzing context sufficiency...")

    clarify_needed = []
    if "1889" not in state.context:
        clarify_needed.append(
            "Could you clarify what specific information you want (e.g., year, designer, or purpose)?"
        )

    if clarify_needed:
        print("⚠️ Context insufficient → asking for clarification.")
    else:
        print("✅ Context sufficient → ready to generate answer.")

    return {"clarify_questions": clarify_needed}


def clarify_node(state: AgentState) -> Command:
    """Handle human-in-the-loop clarification"""
    if len(state.clarify_questions) > 0:
        question_to_user = state.clarify_questions[0]
        human_input = interrupt({
            "type": "clarification_request",
            "message": question_to_user,
        })

        return Command(
            update={"clarify_answers": [human_input["clarification"]]},
            goto="retrieve_context",
        )

    return Command(goto="generate_answer")


def generate_answer_node(state: AgentState):
    """Generate final answer based on context"""
    print("💬 Generating final answer...")
    
    if "1889" in state.context or "year" in " ".join(state.clarify_answers):
        answer = (
            "The Eiffel Tower was completed in 1889 in Paris, France. "
            "It stands as a global icon of French architecture."
        )
    else:
        answer = (
            "The Eiffel Tower is located in Paris, France, "
            "and is one of the most recognizable structures in the world."
        )
    
    return {"final_answer": answer}


# ===========================================================
# Graph Builder
# ===========================================================
def build_graph():
    """Build and compile the LangGraph workflow"""
    graph = StateGraph(AgentState)

    # Add nodes
    graph.add_node("retrieve_context", retrieve_context_node)
    graph.add_node("analyze_context", analyze_context_node)
    graph.add_node("clarify", clarify_node)
    graph.add_node("generate_answer", generate_answer_node)

    # Add edges
    graph.add_edge(START, "retrieve_context")
    graph.add_edge("retrieve_context", "analyze_context")

    graph.add_conditional_edges(
        "analyze_context",
        lambda state: "clarify" if len(state.clarify_questions) > 0 else "generate_answer",
        {
            "clarify": "clarify",
            "generate_answer": "generate_answer",
        },
    )

    graph.add_edge("generate_answer", END)

    # Compile with checkpointer
    checkpointer = MemorySaver()
    return graph.compile(checkpointer=checkpointer)


# ===========================================================
# Agent Class
# ===========================================================
class HITLAgent:
    """Human-in-the-Loop Agent wrapper"""
    
    def __init__(self):
        self.graph = build_graph()
    
    def start_conversation(self, question: str, thread_id: str = "default") -> Dict[str, Any]:
        """
        Start a new conversation with the agent
        
        Args:
            question: The user's question
            thread_id: Unique identifier for this conversation thread
            
        Returns:
            Dictionary containing the result or interrupt information
        """
        config = {"configurable": {"thread_id": thread_id}}
        inputs = AgentState(question=question)
        
        result = self.graph.invoke(inputs, config=config)
        
        # Check if we need clarification
        if "__interrupt__" in result:
            interrupt_data = result["__interrupt__"][0].value
            return {
                "status": "awaiting_clarification",
                "message": interrupt_data["message"],
                "thread_id": thread_id,
                "state": result
            }
        
        return {
            "status": "completed",
            "final_answer": result.get("final_answer"),
            "thread_id": thread_id,
            "state": result
        }
    
    def continue_conversation(
        self, 
        clarification: str, 
        thread_id: str = "default"
    ) -> Dict[str, Any]:
        """
        Continue a conversation after providing clarification
        
        Args:
            clarification: User's clarification response
            thread_id: The thread ID from the previous interaction
            
        Returns:
            Dictionary containing the final result
        """
        config = {"configurable": {"thread_id": thread_id}}
        human_reply = {"clarification": clarification}
        
        result = self.graph.invoke(
            Command(resume=human_reply),
            config=config
        )
        
        return {
            "status": "completed",
            "final_answer": result.get("final_answer"),
            "thread_id": thread_id,
            "state": result
        }


# ===========================================================
# CLI Interface (for testing)
# ===========================================================
def run_cli():
    """Run the agent in CLI mode"""
    print("🚀 Starting Human-in-the-Loop LangGraph Agent\n")
    
    agent = HITLAgent()
    question = input("❓ Enter your question: ")
    
    # Start conversation
    result = agent.start_conversation(question, thread_id="cli-session")
    
    # Handle clarification if needed
    if result["status"] == "awaiting_clarification":
        print(f"\n🤖 Agent: {result['message']}")
        user_input = input("\n👤 Your response: ")
        
        # Continue with clarification
        result = agent.continue_conversation(user_input, thread_id="cli-session")
    
    # Display final answer
    print("\n✅ Final Answer:")
    print(result["final_answer"])
    print("\n📊 Full State:")
    print(result["state"])


if __name__ == "__main__":
    run_cli()