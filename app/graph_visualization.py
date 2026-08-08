# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Graph Visualization Module
# Version: 2.3.0
#
# Purpose:
# Create interactive charts for solar-resource analysis.
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import pandas as pd
import plotly.express as px


# ==========================================================
# SECTION 2 - SOLAR RESOURCE GRAPH
# ==========================================================

def create_solar_resource_chart(
    monthly_solar
):
    """
    Create an interactive monthly solar-resource chart.

    Expected input:

    [
        {
            "month": "January",
            "month_short": "Jan",
            "month_number": 1,
            "solar_value": 5.2
        }
    ]
    """

    if not monthly_solar:

        return None


    dataframe = pd.DataFrame(
        monthly_solar
    )


    required_columns = [
        "month_short",
        "solar_value"
    ]


    for column in required_columns:

        if column not in dataframe.columns:

            return None


    dataframe = dataframe.sort_values(
        "month_short",
        key=lambda series: pd.Categorical(
            series,
            categories=[
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
            ],
            ordered=True
        )
    )


    figure = px.line(
        dataframe,
        x="month_short",
        y="solar_value",
        markers=True,
        title="Monthly Solar Resource",
        labels={
            "month_short": "Month",
            "solar_value": "Solar Resource"
        }
    )


    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Solar Resource (kWh/m²/day)",
        hovermode="x unified"
    )


    return figure


# ==========================================================
# SECTION 3 - TEMPERATURE GRAPH
# ==========================================================

def create_temperature_chart(
    monthly_temperature
):
    """
    Create an interactive monthly temperature chart.
    """

    if not monthly_temperature:

        return None


    dataframe = pd.DataFrame(
        monthly_temperature
    )


    required_columns = [
        "month_short",
        "temperature"
    ]


    for column in required_columns:

        if column not in dataframe.columns:

            return None


    dataframe = dataframe.sort_values(
        "month_short",
        key=lambda series: pd.Categorical(
            series,
            categories=[
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
            ],
            ordered=True
        )
    )


    figure = px.line(
        dataframe,
        x="month_short",
        y="temperature",
        markers=True,
        title="Monthly Average Temperature",
        labels={
            "month_short": "Month",
            "temperature": "Temperature"
        }
    )


    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Temperature (°C)",
        hovermode="x unified"
    )


    return figure


# ==========================================================
# SECTION 4 - SOLAR BAR CHART
# ==========================================================

def create_solar_bar_chart(
    monthly_solar
):
    """
    Create a monthly solar-resource bar chart.
    """

    if not monthly_solar:

        return None


    dataframe = pd.DataFrame(
        monthly_solar
    )


    if (
        "month_short" not in dataframe.columns
        or
        "solar_value" not in dataframe.columns
    ):

        return None


    figure = px.bar(
        dataframe,
        x="month_short",
        y="solar_value",
        title="Monthly Solar Resource",
        labels={
            "month_short": "Month",
            "solar_value": "Solar Resource"
        }
    )


    figure.update_layout(
        xaxis_title="Month",
        yaxis_title="Solar Resource (kWh/m²/day)"
    )


    return figure


# ==========================================================
# SECTION 5 - COMBINED DATA TABLE
# ==========================================================

def create_combined_dataframe(
    monthly_solar,
    monthly_temperature
):
    """
    Combine solar and temperature data into one DataFrame.
    """

    if (
        not monthly_solar
        and
        not monthly_temperature
    ):

        return pd.DataFrame()


    solar_dataframe = pd.DataFrame(
        monthly_solar
    )


    temperature_dataframe = pd.DataFrame(
        monthly_temperature
    )


    if solar_dataframe.empty:

        return temperature_dataframe


    if temperature_dataframe.empty:

        return solar_dataframe


    combined = pd.merge(
        solar_dataframe[
            [
                "month",
                "month_short",
                "month_number",
                "solar_value"
            ]
        ],
        temperature_dataframe[
            [
                "temperature"
            ]
        ],
        left_index=True,
        right_index=True,
        how="outer"
    )


    return combined
