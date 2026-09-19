import pandas as pd
import joblib

from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def validate_model(
    name,
    dataset_path,
    model_path,
    features
):
    print()
    print("=" * 50)
    print(name)
    print("=" * 50)

    data = pd.read_csv(
        PROJECT_ROOT / dataset_path
    )

    X = data[features]
    y = data["risk"]

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    model = joblib.load(
        PROJECT_ROOT / model_path
    )

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        zero_division=0
    )

    matrix = confusion_matrix(
        y_test,
        predictions
    )

    print("Dataset records:", len(data))
    print("Testing records:", len(X_test))
    print()

    print("Features:")
    for feature in features:
        print("-", feature)

    print()

    print(
        "Accuracy :",
        round(accuracy * 100, 2),
        "%"
    )

    print(
        "Precision:",
        round(precision * 100, 2),
        "%"
    )

    print(
        "Recall   :",
        round(recall * 100, 2),
        "%"
    )

    print(
        "F1 Score :",
        round(f1 * 100, 2),
        "%"
    )

    print()

    print("Confusion Matrix:")
    print(matrix)


# ============================================================
# FLOOD MODEL
# ============================================================

validate_model(
    name="FLOOD MODEL",

    dataset_path=(
        "data/raw/flood.csv"
    ),

    model_path=(
        "ml/flood/flood_model.joblib"
    ),

    features=[
        "rainfall",
        "water_level",
        "soil_moisture"
    ]
)


# ============================================================
# LANDSLIDE MODEL
# ============================================================

validate_model(
    name="LANDSLIDE MODEL",

    dataset_path=(
        "data/raw/landslide.csv"
    ),

    model_path=(
        "ml/landslide/landslide_model.joblib"
    ),

    features=[
        "rainfall",
        "soil_moisture",
        "slope"
    ]
)


# ============================================================
# STORM MODEL
# ============================================================

validate_model(
    name="STORM MODEL",

    dataset_path=(
        "data/real/storm/storm_training_data.csv"
    ),

    model_path=(
        "ml/storm/storm_model.joblib"
    ),

    features=[
        "latitude",
        "longitude",
        "central_pressure_hpa",
        "pressure_drop_hpa",
        "wind_speed_kt"
    ]
)


print()
print("=" * 50)
print("MODEL VALIDATION COMPLETE")
print("=" * 50)

print()
print("IMPORTANT:")
print(
    "The storm model uses an IMD-derived dataset."
)

print(
    "Its risk label is derived from wind_speed_kt >= 34."
)

print(
    "Therefore, storm validation metrics should not "
    "be interpreted as real-world predictive accuracy."
)