import sqlite3
import os

def get_db_path():
    return os.getenv("DATABASE_URL", "sqlite:///./data/watchagent.db").replace("sqlite:///./", "")

def get_conn():
    path = get_db_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            temperature_2m REAL,
            apparent_temperature REAL,
            precipitation REAL,
            wind_speed_10m REAL,
            weather_code INTEGER,
            fetched_at TEXT,
            UNIQUE(city, timestamp)
        );
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city TEXT NOT NULL,
            event_type TEXT NOT NULL,
            description TEXT NOT NULL,
            severity TEXT NOT NULL,
            timestamp TEXT NOT NULL,
            reading_id INTEGER
        );
    """)
    conn.commit()
    conn.close()

def save_reading(reading: dict) -> int | None:
    conn = get_conn()
    try:
        cur = conn.execute("""
            INSERT OR IGNORE INTO readings
            (city, timestamp, temperature_2m, apparent_temperature,
             precipitation, wind_speed_10m, weather_code, fetched_at)
            VALUES (:city, :timestamp, :temperature_2m, :apparent_temperature,
                    :precipitation, :wind_speed_10m, :weather_code, :fetched_at)
        """, reading)
        conn.commit()
        return cur.lastrowid if cur.rowcount else None
    finally:
        conn.close()

def save_event(event: dict):
    conn = get_conn()
    try:
        conn.execute("""
            INSERT INTO events (city, event_type, description, severity, timestamp, reading_id)
            VALUES (:city, :event_type, :description, :severity, :timestamp, :reading_id)
        """, event)
        conn.commit()
    finally:
        conn.close()

def get_readings(city=None, limit=50):
    conn = get_conn()
    try:
        if city:
            rows = conn.execute("SELECT * FROM readings WHERE city=? ORDER BY timestamp DESC LIMIT ?", (city, limit)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM readings ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def get_events(city=None, limit=50):
    conn = get_conn()
    try:
        if city:
            rows = conn.execute("SELECT * FROM events WHERE city=? ORDER BY timestamp DESC LIMIT ?", (city, limit)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM events ORDER BY timestamp DESC LIMIT ?", (limit,)).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()

def count_readings():
    conn = get_conn()
    try:
        return conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]
    finally:
        conn.close()

def count_events():
    conn = get_conn()
    try:
        return conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]
    finally:
        conn.close()