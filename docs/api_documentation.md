# API Documentation

## POST `/api/plan`

Request body:

```json
{
  "destination": "Paris",
  "origin": "CDG Airport",
  "start_date": "2026-06-10",
  "end_date": "2026-06-12",
  "travelers": 2,
  "budget": 1500,
  "interests": "art, food"
}
```

Response: trip metadata, specialist pipeline outputs, combined context, and manager summary.

## Live Provider Keys

- Manager / Itinerary LLM: `GROQ_API_KEY` or `GEMINI_API_KEY`
- Weather: `WEATHER_API_KEY` for `https://api.weatherapi.com/v1/current.json`
- Route: `OPENROUTESERVICE_API_KEY`
- News: `NEWSDATA_API_KEY` for `https://newsdata.io/api/1/news`
- Weather geocoding: optional `WEATHER_GEOCODING_API_KEY` slot is available
- Attraction: OpenStreetMap / Overpass does not require a key
