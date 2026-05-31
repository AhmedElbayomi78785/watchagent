import os, tempfile
from fastapi.testclient import TestClient
from app.db import init_db
from app.api import app

def setup():
    os.environ["DATABASE_URL"] = tempfile.mktemp(suffix=".db")
    init_db()

client = TestClient(app)

def test_health():
    setup()
    r = client.get("/health")
    assert r.status_code == 200
    assert "status" in r.json()

def test_readings():
    setup()
    r = client.get("/readings")
    assert r.status_code == 200
    assert "readings" in r.json()

def test_events():
    setup()
    r = client.get("/events")
    assert r.status_code == 200
    assert "events" in r.json()