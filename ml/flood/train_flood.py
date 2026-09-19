import pandas as pd
import joblib

from pathlib import Path

from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "flood"
    / "flood_training_data.csv"
)

MODEL_PATH = (
    PROJECT_ROOT
    / "ml"
    / "flood"
    / "flood_model.joblib"
)


# ------------------------------------------------------------
# LOAD DATA
# ------------------------------------------------------------

data = pd.read_csv(DATA_PATH)


features = [
    "rainfall",
    "rainfall_3h",
    "rainfall_6h",
    "rainfall_24h",
    "previous_water_level"
]

X = data[features]
y = data["risk"]


# ------------------------------------------------------------
# TRAIN / TEST SPLIT
# ------------------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# ------------------------------------------------------------
# RANDOM FOREST
# ------------------------------------------------------------

model = RandomForestClassifier(
    n_estimators=300,
    random_state=42,
    class_weight="balanced"
)

model.fit(
    X_train,
    y_train
)


# ------------------------------------------------------------
# PREDICTION
# ------------------------------------------------------------

predictions = model.predict(X_test)


# ------------------------------------------------------------
# METRICS
# ------------------------------------------------------------

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


# ------------------------------------------------------------
# SAVE MODEL
# ------------------------------------------------------------

joblib.dump(
    model,
    MODEL_PATH
)


# ------------------------------------------------------------
# OUTPUT
# ------------------------------------------------------------

print()
print("=" * 60)
print("REAL CWC FLOOD MODEL TRAINING")
print("=" * 60)
print()

print("Dataset records:", len(data))
print("Training records:", len(X_train))
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

print()

print("Feature Importance:")

for feature, importance in zip(
    features,
    model.feature_importances_
):
    print(
        f"{feature}: "
        f"{importance:.4f}"
    )

print()

print("Model saved to:")
print(MODEL_PATH)