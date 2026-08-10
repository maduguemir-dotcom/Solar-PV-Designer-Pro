# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Solar Analytics Dashboard
# Version: 2.3.2
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Professional visualization and interpretation of
# NASA POWER solar-resource and temperature data.
#
# ==========================================================

import streamlit as st
import pandas as pd


# ==========================================================
# SECTION 1 - BUILD DATAFRAME
# ==========================================================

def build_analytics_dataframe(analytics):
    """
    Convert the analytics package produced by
    solar_analytics.py into a Pandas DataFrame.
    """

    if not isinstance(analytics, dict):
        return pd.DataFrame()

    graph_data = analytics.get(
        "graph_data",
        []
    )

    if not graph_data:
        return pd.DataFrame()

    try:

        dataframe = pd.DataFrame(
            graph_data
        )

    except Exception:
        return pd.DataFrame()

    return dataframe


# ==========================================================
# SECTION 2 - MONTHLY SOLAR RESOURCE GRAPH
# ==========================================================

def display_solar_resource_graph(
    dataframe
):
    """
    Display monthly solar-resource graph.
    """

    if dataframe.empty:
        st.info(
            "No monthly solar data available for graphing."
        )
        return

    if "solar_resource" not in dataframe.columns:
        st.info(
            "No monthly solar data available for graphing."
        )
        return

    solar_dataframe = dataframe[
        [
            "month",
            "solar_resource"
        ]
    ].copy()

    solar_dataframe = solar_dataframe.dropna(
        subset=["solar_resource"]
    )

    if solar_dataframe.empty:
        st.info(
            "No monthly solar data available for graphing."
        )
        return

    solar_dataframe = solar_dataframe.set_index(
        "month"
    )

    st.subheader(
        "☀️ Monthly Solar Resource"
    )

    st.caption(
        "NASA POWER climatological solar resource"
    )

    st.line_chart(
        solar_dataframe[
            "solar_resource"
        ],
        use_container_width=True
    )

    st.caption(
        "Solar Resource (kWh/m²/day)"
    )


# ==========================================================
# SECTION 3 - MONTHLY TEMPERATURE GRAPH
# ==========================================================

def display_temperature_graph(
    dataframe
):
    """
    Display monthly average temperature graph.
    """

    if dataframe.empty:
        st.info(
            "No monthly temperature data available for graphing."
        )
        return

    if "temperature" not in dataframe.columns:
        st.info(
            "No monthly temperature data available for graphing."
        )
        return

    temperature_dataframe = dataframe[
        [
            "month",
            "temperature"
        ]
    ].copy()

    temperature_dataframe = (
        temperature_dataframe.dropna(
            subset=["temperature"]
        )
    )

    if temperature_dataframe.empty:
        st.info(
            "No monthly temperature data available for graphing."
        )
        return

    temperature_dataframe = (
        temperature_dataframe.set_index(
            "month"
        )
    )

    st.subheader(
        "🌡️ Monthly Average Temperature"
    )

    st.caption(
        "NASA POWER climatological temperature"
    )

    st.line_chart(
        temperature_dataframe[
            "temperature"
        ],
        use_container_width=True
    )

    st.caption(
        "Temperature (°C)"
    )


# ==========================================================
# SECTION 4 - SOLAR RESOURCE BAR GRAPH
# ==========================================================

def display_solar_bar_graph(
    dataframe
):
    """
    Display monthly solar-resource bar chart.
    """

    if dataframe.empty:
        return

    if "solar_resource" not in dataframe.columns:
        return

    solar_dataframe = dataframe[
        [
            "month",
            "solar_resource"
        ]
    ].copy()

    solar_dataframe = solar_dataframe.dropna(
        subset=["solar_resource"]
    )

    if solar_dataframe.empty:
        return

    solar_dataframe = solar_dataframe.set_index(
        "month"
    )

    st.subheader(
        "📊 Monthly Solar Resource Comparison"
    )

    st.bar_chart(
        solar_dataframe[
            "solar_resource"
        ],
        use_container_width=True
    )

    st.caption(
        "Solar Resource (kWh/m²/day)"
    )


# ==========================================================
# SECTION 5 - STATISTICS
# ==========================================================

def display_solar_statistics(
    analytics
):
    """
    Display solar-resource statistics.
    """

    statistics = analytics.get(
        "solar_statistics",
        {}
    )

    st.subheader(
        "📈 Solar Resource Statistics"
    )

    col1, col2, col3, col4, col5 = (
        st.columns(5)
    )

    average = statistics.get(
        "annual_average"
    )

    maximum = statistics.get(
        "maximum"
    )

    minimum = statistics.get(
        "minimum"
    )

    best_month = statistics.get(
        "best_month"
    )

    lowest_month = statistics.get(
        "lowest_month"
    )

    col1.metric(
        "Annual Average",
        (
            f"{average:.2f}"
            if average is not None
            else "N/A"
        )
    )

    col2.metric(
        "Maximum",
        (
            f"{maximum:.2f}"
            if maximum is not None
            else "N/A"
        )
    )

    col3.metric(
        "Minimum",
        (
            f"{minimum:.2f}"
            if minimum is not None
            else "N/A"
        )
    )

    col4.metric(
        "Best Month",
        best_month
        if best_month
        else "N/A"
    )

    col5.metric(
        "Lowest Month",
        lowest_month
        if lowest_month
        else "N/A"
    )

    st.caption(
        "Solar-resource values are expressed in "
        "kWh/m²/day."
    )


# ==========================================================
# SECTION 6 - TEMPERATURE STATISTICS
# ==========================================================

