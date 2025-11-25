# 🚀 Quick Start - 5 Minutes to Running Agent

## Step 1: Install (1 minute)
```bash
pip install -r requirements.txt
```

## Step 2: Get API Key (2 minutes)
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google
3. Click "Create API Key"
4. Copy the key

## Step 3: Create .env File (30 seconds)
Create a file named `.env` in the root directory:
```
GEMINI_API_KEY=paste_your_key_here
```

## Step 4: Test (1 minute)
```bash
python test_agent.py
```

## Step 5: Run Notebook (30 seconds)
```bash
jupyter notebook Travel_Agent_Notebook.ipynb
```

## ✅ Done!

Your agent is ready. The notebook has 5 test queries ready to run.

---

## Files Overview

- `travel_agent.py` - Main LangGraph agent
- `travel_tools.py` - 4 tools (weather, attractions, budget, flights)
- `Travel_Agent_Notebook.ipynb` - Testing notebook with 5 queries
- `test_agent.py` - Quick test script
- `requirements.txt` - Dependencies
- `README.md` - Full documentation

## Need Help?

See `SETUP_GUIDE.md` for detailed instructions or `TERMINAL_COMMANDS.md` for all commands.

