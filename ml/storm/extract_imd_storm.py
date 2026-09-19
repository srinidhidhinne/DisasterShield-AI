import fitz
import pandas as pd
import re
from pathlib import Path


# --------------------------------------------------
# PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

PDF_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "storm"
    / "33_6a2fe6738ccb6.pdf"
)

OUTPUT_PATH = (
    PROJECT_ROOT
    / "data"
    / "real"
    / "storm"
    / "imd_storm_data.csv"
)


# --------------------------------------------------
# REGEX PATTERNS
# --------------------------------------------------

DATE_PATTERN = r"\d{2}\.\d{2}\.\d{4}"

TIME_PATTERN = r"\d{4}"

NUMBER_PATTERN = r"-?\d+(?:\.\d+)?"


# --------------------------------------------------
# OPEN PDF
# --------------------------------------------------

document = fitz.open(
    PDF_PATH
)

records = []


# --------------------------------------------------
# PROCESS EACH PAGE
# --------------------------------------------------

for page_number, page in enumerate(
    document,
    start=1
):

    text = page.get_text()

    # --------------------------------------------------
    # FIND EVENT NAME
    # --------------------------------------------------

    event_match = re.search(
        r"Table\s+\d+:\s*(.*?)\s+during",
        text,
        re.IGNORECASE | re.DOTALL
    )

    if event_match:

        event = (
            event_match.group(1)
            .replace("\n", " ")
        )

        event = re.sub(
            r"\s+",
            " ",
            event
        ).strip()

    else:

        event = "Unknown"


    # --------------------------------------------------
    # SPLIT INTO LINES
    # --------------------------------------------------

    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]


    # --------------------------------------------------
    # FIND DATES
    # --------------------------------------------------

    for i, line in enumerate(lines):

        if not re.fullmatch(
            DATE_PATTERN,
            line
        ):
            continue

        date = line


        # --------------------------------------------------
        # SEARCH FOLLOWING LINES
        # --------------------------------------------------

        j = i + 1

        while j < len(lines):

            # Stop when another date begins
            if re.fullmatch(
                DATE_PATTERN,
                lines[j]
            ):
                break


            # Need time
            if not re.fullmatch(
                TIME_PATTERN,
                lines[j]
            ):

                j += 1
                continue


            time = lines[j]


            # --------------------------------------------------
            # COLLECT NUMBERS AFTER TIME
            # --------------------------------------------------

            numbers = []

            k = j + 1

            while (
                k < len(lines)
                and len(numbers) < 6
            ):

                value = lines[k]

                if re.fullmatch(
                    NUMBER_PATTERN,
                    value
                ):

                    numbers.append(value)

                elif value == "-":

                    numbers.append("-")

                else:

                    break

                k += 1


            # --------------------------------------------------
            # VALID OBSERVATION
            # --------------------------------------------------

            if len(numbers) >= 6:

                try:

                    latitude = float(
                        numbers[0]
                    )

                    longitude = float(
                        numbers[1]
                    )


                    # Current intensity

                    if numbers[2] == "-":

                        intensity = None

                    else:

                        intensity = float(
                            numbers[2]
                        )


                    pressure = float(
                        numbers[3]
                    )

                    pressure_drop = float(
                        numbers[4]
                    )

                    wind_speed = float(
                        numbers[5]
                    )


                    # --------------------------------------------------
                    # SANITY CHECK
                    # --------------------------------------------------

                    if (
                        -90 <= latitude <= 90
                        and
                        0 <= longitude <= 180
                        and
                        850 <= pressure <= 1050
                        and
                        0 <= pressure_drop <= 100
                        and
                        0 <= wind_speed <= 200
                    ):

                        records.append({

                            "page":
                                page_number,

                            "date":
                                date,

                            "time_utc":
                                time,

                            "latitude":
                                latitude,

                            "longitude":
                                longitude,

                            "current_intensity":
                                intensity,

                            "central_pressure_hpa":
                                pressure,

                            "pressure_drop_hpa":
                                pressure_drop,

                            "wind_speed_kt":
                                wind_speed,

                            "event":
                                event

                        })

                except (TypeError, ValueError):

                    # Ignore malformed numeric observations.
                    pass


            j += 1


# --------------------------------------------------
# DATAFRAME
# --------------------------------------------------

data = pd.DataFrame(
    records
)


# --------------------------------------------------
# REMOVE DUPLICATES
# --------------------------------------------------

if not data.empty:

    data = data.drop_duplicates(
        subset=[
            "date",
            "time_utc",
            "latitude",
            "longitude",
            "event"
        ]
    )


# --------------------------------------------------
# SAVE
# --------------------------------------------------

data.to_csv(
    OUTPUT_PATH,
    index=False
)


# --------------------------------------------------
# SUMMARY
# --------------------------------------------------

print()
print("=" * 60)
print("IMD STORM DATA EXTRACTION")
print("=" * 60)

print()

print(
    "Pages processed:",
    len(document)
)

print(
    "Records extracted:",
    len(data)
)

print()

if not data.empty:

    print(
        "Events:",
        data["event"].nunique()
    )

    print()

    print(
        "First 15 records:"
    )

    print()

    print(
        data.head(15).to_string(
            index=False
        )
    )

    print()

    print(
        "CSV:"
    )

    print(
        OUTPUT_PATH
    )

else:

    print(
        "ERROR: No records extracted."
    )