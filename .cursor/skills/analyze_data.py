import sqlite3
import os

# the database
db = os.getenv("DATABASE_URL", "sqlite:///./data/watchagent.db").replace("sqlite:///./", "")
conn = sqlite3.connect(db)

print("=" * 50)
print("WATCHAGENT — DATA SUMMARY")
print("=" * 50)

# total readings and events stored
readings = conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
events   = conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
print(f"\nTotal readings stored: {readings}")
print(f"Total events stored:   {events}")

# how many readings each city has
print("\n--- Readings per city ---")
for row in conn.execute("SELECT city, COUNT(*) FROM readings GROUP BY city").fetchall():
    print(f"  {row[0]}: {row[1]} readings")

# average temperature per city
print("\n--- Average temperature per city ---")
for row in conn.execute("SELECT city, ROUND(AVG(temperature_2m), 1) FROM readings GROUP BY city").fetchall():
    print(f"  {row[0]}: {row[1]}°C")

# how many events each city has
print("\n--- Events per city ---")
for row in conn.execute("SELECT city, COUNT(*) FROM events GROUP BY city").fetchall():
    print(f"  {row[0]}: {row[1]} events")

# what happened in the last 24 hours
print("\n--- Last 24 hours ---")
for row in conn.execute("""
    SELECT city, event_type, severity, timestamp 
    FROM events 
    WHERE timestamp >= datetime('now', '-24 hours')
    ORDER BY timestamp DESC
""").fetchall():
    print(f"  {row[3]} | {row[0]} | {row[1]} | {row[2]}")

# latest 5 events overall
print("\n--- Latest 5 events ---")
for row in conn.execute("SELECT timestamp, city, event_type, severity FROM events ORDER BY timestamp DESC LIMIT 5").fetchall():
    print(f"  {row[0]} | {row[1]} | {row[2]} | {row[3]}")

print("\n" + "=" * 50)
conn.close()