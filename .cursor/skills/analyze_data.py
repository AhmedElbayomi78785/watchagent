import sqlite3
import os

db = os.getenv("DATABASE_URL", "sqlite:///./data/watchagent.db").replace("sqlite:///./", "")
conn = sqlite3.connect(db)

readings = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
events   = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]

print(f"Total readings: {readings}")
print(f"Total events:   {events}")

print("\nLatest 5 events:")
for row in conn.execute("SELECT timestamp, city, event_type, severity FROM events ORDER BY timestamp DESC LIMIT 5").fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")

conn.close()