def display_temperature_statistics(
    analytics
):
    """
    Display temperature statistics.
    """

    statistics = analytics.get(
        "temperature_statistics",
        {}
    )

    st.subheader(
        "🌡️ Temperature Statistics"
    )

    col1, col2, col3, col4, col5 = (
        st.columns(5)
    )

    average = statistics.get(
        "annual_average"
    )

    maximum = statistics.get(
        "maximum"
    )

    minimum = statistics.get(
        "minimum"
    )

    hottest_month = statistics.get(
        "hottest_month"
    )

    coolest_month = statistics.get(
        "coolest_month"
    )

    col1.metric(
        "Annual Average",
        (
            f"{average:.1f} °C"
            if average is not None
            else "N/A"
        )
    )

    col2.metric(
        "Maximum",
        (
            f"{maximum:.1f} °C"
            if maximum is not None
            else "N/A"
        )
    )

    col3.metric(
        "Minimum",
        (
            f"{minimum:.1f} °C"
            if minimum is not None
            else "N/A"
        )
    )

    col4.metric(
        "Hottest Month",
        hottest_month
        if hottest_month
        else "N/A"
    )

    col5.metric(
        "Coolest Month",
        coolest_month
        if coolest_month
        else "N/A"
    )


# ==========================================================
# SECTION 7 - SEASONAL ANALYSIS
# ==========================================================

def display_seasonal_analysis(
    analytics
):
    """
    Display high, medium and low solar months.
    """

    seasonal = analytics.get(
        "seasonal_analysis",
        {}
    )

    st.subheader(
        "☀️ Seasonal Solar Analysis"
    )

    high = seasonal.get(
        "high_solar_months",
        []
    )

    medium = seasonal.get(
        "medium_solar_months",
        []
    )

    low = seasonal.get(
        "low_solar_months",
        []
    )

    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:

        st.markdown(
            "### 🟢 High Solar"
        )

        if high:

            for month in high:

                st.write(
                    f"• {month}"
                )

        else:

            st.write(
                "No months classified"
            )

    with col2:

        st.markdown(
            "### 🟡 Medium Solar"
        )

        if medium:

            for month in medium:

                st.write(
                    f"• {month}"
                )

        else:

            st.write(
                "No months classified"
            )

    with col3:

        st.markdown(
            "### 🔴 Low Solar"
        )

        if low:

            for month in low:

                st.write(
                    f"• {month}"
                )

        else:

            st.write(
                "No months classified"
            )


# ==========================================================
# SECTION 8 - ENGINEERING INTERPRETATION
# ==========================================================

def generate_engineering_interpretation(
    analytics
):
    """
    Generate basic engineering interpretation from
    the calculated solar-resource statistics.
    """

    statistics = analytics.get(
        "solar_statistics",
        {}
    )

    average = statistics.get(
        "annual_average"
    )

    maximum = statistics.get(
        "maximum"
    )

    minimum = statistics.get(
        "minimum"
    )

    best_month = statistics.get(
        "best_month"
    )

    lowest_month = statistics.get(
        "lowest_month"
    )

    if average is None:

        return [
            "Solar-resource statistics are not "
            "available for engineering interpretation."
        ]

    interpretation = []

    interpretation.append(
        f"The annual average solar resource is "
        f"{average:.2f} kWh/m²/day."
    )

    if maximum is not None:

        interpretation.append(
            f"The maximum monthly solar resource is "
            f"{maximum:.2f} kWh/m²/day."
        )

    if minimum is not None:

        interpretation.append(
            f"The minimum monthly solar resource is "
            f"{minimum:.2f} kWh/m²/day."
        )

    if best_month:

        interpretation.append(
            f"{best_month} has the strongest "
            f"solar-resource conditions."
        )

    if lowest_month:

        interpretation.append(
            f"{lowest_month} has the weakest "
            f"solar-resource conditions and should "
            f"be considered during system design."
        )

    return interpretation


def display_engineering_interpretation(
    analytics
):
    """
    Display engineering interpretation.
    """

    st.subheader(
        "🧠 Engineering Interpretation"
    )

    interpretation = (
        generate_engineering_interpretation(
            analytics
        )
    )

    for item in interpretation:

        st.info(item)


# ==========================================================
# SECTION 9 - COMPLETE DASHBOARD
# ==========================================================

def display_analytics_dashboard(
    analytics
):
    """
    Display the complete Solar Analytics Dashboard.
    """

    if not isinstance(
        analytics,
        dict
    ):

        st.warning(
            "Solar analytics data is unavailable."
        )

        return

    dataframe = (
        build_analytics_dataframe(
            analytics
        )
    )

    st.header(
        "📊 Solar Resource Analytics"
    )

    st.write(
        """
        This dashboard provides a monthly analysis of
        solar-resource availability and temperature
        conditions using NASA POWER climatological data.
        """
    )

    # ------------------------------------------------------
    # Statistics
    # ------------------------------------------------------

    display_solar_statistics(
        analytics
    )

    st.divider()

    display_temperature_statistics(
        analytics
    )

    st.divider()

    # ------------------------------------------------------
    # Graphs
    # ------------------------------------------------------

    graph_col1, graph_col2 = (
        st.columns(2)
    )

    with graph_col1:

        display_solar_resource_graph(
            dataframe
        )

    with graph_col2:

        display_temperature_graph(
            dataframe
        )

    st.divider()

    # ------------------------------------------------------
    # Solar comparison
    # ------------------------------------------------------

    display_solar_bar_graph(
        dataframe
    )

    st.divider()

    # ------------------------------------------------------
    # Seasonal analysis
    # ------------------------------------------------------

    display_seasonal_analysis(
        analytics
    )

    st.divider()

    # ------------------------------------------------------
    # Engineering interpretation
    # ------------------------------------------------------

    display_engineering_interpretation(
        analytics
    )
