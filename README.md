# Travel Planner AI Agent

A comprehensive AI agent built with LangGraph and Google Gemini API for multi-destination travel itinerary optimization. The agent integrates multiple tools to provide weather forecasts, tourist attractions, budget optimization, and flight/hotel search capabilities.

## 🎯 Agent Goal

**Multi-destination itinerary optimization** - The agent helps users plan optimized travel itineraries across multiple destinations by:
- Searching flights and hotels
- Checking weather forecasts
- Finding tourist attractions
- Optimizing budget allocation
- Generating comprehensive travel plans

## 🛠️ Tools Integrated

1. **Weather Forecast Tool** - Get 5-day weather forecasts for any city
2. **Tourist Attractions Database** - Search for top attractions in cities
3. **Budget Optimizer** - Allocate and optimize budget across multiple destinations
4. **Flight/Hotel Search** - Find flight and hotel options with pricing

## 📋 Requirements

- Python 3.8+
- Google Gemini API Key (free tier available)
- LangGraph framework
- LangChain with Google Generative AI integration

## ⚡ Rate Limiting & Error Handling

The agent includes built-in rate limiting and retry logic to handle API rate limits:

- **Automatic rate limiting**: 2-second delay between API calls (configurable)
- **Exponential backoff**: Automatic retries with increasing delays on rate limit errors
- **Error handling**: Graceful handling of `ResourceExhausted` errors
- **Configurable delays**: Adjust delays via environment variables

### Rate Limiting Configuration

You can configure rate limiting in your `.env` file:

```bash
# Rate limiting settings (optional)
RATE_LIMIT_DELAY=2.0          # Delay between API calls (seconds)
MAX_RETRIES=5                  # Maximum retry attempts
INITIAL_RETRY_DELAY=5.0        # Initial retry delay (seconds)
GEMINI_MODEL=gemini-1.5-flash  # Model name (gemini-1.5-flash or gemini-1.5-pro)
```

**Note**: If you hit rate limits frequently, increase `RATE_LIMIT_DELAY` to 5-10 seconds.

## 🚀 Quick Setup (GitHub Codespaces)

### Step 1: Clone/Open Repository in Codespaces

1. Open this repository in GitHub Codespaces
2. The environment will automatically set up Python

### Step 2: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 3: Get Gemini API Key

1. Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Create a new API key (free tier available)
4. Copy the API key

### Step 4: Configure Environment

```bash
# Create .env file
cp .env.example .env

# Edit .env and add your API key
# GEMINI_API_KEY=your_actual_api_key_here
```

Or create `.env` file manually:
```
GEMINI_API_KEY=your_gemini_api_key_here
```

### Step 5: Test the Agent

#### Option A: Run in Jupyter Notebook (Recommended)

```bash
# Start Jupyter
jupyter notebook

# Open Travel_Agent_Notebook.ipynb
# Run all cells
```

#### Option B: Run Python Script

```bash
python travel_agent.py
```

## 📊 Architecture

### LangGraph Structure

```
START
  ↓
Agent Node (Gemini LLM)
  ↓
[Has Tool Calls?]
  ├─ Yes → Tools Node → Agent Node (loop)
  └─ No → END
```

### State Management

The agent uses `TypedDict` for state management:
- **messages**: Sequence of BaseMessage objects (HumanMessage, AIMessage, ToolMessage)

### Node Types

1. **Agent Node**: LLM node using Gemini Pro that processes queries and decides tool usage
2. **Tools Node**: Executes tool calls (weather, attractions, budget, flights/hotels)

## 🧪 Testing

The notebook includes 5 test queries:

1. **Multi-destination planning**: "Plan a 7-day trip to Paris and London with a budget of $4000..."
2. **Budget optimization**: "I want to visit Tokyo and New York. I have $5000 for 10 days..."
3. **Flight/hotel search**: "Find flights and hotels from New York to Paris..."
4. **Weather and attractions**: "What's the weather forecast for Tokyo for the next 5 days?"
5. **Complete itinerary**: "Create a complete 5-day itinerary for Paris..."

## 📁 Project Structure

```
TravelAIAgent/
├── travel_agent.py          # Main LangGraph agent implementation
├── travel_tools.py          # Tool definitions (4 tools)
├── Travel_Agent_Notebook.ipynb  # Testing notebook
├── requirements.txt         # Python dependencies
├── .env.example            # Environment variables template
└── README.md               # This file
```

## 🔧 Key Components

### 1. Agent State (TypedDict)
```python
class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
```

### 2. Tool Integration
- Tools are defined using `@tool` decorator from LangChain
- Bound to LLM using `.bind_tools()`
- Executed via `ToolNode` in LangGraph

### 3. Graph Workflow
- Entry point: Agent node
- Conditional routing based on tool calls
- Loop back to agent after tool execution

## 📈 Example Output

```
Query: Plan a 7-day trip to Paris and London with a budget of $4000...

Agent Response:
Based on your requirements, I'll help you plan a 7-day trip to Paris and London...

[Tool calls made: 4]

Weather forecast for Paris:
Day 1: 22°C, Sunny, Humidity: 65%
...

Tourist attractions in Paris:
1. Eiffel Tower (landmark) - Rating: 4.8/5, Price: €25
...

Budget Optimization for 4000 USD:
Total days: 7
Average daily budget: $571.43
...
```

## 🎓 Learning Outcomes Demonstrated

✅ **Agentic AI Design**: Graph-based workflow using LangGraph  
✅ **Stateful Conversations**: TypedDict state management with message history  
✅ **Tool Integration**: 4 external tools (weather, attractions, budget, flights)  
✅ **Multi-step Reasoning**: Agent chains multiple tool calls for complex queries  
✅ **LLM Integration**: Google Gemini API (free tier)  
✅ **Workflow Edges**: Conditional routing and loops  

## 🔍 Evaluation Metrics

- **Tool Invocation**: Correct tool selection based on query
- **Multi-step Reasoning**: Chains multiple tools for complex queries
- **Output Quality**: Coherent, structured travel plans
- **Error Handling**: Graceful handling of missing data/API errors

## 🚧 Limitations & Future Improvements

### Current Limitations:
- Mock data for flights/hotels (can integrate Amadeus API)
- Limited city database for attractions
- Weather API uses mock data (can integrate OpenWeatherMap)

### Potential Improvements:
- Real-time API integrations (Amadeus, OpenWeatherMap)
- Database for attractions (Wikipedia API, Google Places)
- Booking integration
- Multi-language support
- Cost tracking and alerts

## 📚 References

- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Google Gemini API](https://ai.google.dev/)
- [LangChain Documentation](https://python.langchain.com/)
- [LangGraph Tutorials](https://langchain-ai.github.io/langgraph/tutorials/)

## 📝 License

This project is created for educational purposes as part of an AI Agent assignment.

## 👤 Author

Created for LangGraph AI Agent Assignment - Travel Planner Use Case

---

**Note**: This implementation uses free-tier APIs and mock data where necessary to ensure the solution works without requiring paid subscriptions.

