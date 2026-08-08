# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER Solar Resource Engine
# Version 2.1.4
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
# NASA POWER CLIMATOLOGY PERIOD
# ==========================================================

NASA_START_YEAR = 2001
NASA_END_YEAR = 2020


# ==========================================================
# MONTH DEFINITIONS
# ==========================================================

MONTHS = {

    "JAN": "January",
    "FEB": "February",
    "MAR": "March",
    "APR": "April",
    "MAY": "May",
    "JUN": "June",
    "JUL": "July",
    "AUG": "August",
    "SEP": "September",
    "OCT": "October",
    "NOV": "November",
    "DEC": "December"

}


# ==========================================================
# SAFE FLOAT CONVERSION
# ==========================================================

def safe_float(value):

    """
    Safely convert a value to float.

    Returns None if the value is missing
    or cannot be converted.
    """

    if value is None:
        return None

    try:

        number = float(value)

        # Check for NaN
        if number != number:
            return None

        # NASA POWER may use -999 as a
        # missing-data indicator.
        if number <= -900:
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
    and temperature information from NASA POWER.

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

    # ======================================================
    # REQUEST PARAMETERS
    # ======================================================

    request_parameters = {

        "parameters":
            "ALLSKY_SFC_SW_DWN,T2M",

        "community":
            "RE",

        "longitude":
            longitude,

        "latitude":
            latitude,

        "start":
            NASA_START_YEAR,

        "end":
            NASA_END_YEAR,

        "format":
            "JSON"

    }


    # ======================================================
    # REQUEST NASA POWER
    # ======================================================

    try:

        response = requests.get(

            NASA_POWER_URL,

            params=request_parameters,

            timeout=30

        )


        # --------------------------------------------------
        # HTTP ERROR
        # --------------------------------------------------

        if response.status_code != 200:

            try:

                error_data = response.json()

            except Exception:

                error_data = {}


            messages = (
                error_data.get(
                    "messages",
                    ""
                )
            )


            if isinstance(
                messages,
                list
            ):

                messages = " ".join(
                    str(message)
                    for message in messages
                )


            raise Exception(

                f"NASA POWER returned HTTP "
                f"{response.status_code}. "
                f"{messages}"

            )


        # --------------------------------------------------
        # JSON RESPONSE
        # --------------------------------------------------

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

            "NASA POWER returned invalid JSON."

        )


    # ======================================================
    # RESPONSE VALIDATION
    # ======================================================

    if not isinstance(
        data,
        dict
    ):

        raise Exception(

            "NASA POWER returned an "
            "unexpected response."

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
    # EXTRACT SOLAR PARAMETER
    # ======================================================

    solar_parameter = parameter_data.get(

        "ALLSKY_SFC_SW_DWN",

        {}

    )


    # ======================================================
    # EXTRACT TEMPERATURE PARAMETER
    # ======================================================

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
    # EXTRACT MONTHLY SOLAR DATA
    # ======================================================

    monthly_solar = {}


    for month_code in MONTHS:

        value = solar_parameter.get(

            month_code

        )


        number = safe_float(

            value

        )


        if number is not None:

            monthly_solar[
                month_code
            ] = number


    # ======================================================
    # EXTRACT MONTHLY TEMPERATURE DATA
    # ======================================================

    monthly_temperature = {}


    for month_code in MONTHS:

        value = temperature_parameter.get(

            month_code

        )


        number = safe_float(

            value

        )


        if number is not None:

            monthly_temperature[
                month_code
            ] = number


    # ======================================================
    # VALIDATE SOLAR DATA
    # ======================================================

    if not monthly_solar:

        # Provide diagnostic information.
        # This will help us troubleshoot future
        # NASA POWER response changes.

        returned_parameters = list(
            parameter_data.keys()
        )


        raise Exception(

            "NASA POWER responded successfully, "
            "but no usable monthly solar-resource "
            "values were found. Returned parameters: "
            f"{returned_parameters}"

        )


    # ======================================================
    # CALCULATE AVERAGE SOLAR RESOURCE
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
    # CALCULATE AVERAGE TEMPERATURE
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
    # BEST SOLAR MONTH
    # ======================================================

    best_month_code = max(

        monthly_solar,

        key=monthly_solar.get

    )


    best_month_value = (

        monthly_solar[
            best_month_code
        ]

    )


    # ======================================================
    # WORST SOLAR MONTH
    # ======================================================

    worst_month_code = min(

        monthly_solar,

        key=monthly_solar.get

    )


    worst_month_value = (

        monthly_solar[
            worst_month_code
        ]

    )


    # ======================================================
    # MONTHLY DISPLAY DATA
    # ======================================================

    monthly_display = []


    for month_code, month_name in MONTHS.items():

        monthly_display.append({

            "month":
                month_name,

            "solar_resource":
                monthly_solar.get(
                    month_code
                ),

            "temperature":
                monthly_temperature.get(
                    month_code
                )

        })


    # ======================================================
    # RETURN RESULT
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
            MONTHS[
                best_month_code
            ],

        "best_month_value":
            best_month_value,

        "worst_month":
            MONTHS[
                worst_month_code
            ],

        "worst_month_value":
            worst_month_value,

        "data_source":
            "NASA POWER",

        "climatology_period":
            f"{NASA_START_YEAR}-{NASA_END_YEAR}",

        "api_url":
            NASA_POWER_URL

    }


# ==========================================================
# PEAK SUN HOURS
# ==========================================================

def calculate_peak_sun_hours(
    average_solar
):

    """
    Convert average daily solar irradiation
    in kWh/m²/day into equivalent peak sun hours.

    For this solar-resource quantity, the numerical
    value is approximately equivalent to peak sun hours.
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
    Create a simplified summary for the UI.
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
            ),

        "climatology_period":
            solar_data.get(
                "climatology_period",
                f"{NASA_START_YEAR}-{NASA_END_YEAR}"
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
