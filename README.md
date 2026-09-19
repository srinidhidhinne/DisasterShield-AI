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

---

## ✨ Key Features

* 🌊 **Flood Risk Assessment** — Estimates flood risk using rainfall and water-level conditions.
* ⛰️ **Landslide Risk Assessment** — Considers rainfall, soil moisture, and slope conditions.
* ⛈️ **Severe Storm Risk Assessment** — Uses meteorological parameters such as wind speed, pressure, and pressure drop.
* 🗺️ **Interactive Map** — Displays the selected location and available monitoring stations.
* 📊 **Overall Risk Score** — Combines individual hazard assessments into a single risk level.
* 🚨 **Smart Alert** — Identifies the highest-priority hazard and generates a corresponding warning.
* 🛡️ **Recommended Actions** — Provides practical precautionary actions based on the identified hazard.
* 📡 **Environmental Monitoring** — Displays available rainfall and water-level observations from CWC datasets.
* ⚡ **Fast API-Based Predictions** — Connects the React dashboard with a FastAPI backend for real-time prototype predictions.

---

## 🤖 Machine Learning

DisasterShield AI uses hazard-specific machine learning models to estimate the risk associated with different environmental conditions.

### Flood Model

The flood model uses:

- Rainfall
- 3-hour rainfall
- 6-hour rainfall
- 24-hour rainfall
- Previous water level

A **Random Forest Classifier** is used to estimate flood-risk probability.

### Landslide Model

The landslide risk assessment considers:

- Rainfall
- Soil moisture
- Slope

### Severe Storm Model

The severe storm assessment considers:

- Latitude
- Longitude
- Central pressure
- Pressure drop
- Wind speed

The models produce a probability and risk level such as **LOW, MODERATE, or HIGH**.

> The predictions are intended as prototype risk-assessment outputs and should not be treated as official disaster warnings.

---

## 📡 Data Sources

DisasterShield AI uses historical and environmental datasets to support its prototype risk-assessment models.

### Central Water Commission (CWC)

CWC datasets are used for rainfall and river water-level information.

The dashboard can display available monitoring-station observations such as:

- Rainfall
- Previous water level
- Current water level
- 3-hour rainfall
- 6-hour rainfall
- 24-hour rainfall
- Observation time

The CWC data used in this prototype represents the **latest available observations in the uploaded datasets**, not live telemetry.

### India Meteorological Department (IMD)

Historical meteorological information from IMD is used for the severe-storm risk modelling component.

### Geological Survey of India (GSI)

GSI landslide inventory data is used as a reference dataset for the landslide component.

> The datasets used in this prototype are historical and are intended for research, demonstration, and model development. They are not a substitute for official emergency alerts or government disaster-warning systems.

---

## 🛠️ Technology Stack

### Frontend

- React.js
- Vite
- JavaScript
- Leaflet
- React Leaflet
- HTML5
- CSS3

### Backend

- Python
- FastAPI
- Uvicorn

### Machine Learning

- Scikit-learn
- Pandas
- Joblib

### Data & Visualization

- CSV datasets
- Historical environmental observations
- Interactive geographical maps

### Development Tools

- Visual Studio Code
- Git
- GitHub

---

## 📁 Project Structure

```text
DisasterShield/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── package.json
│   └── ...
│
├── backend/
│   ├── main.py
│   ├── cwc_data.py
│   ├── models/
│   │   └── ml_models.py
│   ├── risk_engine/
│   │   ├── flood.py
│   │   ├── landslide.py
│   │   └── storm.py
│   └── ...
│
├── data/
│   ├── raw/
│   └── real/
│
├── ml/
│   ├── flood/
│   ├── landslide/
│   └── storm/
│
├── screenshots/
│   ├── img1.jpg
│   ├── img2.jpg
│   ├── img3.jpg
│   └── img4.jpg
│
├── .gitignore
└── README.md

---

## 🖥️ Dashboard

The DisasterShield AI dashboard provides a unified view of environmental conditions, hazard predictions, overall risk, alerts, and recommended actions.

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

---

## 📊 Model Performance

The flood model was evaluated using a held-out test set from the prepared historical dataset.

| Metric | Score |
|---|---:|
| Accuracy | 86.84% |
| Precision | 68.50% |
| Recall | 83.25% |
| F1 Score | 75.16% |

The flood model uses a station-specific high-water risk proxy derived from historical observations.

These results represent performance on the prepared historical dataset and should not be interpreted as real-world operational warning accuracy.

---

## 🧪 Testing & Validation

The prototype was tested through multiple stages to verify the functionality of the system.

### Backend Testing

- Tested the FastAPI prediction endpoint with representative environmental inputs.
- Verified that the API returns flood, landslide, and severe-storm predictions.
- Verified probability and risk-level outputs.
- Tested the overall risk calculation.

### Frontend Testing

- Tested map-based location selection.
- Tested display of environmental conditions.
- Tested hazard prediction cards.
- Tested overall risk display.
- Tested Smart Alert generation.
- Tested recommended safety actions.
- Tested CWC monitoring-station display.

### End-to-End Testing

The complete flow was tested from the React frontend to the FastAPI backend and back to the dashboard.

```text
User Input
    ↓
React Frontend
    ↓
FastAPI Backend
    ↓
ML Models
    ↓
Risk Engine
    ↓
Prediction Response
    ↓
Dashboard

---

## 🔄 How It Works

1. The user selects a geographical location on the interactive map.
2. Environmental and meteorological parameters are collected or provided.
3. The relevant parameters are passed to the corresponding hazard models.
4. Flood, landslide, and severe-storm risks are assessed independently.
5. The Risk Engine combines the individual hazard results.
6. An overall risk level is generated.
7. The system identifies the highest-priority hazard.
8. Smart Alert generates a hazard-specific warning.
9. Recommended precautionary actions are displayed to the user.

---

## 💡 What Makes DisasterShield AI Different

Instead of focusing on a single disaster type, DisasterShield AI combines multiple hazard assessments into one location-aware platform.

The system connects:

**Environmental Data → ML Models → Risk Engine → Map → Smart Alert → Recommended Action**

This allows users to view multiple potential hazards and their corresponding environmental conditions through a single interface.

---

## 🚀 Future Scope

The platform can be further enhanced with:

- Real-time integration with CWC and IMD data sources
- Continuous weather and environmental data updates
- Improved hazard prediction models using larger datasets
- Satellite and remote-sensing data integration
- Additional hazards such as wildfires and extreme heat
- Location-based notifications and mobile alerts
- Historical risk visualization and trend analysis
- Integration with official emergency-warning systems
- Deployment on cloud infrastructure for large-scale use

---

## ⚠️ Limitations

- The prototype uses historical datasets rather than continuously updated live data.
- Hazard predictions depend on the quality and availability of input data.
- The flood model uses a historical high-water risk proxy rather than an official flood-warning label.
- Landslide risk assessment requires further validation with environmental predictors and independent events.
- The severe-storm model requires further validation on independent data because of limitations in the available training dataset.
- Model outputs should be treated as risk-assessment support and not as official disaster warnings.
- Further testing with larger, independent, and continuously updated datasets is required before real-world deployment.