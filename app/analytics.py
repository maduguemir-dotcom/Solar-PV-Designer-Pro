# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Solar Analytics Module
# Version: 2.3.1
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Process NASA POWER monthly solar and temperature data
# returned by solar_api.py.
#
# ==========================================================


# ==========================================================
# SECTION 1 - MONTH DEFINITIONS
# ==========================================================

MONTH_CODES = [
    "JAN",
    "FEB",
    "MAR",
    "APR",
    "MAY",
    "JUN",
    "JUL",
    "AUG",
    "SEP",
    "OCT",
    "NOV",
    "DEC"
]


MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


MONTH_ABBREVIATIONS = [
    "Jan",
    "Feb",
    "Mar",
    "Apr",
    "May",
    "Jun",
    "Jul",
    "Aug",
    "Sep",
    "Oct",
    "Nov",
    "Dec"
]


# ==========================================================
# SECTION 2 - SAFE FLOAT CONVERSION
# ==========================================================

def safe_float(value):
    """
    Safely convert a value to float.

    Returns None if conversion fails.
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
# SECTION 3 - EXTRACT MONTHLY SOLAR DATA
# ==========================================================

def extract_monthly_solar_data(solar_data):
    """
    Extract monthly solar-resource values from the
    structure returned by solar_api.py.

    Expected structure:

        solar_data["monthly_solar"]

    Example:

        {
            "JAN": 5.2,
            "FEB": 5.4,
            ...
        }
    """

    results = []

    if not isinstance(solar_data, dict):
        return results

    parameter_data = solar_data.get(
        "monthly_solar",
        {}
    )

    if not isinstance(parameter_data, dict):
        return results

    for index, month_code in enumerate(MONTH_CODES):

        value = parameter_data.get(
            month_code
        )

        # Also support lowercase keys
        if value is None:

            value = parameter_data.get(
                month_code.lower()
            )

        value = safe_float(value)

        if value is not None:

            results.append({

                "month":
                    MONTH_NAMES[index],

                "month_short":
                    MONTH_ABBREVIATIONS[index],

                "month_code":
                    month_code,

                "month_number":
                    index + 1,

                "solar_value":
                    value

            })

    return results


# ==========================================================
# SECTION 4 - EXTRACT MONTHLY TEMPERATURE
# ==========================================================

def extract_monthly_temperature_data(solar_data):
    """
    Extract monthly temperature values from the structure
    returned by solar_api.py.

    Expected structure:

        solar_data["monthly_temperature"]
    """

    results = []

    if not isinstance(solar_data, dict):
        return results

    parameter_data = solar_data.get(
        "monthly_temperature",
        {}
    )

    if not isinstance(parameter_data, dict):
        return results

    for index, month_code in enumerate(MONTH_CODES):

        value = parameter_data.get(
            month_code
        )

        if value is None:

            value = parameter_data.get(
                month_code.lower()
            )

        value = safe_float(value)

        if value is not None:

            results.append({

                "month":
                    MONTH_NAMES[index],

                "month_short":
                    MONTH_ABBREVIATIONS[index],

                "month_code":
                    month_code,

                "month_number":
                    index + 1,

                "temperature":
                    value

            })

    return results


# ==========================================================
# SECTION 5 - ANNUAL SOLAR STATISTICS
# ==========================================================

def calculate_solar_statistics(monthly_solar):
    """
    Calculate annual solar-resource statistics.
    """

    if not monthly_solar:

        return {

            "annual_average": None,

            "maximum": None,

            "minimum": None,

            "best_month": None,

            "lowest_month": None

        }

    values = []

    for item in monthly_solar:

        value = safe_float(
            item.get("solar_value")
        )

        if value is not None:

            values.append(
                (item, value)
            )

    if not values:

        return {

            "annual_average": None,

            "maximum": None,

            "minimum": None,

            "best_month": None,

            "lowest_month": None

        }

    average = (
        sum(
            value
            for item, value in values
        )
        /
        len(values)
    )

    best_item, best_value = max(
        values,
        key=lambda pair: pair[1]
    )

    lowest_item, lowest_value = min(
        values,
        key=lambda pair: pair[1]
    )

    return {

        "annual_average":
            average,

        "maximum":
            best_value,

        "minimum":
            lowest_value,

        "best_month":
            best_item.get("month"),

        "lowest_month":
            lowest_item.get("month")

    }


# ==========================================================
# SECTION 6 - TEMPERATURE STATISTICS
# ==========================================================

def calculate_temperature_statistics(
    monthly_temperature
):
    """
    Calculate annual temperature statistics.
    """

    if not monthly_temperature:

        return {

            "annual_average": None,

            "maximum": None,

            "minimum": None,

            "hottest_month": None,

            "coolest_month": None

        }

    values = []

    for item in monthly_temperature:

        value = safe_float(
            item.get("temperature")
        )

        if value is not None:

            values.append(
                (item, value)
            )

    if not values:

        return {

            "annual_average": None,

            "maximum": None,

            "minimum": None,

            "hottest_month": None,

            "coolest_month": None

        }

    average = (
        sum(
            value
            for item, value in values
        )
        /
        len(values)
    )

    hottest_item, hottest_value = max(
        values,
        key=lambda pair: pair[1]
    )

    coolest_item, coolest_value = min(
        values,
        key=lambda pair: pair[1]
    )

    return {

        "annual_average":
            average,

        "maximum":
            hottest_value,

        "minimum":
            coolest_value,

        "hottest_month":
            hottest_item.get("month"),

        "coolest_month":
            coolest_item.get("month")

    }


# ==========================================================
# SECTION 7 - SEASONAL ANALYSIS
# ==========================================================

def calculate_seasonal_analysis(monthly_solar):
    """
    Classify months according to their solar resource.

    High:
        >= 110% of annual average

    Low:
        <= 90% of annual average

    Medium:
        between the two thresholds
    """

    if not monthly_solar:

        return {

            "high_solar_months": [],

            "medium_solar_months": [],

            "low_solar_months": [],

            "average": None,

            "high_threshold": None,

            "low_threshold": None

        }

    values = []

    for item in monthly_solar:

        value = safe_float(
            item.get("solar_value")
        )

        if value is not None:

            values.append(value)

    if not values:

        return {

            "high_solar_months": [],

            "medium_solar_months": [],

            "low_solar_months": [],

            "average": None,

            "high_threshold": None,

            "low_threshold": None

        }

    average = (
        sum(values)
        /
        len(values)
    )

    high_threshold = average * 1.10
    low_threshold = average * 0.90

    high = []
    medium = []
    low = []

    for item in monthly_solar:

        value = safe_float(
            item.get("solar_value")
        )

        if value is None:
            continue

        month = item.get(
            "month",
            "Unknown"
        )

        if value >= high_threshold:

            high.append(month)

        elif value <= low_threshold:

            low.append(month)

        else:

            medium.append(month)

    return {

        "high_solar_months":
            high,

        "medium_solar_months":
            medium,

        "low_solar_months":
            low,

        "average":
            average,

        "high_threshold":
            high_threshold,

        "low_threshold":
            low_threshold

    }


# ==========================================================
# SECTION 8 - CREATE CHART DATA
# ==========================================================

def create_monthly_chart_data(
    solar_data
):
    """
    Create a simple monthly table suitable for
    Streamlit charts and PDF reports.
    """

    monthly_solar = (
        extract_monthly_solar_data(
            solar_data
        )
    )

    monthly_temperature = (
        extract_monthly_temperature_data(
            solar_data
        )
    )

    temperature_lookup = {

        item["month_code"]:
            item["temperature"]

        for item in monthly_temperature

        if item.get("temperature") is not None

    }

    chart_data = []

    for item in monthly_solar:

        month_code = item.get(
            "month_code"
        )

        chart_data.append({

            "Month":
                item.get("month"),

            "Month Short":
                item.get("month_short"),

            "Solar Resource":
                item.get("solar_value"),

            "Temperature":
                temperature_lookup.get(
                    month_code
                )

        })

    return chart_data


# ==========================================================
# SECTION 9 - COMPLETE ANALYTICS FUNCTION
# ==========================================================

def analyze_solar_resource(
    solar_data
):
    """
    Perform complete solar-resource analysis.

    This function is designed to work directly with the
    dictionary returned by:

        get_solar_resource()
    """

    monthly_solar = (
        extract_monthly_solar_data(
            solar_data
        )
    )

    monthly_temperature = (
        extract_monthly_temperature_data(
            solar_data
        )
    )

    solar_statistics = (
        calculate_solar_statistics(
            monthly_solar
        )
    )

    temperature_statistics = (
        calculate_temperature_statistics(
            monthly_temperature
        )
    )

    seasonal_analysis = (
        calculate_seasonal_analysis(
            monthly_solar
        )
    )

    chart_data = (
        create_monthly_chart_data(
            solar_data
        )
    )

    return {

        "monthly_solar":
            monthly_solar,

        "monthly_temperature":
            monthly_temperature,

        "solar_statistics":
            solar_statistics,

        "temperature_statistics":
            temperature_statistics,

        "seasonal_analysis":
            seasonal_analysis,

        "chart_data":
            chart_data,

        "data_source":
            solar_data.get(
                "data_source",
                "NASA POWER"
            ),

        "climatology_period":
            solar_data.get(
                "climatology_period"
            )

    }


# ==========================================================
# SECTION 10 - QUICK VALIDATION
# ==========================================================

def analytics_available(
    solar_data
):
    """
    Return True if usable monthly solar data exists.
    """

    monthly_solar = (
        extract_monthly_solar_data(
            solar_data
        )
    )

    return len(monthly_solar) > 0
