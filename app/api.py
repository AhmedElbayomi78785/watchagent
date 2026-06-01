from contextlib import asynccontextmanager
from fastapi import FastAPI, Query
from app.db import init_db, get_readings, get_events, count_readings, count_events

@asynccontextmanager
async def lifespan(app):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.get("/health")
def health():
    return {
        "status": "ok",
        "readings_stored": count_readings(),
        "events_stored": count_events()
    }

@app.get("/readings")
def readings(city: str = None, limit: int = Query(50)):
    return {"readings": get_readings(city, limit)}

@app.get("/events")
def events(city: str = None, limit: int = Query(50)):
    return {"events": get_events(city, limit)}