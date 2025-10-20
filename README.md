
# Sales Agent MVP

An MVP agent platform for sales to analyze client option positions, identify trading opportunities, and chat with an LLM assistant.

## Structure
- `backend/`: FastAPI server serving position data, Deepseek LLM integration, and logs
- `gui/`: Streamlit interface for chatting and reviewing reports
- `data/`: SQLite database and log files

## Setup
```bash
git clone <repo-url>
cd sales_agent_mvp
python -m venv venv
source venv/bin/activate  # (Windows: venv\Scripts\activate)
pip install -r requirements.txt
python backend/init_db.py
```

## Run
```bash
# Terminal 1
uvicorn backend.main:app --reload --port 8000

# Terminal 2
streamlit run gui/app.py
```

## Environment
Copy `.env.example` to `.env` and fill in your Deepseek API key:
```
DEEPSEEK_API_KEY=your_api_key_here
```
