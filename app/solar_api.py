# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER Solar Resource Module
# Version 2.1
# ==========================================================
#
# Purpose:
# Retrieve solar-resource and temperature information
# for any geographical coordinate using NASA POWER.
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import requests
import streamlit as st


# ==========================================================
# SECTION 2 - NASA POWER API CONFIGURATION
# ==========================================================

NASA_POWER_URL = (
    "https://power.larc.nasa.gov/api/temporal/climatology/point"
)


# ==========================================================
# SECTION 3 - GET SOLAR RESOURCE
# ==========================================================

@st.cache_data(ttl=86400)
def get_solar_resource(
    latitude,
    longitude
):
    """
    Retrieve climatological solar-resource data
    from NASA POWER.

    Parameters
    ----------
    latitude : float
        Geographic latitude.

    longitude : float
        Geographic longitude.

    Returns
    -------
    dict
        Solar-resource information.
    """

    parameters = (
        "ALLSKY_SFC_SW_DWN,"
        "T2M"
    )


    request_parameters = {

        "parameters": parameters,

        "community": "RE",

        "longitude": longitude,

        "latitude": latitude,

        "format": "JSON"

    }


    try:

        response = requests.get(

            NASA_POWER_URL,

            params=request_parameters,

            timeout=30
        )


        response.raise_for_status()


        data = response.json()


    except requests.exceptions.Timeout:

        raise Exception(
            "NASA POWER request timed out. "
            "Please try again."
        )


    except requests.exceptions.RequestException as error:

        raise Exception(
            f"NASA POWER request failed: {error}"
        )


    except ValueError:

        raise Exception(
            "NASA POWER returned an invalid response."
        )


    # ======================================================
    # SECTION 4 - EXTRACT API DATA
    # ======================================================

    properties = (
        data.get("properties", {})
    )


    parameter_data = (
        properties.get("parameter", {})
    )


    solar_data = parameter_data.get(
        "ALLSKY_SFC_SW_DWN",
        {}
    )


    temperature_data = parameter_data.get(
        "T2M",
        {}
    )


    if not solar_data:

        raise Exception(
            "No solar-resource data were returned "
            "for the selected coordinates."
        )


    # ======================================================
    # SECTION 5 - MONTHLY SOLAR RESOURCE
    # ======================================================

    monthly_solar = {}


    for month in range(1, 13):

        month_key = f"{month:02d}"

        value = solar_data.get(
            month_key
        )


        if value is not None:

            monthly_solar[month_key] = float(
                value
            )


    # ======================================================
    # SECTION 6 - MONTHLY TEMPERATURE
    # ======================================================

    monthly_temperature = {}


    for month in range(1, 13):

        month_key = f"{month:02d}"

        value = temperature_data.get(
            month_key
        )


        if value is not None:

            monthly_temperature[month_key] = float(
                value
            )


    # ======================================================
    # SECTION 7 - CALCULATE ANNUAL AVERAGE
    # ======================================================

    if monthly_solar:

        average_solar = (
            sum(monthly_solar.values())
            /
            len(monthly_solar)
        )

    else:

        average_solar = None


    # ======================================================
    # SECTION 8 - CALCULATE TEMPERATURE AVERAGE
    # ======================================================

    if monthly_temperature:

        average_temperature = (
            sum(monthly_temperature.values())
            /
            len(monthly_temperature)
        )

    else:

        average_temperature = None


    # ======================================================
    # SECTION 9 - RETURN SOLAR RESOURCE
    # ======================================================

    return {

        "latitude": latitude,

        "longitude": longitude,

        "monthly_solar": monthly_solar,

        "monthly_temperature":
            monthly_temperature,

        "average_solar":
            average_solar,

        "average_temperature":
            average_temperature,

        "data_source":
            "NASA POWER",

        "api_url":
            NASA_POWER_URL
    }


# ==========================================================
# SECTION 10 - CONVERT SOLAR RESOURCE TO SUN HOURS
# ==========================================================

def calculate_peak_sun_hours(
    average_solar
):
    """
    Convert average daily solar irradiation
    expressed in kWh/m²/day into equivalent
    peak sun hours.

    Numerically, 1 kWh/m²/day corresponds
    approximately to 1 peak sun hour.
    """

    if average_solar is None:

        return None


    return float(
        average_solar
    )


# ==========================================================
# SECTION 11 - SOLAR RESOURCE SUMMARY
# ==========================================================

def create_solar_summary(
    solar_data
):
    """
    Create a simplified summary suitable
    for display in the Streamlit interface.
    """

    average_solar = (
        solar_data.get(
            "average_solar"
        )
    )


    average_temperature = (
        solar_data.get(
            "average_temperature"
        )
    )


    peak_sun_hours = (
        calculate_peak_sun_hours(
            average_solar
        )
    )


    return {

        "peak_sun_hours":
            peak_sun_hours,

        "average_temperature":
            average_temperature,

        "data_source":
            solar_data.get(
                "data_source",
                "Unknown"
            )
    }


# ==========================================================
# SECTION 12 - TEST API CONNECTION
# ==========================================================

def test_solar_api(
    latitude,
    longitude
):
    """
    Test whether NASA POWER can return
    solar-resource information for a
    coordinate.
    """

    try:

        result = get_solar_resource(
            latitude,
            longitude
        )


        return {

            "success": True,

            "message":
                "NASA POWER connection successful.",

            "data":
                result

        }


    except Exception as error:

        return {

            "success": False,

            "message":
                str(error),

            "data":
                None
        }
