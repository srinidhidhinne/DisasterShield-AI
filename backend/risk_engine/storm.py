def calculate_storm_risk(wind_speed, rainfall, pressure):
    score = 0

    # Wind speed in km/h
    if wind_speed >= 100:
        score += 45
    elif wind_speed >= 70:
        score += 35
    elif wind_speed >= 40:
        score += 20
    elif wind_speed >= 20:
        score += 10

    # Rainfall
    if rainfall >= 100:
        score += 30
    elif rainfall >= 60:
        score += 20
    elif rainfall >= 30:
        score += 10

    # Atmospheric pressure in hPa
    if pressure < 980:
        score += 25
    elif pressure < 1000:
        score += 15
    elif pressure < 1010:
        score += 5

    if score >= 70:
        level = "HIGH"
    elif score >= 40:
        level = "MODERATE"
    else:
        level = "LOW"

    return {
        "hazard": "Severe Storm",
        "score": min(score, 100),
        "level": level
    }