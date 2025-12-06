"""
test_api.py - Interactive API Testing Script
"""
import requests
import json
from typing import Optional

BASE_URL = "http://localhost:8000"

class APITester:
    """Interactive tester for the HITL Agent API"""
    
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.current_thread_id: Optional[str] = None
    
    def print_separator(self, title: str = ""):
        """Print a nice separator"""
        if title:
            print(f"\n{'=' * 60}")
            print(f"  {title}")
            print('=' * 60)
        else:
            print('=' * 60)
    
    def test_health(self):
        """Test health check endpoint"""
        self.print_separator("Health Check")
        try:
            response = requests.get(f"{self.base_url}/health")
            print(f"✅ Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
            return True
        except Exception as e:
            print(f"❌ Error: {e}")
            return False
    
    def ask_question(self, question: str, thread_id: Optional[str] = None):
        """Ask a question to the agent"""
        self.print_separator("Asking Question")
        
        data = {"question": question}
        if thread_id:
            data["thread_id"] = thread_id
        
        print(f"❓ Question: {question}")
        if thread_id:
            print(f"🔗 Thread ID: {thread_id}")
        
        try:
            response = requests.post(f"{self.base_url}/ask", json=data)
            result = response.json()
            
            self.current_thread_id = result.get("thread_id")
            
            print(f"\n📊 Status: {result['status']}")
            print(f"🔗 Thread ID: {result['thread_id']}")
            
            if result["status"] == "awaiting_clarification":
                print(f"\n🤖 Agent needs clarification:")
                print(f"   {result['message']}")
                return "awaiting_clarification", result
            else:
                print(f"\n✅ Final Answer:")
                print(f"   {result['final_answer']}")
                return "completed", result
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return "error", None
    
    def provide_clarification(self, clarification: str, thread_id: Optional[str] = None):
        """Provide clarification to continue conversation"""
        self.print_separator("Providing Clarification")
        
        thread_id = thread_id or self.current_thread_id
        
        if not thread_id:
            print("❌ Error: No thread_id available. Ask a question first.")
            return "error", None
        
        data = {
            "clarification": clarification,
            "thread_id": thread_id
        }
        
        print(f"👤 Your clarification: {clarification}")
        print(f"🔗 Thread ID: {thread_id}")
        
        try:
            response = requests.post(f"{self.base_url}/clarify", json=data)
            result = response.json()
            
            print(f"\n📊 Status: {result['status']}")
            
            if result["status"] == "completed":
                print(f"\n✅ Final Answer:")
                print(f"   {result['final_answer']}")
            
            return result["status"], result
                
        except Exception as e:
            print(f"❌ Error: {e}")
            return "error", None
    
    def interactive_conversation(self):
        """Run an interactive conversation"""
        self.print_separator("Interactive Conversation Mode")
        
        question = input("\n❓ Enter your question: ").strip()
        if not question:
            print("❌ No question provided.")
            return
        
        # Ask the question
        status, result = self.ask_question(question)
        
        # Handle clarification if needed
        if status == "awaiting_clarification":
            clarification = input("\n👤 Your clarification: ").strip()
            if clarification:
                self.provide_clarification(clarification)
            else:
                print("❌ No clarification provided.")
    
    def run_automated_tests(self):
        """Run automated test suite"""
        self.print_separator("Automated Test Suite")
        
        # Test 1: Health check
        print("\n1️⃣ Testing health endpoint...")
        if not self.test_health():
            print("❌ Health check failed. Make sure the server is running.")
            return
        
        # Test 2: Question with clarification needed
        print("\n\n2️⃣ Testing question that needs clarification...")
        status, result = self.ask_question(
            "When was the Eiffel Tower built?",
            thread_id="test-session-001"
        )
        
        if status == "awaiting_clarification":
            print("\n   Providing clarification...")
            self.provide_clarification(
                "I'm asking about the year it was built (1889)",
                thread_id="test-session-001"
            )
        
        # Test 3: Auto thread_id generation
        print("\n\n3️⃣ Testing auto thread_id generation...")
        self.ask_question("Tell me about the Eiffel Tower")
        
        # Test 4: Multiple concurrent threads
        print("\n\n4️⃣ Testing multiple concurrent threads...")
        self.ask_question("What is the Eiffel Tower?", thread_id="session-A")
        self.ask_question("When was the Eiffel Tower built?", thread_id="session-B")
        
        self.print_separator("All Tests Completed! ✅")


def show_menu():
    """Display interactive menu"""
    print("\n" + "=" * 60)
    print("  Human-in-the-Loop Agent API Tester")
    print("=" * 60)
    print("\nChoose an option:")
    print("  1. Run automated tests")
    print("  2. Interactive conversation")
    print("  3. Health check only")
    print("  4. Custom request")
    print("  5. Exit")
    print("=" * 60)


def custom_request(tester: APITester):
    """Handle custom API request"""
    print("\n" + "=" * 60)
    print("  Custom Request")
    print("=" * 60)
    print("\nChoose endpoint:")
    print("  1. POST /ask")
    print("  2. POST /clarify")
    
    choice = input("\nYour choice: ").strip()
    
    if choice == "1":
        question = input("Question: ").strip()
        thread_id = input("Thread ID (press Enter to auto-generate): ").strip() or None
        tester.ask_question(question, thread_id)
    
    elif choice == "2":
        clarification = input("Clarification: ").strip()
        thread_id = input("Thread ID: ").strip()
        if thread_id and clarification:
            tester.provide_clarification(clarification, thread_id)
        else:
            print("❌ Both clarification and thread_id are required.")


def main():
    """Main interactive menu"""
    tester = APITester()
    
    while True:
        show_menu()
        choice = input("\nYour choice: ").strip()
        
        if choice == "1":
            tester.run_automated_tests()
        
        elif choice == "2":
            tester.interactive_conversation()
        
        elif choice == "3":
            tester.test_health()
        
        elif choice == "4":
            custom_request(tester)
        
        elif choice == "5":
            print("\n👋 Goodbye!")
            break
        
        else:
            print("\n❌ Invalid choice. Please try again.")


if __name__ == "__main__":
    print("\n🚀 Starting API Tester...")
    print("📍 Server URL:", BASE_URL)
    
    try:
        # Quick health check
        response = requests.get(f"{BASE_URL}/health", timeout=2)
        if response.status_code == 200:
            print("✅ Server is online!\n")
            main()
        else:
            print("⚠️  Server responded but may have issues.\n")
            main()
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API server")
        print("💡 Make sure the server is running:")
        print("   python api.py")
    except Exception as e:
        print(f"\n❌ Error: {e}")