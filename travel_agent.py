"""
Travel Planner AI Agent using LangGraph and Gemini
Implements a multi-destination itinerary optimization agent
"""
import os
from typing import TypedDict, Annotated, Sequence
from dotenv import load_dotenv
import operator

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode
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

# Initialize Gemini LLM
def get_llm():
    """Initialize Google Gemini LLM"""
    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in environment variables. Please set it in .env file")
    
    return ChatGoogleGenerativeAI(
        model="gemini-pro",
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
    
    # Define the agent node (LLM)
    def agent_node(state: AgentState):
        """Agent node that calls the LLM"""
        messages = state["messages"]
        response = llm_with_tools.invoke(messages)
        return {"messages": [response]}
    
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


def run_agent(query: str, agent=None):
    """
    Run the travel agent with a query
    
    Args:
        query: User query string
        agent: Optional pre-initialized agent (for efficiency)
    
    Returns:
        Final response from the agent
    """
    if agent is None:
        agent = create_travel_agent()
    
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

