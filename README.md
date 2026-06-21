<div align="center">

# 🌍 Travelo — AI Powered Multi-Agent Travel Planner

<img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
<img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white"/>
<img src="https://img.shields.io/badge/Google%20Gemini-8E75B2?style=for-the-badge&logo=googlegemini&logoColor=white"/>
<img src="https://img.shields.io/badge/Groq-F55036?style=for-the-badge&logo=groq&logoColor=white"/>
<img src="https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white"/>
<img src="https://img.shields.io/badge/License-MIT-green?style=for-the-badge"/>

<br/>

> ✈️ **Plan Smarter. Travel Better. Powered by Agentic AI.**

An intelligent **Multi-Agent AI Travel Planner** that generates personalized travel itineraries by combining real-time weather, attractions, route planning, crowd analysis, budget optimization, food recommendations, and destination news.

Instead of relying on a single AI response, **Travelo** orchestrates multiple specialized AI agents to provide accurate, explainable, and data-driven travel recommendations.

🚀 *Developed using Agentic AI Architecture*

</div>

---

## 🎯 Project Overview

**Travelo** is an AI-powered travel planning platform built using a **Multi-Agent Architecture**.

Instead of a single Large Language Model attempting to solve every travel-related problem, Travelo delegates responsibilities to multiple specialized AI agents. Each agent focuses on a specific domain:

| Agent | Domain |
|---|---|
| 🏛️ Attractions Agent | Discover tourist spots |
| 🌦️ Weather Agent | Real-time forecasts |
| 🛣️ Route Agent | Route & transport planning |
| 📰 News Agent | Destination travel news |
| 👥 Crowd Agent | Crowd level estimation |
| 🍽️ Food Agent | Local cuisine recommendations |
| 💰 Budget Agent | Budget optimization |
| 🗓️ Itinerary Agent | Day-wise trip planning |

A central **Manager Agent** orchestrates all specialized agents and combines their outputs into a comprehensive travel plan.

This approach significantly improves **Accuracy**, **Reliability**, **Explainability**, and **Scalability**.

---

## 🚀 Key Features

### 🗓️ Personalized Travel Itinerary
Generate day-wise travel plans based on destination, travel dates, budget, interests, and number of travelers.

### 💰 Budget Optimization
Analyze whether the trip budget is **Under Budget**, **Balanced**, or **Over Budget** using predefined city cost datasets.

### 🌦️ Real-Time Weather Analysis
Fetch weather information and forecasts to recommend optimal activities.

### 🏛️ Attraction Discovery
Discover tourist attractions using **OpenStreetMap** and **Overpass APIs**.

### 🛣️ Route Planning
Generate travel routes and transportation recommendations.

### 🍽️ Food Recommendations
Suggest local cuisines and famous food spots.

### 👥 Crowd Estimation
Estimate crowd levels using holidays, weather, events, and travel dates.

### 📰 Destination News
Fetch relevant travel news to keep travelers informed.

### 🤖 AI-Powered Summary Generation
Generate intelligent travel summaries using **Google Gemini** and **Groq**.

---

## 🏗️ System Architecture

```
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
    ├── Budget Agent
    ├── Weather Agent
    ├── News Agent
    ├── Route Agent
    ├── Crowd Agent
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
```

---

## 🧠 Multi-Agent Workflow

### 1️⃣ Attraction Agent
Responsible for discovering attractions, filtering based on interests, and gathering location data.
**Provider:** OpenStreetMap, Overpass API

### 2️⃣ Budget Agent
Responsible for budget estimation, cost comparison, and expense categorization.
**Dataset:** `city_costs.json`

### 3️⃣ Weather Agent
Responsible for weather forecasts and travel suitability analysis.
**Provider:** WeatherAPI

### 4️⃣ News Agent
Responsible for destination news and important alerts.
**Provider:** NewsData.io

### 5️⃣ Route Agent
Responsible for route generation and transportation suggestions.
**Provider:** OpenRouteService

