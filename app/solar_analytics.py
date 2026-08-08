# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Solar Analytics Module
# Version: 2.3.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Process NASA POWER monthly solar and temperature data
# for visualization and engineering analysis.
#
# ==========================================================


# ==========================================================
# SECTION 1 - MONTH DEFINITIONS
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
# SECTION 2 - SAFE FLOAT CONVERSION
# ==========================================================

def safe_float(value):
    """
    Safely convert a value to float.

    Returns None if conversion fails.
    """

    try:

        if value is None:

            return None

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return None


# ==========================================================
# SECTION 3 - EXTRACT MONTHLY SOLAR DATA
# ==========================================================

def extract_monthly_solar_data(
    solar_data
):
    """
    Extract monthly solar-resource values.

    Expected NASA POWER parameter:

        ALLSKY_SFC_SW_DWN

    Returns a list containing:

        month
        month_number
        solar_value
    """

    results = []


    if not isinstance(
        solar_data,
        dict
    ):

        return results


    # ------------------------------------------------------
    # NASA POWER may store data under different structures.
    # ------------------------------------------------------

    parameter_data = (
        solar_data.get(
            "ALLSKY_SFC_SW_DWN"
        )
    )


    if parameter_data is None:

        # Try nested properties

        properties = (
            solar_data.get(
                "properties",
                {}
            )
        )


        parameter_data = (
            properties.get(
                "parameter",
                {}
            ).get(
                "ALLSKY_SFC_SW_DWN"
            )
        )


    if not isinstance(
        parameter_data,
        dict
    ):

        return results


    # ------------------------------------------------------
    # Process monthly values
    # ------------------------------------------------------

    for month_number in range(
        1,
        13
    ):

        month_key = (
            f"{month_number:02d}"
        )


        value = (
            parameter_data.get(
                month_key
            )
        )


        if value is None:

            # Try integer key

            value = (
                parameter_data.get(
                    month_number
                )
            )


        value = safe_float(
            value
        )


        if value is not None:

            results.append({

                "month":
                    MONTH_NAMES[
                        month_number - 1
                    ],

                "month_short":
                    MONTH_ABBREVIATIONS[
                        month_number - 1
                    ],

                "month_number":
                    month_number,

                "solar_value":
                    value

            })


    return results


# ==========================================================
# SECTION 4 - EXTRACT MONTHLY TEMPERATURE
# ==========================================================

def extract_monthly_temperature_data(
    solar_data
):
    """
    Extract monthly average temperature.

    Expected NASA POWER parameter:

        T2M

    Returns monthly records.
    """

    results = []


    if not isinstance(
        solar_data,
        dict
    ):

        return results


    parameter_data = (
        solar_data.get(
            "T2M"
        )
    )


    if parameter_data is None:

        properties = (
            solar_data.get(
                "properties",
                {}
            )
        )


        parameter_data = (
            properties.get(
                "parameter",
                {}
            ).get(
                "T2M"
            )
        )


    if not isinstance(
        parameter_data,
        dict
    ):

        return results


    for month_number in range(
        1,
        13
    ):

        month_key = (
            f"{month_number:02d}"
        )


        value = (
            parameter_data.get(
                month_key
            )
        )


        if value is None:

            value = (
                parameter_data.get(
                    month_number
                )
            )


        value = safe_float(
            value
        )


        if value is not None:

            results.append({

                "month":
                    MONTH_NAMES[
                        month_number - 1
                    ],

                "month_short":
                    MONTH_ABBREVIATIONS[
                        month_number - 1
                    ],

                "month_number":
                    month_number,

                "temperature":
                    value

            })


    return results


# ==========================================================
# SECTION 5 - ANNUAL SOLAR ANALYSIS
# ==========================================================

def calculate_solar_statistics(
    monthly_solar
):
    """
    Calculate annual solar statistics.
    """

    if not monthly_solar:

        return {

            "annual_average":
                None,

            "maximum":
                None,

            "minimum":
                None,

            "best_month":
                None,

            "lowest_month":
                None

        }


    values = []


    for item in monthly_solar:

        value = safe_float(
            item.get(
                "solar_value"
            )
        )


        if value is not None:

            values.append(
                (
                    item,
                    value
                )
            )


    if not values:

        return {

            "annual_average":
                None,

            "maximum":
                None,

            "minimum":
                None,

            "best_month":
                None,

            "lowest_month":
                None

        }


    average = (
        sum(
            value
            for item, value
            in values
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
            best_item.get(
                "month"
            ),

        "lowest_month":
            lowest_item.get(
                "month"
            )

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

            "annual_average":
                None,

            "maximum":
                None,

            "minimum":
                None,

            "hottest_month":
                None,

            "coolest_month":
                None

        }


    values = []


    for item in monthly_temperature:

        value = safe_float(
            item.get(
                "temperature"
            )
        )


        if value is not None:

            values.append(
                (
                    item,
                    value
                )
            )


    if not values:

        return {

            "annual_average":
                None,

            "maximum":
                None,

            "minimum":
                None,

            "hottest_month":
                None,

            "coolest_month":
                None

        }


    average = (
        sum(
            value
            for item, value
            in values
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
            hottest_item.get(
                "month"
            ),

        "coolest_month":
            coolest_item.get(
                "month"
            )

    }


# ==========================================================
# SECTION 7 - SEASONAL ANALYSIS
# ==========================================================

def calculate_seasonal_analysis(
    monthly_solar
):
    """
    Classify months into broad solar-resource seasons.

    The classification is based on the monthly values
    themselves rather than fixed geographic assumptions.
    """

    if not monthly_solar:

        return {

            "high_solar_months":
                [],

            "medium_solar_months":
                [],

            "low_solar_months":
                []

        }


    values = [

        item["solar_value"]

        for item in monthly_solar

        if item.get(
            "solar_value"
        ) is not None

    ]


    if not values:

        return {

            "high_solar_months":
                [],

            "medium_solar_months":
                [],

            "low_solar_months":
                []

        }


    average = (
        sum(values)
        /
        len(values)
    )


    high_threshold = (
        average * 1.10
    )


    low_threshold = (
        average * 0.90
    )


    high = []

    medium = []

    low = []


    for item in monthly_solar:

        value = item.get(
            "solar_value"
        )


        if value is None:

            continue


        if value >= high_threshold:

            high.append(
                item["month"]
            )

        elif value <= low_threshold:

            low.append(
                item["month"]
            )

        else:

            medium.append(
                item["month"]
            )


    return {

        "high_solar_months":
            high,

        "medium_solar_months":
            medium,

        "low_solar_months":
            low

    }


# ==========================================================
# SECTION 8 - COMPLETE ANALYTICS FUNCTION
# ==========================================================

def analyze_solar_resource(
    solar_data
):
    """
    Perform complete solar-resource analysis.

    Returns a single dictionary suitable for use by
    Streamlit, charts and PDF reports.
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
            seasonal_analysis

    }
