import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]

RAINFALL_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "rainfall"
    / "cwc_ap_rainfall.csv"
)

WATER_LEVEL_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "storm"
    / "godavari_water_level.csv"
)


def clean_columns(data):
    data.columns = (
        data.columns
        .astype(str)
        .str.strip()
        .str.replace(r"\s+", " ", regex=True)
    )
    return data


def find_column(data, words):
    for column in data.columns:
        column_clean = (
            column.lower()
            .replace(" ", "")
            .replace("_", "")
            .replace("-", "")
            .replace("(", "")
            .replace(")", "")
        )

        if all(word.lower() in column_clean for word in words):
            return column

    return None


def get_cwc_data():
    rainfall = clean_columns(pd.read_csv(RAINFALL_PATH))
    water = clean_columns(pd.read_csv(WATER_LEVEL_PATH))

    rainfall_time_column = find_column(
        rainfall, ["data", "acquisition", "time"]
    )
    rainfall_value_column = find_column(
        rainfall, ["telemetry", "hourly", "rainfall"]
    )
    water_time_column = find_column(
        water, ["data", "acquisition", "time"]
    )
    water_value_column = find_column(
        water, ["river", "water", "level", "telemetry", "hourly"]
    )

    if rainfall_time_column is None:
        raise ValueError(
            f"Could not find rainfall time column. Available: {list(rainfall.columns)}"
        )

    if rainfall_value_column is None:
        raise ValueError(
            f"Could not find rainfall value column. Available: {list(rainfall.columns)}"
        )

    if water_time_column is None:
        raise ValueError(
            f"Could not find water-level time column. Available: {list(water.columns)}"
        )

    if water_value_column is None:
        raise ValueError(
            f"Could not find water-level column. Available: {list(water.columns)}"
        )

    rainfall["time"] = pd.to_datetime(
        rainfall[rainfall_time_column], errors="coerce"
    )
    water["time"] = pd.to_datetime(
        water[water_time_column], errors="coerce"
    )

    rainfall["rainfall"] = pd.to_numeric(
        rainfall[rainfall_value_column], errors="coerce"
    )
    water["water_level"] = pd.to_numeric(
        water[water_value_column], errors="coerce"
    )

    rainfall = rainfall.dropna(
        subset=["Station", "Latitude", "Longitude", "time", "rainfall"]
    )
    water = water.dropna(
        subset=["Station", "time", "water_level"]
    )

    common_stations = sorted(
        set(rainfall["Station"].dropna())
        & set(water["Station"].dropna())
    )

    rainfall = rainfall[
        rainfall["Station"].isin(common_stations)
    ].copy()

    water = water[
        water["Station"].isin(common_stations)
    ].copy()

    rainfall["time"] = rainfall["time"].dt.floor("h")
    water["time"] = water["time"].dt.floor("h")

    # Combine duplicate hourly observations.
    rainfall = (
        rainfall
        .groupby(
            ["Station", "Latitude", "Longitude", "time"],
            as_index=False
        )["rainfall"]
        .sum()
    )

    water = (
        water
        .groupby(
            ["Station", "time"],
            as_index=False
        )["water_level"]
        .mean()
    )

    stations = []

    # Calculate real rolling rainfall and previous water level
    # independently for each station.
    for station in common_stations:
        r = rainfall[rainfall["Station"] == station].copy()
        w = water[water["Station"] == station].copy()

        r = r.sort_values("time").reset_index(drop=True)
        w = w.sort_values("time").reset_index(drop=True)

        if r.empty or w.empty:
            continue

        r["rainfall_3h"] = (
            r["rainfall"]
            .rolling(3, min_periods=1)
            .sum()
        )

        r["rainfall_6h"] = (
            r["rainfall"]
            .rolling(6, min_periods=1)
            .sum()
        )

        r["rainfall_24h"] = (
            r["rainfall"]
            .rolling(24, min_periods=1)
            .sum()
        )

        # Latest rainfall observation.
        latest_rain = r.iloc[-1]

        # Latest water-level observation and previous observation.
        latest_water = w.iloc[-1]
        previous_water = (
            float(w.iloc[-2]["water_level"])
            if len(w) >= 2
            else float(latest_water["water_level"])
        )

        # Use the latest available observation time from either source.
        latest_time = max(
            latest_rain["time"],
            latest_water["time"]
        )

        stations.append({
            "station": station,
            "latitude": float(latest_rain["Latitude"]),
            "longitude": float(latest_rain["Longitude"]),
            "rainfall": round(float(latest_rain["rainfall"]), 3),
            "rainfall_3h": round(float(latest_rain["rainfall_3h"]), 3),
            "rainfall_6h": round(float(latest_rain["rainfall_6h"]), 3),
            "rainfall_24h": round(float(latest_rain["rainfall_24h"]), 3),
            "water_level": round(float(latest_water["water_level"]), 3),
            "previous_water_level": round(previous_water, 3),
            "time": str(latest_time)
        })

    stations.sort(
        key=lambda x: x["time"],
        reverse=True
    )

    return stations
