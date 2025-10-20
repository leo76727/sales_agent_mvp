
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, json, os, requests
from datetime import datetime

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "data/positions.db"
LOG_PATH = "data/logs.json"

@app.get("/api/positions")
def get_positions():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM positions")
    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]
    conn.close()
    data = [dict(zip(columns, row)) for row in rows]
    return {"positions": data}

@app.post("/api/llm")
def query_llm(payload: dict):
    prompt = payload.get("prompt")
    response = requests.post(
        "https://api.deepseek.com/v1/chat/completions",
        headers={"Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}", "Content-Type": "application/json"},
        json={"model": "deepseek-chat", "messages": [{"role": "user", "content": prompt}]}
    )
    result = response.json()
    text = result.get("choices", [{}])[0].get("message", {}).get("content", "No response")

    log = {"timestamp": datetime.now().isoformat(), "prompt": prompt, "response": text}
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r") as f:
            logs = json.load(f)
    else:
        logs = []
    logs.append(log)
    with open(LOG_PATH, "w") as f:
        json.dump(logs, f, indent=2)
    return log

@app.get("/api/logs")
def get_logs():
    if not os.path.exists(LOG_PATH):
        return {"logs": []}
    with open(LOG_PATH) as f:
        return {"logs": json.load(f)}

@app.post("/api/generate_report")
def generate_report():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM positions WHERE julianday(expiration_date) - julianday('now') < 5")
    df = cursor.fetchall()
    conn.close()
    report = f"Daily report generated on {datetime.now()} with {len(df)} expiring positions."
    return {"report": report}
