def calculate_flood_risk(rainfall, water_level, soil_moisture):
    score = 0

    # Rainfall contribution
    if rainfall >= 100:
        score += 40
    elif rainfall >= 60:
        score += 30
    elif rainfall >= 30:
        score += 20
    elif rainfall >= 10:
        score += 10

    # Water level contribution
    if water_level >= 90:
        score += 40
    elif water_level >= 70:
        score += 30
    elif water_level >= 50:
        score += 20
    elif water_level >= 30:
        score += 10

    # Soil moisture contribution
    if soil_moisture >= 90:
        score += 20
    elif soil_moisture >= 70:
        score += 15
    elif soil_moisture >= 50:
        score += 10
    elif soil_moisture >= 30:
        score += 5

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MODERATE"
    else:
        level = "LOW"

    return {
        "hazard": "Flood",
        "score": min(score, 100),
        "level": level
    }