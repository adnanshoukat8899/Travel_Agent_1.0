# Quick Setup Guide for GitHub Codespaces

## ⚡ 30-Second Setup

### Step 1: Open in Codespaces
1. Open this repo in GitHub Codespaces
2. Wait for environment to initialize

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Get Gemini API Key
1. Go to: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Click "Create API Key"
4. Copy the key

### Step 4: Create .env File
```bash
echo "GEMINI_API_KEY=your_key_here" > .env
```
Or manually create `.env` file with:
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 5: Run Notebook
```bash
jupyter notebook Travel_Agent_Notebook.ipynb
```

## 🧪 Quick Test

Run this in Python to verify setup:

```python
from travel_agent import create_travel_agent, run_agent

# Initialize agent
agent = create_travel_agent()

# Test query
result = run_agent("Plan a 3-day trip to Paris with $1500 budget", agent)
print(result["messages"][-1].content)
```

## ✅ Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `GEMINI_API_KEY`
- [ ] Agent initializes without errors
- [ ] Notebook runs all cells successfully
- [ ] At least one test query works

## 🐛 Troubleshooting

### Error: "GEMINI_API_KEY not found"
- Make sure `.env` file exists in root directory
- Check that API key is correctly formatted (no quotes, no spaces)

### Error: "Module not found"
- Run: `pip install -r requirements.txt`
- Restart kernel if using Jupyter

### Error: API rate limit
- Gemini free tier has rate limits
- Wait a few minutes and try again
- Consider using a different API key

## 📝 Terminal Commands Summary

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Create .env file (replace with your key)
echo "GEMINI_API_KEY=your_key" > .env

# 3. Test agent
python travel_agent.py

# 4. Or run notebook
jupyter notebook Travel_Agent_Notebook.ipynb
```

## 🎯 For Assignment Submission

Make sure you have:
1. ✅ Working code (all files)
2. ✅ README.md with instructions
3. ✅ Notebook with 5 test queries
4. ✅ .env.example (without actual keys)
5. ✅ requirements.txt
6. ✅ All code runs without errors

Good luck! 🚀

