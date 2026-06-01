import os, tempfile
from app.db import init_db
from app.detector import detect_events

def setup():
    os.environ["DATABASE_URL"] = tempfile.mktemp(suffix=".db")
    init_db()

#test reading data
def reading(temp=20.0, wind=10.0, precip=0.0, code=1):
    return {"id": 1, "city": "Ottawa", "timestamp": "2026-01-01T12:00",
            "temperature_2m": temp, "apparent_temperature": temp - 2,
            "precipitation": precip, "wind_speed_10m": wind,
            "weather_code": code, "fetched_at": "2026-01-01T12:00:00+00:00"}

def test_normal():
    setup()
    assert detect_events(reading(), []) == []

def test_heat():
    assert any(e["event_type"] == "extreme_heat" for e in detect_events(reading(temp=36), []))

def test_wind():
    assert any(e["event_type"] == "high_wind" for e in detect_events(reading(wind=90), []))

def test_storm():
    assert any(e["event_type"] == "storm" for e in detect_events(reading(code=95), []))

def test_temp_drop():
    assert any(e["event_type"] == "temperature_drop" for e in detect_events(reading(temp=10), [reading(temp=20)]))