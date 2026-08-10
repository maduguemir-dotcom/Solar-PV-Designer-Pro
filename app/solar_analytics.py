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
# for visualization and engineering analysis.
#
# ==========================================================

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
# SECTION 1 - SAFE FLOAT CONVERSION
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
# SECTION 2 - EXTRACT MONTHLY SOLAR DATA
# ==========================================================

def extract_monthly_solar_data(solar_data):
    """
    Extract monthly solar-resource data.

    Supports the structure returned directly by
    solar_api.py.
    """

    results = []

    if not isinstance(solar_data, dict):
        return results

    # ------------------------------------------------------
    # Primary structure used by solar_api.py
    # ------------------------------------------------------

    parameter_data = solar_data.get(
        "monthly_solar"
    )

    # ------------------------------------------------------
    # Alternative NASA POWER structure
    # ------------------------------------------------------

    if parameter_data is None:

        parameter_data = solar_data.get(
            "ALLSKY_SFC_SW_DWN"
        )

    # ------------------------------------------------------
    # Nested NASA POWER structure
    # ------------------------------------------------------

    if parameter_data is None:

        properties = solar_data.get(
            "properties",
            {}
        )

        if isinstance(properties, dict):

            parameter = properties.get(
                "parameter",
                {}
            )

            if isinstance(parameter, dict):

                parameter_data = parameter.get(
                    "ALLSKY_SFC_SW_DWN"
                )

    if not isinstance(parameter_data, dict):
        return results

    # ------------------------------------------------------
    # NASA POWER monthly keys can be:
    #
    # JAN, FEB, MAR...
    #
    # or:
    #
    # 01, 02, 03...
    # ------------------------------------------------------

    nasa_month_codes = [
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

    for index in range(12):

        month_number = index + 1

        month_code = nasa_month_codes[index]

        value = parameter_data.get(
            month_code
        )

        if value is None:

            value = parameter_data.get(
                f"{month_number:02d}"
            )

        if value is None:

            value = parameter_data.get(
                month_number
            )

        value = safe_float(value)

        if value is not None:

            results.append({

                "month":
                    MONTH_NAMES[index],

                "month_short":
                    MONTH_ABBREVIATIONS[index],

                "month_number":
                    month_number,

                "solar_value":
                    value

            })

    return results


# ==========================================================
# SECTION 3 - EXTRACT MONTHLY TEMPERATURE DATA
# ==========================================================

def extract_monthly_temperature_data(solar_data):
    """
    Extract monthly average temperature.

    Supports the structure returned directly by
    solar_api.py.
    """

    results = []

    if not isinstance(solar_data, dict):
        return results

    # ------------------------------------------------------
    # Primary structure used by solar_api.py
    # ------------------------------------------------------

    parameter_data = solar_data.get(
        "monthly_temperature"
    )

    # ------------------------------------------------------
    # Alternative structure
    # ------------------------------------------------------

    if parameter_data is None:

        parameter_data = solar_data.get(
            "T2M"
        )

    # ------------------------------------------------------
    # Nested NASA POWER structure
    # ------------------------------------------------------

    if parameter_data is None:

        properties = solar_data.get(
            "properties",
            {}
        )

        if isinstance(properties, dict):

            parameter = properties.get(
                "parameter",
                {}
            )

            if isinstance(parameter, dict):

                parameter_data = parameter.get(
                    "T2M"
                )

    if not isinstance(parameter_data, dict):
        return results

    nasa_month_codes = [
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

    for index in range(12):

        month_number = index + 1

        month_code = nasa_month_codes[index]

        value = parameter_data.get(
            month_code
        )

        if value is None:

            value = parameter_data.get(
                f"{month_number:02d}"
            )

        if value is None:

            value = parameter_data.get(
                month_number
            )

        value = safe_float(value)

        if value is not None:

            results.append({

                "month":
                    MONTH_NAMES[index],

                "month_short":
                    MONTH_ABBREVIATIONS[index],

                "month_number":
                    month_number,

                "temperature":
                    value

            })

    return results


# ==========================================================
# SECTION 4 - ANNUAL SOLAR STATISTICS
# ==========================================================

def calculate_solar_statistics(monthly_solar):

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
# SECTION 5 - TEMPERATURE STATISTICS
# ==========================================================

def calculate_temperature_statistics(
    monthly_temperature
):

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
# SECTION 6 - SEASONAL ANALYSIS
# ==========================================================

def calculate_seasonal_analysis(
    monthly_solar
):

    if not monthly_solar:

        return {

            "high_solar_months": [],
            "medium_solar_months": [],
            "low_solar_months": []

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
            "low_solar_months": []

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
            low

    }


# ==========================================================
# SECTION 7 - BUILD GRAPH DATA
# ==========================================================

def build_monthly_graph_data(
    monthly_solar,
    monthly_temperature
):
    """
    Create a unified 12-month dataset suitable for
    Streamlit charts.
    """

    solar_lookup = {}

    temperature_lookup = {}

    for item in monthly_solar:

        month = item.get(
            "month"
        )

        value = safe_float(
            item.get(
                "solar_value"
            )
        )

        if month and value is not None:

            solar_lookup[month] = value

    for item in monthly_temperature:

        month = item.get(
            "month"
        )

        value = safe_float(
            item.get(
                "temperature"
            )
        )

        if month and value is not None:

            temperature_lookup[month] = value

    graph_data = []

    for index in range(12):

        month = MONTH_NAMES[index]

        graph_data.append({

            "month":
                month,

            "month_short":
                MONTH_ABBREVIATIONS[index],

            "solar_resource":
                solar_lookup.get(
                    month
                ),

            "temperature":
                temperature_lookup.get(
                    month
                )

        })

    return graph_data


# ==========================================================
# SECTION 8 - COMPLETE SOLAR ANALYSIS
# ==========================================================

def analyze_solar_resource(
    solar_data
):
    """
    Perform complete solar-resource analysis.

    This function is deliberately compatible with the
    existing solar_api.py used by Solar PV Designer Pro.
    """

    # ------------------------------------------------------
    # Extract monthly datasets
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # If extraction failed, try monthly_display
    # returned directly by solar_api.py.
    # ------------------------------------------------------

    if (
        not monthly_solar
        or not monthly_temperature
    ):

        if isinstance(
            solar_data,
            dict
        ):

            monthly_display = (
                solar_data.get(
                    "monthly_display",
                    []
                )
            )

            if isinstance(
                monthly_display,
                list
            ):

                if not monthly_solar:

                    for index, item in enumerate(
                        monthly_display
                    ):

                        if not isinstance(
                            item,
                            dict
                        ):
                            continue

                        value = safe_float(
                            item.get(
                                "solar_resource"
                            )
                        )

                        if value is not None:

                            monthly_solar.append({

                                "month":
                                    item.get(
                                        "month",
                                        MONTH_NAMES[index]
                                    ),

                                "month_short":
                                    MONTH_ABBREVIATIONS[index],

                                "month_number":
                                    index + 1,

                                "solar_value":
                                    value

                            })

                if not monthly_temperature:

                    for index, item in enumerate(
                        monthly_display
                    ):

                        if not isinstance(
                            item,
                            dict
                        ):
                            continue

                        value = safe_float(
                            item.get(
                                "temperature"
                            )
                        )

                        if value is not None:

                            monthly_temperature.append({

                                "month":
                                    item.get(
                                        "month",
                                        MONTH_NAMES[index]
                                    ),

                                "month_short":
                                    MONTH_ABBREVIATIONS[index],

                                "month_number":
                                    index + 1,

                                "temperature":
                                    value

                            })

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # Graph data
    # ------------------------------------------------------

    graph_data = build_monthly_graph_data(
        monthly_solar,
        monthly_temperature
    )

    # ------------------------------------------------------
    # Return complete analytics package
    # ------------------------------------------------------

    return {

        "monthly_solar":
            monthly_solar,

        "monthly_temperature":
            monthly_temperature,

        "graph_data":
            graph_data,

        "solar_statistics":
            solar_statistics,

        "temperature_statistics":
            temperature_statistics,

        "seasonal_analysis":
            seasonal_analysis

    }
