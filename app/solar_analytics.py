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
# Improvements in v2.3.1:
# - Correct NASA POWER monthly data extraction
# - Monthly solar-resource analysis
# - Monthly temperature analysis
# - Seasonal classification
# - Solar statistics
# - Temperature statistics
# - Proper graph units
# - Solar Resource axis: kWh/m²/day
# - Temperature axis: °C
# - Safe handling of missing data
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

        number = float(value)

        # Reject NaN
        if number != number:
            return None

        # NASA POWER uses very large negative values
        # to represent unavailable data.
        if number <= -900:
            return None

        return number

    except (TypeError, ValueError):

        return None


# ==========================================================
# SECTION 3 - FIND NASA PARAMETER DATA
# ==========================================================

def _get_parameter_data(
    solar_data,
    parameter_name
):
    """
    Locate a NASA POWER parameter regardless of whether
    the data is stored directly or inside the standard
    NASA POWER properties/parameter structure.
    """

    if not isinstance(
        solar_data,
        dict
    ):
        return {}


    # ------------------------------------------------------
    # Direct structure
    # ------------------------------------------------------

    parameter_data = solar_data.get(
        parameter_name
    )

    if isinstance(
        parameter_data,
        dict
    ):

        return parameter_data


    # ------------------------------------------------------
    # NASA POWER standard structure
    # ------------------------------------------------------

    properties = solar_data.get(
        "properties",
        {}
    )


    if not isinstance(
        properties,
        dict
    ):

        return {}


    parameters = properties.get(
        "parameter",
        {}
    )


    if not isinstance(
        parameters,
        dict
    ):

        return {}


    parameter_data = parameters.get(
        parameter_name
    )


    if isinstance(
        parameter_data,
        dict
    ):

        return parameter_data


    return {}


# ==========================================================
# SECTION 4 - EXTRACT MONTHLY SOLAR DATA
# ==========================================================

