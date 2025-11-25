"""
Quick test script for Travel Planner AI Agent
Run this to verify everything works before using the notebook
"""
import os
from dotenv import load_dotenv

# Load environment
load_dotenv()

# Check API key
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("❌ ERROR: GEMINI_API_KEY not found in .env file")
    print("Please create .env file with: GEMINI_API_KEY=your_key_here")
    exit(1)

print("✅ API key found")
print("Initializing agent...")

try:
    from travel_agent import create_travel_agent, run_agent
    
    # Create agent
    agent = create_travel_agent()
    print("✅ Agent created successfully!")
    
    # Test query
    print("\n" + "="*60)
    print("Running test query...")
    print("="*60)
    
    query = "Plan a 3-day trip to Paris with a budget of $1500. Show weather and top attractions."
    print(f"\nQuery: {query}\n")
    
    result = run_agent(query, agent)
    
    # Show results
    print("\n" + "="*60)
    print("AGENT RESPONSE:")
    print("="*60)
    
    for i, message in enumerate(result["messages"], 1):
        msg_type = type(message).__name__
        if hasattr(message, 'content') and message.content:
            print(f"\n[{i}] {msg_type}:")
            print(message.content[:500] + "..." if len(message.content) > 500 else message.content)
        
        if hasattr(message, 'tool_calls') and message.tool_calls:
            print(f"  → Tool calls: {len(message.tool_calls)}")
            for tc in message.tool_calls:
                print(f"    - {tc.get('name', 'unknown')}")
    
    print("\n" + "="*60)
    print("✅ Test completed successfully!")
    print("="*60)
    print("\nYou can now run the Jupyter notebook: Travel_Agent_Notebook.ipynb")
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
    print("\nTroubleshooting:")
    print("1. Make sure all dependencies are installed: pip install -r requirements.txt")
    print("2. Check that GEMINI_API_KEY is correct in .env file")
    print("3. Verify internet connection (needed for Gemini API)")

