from pathlib import Path
import joblib


PROJECT_ROOT = Path(__file__).resolve().parents[2]


FLOOD_MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "flood"
    / "flood_model.joblib"
)

LANDSLIDE_MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "landslide"
    / "landslide_model.joblib"
)

STORM_MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "storm"
    / "storm_model.joblib"
)


# Load trained models
flood_model = joblib.load(FLOOD_MODEL_PATH)

landslide_model = joblib.load(
    LANDSLIDE_MODEL_PATH
)

storm_model = joblib.load(
    STORM_MODEL_PATH
)


# ============================================================
# FLOOD MODEL
# ============================================================

def predict_flood(
    rainfall,
    rainfall_3h,
    rainfall_6h,
    rainfall_24h,
    previous_water_level
):

    prediction = flood_model.predict([
        [
            rainfall,
            rainfall_3h,
            rainfall_6h,
            rainfall_24h,
            previous_water_level
        ]
    ])[0]

    probability = flood_model.predict_proba([
        [
            rainfall,
            rainfall_3h,
            rainfall_6h,
            rainfall_24h,
            previous_water_level
        ]
    ])[0][1]

    if prediction == 1:

        if probability >= 0.75:
            level = "HIGH"

        else:
            level = "MODERATE"

    else:
        level = "LOW"


    return {
        "hazard": "Flood",
        "prediction": int(prediction),
        "probability": round(
            probability * 100,
            2
        ),
        "level": level
    }


# ============================================================
# LANDSLIDE MODEL
# ============================================================

def predict_landslide(
    rainfall,
    soil_moisture,
    slope
):

    prediction = landslide_model.predict([
        [
            rainfall,
            soil_moisture,
            slope
        ]
    ])[0]

    probability = landslide_model.predict_proba([
        [
            rainfall,
            soil_moisture,
            slope
        ]
    ])[0][1]


    if prediction == 1:

        if probability >= 0.75:
            level = "HIGH"

        else:
            level = "MODERATE"

    else:
        level = "LOW"


    return {
        "hazard": "Landslide",
        "prediction": int(prediction),
        "probability": round(
            probability * 100,
            2
        ),
        "level": level
    }


# ============================================================
# STORM MODEL
# ============================================================

def predict_storm(
    latitude,
    longitude,
    central_pressure,
    pressure_drop,
    wind_speed
):

    prediction = storm_model.predict([
        [
            latitude,
            longitude,
            central_pressure,
            pressure_drop,
            wind_speed
        ]
    ])[0]

    probability = storm_model.predict_proba([
        [
            latitude,
            longitude,
            central_pressure,
            pressure_drop,
            wind_speed
        ]
    ])[0][1]


    if prediction == 1:

        if probability >= 0.75:
            level = "HIGH"

        else:
            level = "MODERATE"

    else:
        level = "LOW"


    return {
        "hazard": "Severe Storm",
        "prediction": int(prediction),
        "probability": round(
            probability * 100,
            2
        ),
        "level": level
    }