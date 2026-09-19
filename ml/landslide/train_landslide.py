import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib


data = pd.read_csv("data/raw/landslide.csv")


X = data[
    [
        "rainfall",
        "soil_moisture",
        "slope"
    ]
]

y = data["risk"]


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)


model.fit(X_train, y_train)


predictions = model.predict(X_test)


accuracy = accuracy_score(
    y_test,
    predictions
)


print(
    "Landslide Model Accuracy:",
    round(accuracy * 100, 2),
    "%"
)


joblib.dump(
    model,
    "ml/landslide/landslide_model.joblib"
)


print(
    "Landslide model saved successfully!"
)