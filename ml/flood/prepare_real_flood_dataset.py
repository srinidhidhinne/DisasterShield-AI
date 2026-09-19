import pandas as pd
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]

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

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "flood"
    / "flood_training_data.csv"
)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

rainfall = pd.read_csv(RAINFALL_PATH)

water = pd.read_csv(WATER_LEVEL_PATH)


# ------------------------------------------------------------
# CONVERT TIME
# ------------------------------------------------------------

rainfall["time"] = pd.to_datetime(
    rainfall["Data Acquisition Time"],
    dayfirst=True,
    errors="coerce"
)

water["time"] = pd.to_datetime(
    water["Data Acquisition Time"],
    dayfirst=True,
    errors="coerce"
)


# ------------------------------------------------------------
# KEEP COMMON STATIONS
# ------------------------------------------------------------

common_stations = sorted(
    set(rainfall["Station"].dropna())
    &
    set(water["Station"].dropna())
)

print()
print("=" * 60)
print("REAL CWC FLOOD DATA PREPARATION")
print("=" * 60)
print()

print("Common stations:")
for station in common_stations:
    print("-", station)

print()


rainfall = rainfall[
    rainfall["Station"].isin(common_stations)
].copy()

water = water[
    water["Station"].isin(common_stations)
].copy()


# ------------------------------------------------------------
# SELECT REQUIRED COLUMNS
# ------------------------------------------------------------

rainfall = rainfall[
    [
        "Station",
        "Latitude",
        "Longitude",
        "time",
        "Telemetry Hourly Rainfall (mm)"
    ]
].copy()

water = water[
    [
        "Station",
        "time",
        "River Water Level Telemetry Hourly (meter)"
    ]
].copy()


rainfall = rainfall.rename(
    columns={
        "Telemetry Hourly Rainfall (mm)": "rainfall"
    }
)

water = water.rename(
    columns={
        "River Water Level Telemetry Hourly (meter)":
        "water_level"
    }
)


# ------------------------------------------------------------
# REMOVE INVALID VALUES
# ------------------------------------------------------------

rainfall = rainfall.dropna(
    subset=[
        "Station",
        "time",
        "rainfall"
    ]
)

water = water.dropna(
    subset=[
        "Station",
        "time",
        "water_level"
    ]
)


# ------------------------------------------------------------
# ROUND TIME TO HOURLY
# ------------------------------------------------------------

rainfall["time"] = rainfall["time"].dt.floor("h")
water["time"] = water["time"].dt.floor("h")


# Multiple readings in the same hour
rainfall = (
    rainfall
    .groupby(
        [
            "Station",
            "Latitude",
            "Longitude",
            "time"
        ],
        as_index=False
    )["rainfall"]
    .sum()
)

water = (
    water
    .groupby(
        [
            "Station",
            "time"
        ],
        as_index=False
    )["water_level"]
    .mean()
)


# ------------------------------------------------------------
# MERGE RAINFALL + WATER LEVEL
# ------------------------------------------------------------

data = pd.merge(
    rainfall,
    water,
    on=["Station", "time"],
    how="inner"
)


# ------------------------------------------------------------
# SORT BY STATION AND TIME
# ------------------------------------------------------------

data = data.sort_values(
    ["Station", "time"]
).reset_index(drop=True)


# ------------------------------------------------------------
# CREATE RAINFALL FEATURES
# ------------------------------------------------------------

data["rainfall_3h"] = (
    data
    .groupby("Station")["rainfall"]
    .transform(
        lambda x:
        x.rolling(3, min_periods=1).sum()
    )
)

data["rainfall_6h"] = (
    data
    .groupby("Station")["rainfall"]
    .transform(
        lambda x:
        x.rolling(6, min_periods=1).sum()
    )
)

data["rainfall_24h"] = (
    data
    .groupby("Station")["rainfall"]
    .transform(
        lambda x:
        x.rolling(24, min_periods=1).sum()
    )
)


# ------------------------------------------------------------
# CREATE PREVIOUS WATER LEVEL
# ------------------------------------------------------------

data["previous_water_level"] = (
    data
    .groupby("Station")["water_level"]
    .shift(1)
)


# ------------------------------------------------------------
# CREATE FUTURE 6-HOUR MAX WATER LEVEL
# ------------------------------------------------------------

data["future_water_level"] = (
    data
    .groupby("Station")["water_level"]
    .transform(
        lambda x:
        x.shift(-1)
        .rolling(
            6,
            min_periods=1
        )
        .max()
    )
)


# ------------------------------------------------------------
# CREATE STATION-SPECIFIC HIGH-WATER THRESHOLD
# ------------------------------------------------------------

thresholds = (
    data
    .groupby("Station")["water_level"]
    .quantile(0.90)
    .rename("high_water_threshold")
)

data = data.merge(
    thresholds,
    on="Station",
    how="left"
)


# ------------------------------------------------------------
# FLOOD-RISK LABEL
# ------------------------------------------------------------

data["risk"] = (
    data["future_water_level"]
    >= data["high_water_threshold"]
).astype(int)


# ------------------------------------------------------------
# REMOVE INCOMPLETE ROWS
# ------------------------------------------------------------

data = data.dropna(
    subset=[
        "rainfall",
        "rainfall_3h",
        "rainfall_6h",
        "rainfall_24h",
        "previous_water_level",
        "future_water_level",
        "high_water_threshold"
    ]
)


# ------------------------------------------------------------
# FINAL TRAINING DATA
# ------------------------------------------------------------

training_data = data[
    [
        "Station",
        "Latitude",
        "Longitude",
        "time",
        "rainfall",
        "rainfall_3h",
        "rainfall_6h",
        "rainfall_24h",
        "previous_water_level",
        "risk"
    ]
].copy()


# ------------------------------------------------------------
# SAVE
# ------------------------------------------------------------

OUTPUT_PATH.parent.mkdir(
    parents=True,
    exist_ok=True
)

training_data.to_csv(
    OUTPUT_PATH,
    index=False
)


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print("Merged records:", len(data))
print("Training records:", len(training_data))

print()

print(
    "Risk = 0:",
    (training_data["risk"] == 0).sum()
)

print(
    "Risk = 1:",
    (training_data["risk"] == 1).sum()
)

print()

print("Features:")

for column in [
    "rainfall",
    "rainfall_3h",
    "rainfall_6h",
    "rainfall_24h",
    "previous_water_level"
]:
    print("-", column)

print()

print("First 10 records:")
print(
    training_data.head(10).to_string(
        index=False
    )
)

print()

print("Saved to:")
print(OUTPUT_PATH)