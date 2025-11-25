"""
Travel Planner AI Agent using LangGraph and Gemini
Implements a multi-destination itinerary optimization agent
"""
import os
import time
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
import operator

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
from google.api_core.exceptions import ResourceExhausted
try:
    from langgraph.graph.message import add_messages
except ImportError:
    # Fallback for older versions
    from langgraph.checkpoint.memory import MemorySaver
    from operator import add
    def add_messages(left, right):
        return left + right

# Load environment variables
load_dotenv()

# Import tools
from travel_tools import TRAVEL_TOOLS

# Rate limiting configuration
RATE_LIMIT_DELAY = float(os.getenv("RATE_LIMIT_DELAY", "2.0"))  # Delay between requests in seconds
MAX_RETRIES = int(os.getenv("MAX_RETRIES", "5"))  # Maximum retry attempts
INITIAL_RETRY_DELAY = float(os.getenv("INITIAL_RETRY_DELAY", "5.0"))  # Initial retry delay in seconds

# Track last API call time for rate limiting
_last_api_call_time = 0

def rate_limit():
    """Enforce rate limiting between API calls"""
    global _last_api_call_time
    current_time = time.time()
    time_since_last_call = current_time - _last_api_call_time
    
    if time_since_last_call < RATE_LIMIT_DELAY:
        sleep_time = RATE_LIMIT_DELAY - time_since_last_call
        print(f"⏳ Rate limiting: waiting {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)
    
    _last_api_call_time = time.time()

# Initialize Gemini LLM
def get_llm():
    """Initialize Google Gemini LLM"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file")
    
    # Use newer model names (gemini-pro is deprecated)
    # Options: "gemini-1.5-flash" (faster, free) or "gemini-1.5-pro" (more capable)
    model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    
    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.7,
    )


# Define the agent state
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


def create_travel_agent():
    """
    Create and configure the Travel Planner AI Agent using LangGraph
    """
    # Initialize LLM
    llm = get_llm()
    
    # Bind tools to LLM
    llm_with_tools = llm.bind_tools(TRAVEL_TOOLS)
    
    # Create tool node
    tool_node = ToolNode(TRAVEL_TOOLS)
    
    # Define the agent node (LLM) with rate limiting and retry logic
    def agent_node(state: AgentState):
        """Agent node that calls the LLM with rate limiting and retry logic"""
        messages = state["messages"]
        
        # Apply rate limiting
        rate_limit()
        
        # Retry logic with exponential backoff
        retry_count = 0
        retry_delay = INITIAL_RETRY_DELAY
        
        while retry_count < MAX_RETRIES:
            try:
                response = llm_with_tools.invoke(messages)
                return {"messages": [response]}
            
            except ResourceExhausted as e:
                retry_count += 1
                if retry_count >= MAX_RETRIES:
                    error_msg = (
                        f"❌ Rate limit exceeded after {MAX_RETRIES} retries. "
                        f"Please wait a few minutes before trying again. "
                        f"Error: {str(e)}"
                    )
                    print(error_msg)
                    # Return an error message instead of crashing
                    error_response = AIMessage(
                        content=error_msg + "\n\n💡 Tip: The Gemini API has rate limits. Please wait a few minutes and try again, or reduce the number of queries."
                    )
                    return {"messages": [error_response]}
                
                # Exponential backoff with jitter
                wait_time = retry_delay * (2 ** (retry_count - 1))
                print(f"⚠️ Rate limit hit. Retrying in {wait_time:.1f} seconds... (Attempt {retry_count}/{MAX_RETRIES})")
                time.sleep(wait_time)
                retry_delay = wait_time
            
            except Exception as e:
                # For other errors, raise immediately
                print(f"❌ Error: {str(e)}")
                raise
        
        # Should not reach here, but just in case
        error_response = AIMessage(
            content="❌ Failed to get response from the API after multiple retries. Please try again later."
        )
        return {"messages": [error_response]}
    
    # Define router function to decide next step
    def should_continue(state: AgentState) -> str:
        """Determine if we should continue to tools or end"""
        messages = state["messages"]
        last_message = messages[-1]
        
        # If the last message has tool calls, go to tools
        if hasattr(last_message, 'tool_calls') and last_message.tool_calls:
            return "tools"
        # Otherwise, end
        return "end"
    
    # Build the graph
    workflow = StateGraph(AgentState)
    
    # Add nodes
    workflow.add_node("agent", agent_node)
    workflow.add_node("tools", tool_node)
    
    # Set entry point
    workflow.set_entry_point("agent")
    
    # Add conditional edges
    workflow.add_conditional_edges(
        "agent",
        should_continue,
        {
            "tools": "tools",
            "end": END
        }
    )
    
    # Add edge from tools back to agent
    workflow.add_edge("tools", "agent")
    
    # Compile the graph
    app = workflow.compile()
    
    return app


def run_agent(query: str, agent=None, delay_before_start=0):
    """
    Run the travel agent with a query
    
    Args:
        query: User query string
        agent: Optional pre-initialized agent (for efficiency)
        delay_before_start: Optional delay in seconds before starting (for rate limiting)
    
    Returns:
        Final response from the agent
    """
    if agent is None:
        agent = create_travel_agent()
    
    # Optional delay before starting (useful when running multiple queries)
    if delay_before_start > 0:
        print(f"⏳ Waiting {delay_before_start} seconds before starting...")
        time.sleep(delay_before_start)
    
    # Create initial state
    initial_state = {
        "messages": [HumanMessage(content=query)]
    }
    
    # Run the agent
    result = agent.invoke(initial_state)
    
    return result


if __name__ == "__main__":
    # Example usage
    print("Travel Planner AI Agent")
    print("=" * 50)
    
    try:
        agent = create_travel_agent()
        
        # Test query
        query = "Plan a 5-day trip to Paris and Tokyo with a budget of $3000. Include weather forecast and top attractions."
        print(f"\nQuery: {query}\n")
        
        result = run_agent(query, agent)
        
        # Print final response
        print("\nAgent Response:")
        print("-" * 50)
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                print(message.content)
                if hasattr(message, 'tool_calls') and message.tool_calls:
                    print(f"\nTool calls made: {len(message.tool_calls)}")
    except Exception as e:
        print(f"Error: {e}")
        print("\nMake sure to set GEMINI_API_KEY in your .env file")

