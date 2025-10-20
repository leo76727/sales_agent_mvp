
import sqlite3, random, datetime, os

os.makedirs("data", exist_ok=True)
conn = sqlite3.connect("data/positions.db")
cur = conn.cursor()
cur.execute("DROP TABLE IF EXISTS positions")
cur.execute("CREATE TABLE positions (id INTEGER PRIMARY KEY, client_id TEXT, underlyer TEXT, option_name TEXT, quantity INT, expiration_date TEXT)")

clients = [f"Client_{i}" for i in range(1,6)]
stocks = ["AAPL", "MSFT", "GOOG", "TSLA", "AMZN"]

for _ in range(100):
    client = random.choice(clients)
    stock = random.choice(stocks)
    expiry = datetime.date.today() + datetime.timedelta(days=random.randint(1,10))
    opt = f"{stock}_CALL_{expiry.strftime('%Y%m%d')}"
    qty = random.randint(10,100)
    cur.execute("INSERT INTO positions (client_id, underlyer, option_name, quantity, expiration_date) VALUES (?, ?, ?, ?, ?)",
                (client, stock, opt, qty, expiry.isoformat()))
conn.commit()
conn.close()
print("Database initialized with mock positions.")
