import pandas as pd
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

INPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "storm"
    / "imd_storm_data.csv"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "storm"
    / "storm_training_data.csv"
)


# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

data = pd.read_csv(
    INPUT_PATH
)


# --------------------------------------------------
# CREATE STORM RISK LABEL
# --------------------------------------------------

data["risk"] = (
    data["wind_speed_kt"] >= 34
).astype(int)


# --------------------------------------------------
# REMOVE INVALID VALUES
# --------------------------------------------------

data = data.dropna(
    subset=[
        "latitude",
        "longitude",
        "central_pressure_hpa",
        "pressure_drop_hpa",
        "wind_speed_kt"
    ]
)


# --------------------------------------------------
# SELECT ML FEATURES
# --------------------------------------------------

training_data = data[
    [
        "latitude",
        "longitude",
        "central_pressure_hpa",
        "pressure_drop_hpa",
        "wind_speed_kt",
        "risk"
    ]
]


# --------------------------------------------------
# SAVE
# --------------------------------------------------

training_data.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# DISPLAY
# --------------------------------------------------

print()
print("=" * 60)
print("REAL STORM TRAINING DATA PREPARED")
print("=" * 60)

print()

print(
    "Total records:",
    len(training_data)
)

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

print(
    "Training columns:"
)

for column in training_data.columns:

    print(
        "-",
        column
    )

print()

print(
    training_data.head(10).to_string(
        index=False
    )
)

print()

print(
    "Saved to:"
)

print(
    OUTPUT_PATH
)