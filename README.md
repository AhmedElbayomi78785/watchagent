# WatchAgent — Weather Monitor & AI Assistant

## Overview
For this project I built a weather monitoring service that keeps an eye on three
Canadian cities: Ottawa, Toronto, and Vancouver. Every 5 minutes it fetches live
weather data, saves it to a database, and checks if anything unusual happened like
a storm or extreme cold. Everything is available through a simple API.

## Architecture

```
[Open-Meteo API]
      |
      v
  [Poller] --dedup--> [SQLite DB]
                           |
                      [Event Detector]
                           |
                       [FastAPI]
                           |
                    /health /readings /events
```

## Setup
First clone the repo to the device
git clone https://github.com/AhmedElbayomi78785/watchagent
cd watchagent

----------------------------------------------------------
Then install all the libraries the project needs to run and these are the ones i used
pip install fastapi uvicorn httpx apscheduler pydantic pytest

----------------------------------------------------------
Now start the API server — this is what handles all the requests:
uvicorn app.api:app --reload
-------------------------------------------------------------
Open a second terminal and run the poller — this is what goes and fetches 
the weather data from Ottawa, Toronto and Vancouver every 5 minutes and 
saves it to the database:

python -m app.poller

----------------------------------------------------------------
Once both are running, open the browser and check these links to see 
if everything is working:

1st : uvicorn app.api:app --reload
2nd (in a new terminal) : python -m app.poller
then:
http://127.0.0.1:8000/health     shows how many readings and events are stored
http://127.0.0.1:8000/readings   shows the weather readings for all 3 cities
http://127.0.0.1:8000/events     shows any if any weather events detected

-----------------------------------------------------------------------------



## Event Detection Design
I wanted the system to only fire an event when something is actually worth paying
attention to, not just any small change. So I came up with these rules:

If temperature goes above 35°C it's extreme heat
If temperature drops below -20°C it's extreme cold
If wind speed goes above 80 km/h that's dangerous
If precipitation hits 10mm in one hour that's heavy rain
If the WMO weather code matches known storm codes the system fires a storm event
If temperature drops 8°C or more in one hour compared to the last reading,
that's a sudden drop worth flagging

Normal weather on a regular day won't trigger anything. I also made sure the same
reading never gets saved twice by checking the city and timestamp before inserting.


**Rules:**
`error-handling.mdc` — when the weather API fails, log a warning with the city
  name and error, and skip that city instead of crashing

`event-schema.mdc` — every event must always have these fields: city, event_type,
  description, severity, timestamp, and reading_id

**Agent:**
`event-reviewer.md` — I set up an agent to help me review my detection logic and
  check if my thresholds make sense for Canadian weather conditions

**Skill:**
`analyze_data.py` — a script I can run anytime to get a quick summary of how many
  readings and events are stored and what the latest ones are

## Running Tests
pip install pytest httpx fastapi
pytest tests/ (this actually runs the test)

This runs tests covering:
Deduplication — same reading saved twice only stores once
Event detection — extreme heat, cold, wind, storm, and temperature drop
API shape — /health, /readings, and /events all return the correct structure