def extract_monthly_solar_data(
    solar_data
):
    """
    Extract monthly NASA POWER solar-resource values.

    NASA POWER parameter:

        ALLSKY_SFC_SW_DWN

    Unit:

        kWh/m²/day

    Returns a list containing:

        month
        month_short
        month_number
        solar_value
    """

    results = []


    parameter_data = _get_parameter_data(
        solar_data,
        "ALLSKY_SFC_SW_DWN"
    )


    if not parameter_data:

        return results


    # ------------------------------------------------------
    # Process all 12 months
    # ------------------------------------------------------

    for month_number in range(
        1,
        13
    ):

        month_key = (
            f"{month_number:02d}"
        )


        value = parameter_data.get(
            month_key
        )


        # Try integer key
        if value is None:

            value = parameter_data.get(
                month_number
            )


        # Try abbreviated NASA-style keys
        if value is None:

            value = parameter_data.get(
                MONTH_ABBREVIATIONS[
                    month_number - 1
                ].upper()
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
# SECTION 5 - EXTRACT MONTHLY TEMPERATURE
# ==========================================================

def extract_monthly_temperature_data(
    solar_data
):
    """
    Extract monthly NASA POWER average temperature.

    NASA POWER parameter:

        T2M

    Unit:

        °C

    Returns monthly records.
    """

    results = []


    parameter_data = _get_parameter_data(
        solar_data,
        "T2M"
    )


    if not parameter_data:

        return results


    # ------------------------------------------------------
    # Process all 12 months
    # ------------------------------------------------------

    for month_number in range(
        1,
        13
    ):

        month_key = (
            f"{month_number:02d}"
        )


        value = parameter_data.get(
            month_key
        )


        # Try integer key
        if value is None:

            value = parameter_data.get(
                month_number
            )


        # Try abbreviated keys
        if value is None:

            value = parameter_data.get(
                MONTH_ABBREVIATIONS[
                    month_number - 1
                ].upper()
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
# SECTION 6 - ANNUAL SOLAR STATISTICS
# ==========================================================

def calculate_solar_statistics(
    monthly_solar
):
    """
    Calculate annual solar-resource statistics.
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
# SECTION 7 - TEMPERATURE STATISTICS
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
# SECTION 8 - SEASONAL ANALYSIS
# ==========================================================

def calculate_seasonal_analysis(
    monthly_solar
):
    """
    Classify months into broad solar-resource categories.

    Classification is based on the actual monthly values:

        High:
            >= 110% of annual average

        Medium:
            between 90% and 110%

        Low:
            <= 90% of annual average
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


    values = []


    for item in monthly_solar:

        value = safe_float(
            item.get(
                "solar_value"
            )
        )


        if value is not None:

            values.append(
                value
            )


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

        value = safe_float(
            item.get(
                "solar_value"
            )
        )


        if value is None:

            continue


        month = item.get(
            "month",
            "Unknown"
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
# SECTION 9 - COMPLETE ANALYTICS FUNCTION
# ==========================================================

def analyze_solar_resource(
    solar_data
):
    """
    Perform complete solar-resource analysis.

    Returns a single dictionary suitable for:

        Streamlit
        Charts
        Engineering analysis
        PDF reports
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
            seasonal_analysis,

        # --------------------------------------------------
        # Explicit engineering units
        # --------------------------------------------------

        "solar_resource_unit":
            "kWh/m²/day",

        "temperature_unit":
            "°C"

    }


# ==========================================================
# SECTION 10 - PREPARE MONTHLY CHART DATA
# ==========================================================

def prepare_monthly_chart_data(
    analytics
):
    """
    Prepare a simple dictionary for Streamlit charts.

    This function does not create the charts itself.
    It prepares clean data for main.py or another UI module.
    """

    if not isinstance(
        analytics,
        dict
    ):

        return {

            "solar":
                [],

            "temperature":
                []

        }


    solar_records = (
        analytics.get(
            "monthly_solar",
            []
        )
    )


    temperature_records = (
        analytics.get(
            "monthly_temperature",
            []
        )
    )


    solar_chart = []

    for item in solar_records:

        solar_chart.append({

            "Month":
                item.get(
                    "month_short"
                ),

            "Solar Resource (kWh/m²/day)":
                safe_float(
                    item.get(
                        "solar_value"
                    )
                )

        })


    temperature_chart = []

    for item in temperature_records:

        temperature_chart.append({

            "Month":
                item.get(
                    "month_short"
                ),

            "Temperature (°C)":
                safe_float(
                    item.get(
                        "temperature"
                    )
                )

        })


    return {

        "solar":
            solar_chart,

        "temperature":
            temperature_chart

    }


# ==========================================================
# SECTION 11 - GET GRAPH LABELS
# ==========================================================

def get_graph_labels():
    """
    Return standard engineering labels for graphs.
    """

    return {

        "solar_x":
            "Month",

        "solar_y":
            "Solar Resource (kWh/m²/day)",

        "temperature_x":
            "Month",

        "temperature_y":
            "Temperature (°C)"

    }


# ==========================================================
# SECTION 12 - ANALYTICS SUMMARY
# ==========================================================

def create_analytics_summary(
    analytics
):
    """
    Create a concise human-readable analytics summary.

    Useful for Streamlit and PDF reporting.
    """

    if not isinstance(
        analytics,
        dict
    ):

        return {

            "solar_average":
                "N/A",

            "solar_maximum":
                "N/A",

            "solar_minimum":
                "N/A",

            "best_month":
                "N/A",

            "temperature_average":
                "N/A",

            "temperature_maximum":
                "N/A",

            "temperature_minimum":
                "N/A",

            "hottest_month":
                "N/A",

            "coolest_month":
                "N/A"

        }


    solar_stats = analytics.get(
        "solar_statistics",
        {}
    )


    temperature_stats = analytics.get(
        "temperature_statistics",
        {}
    )


    return {

        "solar_average":

            (
                f"{solar_stats['annual_average']:.2f} "
                "kWh/m²/day"
                if solar_stats.get(
                    "annual_average"
                ) is not None
                else "N/A"
            ),

        "solar_maximum":

            (
                f"{solar_stats['maximum']:.2f} "
                "kWh/m²/day"
                if solar_stats.get(
                    "maximum"
                ) is not None
                else "N/A"
            ),

        "solar_minimum":

            (
                f"{solar_stats['minimum']:.2f} "
                "kWh/m²/day"
                if solar_stats.get(
                    "minimum"
                ) is not None
                else "N/A"
            ),

        "best_month":

            (
                solar_stats.get(
                    "best_month"
                )
                or
                "N/A"
            ),

        "temperature_average":

            (
                f"{temperature_stats['annual_average']:.1f} °C"
                if temperature_stats.get(
                    "annual_average"
                ) is not None
                else "N/A"
            ),

        "temperature_maximum":

            (
                f"{temperature_stats['maximum']:.1f} °C"
                if temperature_stats.get(
                    "maximum"
                ) is not None
                else "N/A"
            ),

        "temperature_minimum":

            (
                f"{temperature_stats['minimum']:.1f} °C"
                if temperature_stats.get(
                    "minimum"
                ) is not None
                else "N/A"
            ),

        "hottest_month":

            (
                temperature_stats.get(
                    "hottest_month"
                )
                or
                "N/A"
            ),

        "coolest_month":

            (
                temperature_stats.get(
                    "coolest_month"
                )
                or
                "N/A"
            )

    }


# ==========================================================
# SECTION 13 - GRAPHING FUNCTIONS
# ==========================================================

def plot_monthly_solar_resource(
    analytics
):
    """
    Create a Plotly monthly solar-resource graph.

    Y-axis unit:
        kWh/m²/day

    Returns:
        Plotly Figure or None
    """

    try:

        import plotly.graph_objects as go

    except ImportError:

        return None


    monthly_solar = analytics.get(
        "monthly_solar",
        []
    )


    if not monthly_solar:

        return None


    months = []

    values = []


    for item in monthly_solar:

        value = safe_float(
            item.get(
                "solar_value"
            )
        )


        if value is None:

            continue


        months.append(
            item.get(
                "month_short"
            )
        )


        values.append(
            value
        )


    if not values:

        return None


    figure = go.Figure()


    figure.add_trace(

        go.Bar(

            x=months,

            y=values,

            name="Solar Resource",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Solar Resource: "
                "%{y:.2f} kWh/m²/day"
                "<extra></extra>"
            )

        )

    )


    figure.update_layout(

        title="Monthly Solar Resource",

        xaxis_title="Month",

        yaxis_title=(
            "Solar Resource (kWh/m²/day)"
        ),

        hovermode="x unified",

        margin=dict(
            l=60,
            r=30,
            t=60,
            b=50
        )

    )


    return figure


# ==========================================================
# SECTION 14 - MONTHLY TEMPERATURE GRAPH
# ==========================================================

def plot_monthly_temperature(
    analytics
):
    """
    Create a Plotly monthly temperature graph.

    Y-axis unit:
        °C

    Returns:
        Plotly Figure or None
    """

    try:

        import plotly.graph_objects as go

    except ImportError:

        return None


    monthly_temperature = analytics.get(
        "monthly_temperature",
        []
    )


    if not monthly_temperature:

        return None


    months = []

    values = []


    for item in monthly_temperature:

        value = safe_float(
            item.get(
                "temperature"
            )
        )


        if value is None:

            continue


        months.append(
            item.get(
                "month_short"
            )
        )


        values.append(
            value
        )


    if not values:

        return None


    figure = go.Figure()


    figure.add_trace(

        go.Scatter(

            x=months,

            y=values,

            mode="lines+markers",

            name="Temperature",

            hovertemplate=(
                "<b>%{x}</b><br>"
                "Temperature: "
                "%{y:.1f} °C"
                "<extra></extra>"
            )

        )

    )


    figure.update_layout(

        title="Monthly Average Temperature",

        xaxis_title="Month",

        # IMPORTANT:
        # The temperature unit is explicitly displayed.

        yaxis_title="Temperature (°C)",

        hovermode="x unified",

        margin=dict(
            l=60,
            r=30,
            t=60,
            b=50
        )

    )


    return figure


# ==========================================================
# SECTION 15 - COMBINED GRAPH DATA
# ==========================================================

def get_monthly_graph_data(
    analytics
):
    """
    Return monthly solar and temperature values
    in a consistent structure.
    """

    solar = analytics.get(
        "monthly_solar",
        []
    )


    temperature = analytics.get(
        "monthly_temperature",
        []
    )


    solar_by_month = {

        item.get(
            "month_number"
        ):
            item.get(
                "solar_value"
            )

        for item in solar

    }


    temperature_by_month = {

        item.get(
            "month_number"
        ):
            item.get(
                "temperature"
            )

        for item in temperature

    }


    results = []


    for month_number in range(
        1,
        13
    ):

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

            "solar_resource":
                solar_by_month.get(
                    month_number
                ),

            "temperature":
                temperature_by_month.get(
                    month_number
                )

        })


    return results


# ==========================================================
# SECTION 16 - MODULE TEST
# ==========================================================

def test_solar_analytics(
    solar_data
):
    """
    Basic test function for the analytics module.
    """

    try:

        analytics = analyze_solar_resource(
            solar_data
        )


        return {

            "success":
                True,

            "message":
                "Solar analytics processed successfully.",

            "analytics":
                analytics

        }


    except Exception as error:

        return {

            "success":
                False,

            "message":
                str(error),

            "analytics":
                None

        }
