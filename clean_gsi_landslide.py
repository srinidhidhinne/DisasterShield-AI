import pandas as pd
import re

INPUT = "data/real/landslide/gsi_landslide_inventory.csv"
OUTPUT = "data/real/landslide/gsi_landslide_clean.csv"

df = pd.read_csv(INPUT)

print("Original records:", len(df))

# -------------------------------------------------
# Fix common PDF extraction concatenations
# -------------------------------------------------

state_fixes = {
    "AndhraPradesh": "Andhra Pradesh",
    "ArunachalPradesh": "Arunachal Pradesh",
    "HimachalPradesh": "Himachal Pradesh",
    "MadhyaPradesh": "Madhya Pradesh",
    "WestBengal": "West Bengal",
    "TamilNadu": "Tamil Nadu",
    "UttarPradesh": "Uttar Pradesh",
    "JammuandKashmir": "Jammu and Kashmir",
}

for old, new in state_fixes.items():
    df["State"] = df["State"].replace(old, new)

# Fix obvious state+district concatenation
districts = [
    "Hailakandi",
    "Karimganj",
    "Cachar",
    "Visakhapatanam",
    "Visakhapatnam",
]

for district in districts:
    df["State"] = df["State"].str.replace(
        district,
        "",
        regex=False
    )

# Restore Andhra Pradesh after removing district
mask = df["Slide_No"].astype(str).str.startswith("AP/")
df.loc[mask, "State"] = "Andhra Pradesh"

# -------------------------------------------------
# Convert coordinates to numeric
# -------------------------------------------------

df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# -------------------------------------------------
# Remove impossible coordinates
# -------------------------------------------------

before = len(df)

df = df[
    (df["Latitude"] >= 6) &
    (df["Latitude"] <= 38) &
    (df["Longitude"] >= 68) &
    (df["Longitude"] <= 98)
].copy()

print("Removed invalid coordinates:", before - len(df))

# -------------------------------------------------
# Remove exact duplicates
# -------------------------------------------------

before = len(df)

df = df.drop_duplicates(
    subset=["Slide_No", "Latitude", "Longitude"]
)

print("Removed duplicates:", before - len(df))

# -------------------------------------------------
# Final statistics
# -------------------------------------------------

print()
print("=" * 60)
print("CLEAN GSI LANDSLIDE INVENTORY")
print("=" * 60)

print()
print("FINAL RECORDS:", len(df))
print("STATES:", df["State"].nunique())

print()
print("STATE COUNTS:")
print(df["State"].value_counts().to_string())

print()
print("ANDHRA PRADESH RECORDS:")
ap = df[df["State"] == "Andhra Pradesh"]
print("Count:", len(ap))

print()
print(ap[
    [
        "Slide_No",
        "State",
        "District",
        "Latitude",
        "Longitude",
        "MaterialInvolved",
        "Movement Type"
    ]
].to_string(index=False))

df.to_csv(OUTPUT, index=False)

print()
print("SAVED:", OUTPUT)