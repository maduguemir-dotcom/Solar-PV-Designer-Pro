```python
# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# DATA LOADER
# Version: 2.3
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Load and manage solar-resource location data.
#
# ==========================================================

import os
from pathlib import Path

import pandas as pd


# ==========================================================
# SECTION 1 - DATABASE LOCATIONS
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent

PROJECT_DIR = BASE_DIR.parent


POSSIBLE_DATABASES = [
    BASE_DIR / "solar_database.csv",
    BASE_DIR / "solar_data.csv",
    BASE_DIR / "locations.csv",
    PROJECT_DIR / "solar_database.csv",
    PROJECT_DIR / "solar_data.csv",
    PROJECT_DIR / "locations.csv",
]


# ==========================================================
# SECTION 2 - FIND DATABASE
# ==========================================================

def _find_database():
    """
    Find the first available solar database.
    """

    for database_path in POSSIBLE_DATABASES:

        if database_path.exists():

            return database_path

    # Search nearby directories for CSV files
    search_directories = [
        BASE_DIR,
        BASE_DIR / "data",
        PROJECT_DIR,
        PROJECT_DIR / "data",
    ]

    for directory in search_directories:

        if not directory.exists():
            continue

        csv_files = list(
            directory.glob("*.csv")
        )

        for csv_file in csv_files:

            filename = csv_file.name.lower()

            if any(
                keyword in filename
                for keyword in [
                    "solar",
                    "location",
                    "irradiance",
                    "sun"
                ]
            ):

                return csv_file

    return None


# ==========================================================
# SECTION 3 - NORMALIZE COLUMN NAMES
# ==========================================================

def _normalize_columns(dataframe):
    """
    Normalize common column-name variations.

    The original column names are retained where possible,
    while standard names are added for application use.
    """

    df = dataframe.copy()

    # ------------------------------------------------------
    # Remove accidental spaces
    # ------------------------------------------------------

    df.columns = [
        str(column).strip()
        for column in df.columns
    ]

    # Mapping of normalized names to possible alternatives
    aliases = {

        "Location": [
            "Location",
            "location",
            "City",
            "city",
            "Place",
            "place",
            "Town",
            "town",
            "Site",
            "site"
        ],

        "Latitude": [
            "Latitude",
            "latitude",
            "Lat",
            "lat",
            "LATITUDE",
            "LAT"
        ],

        "Longitude": [
            "Longitude",
            "longitude",
            "Lon",
            "lon",
            "Lng",
            "lng",
            "LONGITUDE",
            "LON"
        ],

        "Peak_Sun_Hours": [
            "Peak_Sun_Hours",
            "Peak Sun Hours",
            "Peak_Sun_Hours/day",
            "Peak Sun Hours/day",
            "Sun_Hours",
            "Sun Hours",
            "Average_Sun_Hours",
            "Solar_Hours"
        ],

        "Average_Temperature": [
            "Average_Temperature",
            "Average Temperature",
            "Temperature",
            "Avg_Temperature",
            "Avg Temperature",
            "Average_Temp",
            "Avg_Temp"
        ]
    }

    # ------------------------------------------------------
    # Create standard columns
    # ------------------------------------------------------

    for standard_name, alternatives in aliases.items():

        if standard_name in df.columns:
            continue

        for alternative in alternatives:

            if alternative in df.columns:

                df[standard_name] = df[
                    alternative
                ]

                break

    return df


# ==========================================================
# SECTION 4 - LOAD SOLAR DATABASE
# ==========================================================

def load_solar_database():
    """
    Load the solar-resource database.

    Returns
    -------
    pandas.DataFrame
    """

    database_path = _find_database()

    if database_path is None:

        raise FileNotFoundError(
            """
            Solar database could not be found.

            Expected one of:

            solar_database.csv
            solar_data.csv
            locations.csv

            Place the CSV in the app/ or data/ folder.
            """
        )

    try:

        dataframe = pd.read_csv(
            database_path
        )

    except Exception as error:

        raise RuntimeError(
            f"Unable to read solar database: {error}"
        )

    if dataframe.empty:

        raise ValueError(
            "Solar database is empty."
        )

    dataframe = _normalize_columns(
        dataframe
    )

    # ------------------------------------------------------
    # Required Location column
    # ------------------------------------------------------

    if "Location" not in dataframe.columns:

        raise ValueError(
            """
            Solar database does not contain a
            recognizable Location column.
            """
        )

    return dataframe


# ==========================================================
# SECTION 5 - GET LOCATION DATA
# ==========================================================

def get_location_data(
    solar_data,
    location
):
    """
    Return the row corresponding to a selected location.
    """

    if solar_data is None:

        return None

    if "Location" not in solar_data.columns:

        return None

    matches = solar_data[
        solar_data["Location"].astype(str)
        == str(location)
    ]

    if matches.empty:

        return None

    return matches.iloc[0]


# ==========================================================
# SECTION 6 - VALIDATE COORDINATES
# ==========================================================

def validate_coordinates(
    latitude,
    longitude
):
    """
    Validate geographical coordinates.
    """

    try:

        latitude = float(latitude)
        longitude = float(longitude)

    except (
        TypeError,
        ValueError
    ):

        return False

    return (
        -90.0 <= latitude <= 90.0
        and
        -180.0 <= longitude <= 180.0
    )


# ==========================================================
# SECTION 7 - CREATE COORDINATE LOCATION
# ==========================================================

def create_coordinate_location(
    latitude,
    longitude
):
    """
    Create a location object from coordinates.
    """

    if not validate_coordinates(
        latitude,
        longitude
    ):

        raise ValueError(
            "Invalid latitude or longitude."
        )

    latitude = float(latitude)
    longitude = float(longitude)

    return {

        "Location":
            f"Coordinates: "
            f"{latitude:.4f}, "
            f"{longitude:.4f}",

        "Latitude":
            latitude,

        "Longitude":
            longitude
    }


# ==========================================================
# SECTION 8 - GET COORDINATE SOLAR DATA
# ==========================================================

def get_coordinate_solar_data(
    latitude,
    longitude
):
    """
    Compatibility helper for coordinate-based operation.

    The actual NASA POWER retrieval is handled by solar_api.py.
    """

    if not validate_coordinates(
        latitude,
        longitude
    ):

        return None

    try:

        from solar_api import (
            get_solar_resource
        )

        return get_solar_resource(
            latitude,
            longitude
        )

    except Exception:

        return None


# ==========================================================
# SECTION 9 - GET COORDINATES FROM LOCATION
# ==========================================================

def get_location_coordinates(
    location_data
):
    """
    Extract latitude and longitude from a location record.

    Returns
    -------
    tuple
        (latitude, longitude)
        or
        (None, None)
    """

    if location_data is None:

        return None, None

    latitude = None
    longitude = None

    # ------------------------------------------------------
    # Latitude
    # ------------------------------------------------------

    for column in [
        "Latitude",
        "latitude",
        "Lat",
        "lat"
    ]:

        try:

            if column in location_data.index:

                value = location_data[column]

                if pd.notna(value):

                    latitude = float(value)

                    break

        except (
            TypeError,
            ValueError
        ):

            pass

    # ------------------------------------------------------
    # Longitude
    # ------------------------------------------------------

    for column in [
        "Longitude",
        "longitude",
        "Lon",
        "lon",
        "Lng",
        "lng"
    ]:

        try:

            if column in location_data.index:

                value = location_data[column]

                if pd.notna(value):

                    longitude = float(value)

                    break

        except (
            TypeError,
            ValueError
        ):

            pass

    if not validate_coordinates(
        latitude,
        longitude
    ):

        return None, None

    return latitude, longitude


# ==========================================================
# SECTION 10 - MODULE TEST
# ==========================================================

if __name__ == "__main__":

    try:

        data = load_solar_database()

        print(
            "Solar database loaded successfully."
        )

        print(
            f"Rows: {len(data)}"
        )

        print(
            "Columns:"
        )

        print(
            list(data.columns)
        )

    except Exception as error:

        print(
            f"Database test failed: {error}"
        )
```
