# Terminal Commands for GitHub Codespaces

## Complete Setup & Testing Guide

### 1. Initial Setup (One-time)

```bash
# Navigate to project directory (if not already there)
cd TravelAIAgent

# Install all dependencies
pip install -r requirements.txt

# Verify installation
python -c "import langgraph; print('LangGraph installed:', langgraph.__version__)"
```

### 2. Configure API Key

```bash
# Option A: Create .env file using echo
echo "GEMINI_API_KEY=your_actual_api_key_here" > .env

# Option B: Create .env file manually
# Use the editor to create .env file with:
# GEMINI_API_KEY=your_actual_api_key_here

# Verify .env file exists
cat .env
```

### 3. Quick Test (Python Script)

```bash
# Run the test script
python test_agent.py
```

### 4. Run Main Agent Script

```bash
# Run the main agent
python travel_agent.py
```

### 5. Jupyter Notebook Setup

```bash
# Start Jupyter notebook server
jupyter notebook

# Or use JupyterLab
jupyter lab

# The notebook will open in your browser
# Open: Travel_Agent_Notebook.ipynb
```

### 6. Test Individual Tools

```bash
# Test tools directly
python -c "
from travel_tools import get_weather_forecast, search_tourist_attractions
print(get_weather_forecast('Paris', 3))
print(search_tourist_attractions('Tokyo'))
"
```

### 7. Verify Environment

```bash
# Check Python version (should be 3.8+)
python --version

# Check installed packages
pip list | grep -E "(langgraph|langchain|google-generativeai)"

# Check environment variables (should show your key)
python -c "from dotenv import load_dotenv; import os; load_dotenv(); print('API Key set:', bool(os.getenv('GEMINI_API_KEY')))"
```

## Troubleshooting Commands

### Reinstall Dependencies

```bash
# Uninstall and reinstall
pip uninstall -y langgraph langchain langchain-google-genai
pip install -r requirements.txt
```

### Check for Errors

```bash
# Test imports
python -c "
from travel_agent import create_travel_agent
from travel_tools import TRAVEL_TOOLS
print('All imports successful!')
print(f'Tools available: {len(TRAVEL_TOOLS)}')
"
```

### Clear Python Cache

```bash
# Remove __pycache__ directories
find . -type d -name __pycache__ -exec rm -r {} +
```

## Complete Workflow Example

```bash
# Step 1: Setup
pip install -r requirements.txt

# Step 2: Configure
echo "GEMINI_API_KEY=your_key" > .env

# Step 3: Test
python test_agent.py

# Step 4: Run notebook
jupyter notebook Travel_Agent_Notebook.ipynb
```

## For Assignment Submission

```bash
# Verify all files exist
ls -la

# Should show:
# - travel_agent.py
# - travel_tools.py
# - Travel_Agent_Notebook.ipynb
# - requirements.txt
# - README.md
# - .env.example
# - .gitignore

# Test final run
python test_agent.py

# If successful, you're ready to submit!
```

## Quick Reference

| Task | Command |
|------|---------|
| Install deps | `pip install -r requirements.txt` |
| Set API key | `echo "GEMINI_API_KEY=key" > .env` |
| Quick test | `python test_agent.py` |
| Run agent | `python travel_agent.py` |
| Start notebook | `jupyter notebook` |
| Check version | `python --version` |

