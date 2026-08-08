# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER Solar Resource Engine
# Version 2.1.3
# ==========================================================

import requests
import streamlit as st


# ==========================================================
# NASA POWER CLIMATOLOGY API
# ==========================================================

NASA_POWER_URL = (
    "https://power.larc.nasa.gov/api/"
    "temporal/climatology/point"
)


# ==========================================================
# SAFE FLOAT CONVERSION
# ==========================================================

def safe_float(value):

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
# GET SOLAR RESOURCE
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


    # ======================================================
    # NASA POWER REQUEST
    # ======================================================

    try:

        response = requests.get(

            NASA_POWER_URL,

            params=request_parameters,

            timeout=30

        )


        if response.status_code != 200:

            try:

                error_data = response.json()

            except Exception:

                error_data = {}

            error_message = (
                error_data
                .get("messages", "")
            )


            raise Exception(

                f"NASA POWER returned HTTP "
                f"{response.status_code}. "
                f"{error_message}"

            )


        data = response.json()


    except requests.exceptions.Timeout:

        raise Exception(
            "NASA POWER request timed out."
        )


    except requests.exceptions.RequestException as error:

        raise Exception(
            f"NASA POWER request failed: {error}"
        )


    except ValueError:

        raise Exception(
            "NASA POWER returned invalid JSON."
        )


    # ======================================================
    # RESPONSE STRUCTURE
    # ======================================================

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
    # SOLAR DATA
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
    # MONTH NAMES
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
    # EXTRACT SOLAR VALUES
    # ======================================================

    monthly_solar = {}


    for key, value in solar_parameter.items():

        key_string = str(key)


        if key_string in month_names:

            number = safe_float(
                value
            )


            if number is not None:

                monthly_solar[
                    key_string
                ] = number


    # ======================================================
    # EXTRACT TEMPERATURE VALUES
    # ======================================================

    monthly_temperature = {}


    for key, value in temperature_parameter.items():

        key_string = str(key)


        if key_string in month_names:

            number = safe_float(
                value
            )


            if number is not None:

                monthly_temperature[
                    key_string
                ] = number


    # ======================================================
    # VALIDATE SOLAR DATA
    # ======================================================

    if not monthly_solar:

        raise Exception(
            "NASA POWER responded successfully, "
            "but no monthly solar-resource values "
            "were found."
        )


    # ======================================================
    # AVERAGE SOLAR RESOURCE
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
    # AVERAGE TEMPERATURE
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
    # BEST MONTH
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
    # WORST MONTH
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
    # MONTHLY DISPLAY
    # ======================================================

    monthly_display = []


    for month_number in range(
        1,
        13
    ):

        month_key = (
            f"{month_number:02d}"
        )


        monthly_display.append({

            "month":
                month_names[
                    month_key
                ],

            "solar_resource":
                monthly_solar.get(
                    month_key
                ),

            "temperature":
                monthly_temperature.get(
                    month_key
                )

        })


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
            NASA_POWER_URL

    }


# ==========================================================
# PEAK SUN HOURS
# ==========================================================

def calculate_peak_sun_hours(
    average_solar
):

    value = safe_float(
        average_solar
    )


    if value is None:

        return None


    return value


# ==========================================================
# SUMMARY
# ==========================================================

def create_solar_summary(
    solar_data
):

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


    return {

        "peak_sun_hours":
            calculate_peak_sun_hours(
                average_solar
            ),

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
# API TEST
# ==========================================================

def test_solar_api(
    latitude,
    longitude
):

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
