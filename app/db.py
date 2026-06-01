import sqlite3
import os
from contextlib import contextmanager


def get_db_path():
    return os.getenv("DATABASE_URL", "sqlite:///./data/watchagent.db").replace("sqlite:///./", "")


@contextmanager
def db():
    path = get_db_path()
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row

    try:
        yield conn
        conn.commit()
    finally:
        conn.close()


def init_db():
    with db() as conn:
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


def save_reading(reading: dict):
    with db() as conn:
        cur = conn.execute("""
            INSERT OR IGNORE INTO readings
            (city, timestamp, temperature_2m, apparent_temperature,
             precipitation, wind_speed_10m, weather_code, fetched_at)
            VALUES (:city, :timestamp, :temperature_2m, :apparent_temperature,
                    :precipitation, :wind_speed_10m, :weather_code, :fetched_at)
        """, reading)

        return "inserted" if cur.rowcount else "ignored"


def save_event(event: dict):
    with db() as conn:
        conn.execute("""
            INSERT INTO events
            (city, event_type, description, severity, timestamp, reading_id)
            VALUES (:city, :event_type, :description, :severity, :timestamp, :reading_id)
        """, event)


def get_readings(city=None, limit=50):
    with db() as conn:
        if city:
            rows = conn.execute(
                "SELECT * FROM readings WHERE city=? ORDER BY timestamp DESC LIMIT ?",
                (city, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM readings ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()

        return [dict(r) for r in rows]


def get_events(city=None, limit=50):
    with db() as conn:
        if city:
            rows = conn.execute(
                "SELECT * FROM events WHERE city=? ORDER BY timestamp DESC LIMIT ?",
                (city, limit)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT * FROM events ORDER BY timestamp DESC LIMIT ?",
                (limit,)
            ).fetchall()

        return [dict(r) for r in rows]


def count_readings():
    with db() as conn:
        return conn.execute("SELECT COUNT(*) FROM readings").fetchone()[0]


def count_events():
    with db() as conn:
        return conn.execute("SELECT COUNT(*) FROM events").fetchone()[0]