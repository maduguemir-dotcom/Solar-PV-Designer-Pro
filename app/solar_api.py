# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER Solar Resource Module
# Version 2.1.1
# ==========================================================

import requests
import streamlit as st


# ==========================================================
# NASA POWER API
# ==========================================================

NASA_POWER_URL = (
    "https://power.larc.nasa.gov/api/temporal/"
    "climatology/point"
)


# ==========================================================
# HELPER: SAFE NUMBER
# ==========================================================

def safe_float(value):

    """
    Safely convert a value to float.

    Returns None if the value cannot be converted.
    """

    if value is None:
        return None

    try:

        number = float(value)

        if number != number:
            return None

        return number

    except (TypeError, ValueError):

        return None


# ==========================================================
# GET NASA POWER SOLAR RESOURCE
# ==========================================================

@st.cache_data(ttl=86400)
def get_solar_resource(
    latitude,
    longitude
):

    """
    Retrieve climatological solar-resource
    and temperature data from NASA POWER.
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
            "NASA POWER returned an invalid JSON response."
        )


    # ======================================================
    # CHECK RESPONSE STRUCTURE
    # ======================================================

    if not isinstance(data, dict):

        raise Exception(
            "NASA POWER returned an unexpected response."
        )


    properties = data.get(
        "properties",
        {}
    )


    parameter_data = properties.get(
        "parameter",
        {}
    )


    if not parameter_data:

        raise Exception(
            "NASA POWER returned no parameter data."
        )


    # ======================================================
    # EXTRACT PARAMETERS
    # ======================================================

    solar_data = parameter_data.get(
        "ALLSKY_SFC_SW_DWN",
        {}
    )


    temperature_data = parameter_data.get(
        "T2M",
        {}
    )


    if not isinstance(
        solar_data,
        dict
    ):

        solar_data = {}


    if not isinstance(
        temperature_data,
        dict
    ):

        temperature_data = {}


    # ======================================================
    # MONTH NAMES
    # ======================================================

    month_keys = [

        "01",
        "02",
        "03",
        "04",
        "05",
        "06",
        "07",
        "08",
        "09",
        "10",
        "11",
        "12"

    ]


    # ======================================================
    # MONTHLY SOLAR DATA
    # ======================================================

    monthly_solar = {}


    for month in month_keys:

        value = solar_data.get(
            month
        )

        number = safe_float(
            value
        )

        if number is not None:

            monthly_solar[month] = number


    # ======================================================
    # MONTHLY TEMPERATURE
    # ======================================================

    monthly_temperature = {}


    for month in month_keys:

        value = temperature_data.get(
            month
        )

        number = safe_float(
            value
        )

        if number is not None:

            monthly_temperature[month] = number


    # ======================================================
    # AVERAGE SOLAR RESOURCE
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
    # AVERAGE TEMPERATURE
    # ======================================================

    if monthly_temperature:

        average_temperature = (

            sum(
                monthly_temperature.values()
            )
            /
            len(monthly_temperature)

        )

    else:

        average_temperature = None


    # ======================================================
    # VALIDATE SOLAR DATA
    # ======================================================

    if average_solar is None:

        raise Exception(
            "NASA POWER responded, but no usable "
            "solar-resource values were returned."
        )


    # ======================================================
    # RETURN DATA
    # ======================================================

    return {

        "latitude":
            latitude,

        "longitude":
            longitude,

        "monthly_solar":
            monthly_solar,

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
# CONVERT SOLAR RESOURCE TO PEAK SUN HOURS
# ==========================================================

def calculate_peak_sun_hours(
    average_solar
):

    """
    Convert average daily solar irradiation
    in kWh/m²/day to equivalent peak sun hours.

    Numerically these are approximately equivalent.
    """

    value = safe_float(
        average_solar
    )


    if value is None:

        return None


    return value


# ==========================================================
# CREATE SOLAR SUMMARY
# ==========================================================

def create_solar_summary(
    solar_data
):

    """
    Create a safe summary for Streamlit.
    """

    average_solar = solar_data.get(
        "average_solar"
    )


    average_temperature = solar_data.get(
        "average_temperature"
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
# TEST NASA POWER CONNECTION
# ==========================================================

def test_solar_api(
    latitude,
    longitude
):

    """
    Test the NASA POWER connection.
    """

    try:

        result = get_solar_resource(
            latitude,
            longitude
        )


        return {

            "success":
                True,

            "message":
                "NASA POWER connection successful.",

            "data":
                result

        }


    except Exception as error:

        return {

            "success":
                False,

            "message":
                str(error),

            "data":
                None

        }
