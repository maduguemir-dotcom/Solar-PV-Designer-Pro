# ==========================================================
# Solar PV Designer Pro Africa™
# Global Location & Solar Data Module
# Version 2.1
# ==========================================================

#
# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import pandas as pd


# ==========================================================
# SECTION 2 - LOAD EXISTING SOLAR DATABASE
# ==========================================================

def load_solar_database():

    """
    Load the existing solar location database.

    This database remains available as a quick
    location-selection option.
    """

    file_path = "data/solar_locations.csv"

    try:

        data = pd.read_csv(file_path)

        return data

    except Exception as error:

        raise Exception(
            f"Solar database loading failed: {error}"
        )


# ==========================================================
# SECTION 3 - GET DATABASE LOCATION
# ==========================================================

def get_location_data(
    data,
    location
):

    """
    Retrieve solar information for a
    location contained in the database.
    """

    result = data[
        data["Location"] == location
    ]

    if result.empty:

        return None

    return result.iloc[0]


# ==========================================================
# SECTION 4 - VALIDATE COORDINATES
# ==========================================================

def validate_coordinates(
    latitude,
    longitude
):

    """
    Validate geographical coordinates.

    Latitude:
        -90 to +90

    Longitude:
        -180 to +180
    """

    if latitude < -90 or latitude > 90:

        return False

    if longitude < -180 or longitude > 180:

        return False

    return True


# ==========================================================
# SECTION 5 - CREATE COORDINATE LOCATION
# ==========================================================

def create_coordinate_location(
    latitude,
    longitude
):

    """
    Create a location record from
    user-provided coordinates.
    """

    if not validate_coordinates(
        latitude,
        longitude
    ):

        raise ValueError(
            "Invalid coordinates. "
            "Latitude must be between -90 and 90, "
            "and longitude must be between -180 and 180."
        )


    return {

        "Location": (
            f"Coordinates: "
            f"{latitude:.4f}, "
            f"{longitude:.4f}"
        ),

        "Latitude": latitude,

        "Longitude": longitude
    }


# ==========================================================
# SECTION 6 - SOLAR RESOURCE PLACEHOLDER
# ==========================================================

def get_coordinate_solar_data(
    latitude,
    longitude
):

    """
    Placeholder for the global solar-resource engine.

    In the next stage this function will connect
    to a live solar-resource service such as
    NASA POWER or PVGIS.

    Currently it returns the coordinates only.
    """

    if not validate_coordinates(
        latitude,
        longitude
    ):

        raise ValueError(
            "Invalid geographical coordinates."
        )


    return {

        "latitude": latitude,

        "longitude": longitude,

        "data_source": (
            "Coordinate input - "
            "solar API connection pending"
        )
    }