### 6️⃣ Crowd Agent
Responsible for crowd estimation and peak season analysis.
**Dataset:** `crowd_rules.json`

### 7️⃣ Food Agent
Responsible for local cuisine recommendations and food suggestions.

### 8️⃣ Itinerary Agent
Responsible for day-wise travel planning and activity scheduling.

### 9️⃣ Manager Agent
Responsible for combining all agent outputs and generating the final travel summary.

---

## 🛠️ Tech Stack

| Category | Technologies |
|---|---|
| **Backend** | Python, Flask |
| **AI Models** | Groq, Google Gemini |
| **APIs** | OpenStreetMap, Overpass API, WeatherAPI, OpenRouteService, NewsData.io |
| **Database** | SQLite |
| **Environment** | Hatch |
| **Testing** | Pytest |
| **Version Control** | Git, GitHub |

---

## 📂 Project Structure

```
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
```

---

## ⚙️ Installation

**1. Clone the repository:**
```bash
git clone https://github.com/debasmita-sen/Travelo.git
```

**2. Navigate into the project:**
```bash
cd Travelo
```

**3. Create environment:**
```bash
hatch env create
```

**4. Run the application:**
```bash
hatch run app
```

**5. Open in browser:**
```
http://127.0.0.1:5000
```

---

## 🔑 Environment Variables

Create a `.env` file in the project root:

```env
LLM_PROVIDER=groq

GROQ_API_KEY=
GEMINI_API_KEY=
WEATHER_API_KEY=
OPENROUTESERVICE_API_KEY=
NEWSDATA_API_KEY=
FLASK_SECRET_KEY=
```

---

## 📸 Application Screenshots

### 🏠 Home / Planner Page

<img width="1346" height="633" alt="image" src="https://github.com/user-attachments/assets/03c9372d-cac6-48f6-9db2-fa0f34fbb649" />

<img width="1352" height="628" alt="image" src="https://github.com/user-attachments/assets/5fad27f8-b9c0-40f3-925f-37faaae8c194" />

### 🗓️ Generated Itinerary with Tools On

<img width="1353" height="613" alt="image" src="https://github.com/user-attachments/assets/026cab7f-20c5-4826-8ed4-cb36eee2f159" />

<img width="1355" height="623" alt="image" src="https://github.com/user-attachments/assets/37ced893-0880-4717-b4f4-e51c5a199205" />

<img width="1355" height="613" alt="image" src="https://github.com/user-attachments/assets/1bf4657c-78dc-4f93-99fb-39073d0bc5aa" />

### 🗓️ Generated Details with Tools Off

<img width="1311" height="604" alt="image" src="https://github.com/user-attachments/assets/226a0c37-b72b-4dd5-930e-45e77c200204" />

---

## 🎓 Academic Association

> Developed as part of:
> **Anudip AI Centre of Excellence — Advanced Data Analytics with AI**

---

## 🔮 Future Enhancements

- 🌐 Multi-language support
- 🗺️ Interactive maps
- 🏨 Hotel recommendations
- ✈️ Flight integration
- 💳 Dynamic cost prediction
- 📱 Mobile application
- 🧠 Advanced AI memory
- 🎙️ Voice-based planning
- 🧳 Travel document assistant
- 📈 Personalized travel analytics

---

## 💼 Project Impact

Travelo demonstrates expertise in:

**Agentic AI** · **Multi-Agent Systems** · **Python Development** · **API Integration** · **AI Orchestration** · **Backend Development** · **Data Engineering Concepts** · **Prompt Engineering** · **Travel Recommendation Systems**

---

## 👥 Project Team

### 🚀 Developed By

- **Debasmita Sen** — [@debasmita-sen](https://github.com/debasmita-sen)
- **Souparno**

---

## 📄 License

This project is licensed under the **MIT License**.

---

<div align="center">

⭐ **If you found this project interesting, consider giving it a star!**

*Travelo — Plan Smarter. Travel Better.*

</div>
