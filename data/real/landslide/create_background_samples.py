import pandas as pd
import numpy as np
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]

INPUT = PROJECT_ROOT / "data" / "real" / "landslide" / "gsi_landslide_training_data.csv"
OUTPUT = PROJECT_ROOT / "data" / "real" / "landslide" / "landslide_background_samples.csv"

df = pd.read_csv(INPUT)

np.random.seed(42)

lat_min = df["Latitude"].min()
lat_max = df["Latitude"].max()
lon_min = df["Longitude"].min()
lon_max = df["Longitude"].max()

n_samples = len(df)

background = pd.DataFrame({
    "Latitude": np.random.uniform(lat_min, lat_max, n_samples),
    "Longitude": np.random.uniform(lon_min, lon_max, n_samples)
})

# Remove points very close to known landslides
landslide_coords = df[["Latitude", "Longitude"]].to_numpy()

valid = []

for _, row in background.iterrows():
    distance = np.sqrt(
        (landslide_coords[:, 0] - row["Latitude"]) ** 2 +
        (landslide_coords[:, 1] - row["Longitude"]) ** 2
    )

    if distance.min() > 0.05:
        valid.append(row)

background = pd.DataFrame(valid).head(n_samples)

background["occurrence"] = 0

OUTPUT.parent.mkdir(parents=True, exist_ok=True)
background.to_csv(OUTPUT, index=False)

print("BACKGROUND SAMPLES:", len(background))
print("SAVED:", OUTPUT)
print()
print(background.head(10).to_string(index=False))