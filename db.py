
import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            keyword TEXT,
            context TEXT,
            timestamp TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_alerts(url, alerts):
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()
    for keyword, line in alerts:
        c.execute("""
            INSERT INTO alerts (url, keyword, context, timestamp)
            VALUES (?, ?, ?, ?)
        """, (url, keyword, line[:300], datetime.now().isoformat()))
    conn.commit()
    conn.close()

def fetch_alerts():
    conn = sqlite3.connect("alerts.db")
    c = conn.cursor()
    c.execute("SELECT * FROM alerts ORDER BY timestamp DESC LIMIT 50")
    results = c.fetchall()
    conn.close()
    return results
