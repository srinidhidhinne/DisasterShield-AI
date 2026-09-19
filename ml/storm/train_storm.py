import pandas as pd
from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

import joblib


# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "storm"
    / "storm_training_data.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "storm"
    / "storm_model.joblib"
)


# --------------------------------------------------
# LOAD REAL IMD DATA
# --------------------------------------------------

data = pd.read_csv(
    DATA_PATH
)


# --------------------------------------------------
# FEATURES
# --------------------------------------------------

features = [
    "latitude",
    "longitude",
    "central_pressure_hpa",
    "pressure_drop_hpa",
    "wind_speed_kt"
]


X = data[features]

y = data["risk"]


# --------------------------------------------------
# TRAIN / TEST SPLIT
# --------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.2,

    random_state=42,

    stratify=y
)


# --------------------------------------------------
# RANDOM FOREST
# --------------------------------------------------

model = RandomForestClassifier(

    n_estimators=200,

    random_state=42,

    class_weight="balanced"
)


# --------------------------------------------------
# TRAIN
# --------------------------------------------------

model.fit(
    X_train,
    y_train
)


# --------------------------------------------------
# TEST
# --------------------------------------------------

predictions = model.predict(
    X_test
)


accuracy = accuracy_score(
    y_test,
    predictions
)


# --------------------------------------------------
# SAVE MODEL
# --------------------------------------------------

joblib.dump(
    model,
    MODEL_PATH
)


# --------------------------------------------------
# RESULTS
# --------------------------------------------------

print()
print("=" * 60)
print("REAL IMD STORM MODEL TRAINING")
print("=" * 60)

print()

print(
    "Dataset records:",
    len(data)
)

print(
    "Training records:",
    len(X_train)
)

print(
    "Testing records:",
    len(X_test)
)

print()

print(
    "Features:"
)

for feature in features:

    print(
        "-",
        feature
    )

print()

print(
    "Test Accuracy:",
    round(
        accuracy * 100,
        2
    ),
    "%"
)

print()

print(
    "Model saved to:"
)

print(
    MODEL_PATH
)