import pandas as pd

INPUT = "data/real/landslide/landslide_extracted.txt"
OUTPUT = "data/real/landslide/gsi_landslide_inventory.csv"

states = {
    "Assam",
    "Andhra Pradesh",
    "Arunachal Pradesh",
    "Bihar",
    "Chhattisgarh",
    "Goa",
    "Gujarat",
    "Haryana",
    "Himachal Pradesh",
    "Jammu and Kashmir",
    "Jharkhand",
    "Karnataka",
    "Kerala",
    "Madhya Pradesh",
    "Maharashtra",
    "Manipur",
    "Meghalaya",
    "Mizoram",
    "Nagaland",
    "Odisha",
    "Punjab",
    "Rajasthan",
    "Sikkim",
    "Tamil Nadu",
    "Telangana",
    "Tripura",
    "Uttar Pradesh",
    "Uttarakhand",
    "West Bengal",
}

columns = [
    "Sl.No.",
    "Slide_No",
    "State",
    "District",
    "Slide_Name",
    "NH_SH_Location",
    "Latitude",
    "Longitude",
    "MaterialInvolved",
    "Movement Type",
    "History",
]

print("Reading extracted GSI data...")

with open(INPUT, "r", encoding="utf-8") as f:
    text = f.read()

lines = [x.strip() for x in text.splitlines()]

rows = []
i = 0
n = len(lines)

while i < n:
    # A valid record starts with a serial number
    if lines[i].isdigit() and i + 10 < n:

        # Based on the structure seen in the PDF:
        # number
        # slide_no
        # state
        # district
        # slide name
        # location
        # latitude
        # longitude
        # material
        # movement
        # history

        if lines[i + 2] in states:

            try:
                latitude = float(lines[i + 6])
                longitude = float(lines[i + 7])

                row = lines[i:i + 11]

                if len(row) == 11:
                    rows.append(row)
                    i += 11
                    continue

            except ValueError:
                pass

    i += 1


print()
print("=" * 60)
print("GSI LANDSLIDE INVENTORY PARSER")
print("=" * 60)
print()

print("VALID RECORDS:", len(rows))

if len(rows) == 0:
    print("No records were extracted.")
    print("The PDF formatting may require another parser.")
    raise SystemExit

df = pd.DataFrame(rows, columns=columns)

# Convert coordinates to numeric
df["Latitude"] = pd.to_numeric(df["Latitude"], errors="coerce")
df["Longitude"] = pd.to_numeric(df["Longitude"], errors="coerce")

# Remove invalid coordinates
df = df.dropna(subset=["Latitude", "Longitude"])

# Remove duplicate records
df = df.drop_duplicates()

print("RECORDS AFTER CLEANING:", len(df))
print("NUMBER OF STATES:", df["State"].nunique())

print()
print("STATE COUNTS:")
print(df["State"].value_counts().to_string())

print()
print("FIRST 10 RECORDS:")
print(df.head(10).to_string(index=False))

df.to_csv(OUTPUT, index=False)

print()
print("=" * 60)
print("SAVED:")
print(OUTPUT)
print("=" * 60)