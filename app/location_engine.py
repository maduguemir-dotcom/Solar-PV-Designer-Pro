# ==========================================================
# Solar PV Designer Pro
# Global Location Engine
# Version 2.1.6
# ==========================================================

"""
Global Location Engine

Responsibilities:
1. Accept latitude and longitude.
2. Validate coordinates.
3. Accept an optional location name and country.
4. Connect the location to the NASA POWER solar engine.
5. Return a clean location + solar-resource package.

This module deliberately does NOT contain the PV sizing
calculations. Those remain in the existing calculation
modules.
"""

from solar_api import (
    get_solar_resource,
    create_solar_summary
)


# ==========================================================
# SECTION 1 - VALIDATE COORDINATES
# ==========================================================

def validate_coordinates(latitude, longitude):
    """
    Validate geographical coordinates.

    Latitude:
        -90 to +90

    Longitude:
        -180 to +180
    """

    try:

        latitude = float(latitude)
        longitude = float(longitude)

    except (TypeError, ValueError):

        return {
            "valid": False,
            "message": (
                "Latitude and longitude must be numbers."
            )
        }


    if latitude < -90 or latitude > 90:

        return {
            "valid": False,
            "message": (
                "Latitude must be between "
                "-90 and +90 degrees."
            )
        }


    if longitude < -180 or longitude > 180:

        return {
            "valid": False,
            "message": (
                "Longitude must be between "
                "-180 and +180 degrees."
            )
        }


    return {
        "valid": True,
        "message": "Coordinates are valid.",
        "latitude": latitude,
        "longitude": longitude
    }


# ==========================================================
# SECTION 2 - CREATE LOCATION
# ==========================================================

def create_location(
    latitude,
    longitude,
    location_name="",
    country=""
):
    """
    Create a standardized location object.
    """

    validation = validate_coordinates(
        latitude,
        longitude
    )


    if not validation["valid"]:

        return {
            "success": False,
            "message": validation["message"],
            "location": None
        }


    return {
        "success": True,

        "message": "Location created successfully.",

        "location": {

            "name":
                str(location_name).strip(),

            "country":
                str(country).strip(),

            "latitude":
                validation["latitude"],

            "longitude":
                validation["longitude"]

        }
    }


# ==========================================================
# SECTION 3 - GET SOLAR RESOURCE FOR LOCATION
# ==========================================================

def get_location_solar_resource(
    latitude,
    longitude,
    location_name="",
    country=""
):
    """
    Validate a location and retrieve NASA POWER
    solar-resource data for that location.
    """

    location_result = create_location(
        latitude=latitude,
        longitude=longitude,
        location_name=location_name,
        country=country
    )


    if not location_result["success"]:

        return location_result


    location = location_result["location"]


    try:

        solar_data = get_solar_resource(

            location["latitude"],

            location["longitude"]

        )


        solar_summary = create_solar_summary(
            solar_data
        )


        return {

            "success": True,

            "message":
                "Location and NASA POWER data "
                "retrieved successfully.",

            "location":
                location,

            "solar":
                solar_data,

            "summary":
                solar_summary

        }


    except Exception as error:

        return {

            "success": False,

            "message":
                str(error),

            "location":
                location,

            "solar":
                None,

            "summary":
                None

        }


# ==========================================================
# SECTION 4 - FORMAT LOCATION NAME
# ==========================================================

def format_location_name(
    location_name,
    country,
    latitude,
    longitude
):
    """
    Produce a clean human-readable location label.
    """

    location_name = str(
        location_name
    ).strip()


    country = str(
        country
    ).strip()


    if location_name and country:

        return (
            f"{location_name}, {country}"
        )


    if location_name:

        return location_name


    if country:

        return country


    return (
        f"{float(latitude):.4f}°, "
        f"{float(longitude):.4f}°"
    )


# ==========================================================
# SECTION 5 - LOCATION SUMMARY
# ==========================================================

def get_location_summary(
    location_result
):
    """
    Produce a concise summary suitable for
    displaying in main.py.
    """

    if not location_result.get(
        "success",
        False
    ):

        return {
            "success": False,
            "message":
                location_result.get(
                    "message",
                    "Unknown error."
                )
        }


    location = (
        location_result.get(
            "location",
            {}
        )
    )


    summary = (
        location_result.get(
            "summary",
            {}
        )
    )


    return {

        "success": True,

        "location":
            format_location_name(
                location.get(
                    "name",
                    ""
                ),

                location.get(
                    "country",
                    ""
                ),

                location.get(
                    "latitude"
                ),

                location.get(
                    "longitude"
                )
            ),

        "latitude":
            location.get(
                "latitude"
            ),

        "longitude":
            location.get(
                "longitude"
            ),

        "peak_sun_hours":
            summary.get(
                "peak_sun_hours"
            ),

        "average_temperature":
            summary.get(
                "average_temperature"
            ),

        "best_month":
            summary.get(
                "best_month"
            ),

        "worst_month":
            summary.get(
                "worst_month"
            ),

        "data_source":
            summary.get(
                "data_source",
                "NASA POWER"
            ),

        "climatology_period":
            summary.get(
                "climatology_period"
            )

    }
