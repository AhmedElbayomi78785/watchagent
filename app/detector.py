STORM_CODES = {65, 67, 75, 77, 82, 85, 86, 95, 96, 99}

def detect_events(reading: dict, recent_readings: list) -> list:
    events = []
    city, ts, rid = reading["city"], reading["timestamp"], reading.get("id")
    temp, wind, precip, code = reading["temperature_2m"], reading["wind_speed_10m"], reading["precipitation"], reading["weather_code"]

    if temp >= 35:
        events.append({"city": city, "event_type": "extreme_heat", "description": f"Temperature reached {temp}°C", "severity": "high", "timestamp": ts, "reading_id": rid})
    elif temp <= -20:
        events.append({"city": city, "event_type": "extreme_cold", "description": f"Temperature dropped to {temp}°C", "severity": "high", "timestamp": ts, "reading_id": rid})

    if wind >= 80:
        events.append({"city": city, "event_type": "high_wind", "description": f"Wind reached {wind} km/h", "severity": "medium", "timestamp": ts, "reading_id": rid})

    if precip >= 10:
        events.append({"city": city, "event_type": "heavy_precipitation", "description": f"Precipitation {precip}mm", "severity": "medium", "timestamp": ts, "reading_id": rid})

    if code in STORM_CODES:
        events.append({"city": city, "event_type": "storm", "description": f"Storm detected (WMO {code})", "severity": "high", "timestamp": ts, "reading_id": rid})

    if recent_readings and (recent_readings[0]["temperature_2m"] - temp) >= 8:
        events.append({"city": city, "event_type": "temperature_drop", "description": f"Temp dropped {recent_readings[0]['temperature_2m'] - temp:.1f}°C in 1hr", "severity": "medium", "timestamp": ts, "reading_id": rid})

    return events