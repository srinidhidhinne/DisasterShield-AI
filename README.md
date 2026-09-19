# 🛡️ DisasterShield AI

## Multi-Hazard Early Warning & Risk Prediction Platform

DisasterShield AI is a multi-hazard risk assessment and early-warning support platform designed to help users understand potential disaster risks by analyzing environmental and meteorological conditions.

The platform combines **machine learning, environmental data, geographical visualization, risk scoring, and smart alerts** to assess the risk of:

* 🌊 Floods
* ⛰️ Landslides
* ⛈️ Severe Storms

The goal is to provide a single platform where environmental conditions and multiple hazard risks can be viewed and understood together.

---

## 🚨 Problem

Natural disasters such as floods, landslides, and severe storms can develop from changing environmental and meteorological conditions.

However, information related to different hazards is often spread across different datasets and sources.

There is a need for a system that can:

* Analyze multiple environmental factors
* Assess different hazards together
* Present risk information geographically
* Provide easy-to-understand warnings
* Suggest appropriate precautionary actions

---

## 💡 Our Solution

DisasterShield AI brings multiple hazard-risk assessments together into one interactive dashboard.

The system takes environmental and meteorological inputs, processes them through hazard-specific models, and presents the results through:

* Overall risk assessment
* Hazard-wise risk levels
* Interactive map
* Environmental conditions
* Smart alerts
* Recommended safety actions

### System Architecture

```text
Environmental Data
        ↓
Data Processing
        ↓
Hazard Risk Models
        ↓
Risk Engine
        ↓
Multi-Hazard Dashboard
        ↓
Map + Risk + Smart Alert + Recommended Action
```

---

## ✨ Key Features

### 🌊 Flood Risk Prediction

Uses factors such as:

* Rainfall
* 3-hour rainfall
* 6-hour rainfall
* 24-hour rainfall
* Previous river water level

### ⛰️ Landslide Risk Assessment

Considers environmental factors including:

* Rainfall
* Soil moisture
* Slope

### ⛈️ Severe Storm Risk Assessment

Uses meteorological factors including:

* Latitude
* Longitude
* Central pressure
* Pressure drop
* Wind speed

### 🗺️ Interactive Risk Map

Users can select a geographical location and view the corresponding environmental and hazard information.

### 📊 Overall Risk

The platform combines the individual hazard assessments into an overall risk assessment.

### 🚨 Smart Alert

The Smart Alert identifies the highest-priority hazard and displays:

* Hazard name
* Risk level
* Probability
* Hazard-specific warning
* Recommended actions

### 🌦️ Environmental Monitoring

The dashboard displays environmental conditions used by the prediction system, including rainfall, water level, soil moisture, wind speed, pressure, and other relevant parameters.

### 🛟 Recommended Actions

The system provides precautionary actions depending on the identified hazard.

---

## 🤖 Machine Learning

### Flood Model

The flood model uses a **Random Forest Classifier**.

Input features:

```text
Rainfall
Rainfall 3h
Rainfall 6h
Rainfall 24h
Previous Water Level
```

The training data was created from historical CWC observations using a station-specific high-water risk proxy.

### Landslide Model

The project includes the landslide risk-engine structure and geological inventory data.

Further machine-learning development requires suitable environmental predictor datasets for robust training.

### Storm Model

The storm model uses:

```text
Latitude
Longitude
Central Pressure
Pressure Drop
Wind Speed
```

The current storm model is part of the prototype and requires further validation with independent predictive features before real-world deployment.

---

## 🌐 Data Sources

The project uses information from publicly available environmental and meteorological sources, including:

* **Central Water Commission (CWC)** — rainfall and river water-level observations
* **India Meteorological Department (IMD)** — meteorological and storm-related information
* **Geological Survey of India (GSI)** — geological and landslide inventory information

Some datasets used by the prototype are historical datasets rather than live real-time feeds.

---

## 🛠️ Technology Stack

### Frontend

* React
* Vite
* JavaScript
* React Leaflet
* Leaflet
* CSS

### Backend

* Python
* FastAPI
* Uvicorn

### Machine Learning

* Pandas
* Scikit-learn
* Joblib

### Data Processing

* Python
* Pandas

---

## 📁 Project Structure

```text
DisasterShield/
│
├── frontend/
│   └── React + Vite application
│
├── backend/
│   ├── main.py
│   ├── cwc_data.py
│   │
│   ├── models/
│   │   └── ml_models.py
│   │
│   └── risk_engine/
│       ├── flood.py
│       ├── landslide.py
│       └── storm.py
│
├── data/
│   ├── raw/
│   └── real/
│
└── ml/
    ├── flood/
    ├── landslide/
    └── storm/
```

---

## 🖥️ Dashboard

The DisasterShield AI dashboard provides a unified view of:

```text
Location
   ↓
Environmental Conditions
   ↓
Hazard Predictions
   ↓
Overall Risk
   ↓
Smart Alert
   ↓
Recommended Actions
```

<!-- Add screenshots here -->

### Dashboard Screenshot

```text
Add your dashboard screenshot here
```

---

## ⚙️ How to Run

### 1. Clone the Repository

```bash
git clone https://github.com/srinidhidhinne/DisasterShield-AI.git
cd DisasterShield-AI
```

### 2. Start the Backend

```powershell
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install fastapi uvicorn httpx pandas scikit-learn joblib
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

### 3. Start the Frontend

Open another terminal:

```powershell
cd frontend
npm install
npm run dev
```

Frontend:

```text
http://localhost:5173
```

---

## 🔌 API

### CWC Data

```text
GET /api/cwc
```

Provides available CWC observation data used by the dashboard.

### Weather Data

```text
GET /api/weather
```

Provides weather-related information used by the system.

### Prediction

```text
POST /api/predict
```

Runs the multi-hazard prediction and risk assessment.

### Model Information

```text
GET /api/models
```

Provides information about the available models.

---

## 📈 Future Scope

The platform can be extended with:

* Real-time weather and sensor data
* Satellite imagery
* Advanced GIS hazard layers
* Improved landslide prediction
* More robust temporal model validation
* Location-specific risk calibration
* Mobile notifications
* SMS alerts
* Additional disaster types
* Historical disaster analysis
* Explainable AI
* Cloud deployment
* Scalable real-time infrastructure

---

## ⚠️ Limitations

DisasterShield AI is a **hackathon prototype** and is not an operational disaster-warning system.

Important limitations include:

* Some datasets are historical rather than live.
* Flood labels are based on a high-water risk proxy rather than an official flood-warning label.
* Model performance on historical data does not guarantee future real-world performance.
* The current storm model requires further validation because of limitations in the available training data.
* The landslide component requires additional environmental predictor data for stronger machine-learning development.
* Real-world deployment would require continuous data ingestion, extensive validation, calibration, and domain-expert review.

---

## 🌍 Impact

DisasterShield AI aims to make multi-hazard environmental information easier to understand by bringing different data sources and risk assessments together in one platform.

Potential applications include:

* Disaster preparedness
* Environmental monitoring
* Early awareness
* Risk communication
* Location-based hazard assessment
* Emergency-management support

---

## 👥 Hackathon Project

**Project:** DisasterShield AI
**Category:** Open Innovation
**Hackathon:** HackDevengers 2.0

---

## ⚠️ Disclaimer

DisasterShield AI is an experimental prototype developed for hackathon, research, demonstration, and educational purposes.

Risk estimates generated by the system should not replace official government warnings, emergency services, or professional disaster-management decisions.
