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
# Process the already-processed NASA POWER data returned
# by solar_api.py for visualization and engineering analysis.
#
# IMPORTANT:
# This module works with the structure returned by:
#
#     get_solar_resource(latitude, longitude)
#
# from solar_api.py
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

    if value is None:
        return None

    try:

        number = float(value)

        # Reject NaN
        if number != number:
            return None

        # Reject NASA POWER missing-value indicators
        if number <= -900:
            return None

        return number

    except (TypeError, ValueError):

        return None


# ==========================================================
# SECTION 3 - MONTH KEY NORMALIZATION
# ==========================================================

def get_month_name(key):
    """
    Convert a NASA POWER month key into a month name.

    Supports:

        JAN
        FEB
        ...
        DEC

    and:

        01
        02
        ...
        12

    and integer month numbers.
    """

    if isinstance(key, int):

        if 1 <= key <= 12:

            return MONTH_NAMES[key - 1]

        return str(key)

    key_string = str(key).strip().upper()

    # Numeric month
    if key_string.isdigit():

        month_number = int(key_string)

        if 1 <= month_number <= 12:

            return MONTH_NAMES[
                month_number - 1
            ]

    # NASA POWER month code
    month_codes = {
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

    return month_codes.get(
        key_string,
        key_string
    )


# ==========================================================
# SECTION 4 - EXTRACT MONTHLY SOLAR DATA
# ==========================================================

def extract_monthly_solar_data(solar_data):
    """
    Extract monthly solar-resource values.

    This function is designed specifically for the data
    returned by solar_api.py.

    Expected structure:

        {
            "monthly_solar": {
                "JAN": value,
                "FEB": value,
                ...
            }
        }

    It also supports:

        monthly_display

    and the original NASA POWER structure as a fallback.

    Returns:

        [
            {
                "month": "January",
                "month_short": "Jan",
                "month_number": 1,
                "solar_value": value
            },
            ...
        ]
    """

    results = []

    if not isinstance(
        solar_data,
        dict
    ):
        return results


    # ======================================================
    # FIRST: Use processed monthly_solar data
    # ======================================================

    monthly_solar = solar_data.get(
        "monthly_solar"
    )


    if isinstance(
        monthly_solar,
        dict
    ):

        for index, month_code in enumerate(
            [
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
            ],
            start=1
        ):

            value = monthly_solar.get(
                month_code
            )

            # Also try lowercase
            if value is None:

                value = monthly_solar.get(
                    month_code.lower()
                )

            # Also try numeric key
            if value is None:

                value = monthly_solar.get(
                    index
                )

            # Also try numeric string
            if value is None:

                value = monthly_solar.get(
                    str(index)
                )

            value = safe_float(
                value
            )

            if value is not None:

                results.append({

                    "month":
                        MONTH_NAMES[index - 1],

                    "month_short":
                        MONTH_ABBREVIATIONS[index - 1],

                    "month_number":
                        index,

                    "solar_value":
                        value

                })


        if results:

            return results


    # ======================================================
    # SECOND: Use monthly_display
    # ======================================================

    monthly_display = solar_data.get(
        "monthly_display"
    )


    if isinstance(
        monthly_display,
        list
    ):

        for index, item in enumerate(
            monthly_display,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):
                continue


            value = item.get(
                "solar_resource"
            )


            if value is None:

                value = item.get(
                    "solar_value"
                )


            value = safe_float(
                value
            )


            if value is not None:

                month_name = item.get(
                    "month"
                )


                if not month_name:

                    month_name = (
                        MONTH_NAMES[index - 1]
                    )


                results.append({

                    "month":
                        month_name,

                    "month_short":
                        MONTH_ABBREVIATIONS[index - 1],

                    "month_number":
                        index,

                    "solar_value":
                        value

                })


        if results:

            return results


    # ======================================================
    # THIRD: Original NASA POWER structure
    # ======================================================

    parameter_data = solar_data.get(
        "ALLSKY_SFC_SW_DWN"
    )


    if parameter_data is None:

        properties = solar_data.get(
            "properties",
            {}
        )


        if isinstance(
            properties,
            dict
        ):

            parameter_data = (
                properties
                .get(
                    "parameter",
                    {}
                )
                .get(
                    "ALLSKY_SFC_SW_DWN"
                )
            )


    if isinstance(
        parameter_data,
        dict
    ):

        month_codes = [
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


        for index, month_code in enumerate(
            month_codes,
            start=1
        ):

            value = parameter_data.get(
                month_code
            )


            if value is None:

                value = parameter_data.get(
                    f"{index:02d}"
                )


            if value is None:

                value = parameter_data.get(
                    index
                )


            value = safe_float(
                value
            )


            if value is not None:

                results.append({

                    "month":
                        MONTH_NAMES[index - 1],

                    "month_short":
                        MONTH_ABBREVIATIONS[index - 1],

                    "month_number":
                        index,

                    "solar_value":
                        value

                })


    return results


# ==========================================================
# SECTION 5 - EXTRACT MONTHLY TEMPERATURE
# ==========================================================

def extract_monthly_temperature_data(
    solar_data
):
    """
    Extract monthly average temperature.

    Works with the processed structure returned by
    solar_api.py.
    """

    results = []

    if not isinstance(
        solar_data,
        dict
    ):
        return results


    # ======================================================
    # FIRST: Processed monthly_temperature
    # ======================================================

    monthly_temperature = solar_data.get(
        "monthly_temperature"
    )


    if isinstance(
        monthly_temperature,
        dict
    ):

        month_codes = [
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


        for index, month_code in enumerate(
            month_codes,
            start=1
        ):

            value = monthly_temperature.get(
                month_code
            )


            if value is None:

                value = monthly_temperature.get(
                    month_code.lower()
                )


            if value is None:

                value = monthly_temperature.get(
                    index
                )


            if value is None:

                value = monthly_temperature.get(
                    str(index)
                )


            value = safe_float(
                value
            )


            if value is not None:

                results.append({

                    "month":
                        MONTH_NAMES[index - 1],

                    "month_short":
                        MONTH_ABBREVIATIONS[index - 1],

                    "month_number":
                        index,

                    "temperature":
                        value

                })


        if results:

            return results


    # ======================================================
    # SECOND: monthly_display fallback
    # ======================================================

    monthly_display = solar_data.get(
        "monthly_display"
    )


    if isinstance(
        monthly_display,
        list
    ):

        for index, item in enumerate(
            monthly_display,
            start=1
        ):

            if not isinstance(
                item,
                dict
            ):
                continue


            value = item.get(
                "temperature"
            )


            value = safe_float(
                value
            )


            if value is not None:

                results.append({

                    "month":
                        item.get(
                            "month",
                            MONTH_NAMES[index - 1]
                        ),

                    "month_short":
                        MONTH_ABBREVIATIONS[index - 1],

                    "month_number":
                        index,

                    "temperature":
                        value

                })


        if results:

            return results


    # ======================================================
    # THIRD: Original NASA POWER structure
    # ======================================================

    parameter_data = solar_data.get(
        "T2M"
    )


    if parameter_data is None:

        properties = solar_data.get(
            "properties",
            {}
        )


        if isinstance(
            properties,
            dict
        ):

            parameter_data = (
                properties
                .get(
                    "parameter",
                    {}
                )
                .get(
                    "T2M"
                )
            )


    if isinstance(
        parameter_data,
        dict
    ):

        month_codes = [
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


        for index, month_code in enumerate(
            month_codes,
            start=1
        ):

            value = parameter_data.get(
                month_code
            )


            if value is None:

                value = parameter_data.get(
                    f"{index:02d}"
                )


            if value is None:

                value = parameter_data.get(
                    index
                )


            value = safe_float(
                value
            )


            if value is not None:

                results.append({

                    "month":
                        MONTH_NAMES[index - 1],

                    "month_short":
                        MONTH_ABBREVIATIONS[index - 1],

                    "month_number":
                        index,

                    "temperature":
                        value

                })


    return results


# ==========================================================
# SECTION 6 - SOLAR STATISTICS
# ==========================================================

def calculate_solar_statistics(
    monthly_solar
):
    """
    Calculate annual solar-resource statistics.
    """

    empty_result = {

        "annual_average": None,

        "maximum": None,

        "minimum": None,

        "best_month": None,

        "lowest_month": None

    }


    if not monthly_solar:

        return empty_result


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

        return empty_result


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
# SECTION 7 - TEMPERATURE STATISTICS
# ==========================================================

def calculate_temperature_statistics(
    monthly_temperature
):
    """
    Calculate annual temperature statistics.
    """

    empty_result = {

        "annual_average": None,

        "maximum": None,

        "minimum": None,

        "hottest_month": None,

        "coolest_month": None

    }


    if not monthly_temperature:

        return empty_result


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

        return empty_result


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
# SECTION 8 - SEASONAL ANALYSIS
# ==========================================================

def calculate_seasonal_analysis(
    monthly_solar
):
    """
    Classify months into:

        High solar
        Medium solar
        Low solar

    Classification is based on the annual monthly
    average rather than fixed geographic assumptions.
    """

    empty_result = {

        "high_solar_months": [],

        "medium_solar_months": [],

        "low_solar_months": []

    }


    if not monthly_solar:

        return empty_result


    valid_items = []


    for item in monthly_solar:

        value = safe_float(
            item.get(
                "solar_value"
            )
        )


        if value is not None:

            valid_items.append(
                (
                    item,
                    value
                )
            )


    if not valid_items:

        return empty_result


    average = (
        sum(
            value
            for item, value
            in valid_items
        )
        /
        len(valid_items)
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


    for item, value in valid_items:

        month = item.get(
            "month"
        )


        if value >= high_threshold:

            high.append(
                month
            )

        elif value <= low_threshold:

            low.append(
                month
            )

        else:

            medium.append(
                month
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
# SECTION 9 - MONTHLY COMBINED DATA
# ==========================================================

def create_monthly_combined_data(
    monthly_solar,
    monthly_temperature
):
    """
    Combine solar and temperature data into a single
    monthly dataset suitable for Streamlit charts,
    tables and reports.
    """

    combined = []


    solar_lookup = {}

    temperature_lookup = {}


    # ------------------------------------------------------
    # Solar lookup
    # ------------------------------------------------------

    for item in monthly_solar:

        month_number = item.get(
            "month_number"
        )


        if month_number is not None:

            solar_lookup[
                month_number
            ] = safe_float(
                item.get(
                    "solar_value"
                )
            )


    # ------------------------------------------------------
    # Temperature lookup
    # ------------------------------------------------------

    for item in monthly_temperature:

        month_number = item.get(
            "month_number"
        )


        if month_number is not None:

            temperature_lookup[
                month_number
            ] = safe_float(
                item.get(
                    "temperature"
                )
            )


    # ------------------------------------------------------
    # Build complete 12-month dataset
    # ------------------------------------------------------

    for month_number in range(
        1,
        13
    ):

        combined.append({

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

            "solar_resource":
                solar_lookup.get(
                    month_number
                ),

            "temperature":
                temperature_lookup.get(
                    month_number
                )

        })


    return combined


# ==========================================================
# SECTION 10 - COMPLETE SOLAR ANALYTICS
# ==========================================================

def analyze_solar_resource(
    solar_data
):
    """
    Perform complete solar-resource analysis.

    This is the main function that should be called
    by main.py.

    Returns a dictionary containing:

        monthly_solar
        monthly_temperature
        monthly_combined
        solar_statistics
        temperature_statistics
        seasonal_analysis
        data_source
        climatology_period
    """

    # ------------------------------------------------------
    # Extract monthly solar
    # ------------------------------------------------------

    monthly_solar = (
        extract_monthly_solar_data(
            solar_data
        )
    )


    # ------------------------------------------------------
    # Extract temperature
    # ------------------------------------------------------

    monthly_temperature = (
        extract_monthly_temperature_data(
            solar_data
        )
    )


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


    # ------------------------------------------------------
    # Seasonal classification
    # ------------------------------------------------------

    seasonal_analysis = (
        calculate_seasonal_analysis(
            monthly_solar
        )
    )


    # ------------------------------------------------------
    # Combined monthly data
    # ------------------------------------------------------

    monthly_combined = (
        create_monthly_combined_data(
            monthly_solar,
            monthly_temperature
        )
    )


    # ------------------------------------------------------
    # Metadata
    # ------------------------------------------------------

    data_source = solar_data.get(
        "data_source",
        "NASA POWER"
    ) if isinstance(
        solar_data,
        dict
    ) else "NASA POWER"


    climatology_period = solar_data.get(
        "climatology_period"
    ) if isinstance(
        solar_data,
        dict
    ) else None


    # ------------------------------------------------------
    # Return complete analytics package
    # ------------------------------------------------------

    return {

        "monthly_solar":
            monthly_solar,

        "monthly_temperature":
            monthly_temperature,

        "monthly_combined":
            monthly_combined,

        "solar_statistics":
            solar_statistics,

        "temperature_statistics":
            temperature_statistics,

        "seasonal_analysis":
            seasonal_analysis,

        "data_source":
            data_source,

        "climatology_period":
            climatology_period

    }


# ==========================================================
# SECTION 11 - SIMPLE SUMMARY FUNCTION
# ==========================================================

def get_analytics_summary(
    solar_data
):
    """
    Return a compact human-readable analytics summary.

    Useful for main.py and PDF reports.
    """

    analytics = analyze_solar_resource(
        solar_data
    )


    solar_stats = analytics.get(
        "solar_statistics",
        {}
    )


    temperature_stats = analytics.get(
        "temperature_statistics",
        {}
    )


    seasonal = analytics.get(
        "seasonal_analysis",
        {}
    )


    return {

        "average_solar":
            solar_stats.get(
                "annual_average"
            ),

        "maximum_solar":
            solar_stats.get(
                "maximum"
            ),

        "minimum_solar":
            solar_stats.get(
                "minimum"
            ),

        "best_month":
            solar_stats.get(
                "best_month"
            ),

        "lowest_month":
            solar_stats.get(
                "lowest_month"
            ),

        "average_temperature":
            temperature_stats.get(
                "annual_average"
            ),

        "maximum_temperature":
            temperature_stats.get(
                "maximum"
            ),

        "minimum_temperature":
            temperature_stats.get(
                "minimum"
            ),

        "hottest_month":
            temperature_stats.get(
                "hottest_month"
            ),

        "coolest_month":
            temperature_stats.get(
                "coolest_month"
            ),

        "high_solar_months":
            seasonal.get(
                "high_solar_months",
                []
            ),

        "medium_solar_months":
            seasonal.get(
                "medium_solar_months",
                []
            ),

        "low_solar_months":
            seasonal.get(
                "low_solar_months",
                []
            )

    }


# ==========================================================
# SECTION 12 - DATA AVAILABILITY CHECK
# ==========================================================

def has_solar_analytics_data(
    solar_data
):
    """
    Check whether usable monthly solar data exists.
    """

    monthly_solar = (
        extract_monthly_solar_data(
            solar_data
        )
    )


    return len(
        monthly_solar
    ) > 0


# ==========================================================
# SECTION 13 - TEST FUNCTION
# ==========================================================

def test_solar_analytics(
    solar_data
):
    """
    Test the analytics engine.

    Returns a simple diagnostic dictionary.
    """

    try:

        analytics = analyze_solar_resource(
            solar_data
        )


        monthly_solar_count = len(
            analytics.get(
                "monthly_solar",
                []
            )
        )


        monthly_temperature_count = len(
            analytics.get(
                "monthly_temperature",
                []
            )
        )


        solar_statistics = analytics.get(
            "solar_statistics",
            {}
        )


        seasonal = analytics.get(
            "seasonal_analysis",
            {}
        )


        return {

            "success":
                True,

            "message":
                "Solar analytics processed successfully.",

            "monthly_solar_count":
                monthly_solar_count,

            "monthly_temperature_count":
                monthly_temperature_count,

            "average_solar":
                solar_statistics.get(
                    "annual_average"
                ),

            "best_month":
                solar_statistics.get(
                    "best_month"
                ),

            "lowest_month":
                solar_statistics.get(
                    "lowest_month"
                ),

            "high_solar_months":
                seasonal.get(
                    "high_solar_months",
                    []
                ),

            "medium_solar_months":
                seasonal.get(
                    "medium_solar_months",
                    []
                ),

            "low_solar_months":
                seasonal.get(
                    "low_solar_months",
                    []
                )

        }


    except Exception as error:

        return {

            "success":
                False,

            "message":
                str(error),

            "monthly_solar_count":
                0,

            "monthly_temperature_count":
                0

        }


# ==========================================================
# END OF SOLAR ANALYTICS MODULE
# ==========================================================
