# Setup Guide

Use Python 3.11+ if possible.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

## Required Keys For Live Providers

Set these in `.env`:

```env
LLM_PROVIDER=groq
GROQ_API_KEY=your_groq_free_api_key_here
# or use Gemini
GEMINI_API_KEY=your_gemini_key_here

WEATHER_API_KEY=your_weatherapi_key_here
WEATHER_API_URL=https://api.weatherapi.com/v1/current.json

OPENROUTESERVICE_API_KEY=your_openrouteservice_key_here

NEWSDATA_API_KEY=your_newsdata_key_here
NEWSDATA_API_URL=https://newsdata.io/api/1/news
```

## No-Key Providers

OpenStreetMap / Overpass does not need a key. The app also keeps an optional weather geocoding key placeholder in case you add a separate keyed geocoder later:

```env
WEATHER_GEOCODING_API_URL=
WEATHER_GEOCODING_API_KEY=
```

Keep `.env` private in real projects.
