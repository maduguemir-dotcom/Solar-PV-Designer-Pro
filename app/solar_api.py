# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER Solar Resource Engine
# Version 2.1.2
# ==========================================================
#
# Purpose:
# Retrieve monthly solar-resource and temperature data
# for any geographical coordinate using NASA POWER.
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import requests
import streamlit as st


# ==========================================================
# SECTION 2 - NASA POWER MONTHLY API
# ==========================================================

NASA_POWER_MONTHLY_URL = (
    "https://power.larc.nasa.gov/api/temporal/monthly/point"
)


# ==========================================================
# SECTION 3 - SAFE NUMBER CONVERSION
# ==========================================================

def safe_float(value):

    """
    Safely convert a value to float.

    Returns None when conversion is impossible.
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
# SECTION 4 - GET NASA POWER MONTHLY DATA
# ==========================================================

@st.cache_data(ttl=86400)
def get_solar_resource(
    latitude,
    longitude
):

    """
    Retrieve monthly solar-resource and temperature
    data from NASA POWER.

    Parameters
    ----------
    latitude : float
        Geographic latitude.

    longitude : float
        Geographic longitude.

    Returns
    -------
    dict
        Processed solar-resource information.
    """

    # ------------------------------------------------------
    # NASA POWER parameters
    # ------------------------------------------------------

    parameters = (
        "ALLSKY_SFC_SW_DWN,"
        "T2M"
    )


    # ------------------------------------------------------
    # Request configuration
    # ------------------------------------------------------

    request_parameters = {

        "parameters": parameters,

        "community": "RE",

        "longitude": latitude
        if False
        else longitude,

        "latitude": latitude,

        "format": "JSON"

    }


    # ======================================================
    # SECTION 5 - REQUEST DATA
    # ======================================================

    try:

        response = requests.get(

            NASA_POWER_MONTHLY_URL,

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
    # SECTION 6 - VALIDATE RESPONSE
    # ======================================================

    if not isinstance(
        data,
        dict
    ):

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
    # SECTION 7 - EXTRACT SOLAR DATA
    # ======================================================

    solar_parameter = parameter_data.get(
        "ALLSKY_SFC_SW_DWN",
        {}
    )


    temperature_parameter = parameter_data.get(
        "T2M",
        {}
    )


    if not isinstance(
        solar_parameter,
        dict
    ):

        solar_parameter = {}


    if not isinstance(
        temperature_parameter,
        dict
    ):

        temperature_parameter = {}


    # ======================================================
    # SECTION 8 - MONTH NAMES
    # ======================================================

    month_names = {

        "01": "January",
        "02": "February",
        "03": "March",
        "04": "April",
        "05": "May",
        "06": "June",
        "07": "July",
        "08": "August",
        "09": "September",
        "10": "October",
        "11": "November",
        "12": "December"

    }


    # ======================================================
    # SECTION 9 - EXTRACT MONTHLY SOLAR VALUES
    # ======================================================

    monthly_solar = {}


    for key, value in solar_parameter.items():

        # NASA POWER monthly responses may use
        # YYYYMM keys.

        key_string = str(key)


        if len(key_string) >= 6:

            month = key_string[-2:]


            if month in month_names:

                number = safe_float(
                    value
                )


                if number is not None:

                    monthly_solar[
                        month
                    ] = number


    # ======================================================
    # SECTION 10 - EXTRACT MONTHLY TEMPERATURE
    # ======================================================

    monthly_temperature = {}


    for key, value in temperature_parameter.items():

        key_string = str(key)


        if len(key_string) >= 6:

            month = key_string[-2:]


            if month in month_names:

                number = safe_float(
                    value
                )


                if number is not None:

                    monthly_temperature[
                        month
                    ] = number


    # ======================================================
    # SECTION 11 - VALIDATE SOLAR RESULTS
    # ======================================================

    if not monthly_solar:

        raise Exception(
            "NASA POWER responded, but no usable solar-resource "
            "values were found in the monthly response."
        )


    # ======================================================
    # SECTION 12 - CALCULATE AVERAGE SOLAR RESOURCE
    # ======================================================

    average_solar = (

        sum(
            monthly_solar.values()
        )
        /
        len(
            monthly_solar
        )

    )


    # ======================================================
    # SECTION 13 - CALCULATE TEMPERATURE
    # ======================================================

    if monthly_temperature:

        average_temperature = (

            sum(
                monthly_temperature.values()
            )
            /
            len(
                monthly_temperature
            )

        )

    else:

        average_temperature = None


    # ======================================================
    # SECTION 14 - FIND BEST SOLAR MONTH
    # ======================================================

    best_month_key = max(

        monthly_solar,

        key=monthly_solar.get

    )


    best_month_value = (
        monthly_solar[
            best_month_key
        ]
    )


    # ======================================================
    # SECTION 15 - FIND WORST SOLAR MONTH
    # ======================================================

    worst_month_key = min(

        monthly_solar,

        key=monthly_solar.get

    )


    worst_month_value = (
        monthly_solar[
            worst_month_key
        ]
    )


    # ======================================================
    # SECTION 16 - PREPARE MONTHLY DISPLAY DATA
    # ======================================================

    monthly_display = []


    for month_number in range(
        1,
        13
    ):

        month_key = (
            f"{month_number:02d}"
        )


        solar_value = (
            monthly_solar.get(
                month_key
            )
        )


        temperature_value = (
            monthly_temperature.get(
                month_key
            )
        )


        monthly_display.append({

            "month":
                month_names[
                    month_key
                ],

            "solar_resource":
                solar_value,

            "temperature":
                temperature_value

        })


    # ======================================================
    # SECTION 17 - RETURN RESULTS
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

        "monthly_display":
            monthly_display,

        "average_solar":
            average_solar,

        "average_temperature":
            average_temperature,

        "best_month":
            month_names[
                best_month_key
            ],

        "best_month_value":
            best_month_value,

        "worst_month":
            month_names[
                worst_month_key
            ],

        "worst_month_value":
            worst_month_value,

        "data_source":
            "NASA POWER",

        "api_url":
            NASA_POWER_MONTHLY_URL

    }


# ==========================================================
# SECTION 18 - PEAK SUN HOURS
# ==========================================================

def calculate_peak_sun_hours(
    average_solar
):

    """
    Convert average daily solar irradiation
    in kWh/m²/day into equivalent peak sun hours.

    Numerically, these values are approximately equivalent.
    """

    value = safe_float(
        average_solar
    )


    if value is None:

        return None


    return value


# ==========================================================
# SECTION 19 - CREATE SUMMARY
# ==========================================================

def create_solar_summary(
    solar_data
):

    """
    Create a simplified solar-resource summary.
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

        "best_month":
            solar_data.get(
                "best_month"
            ),

        "best_month_value":
            solar_data.get(
                "best_month_value"
            ),

        "worst_month":
            solar_data.get(
                "worst_month"
            ),

        "worst_month_value":
            solar_data.get(
                "worst_month_value"
            ),

        "data_source":
            solar_data.get(
                "data_source",
                "NASA POWER"
            )

    }


# ==========================================================
# SECTION 20 - TEST API
# ==========================================================

def test_solar_api(
    latitude,
    longitude
):

    """
    Test the NASA POWER solar-resource connection.
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
