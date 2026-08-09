# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# NASA POWER → SOLAR ANALYTICS → GRAPHS TEST
# Version: 2.3.0
#
# Confirmed API function:
#
#     get_solar_resource(latitude, longitude)
#
# ==========================================================

import streamlit as st


# ==========================================================
# SOLAR API
# ==========================================================

from solar_api import (
    get_solar_resource
)


# ==========================================================
# SOLAR ANALYTICS
# ==========================================================

from solar_analytics import (
    analyze_solar_resource
)


# ==========================================================
# GRAPH VISUALIZATION
# ==========================================================

from graph_visualization import (
    create_solar_resource_chart,
    create_temperature_chart,
    create_solar_bar_chart,
    create_combined_dataframe
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NASA POWER Graph Test",
    page_icon="☀️",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "NASA POWER → Solar Analytics → Graph Test"
)


st.write(
    """
    This test verifies the complete solar-data pipeline
    using the existing production modules.
    """
)


# ==========================================================
# PIPELINE
# ==========================================================

st.info(
    """
    📍 Coordinates
        ↓
    📡 NASA POWER / Solar Resource
        ↓
    🧮 Solar Analytics
        ↓
    📊 Graph Visualization
    """
)


# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header(
    "📍 Test Location"
)


latitude = st.sidebar.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=0.3476,
    step=0.0001,
    format="%.4f"
)


longitude = st.sidebar.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=32.5825,
    step=0.0001,
    format="%.4f"
)


st.sidebar.info(
    f"""
    **Coordinates**

    Latitude: {latitude:.4f}°

    Longitude: {longitude:.4f}()
    """
)


# ==========================================================
# RUN TEST
# ==========================================================

run_test = st.button(
    "🚀 Run Complete Solar Analytics Test",
    type="primary"
)


if not run_test:

    st.info(
        """
        ### Suggested Test

        **Location:** Kampala, Uganda

        **Latitude:** 0.3476°

        **Longitude:** 32.5825°

        Click **Run Complete Solar Analytics Test**
        to retrieve and visualize the solar resource.
        """
    )

    st.stop()


# ==========================================================
# STEP 1 — SOLAR RESOURCE
# ==========================================================

st.header(
    "1️⃣ 📡 Solar Resource Retrieval"
)


try:

    solar_resource = get_solar_resource(
        latitude,
        longitude
    )

except Exception as error:

    st.error(
        f"""
        ❌ Solar resource retrieval failed.

        Error:

        {error}
        """
    )

    st.stop()


if solar_resource is None:

    st.error(
        """
        ❌ Solar resource function returned no data.
        """
    )

    st.stop()


st.success(
    "✅ Solar resource retrieved successfully."
)


# ==========================================================
# RAW RESPONSE
# ==========================================================

with st.expander(
    "🔍 View Raw Solar Resource Data"
):

    if isinstance(
        solar_resource,
        dict
    ):

        st.json(
            solar_resource
        )

    else:

        st.write(
            solar_resource
        )


# ==========================================================
# STEP 2 — SOLAR ANALYTICS
# ==========================================================

st.header(
    "2️⃣ 🧮 Solar Analytics"
)


try:

    analytics = analyze_solar_resource(
        solar_resource
    )

except Exception as error:

    st.error(
        f"""
        ❌ Solar Analytics failed.

        Error:

        {error}
        """
    )

    st.stop()


if analytics is None:

    st.error(
        """
        ❌ Solar Analytics returned no results.
        """
    )

    st.stop()


st.success(
    "✅ Solar Analytics processed the data."
)


# ==========================================================
# ANALYTICS RESPONSE
# ==========================================================

with st.expander(
    "🔍 View Analytics Response"
):

    st.write(
        analytics
    )


# ==========================================================
# STEP 3 — EXTRACT MONTHLY VALUES
# ==========================================================

st.header(
    "3️⃣ 📊 Monthly Data Validation"
)


# ----------------------------------------------------------
# Solar data
# ----------------------------------------------------------

monthly_solar = analytics.get(
    "monthly_solar",
    []
)


# ----------------------------------------------------------
# Temperature data
# ----------------------------------------------------------

monthly_temperature = analytics.get(
    "monthly_temperature",
    []
)


# ==========================================================
# DATA COUNTS
# ==========================================================

solar_count = len(
    monthly_solar
)


