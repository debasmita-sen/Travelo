🌍 Travelo - AI Powered Multi-Agent Travel Planner
<div align="center">
✈️ Plan Smarter. Travel Better. Powered by Agentic AI.

An intelligent Multi-Agent AI Travel Planner that generates personalized travel itineraries by combining real-time weather, attractions, route planning, crowd analysis, budget optimization, food recommendations, and destination news.

Instead of relying on a single AI response, Travelo orchestrates multiple specialized AI agents to provide accurate, explainable, and data-driven travel recommendations.

🚀 Developed using Agentic AI Architecture

</div>
🎯 Project Overview

Travelo is an AI-powered travel planning platform built using a Multi-Agent Architecture.

Instead of a single Large Language Model attempting to solve every travel-related problem, Travelo delegates responsibilities to multiple specialized AI agents.

Each agent focuses on a specific domain, such as:

🏛️ Attractions
🌦️ Weather
🛣️ Route Planning
📰 Travel News
👥 Crowd Analysis
🍽️ Food Recommendations
💰 Budget Optimization
🗓️ Itinerary Generation

A central Manager Agent orchestrates these specialized agents and combines their outputs into a comprehensive travel plan.

This approach significantly improves:

Accuracy
Reliability
Explainability
Scalability
🚀 Key Features
🗓️ Personalized Travel Itinerary

Generate day-wise travel plans based on:

Destination
Travel dates
Budget
Interests
Number of travelers
💰 Budget Optimization

Analyze whether the trip budget is:

Under Budget
Balanced
Over Budget

using predefined city cost datasets.

🌦️ Real-Time Weather Analysis

Fetch weather information and forecasts to recommend optimal activities.

🏛️ Attraction Discovery

Discover tourist attractions using OpenStreetMap and Overpass APIs.

🛣️ Route Planning

Generate travel routes and transportation recommendations.

🍽️ Food Recommendations

Suggest local cuisines and famous food spots.

👥 Crowd Estimation

Estimate crowd levels using:

Holidays
Weather
Events
Travel dates
📰 Destination News

Fetch relevant travel news to keep travelers informed.

🤖 AI-Powered Summary Generation

Generate intelligent travel summaries using:

Google Gemini
Groq
🏗️ System Architecture
User Input
    │
    ▼
Planner Form
    │
    ▼
Trip Request
    │
    ▼
Manager Agent
    │
    ├── Attraction Agent
    │
    ├── Budget Agent
    │
    ├── Weather Agent
    │
    ├── News Agent
    │
    ├── Route Agent
    │
    ├── Crowd Agent
    │
    └── Food Agent
    │
    ▼
Itinerary Agent
    │
    ▼
Manager Summary
    │
    ▼
Travel Dashboard
🧠 Multi-Agent Workflow
1️⃣ Attraction Agent

Responsible for:

Discovering attractions
Filtering based on interests
Gathering location data

Provider:

OpenStreetMap
Overpass API
2️⃣ Budget Agent

Responsible for:

Budget estimation
Cost comparison
Expense categorization

Dataset:

city_costs.json
3️⃣ Weather Agent

Responsible for:

Weather forecasts
Travel suitability analysis

Provider:

WeatherAPI
4️⃣ News Agent

Responsible for:

Destination news
Important alerts

Provider:

NewsData.io
5️⃣ Route Agent

Responsible for:

Route generation
Transportation suggestions

Provider:

OpenRouteService
6️⃣ Crowd Agent

Responsible for:

Crowd estimation
Peak season analysis

Dataset:

crowd_rules.json
7️⃣ Food Agent

Responsible for:

Local cuisine recommendations
Food suggestions
8️⃣ Itinerary Agent

Responsible for:

Day-wise travel planning
Activity scheduling
9️⃣ Manager Agent

Responsible for:

Combining all agent outputs
Generating the final travel summary
🛠️ Tech Stack
Backend
Python
Flask
AI Models
Groq
Google Gemini
APIs
OpenStreetMap
Overpass API
WeatherAPI
OpenRouteService
NewsData.io
Database
SQLite
Environment Management
Hatch
Testing
Pytest
Version Control
Git
GitHub
📂 Project Structure
tragent/

├── agents/
├── routes/
├── services/
├── tools/
├── models/
├── prompts/
├── templates/
├── static/
├── tests/
├── data/
├── database/
├── docs/

├── app.py
├── config.py
├── requirements.txt
├── pyproject.toml
└── README.md
⚙️ Installation

Clone the repository:

git clone https://github.com/debasmita-sen/Travelo.git

Navigate into the project:

cd Travelo

Create environment:

hatch env create

Run the application:

hatch run app

Open:

http://127.0.0.1:5000
🔑 Environment Variables

Create a .env file:

LLM_PROVIDER=groq

GROQ_API_KEY=

GEMINI_API_KEY=

WEATHER_API_KEY=

OPENROUTESERVICE_API_KEY=

NEWSDATA_API_KEY=

FLASK_SECRET_KEY=
📸 Application Screenshots

Add screenshots here:

🏠 Home/Planner Page

<img width="1346" height="633" alt="image" src="https://github.com/user-attachments/assets/03c9372d-cac6-48f6-9db2-fa0f34fbb649" />

<img width="1352" height="628" alt="image" src="https://github.com/user-attachments/assets/5fad27f8-b9c0-40f3-925f-37faaae8c194" />

🗓️ Generated Itinerary with Tools On

<img width="1353" height="613" alt="image" src="https://github.com/user-attachments/assets/026cab7f-20c5-4826-8ed4-cb36eee2f159" />

<img width="1355" height="623" alt="image" src="https://github.com/user-attachments/assets/37ced893-0880-4717-b4f4-e51c5a199205" />

<img width="1355" height="613" alt="image" src="https://github.com/user-attachments/assets/1bf4657c-78dc-4f93-99fb-39073d0bc5aa" />

🗓️ Generated Details with Tools Off

<img width="1311" height="604" alt="image" src="https://github.com/user-attachments/assets/226a0c37-b72b-4dd5-930e-45e77c200204" />

🎓 Academic Association

Developed as part of:

Anudip AI Centre of Excellence: Advanced Data Analytics with AI

🔮 Future Enhancements
🌐 Multi-language support
🗺️ Interactive maps
🏨 Hotel recommendations
✈️ Flight integration
💳 Dynamic cost prediction
📱 Mobile application
🧠 Advanced AI memory
🎙️ Voice-based planning
🧳 Travel document assistant
📈 Personalized travel analytics
💼 Project Impact

Travelo demonstrates expertise in:

Agentic AI
Multi-Agent Systems
Python Development
API Integration
AI Orchestration
Backend Development
Data Engineering Concepts
Prompt Engineering
Travel Recommendation Systems
👥 Project Team
🚀 Developed By

Debasmita Sen (@debasmita-sen)

Souparno

📄 License

This project is licensed under the MIT License.

⭐ If you found this project interesting, consider giving it a star!

Travelo — Plan Smarter. Travel Better.
