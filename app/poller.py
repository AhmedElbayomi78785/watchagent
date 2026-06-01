import httpx
import time
import os
from datetime import datetime, timezone
from app.db import init_db, save_reading, save_event, get_readings
from app.detector import detect_events

CITIES = [
    {"name": "Ottawa",    "lat": 45.42, "lon": -75.69},
    {"name": "Toronto",   "lat": 43.70, "lon": -79.42},
    {"name": "Vancouver", "lat": 49.25, "lon": -123.12},
]

INTERVAL = int(os.getenv("POLL_INTERVAL", 300))

def fetch_weather(city: dict) -> dict | None:
    try:
        r = httpx.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": city["lat"],
            "longitude": city["lon"],
            "current": "temperature_2m,apparent_temperature,precipitation,wind_speed_10m,weather_code",
            "wind_speed_unit": "kmh",
            "timezone": "auto",
        }, timeout=10)
        r.raise_for_status()
        c = r.json()["current"]
        return {
            "city": city["name"],
            "timestamp": c["time"],
            "temperature_2m": c["temperature_2m"],
            "apparent_temperature": c["apparent_temperature"],
            "precipitation": c["precipitation"],
            "wind_speed_10m": c["wind_speed_10m"],
            "weather_code": c["weather_code"],
            "fetched_at": datetime.now(timezone.utc).isoformat(),
        }
    except Exception as e:
        print(f"[WARNING] Failed to fetch {city['name']}: {e}")
        return None

def poll():
    """Fetch and save weather data for all cities."""
    saved_count = 0

    for city in CITIES:
        reading = fetch_weather(city)

        if not reading:
            continue

        reading_id = save_reading(reading)

        if reading_id:
            saved_count += 1
            reading["id"] = reading_id

            recent = get_readings(city=city["name"], limit=1)

            for event in detect_events(reading, recent):
                save_event(event)

    print(f"Saved {saved_count} weather readings.")

def main():
    """Start the weather poller."""
    init_db()
    print("Poller started")
    while True:
        poll()
        print(f"Waiting {INTERVAL} seconds until next poll...")
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()
