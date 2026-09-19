from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx

from models.ml_models import (
    predict_flood,
    predict_landslide,
    predict_storm
)

from cwc_data import get_cwc_data


app = FastAPI(
    title="DisasterShield AI",
    description="Multi-Hazard Early Warning and Risk Prediction System",
    version="1.0.0"
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


class EnvironmentInput(BaseModel):
    latitude: float
    longitude: float
    rainfall: float
    rainfall_3h: float
    rainfall_6h: float
    rainfall_24h: float
    previous_water_level: float
    water_level: float
    soil_moisture: float
    wind_speed: float
    pressure: float
    pressure_drop: float
    slope: float


class LocationInput(BaseModel):
    latitude: float
    longitude: float


def calculate_overall_risk(flood, landslide, storm):
    scores = [
        flood["probability"],
        landslide["probability"],
        storm["probability"]
    ]

    overall_score = max(scores)

    if overall_score >= 75:
        level = "HIGH"
    elif overall_score >= 40:
        level = "MODERATE"
    else:
        level = "LOW"

    return {
        "score": round(overall_score, 2),
        "level": level
    }


def generate_alerts(flood, landslide, storm):
    alerts = []

    if flood["level"] == "HIGH":
        alerts.append({
            "hazard": "Flood",
            "level": "HIGH",
            "message": "High flood risk detected.",
            "action": "Move to safer or elevated areas and monitor official flood warnings."
        })
    elif flood["level"] == "MODERATE":
        alerts.append({
            "hazard": "Flood",
            "level": "MODERATE",
            "message": "Moderate flood risk detected.",
            "action": "Monitor rainfall and river water levels closely."
        })

    if landslide["level"] == "HIGH":
        alerts.append({
            "hazard": "Landslide",
            "level": "HIGH",
            "message": "High landslide risk detected.",
            "action": "Avoid steep slopes and areas vulnerable to landslides."
        })
    elif landslide["level"] == "MODERATE":
        alerts.append({
            "hazard": "Landslide",
            "level": "MODERATE",
            "message": "Moderate landslide risk detected.",
            "action": "Avoid unnecessary travel near steep or unstable slopes."
        })

    if storm["level"] == "HIGH":
        alerts.append({
            "hazard": "Severe Storm",
            "level": "HIGH",
            "message": "High severe-storm risk detected.",
            "action": "Stay indoors, secure loose objects, and monitor official weather warnings."
        })
    elif storm["level"] == "MODERATE":
        alerts.append({
            "hazard": "Severe Storm",
            "level": "MODERATE",
            "message": "Moderate severe-storm risk detected.",
            "action": "Monitor wind conditions and official weather warnings."
        })

    if len(alerts) == 0:
        alerts.append({
            "hazard": "System",
            "level": "LOW",
            "message": "No significant hazard detected.",
            "action": "Continue monitoring environmental conditions."
        })

    return alerts


@app.get("/")
def home():
    return {
        "message": "DisasterShield AI Backend is running!"
    }


@app.get("/api/status")
def status():
    return {
        "status": "online",
        "project": "DisasterShield AI",
        "version": "1.0.0",
        "hazards": ["flood", "landslide", "storm"],
        "prediction_engine": "Machine Learning"
    }


@app.get("/api/models")
def model_information():
    return {
        "engine": "Random Forest Classifier",
        "models": [
            {
                "hazard": "Flood",
                "features": [
                    "rainfall",
                    "rainfall_3h",
                    "rainfall_6h",
                    "rainfall_24h",
                    "previous_water_level"
                ],
                "data": "Real CWC telemetry rainfall and river water-level data",
                "output": "Flood risk probability"
            },
            {
                "hazard": "Landslide",
                "features": [
                    "rainfall",
                    "soil_moisture",
                    "slope"
                ],
                "data": "Prototype dataset",
                "output": "Risk probability"
            },
            {
                "hazard": "Severe Storm",
                "features": [
                    "latitude",
                    "longitude",
                    "central_pressure_hpa",
                    "pressure_drop_hpa",
                    "wind_speed_kt"
                ],
                "data": "IMD 2025 Best Track data",
                "output": "Risk probability"
            }
        ],
        "validation_status":
            "Flood model uses real CWC observations; storm model uses IMD observations; landslide model remains a prototype model."
    }


@app.post("/api/weather")
async def get_weather(location: LocationInput):
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={location.latitude}"
        f"&longitude={location.longitude}"
        "&current="
        "temperature_2m,"
        "rain,"
        "wind_speed_10m,"
        "pressure_msl,"
        "soil_moisture_0_to_1cm"
        "&timezone=auto"
    )

    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        weather = response.json()

    current = weather["current"]

    return {
        "location": {
            "latitude": location.latitude,
            "longitude": location.longitude
        },
        "weather": {
            "temperature": current["temperature_2m"],
            "rain": current["rain"],
            "wind_speed": current["wind_speed_10m"],
            "pressure": current["pressure_msl"],
            "soil_moisture": current["soil_moisture_0_to_1cm"]
        }
    }


@app.get("/api/cwc")
def cwc_data():
    stations = get_cwc_data()

    return {
        "source": "Central Water Commission (CWC)",
        "data_type": "Real telemetry observations",
        "note": "Values are calculated from the latest available observations in the uploaded CWC datasets.",
        "stations": stations
    }


@app.post("/api/predict")
def predict(data: EnvironmentInput):

    flood = predict_flood(
        data.rainfall,
        data.rainfall_3h,
        data.rainfall_6h,
        data.rainfall_24h,
        data.previous_water_level
    )

    landslide = predict_landslide(
        data.rainfall,
        data.soil_moisture,
        data.slope
    )

    storm = predict_storm(
        data.latitude,
        data.longitude,
        data.pressure,
        data.pressure_drop,
        data.wind_speed
    )

    overall = calculate_overall_risk(
        flood,
        landslide,
        storm
    )

    alerts = generate_alerts(
        flood,
        landslide,
        storm
    )

    return {
        "location": {
            "latitude": data.latitude,
            "longitude": data.longitude
        },
        "environment": {
            "rainfall": data.rainfall,
            "rainfall_3h": data.rainfall_3h,
            "rainfall_6h": data.rainfall_6h,
            "rainfall_24h": data.rainfall_24h,
            "previous_water_level": data.previous_water_level,
            "water_level": data.water_level,
            "soil_moisture": data.soil_moisture,
            "wind_speed": data.wind_speed,
            "pressure": data.pressure,
            "pressure_drop": data.pressure_drop,
            "slope": data.slope
        },
        "predictions": {
            "flood": flood,
            "landslide": landslide,
            "storm": storm
        },
        "overall_risk": overall,
        "alerts": alerts
    }
