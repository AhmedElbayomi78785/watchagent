from pydantic import BaseModel
from datetime import datetime

#the structure of the data that will be entered
class Reading(BaseModel):
    id: int | None = None
    city: str
    timestamp: str
    temperature_2m: float
    apparent_temperature: float
    precipitation: float
    wind_speed_10m: float
    weather_code: int
    fetched_at: str

class Event(BaseModel):
    id: int | None = None
    city: str
    event_type: str
    description: str
    severity: str          # "low" | "medium" | "high"
    timestamp: str
    reading_id: int | None = None
