import os
import tempfile
from app.db import init_db, save_reading, count_readings

# Create a temporary database for testing
def setup():
    temp_db = tempfile.mktemp(suffix=".db")
    os.environ["DATABASE_URL"] = temp_db
    init_db()

# test the data that will be entered device to check for duplication
def test_deduplication():
    setup()

    reading = {
        "city": "Ottawa",
        "timestamp": "2026-01-01T12:00",
        "temperature_2m": 5.0,
        "apparent_temperature": 3.0,
        "precipitation": 0.0,
        "wind_speed_10m": 10.0,
        "weather_code": 1,
        "fetched_at": "2026-01-01T12:00:00+00:00",
    }

    # Save the same reading twice
    save_reading(reading)
    save_reading(reading)

    # Should only be stored once
    assert count_readings() == 1