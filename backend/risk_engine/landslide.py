def calculate_landslide_risk(rainfall, soil_moisture, slope):
    score = 0

    # Rainfall
    if rainfall >= 100:
        score += 35
    elif rainfall >= 60:
        score += 25
    elif rainfall >= 30:
        score += 15
    elif rainfall >= 10:
        score += 5

    # Soil moisture
    if soil_moisture >= 90:
        score += 35
    elif soil_moisture >= 70:
        score += 25
    elif soil_moisture >= 50:
        score += 15
    elif soil_moisture >= 30:
        score += 5

    # Slope in degrees
    if slope >= 35:
        score += 30
    elif slope >= 25:
        score += 20
    elif slope >= 15:
        score += 10
    elif slope >= 5:
        score += 5

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MODERATE"
    else:
        level = "LOW"

    return {
        "hazard": "Landslide",
        "score": min(score, 100),
        "level": level
    }