temperature_count = len(
    monthly_temperature
)


count_col1, count_col2 = (
    st.columns(2)
)


with count_col1:

    st.metric(
        "Monthly Solar Values",
        solar_count
    )


with count_col2:

    st.metric(
        "Monthly Temperature Values",
        temperature_count
    )


# ==========================================================
# SHOW DATA
# ==========================================================

if solar_count > 0:

    st.success(
        "☀️ Monthly solar data detected."
    )

else:

    st.warning(
        "⚠️ No monthly solar data detected."
    )


if temperature_count > 0:

    st.success(
        "🌡️ Monthly temperature data detected."
    )

else:

    st.warning(
        "⚠️ No monthly temperature data detected."
    )


# ==========================================================
# STEP 4 — SOLAR GRAPH
# ==========================================================

st.header(
    "4️⃣ ☀️ Monthly Solar Resource Graph"
)


solar_chart = None


try:

    solar_chart = (
        create_solar_resource_chart(
            monthly_solar
        )
    )

except Exception as error:

    st.error(
        f"""
        ❌ Solar resource graph failed.

        Error:

        {error}
        """
    )


if solar_chart is not None:

    st.plotly_chart(
        solar_chart,
        use_container_width=True
    )

    st.success(
        "✅ Solar resource graph generated."
    )

else:

    st.warning(
        "⚠️ Solar resource graph is unavailable."
    )


# ==========================================================
# STEP 5 — TEMPERATURE GRAPH
# ==========================================================

st.header(
    "5️⃣ 🌡️ Monthly Temperature Graph"
)


temperature_chart = None


try:

    temperature_chart = (
        create_temperature_chart(
            monthly_temperature
        )
    )

except Exception as error:

    st.error(
        f"""
        ❌ Temperature graph failed.

        Error:

        {error}
        """
    )


if temperature_chart is not None:

    st.plotly_chart(
        temperature_chart,
        use_container_width=True
    )

    st.success(
        "✅ Temperature graph generated."
    )

else:

    st.warning(
        "⚠️ Temperature graph is unavailable."
    )


# ==========================================================
# STEP 6 — BAR GRAPH
# ==========================================================

st.header(
    "6️⃣ 📊 Solar Resource Bar Graph"
)


solar_bar_chart = None


try:

    solar_bar_chart = (
        create_solar_bar_chart(
            monthly_solar
        )
    )

except Exception as error:

    st.error(
        f"""
        ❌ Solar bar graph failed.

        Error:

        {error}
        """
    )


if solar_bar_chart is not None:

    st.plotly_chart(
        solar_bar_chart,
        use_container_width=True
    )

    st.success(
        "✅ Solar bar graph generated."
    )

else:

    st.warning(
        "⚠️ Solar bar graph is unavailable."
    )


# ==========================================================
# STEP 7 — COMBINED DATA TABLE
# ==========================================================

st.header(
    "7️⃣ 📋 Solar & Temperature Data"
)


combined_data = None


try:

    combined_data = (
        create_combined_dataframe(
            monthly_solar,
            monthly_temperature
        )
    )

except Exception as error:

    st.error(
        f"""
        ❌ Combined data table failed.

        Error:

        {error}
        """
    )


if (
    combined_data is not None
    and
    not combined_data.empty
):

    st.dataframe(
        combined_data,
        use_container_width=True
    )

    st.success(
        "✅ Combined data table generated."
    )

else:

    st.warning(
        "⚠️ Combined data table is unavailable."
    )


# ==========================================================
# FINAL TEST
# ==========================================================

st.divider()

st.header(
    "🎯 Final Integration Test"
)


if (
    solar_count > 0
    and
    (
        solar_chart is not None
    )
    and
    (
        temperature_chart is not None
    )
):

    st.success(
        """
        🎉 COMPLETE SOLAR ANALYTICS TEST PASSED!

        The system successfully completed:

        📍 Coordinates
             ↓
        📡 Solar Resource
             ↓
        🧮 Solar Analytics
             ↓
        📊 Interactive Graphs

        The next step is to integrate these graphs
        into the main Solar PV Designer Pro application.
        """
    )

else:

    st.warning(
        """
        ⚠️ The solar-resource connection is working,
        but one or more analytics/visualization
        components still require adjustment.
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    NASA POWER Analytics Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)

