# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# REAL SOLAR RESOURCE → ANALYTICS → GRAPHS TEST
# Version: 2.3.0
#
# Uses the existing:
#     get_solar_resource()
#
# IMPORTANT:
# This is a TEST PAGE.
# It does NOT modify main.py or solar_api.py.
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st
import inspect


# Existing Solar API
from solar_api import (
    get_solar_resource
)


# Solar Analytics
from solar_analytics import (
    analyze_solar_resource
)


# Graph Visualization
from graph_visualization import (
    create_solar_resource_chart,
    create_temperature_chart,
    create_solar_bar_chart,
    create_combined_dataframe
)


# ==========================================================
# SECTION 2 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar Analytics Test",
    page_icon="☀️",
    layout="wide"
)


# ==========================================================
# SECTION 3 - HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "Real Solar Resource → Analytics → Graph Test"
)

st.write(
    """
    This test verifies the complete pipeline:

    Coordinates
        ↓
    Solar Resource Engine
        ↓
    Solar Analytics
        ↓
    Graph Visualization

    The production application is not modified by this test.
    """
)


# ==========================================================
# SECTION 4 - FUNCTION INFORMATION
# ==========================================================

st.header(
    "🔎 Solar Resource Function"
)

try:

    function_signature = inspect.signature(
        get_solar_resource
    )

    st.success(
        "✅ get_solar_resource() loaded successfully."
    )

    st.code(
        f"get_solar_resource{function_signature}"
    )

except Exception as error:

    st.warning(
        f"Could not determine function signature: {error}"
    )


# ==========================================================
# SECTION 5 - LOCATION INPUT
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
    **Selected Coordinates**

    Latitude: {latitude:.4f}°

    Longitude: {longitude:.4f}°
    """
)


# ==========================================================
# SECTION 6 - RUN TEST
# ==========================================================

run_test = st.button(
    "🚀 Retrieve Solar Resource",
    type="primary"
)


if not run_test:

    st.info(
        """
        Enter the project coordinates in the sidebar
        and click:

        **🚀 Retrieve Solar Resource**

        Suggested test location:

        **Kampala, Uganda**

        Latitude: `0.3476`

        Longitude: `32.5825`
        """
    )

    st.stop()


# ==========================================================
# SECTION 7 - RETRIEVE SOLAR RESOURCE
# ==========================================================

st.header(
    "📡 Solar Resource Retrieval"
)


solar_resource = None

last_error = None


# ----------------------------------------------------------
# METHOD 1
# positional arguments
# ----------------------------------------------------------

try:

    solar_resource = get_solar_resource(
        latitude,
        longitude
    )

except Exception as error:

    last_error = error


# ----------------------------------------------------------
# METHOD 2
# keyword arguments: latitude / longitude
# ----------------------------------------------------------

if solar_resource is None:

    try:

        solar_resource = get_solar_resource(
            latitude=latitude,
            longitude=longitude
        )

    except Exception as error:

        last_error = error


# ----------------------------------------------------------
# METHOD 3
# keyword arguments: lat / lon
# ----------------------------------------------------------

if solar_resource is None:

    try:

        solar_resource = get_solar_resource(
            lat=latitude,
            lon=longitude
        )

    except Exception as error:

        last_error = error


# ==========================================================
# CHECK RESULT
# ==========================================================

if solar_resource is None:

    st.error(
        """
        ❌ get_solar_resource() did not return usable data.
        """
    )

    st.code(
        str(last_error)
    )

    st.info(
        """
        The existing solar API is still protected.
        We have not modified solar_api.py.

        The error above tells us exactly what argument
        structure the existing function requires.
        """
    )

    st.stop()


st.success(
    "✅ Solar resource retrieved successfully."
)


# ==========================================================
# SECTION 8 - RAW DATA
# ==========================================================

with st.expander(
    "🔍 View Raw Solar Resource Data"
):

    try:

        st.json(
            solar_resource
        )

    except Exception:

        st.write(
            solar_resource
        )


# ==========================================================
# SECTION 9 - ANALYTICS
# ==========================================================

st.header(
    "🧮 Solar Analytics"
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


# ==========================================================
# SECTION 10 - EXTRACT MONTHLY DATA
# ==========================================================

monthly_solar = analytics.get(
    "monthly_solar",
    []
)


monthly_temperature = analytics.get(
    "monthly_temperature",
    []
)


solar_count = len(
    monthly_solar
)


temperature_count = len(
    monthly_temperature
)


# ==========================================================
# SECTION 11 - DATA STATUS
# ==========================================================

st.header(
    "📊 Data Validation"
)


status_col1, status_col2 = (
    st.columns(2)
)


with status_col1:

    if solar_count > 0:

        st.success(
            f"""
            ☀️ Solar data available

            {solar_count} monthly values detected.
            """
        )

    else:

        st.error(
            "❌ No monthly solar values detected."
        )


with status_col2:

    if temperature_count > 0:

        st.success(
            f"""
            🌡️ Temperature data available

            {temperature_count} monthly values detected.
            """
        )

    else:

        st.warning(
            "⚠️ No monthly temperature values detected."
        )


# ==========================================================
# SECTION 12 - SOLAR GRAPH
# ==========================================================

st.header(
    "☀️ Monthly Solar Resource"
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
        ❌ Solar graph error:

        {error}
        """
    )


if solar_chart is not None:

    st.plotly_chart(
        solar_chart,
        use_container_width=True
    )

else:

    st.warning(
        "Solar resource graph could not be generated."
    )


# ==========================================================
# SECTION 13 - TEMPERATURE GRAPH
# ==========================================================

st.header(
    "🌡️ Monthly Temperature"
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
        ❌ Temperature graph error:

        {error}
        """
    )


if temperature_chart is not None:

    st.plotly_chart(
        temperature_chart,
        use_container_width=True
    )

else:

    st.warning(
        "Temperature graph could not be generated."
    )


# ==========================================================
# SECTION 14 - BAR GRAPH
# ==========================================================

st.header(
    "📊 Monthly Solar Resource — Bar Chart"
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
        ❌ Solar bar chart error:

        {error}
        """
    )


if solar_bar_chart is not None:

    st.plotly_chart(
        solar_bar_chart,
        use_container_width=True
    )

else:

    st.warning(
        "Solar bar chart could not be generated."
    )


# ==========================================================
# SECTION 15 - DATA TABLE
# ==========================================================

st.header(
    "📋 Monthly Solar & Temperature Data"
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
        ❌ Combined data error:

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

else:

    st.warning(
        "Combined monthly data is unavailable."
    )


# ==========================================================
# SECTION 16 - FINAL TEST STATUS
# ==========================================================

st.divider()

st.header(
    "🧪 Integration Test Result"
)


if (
    solar_chart is not None
    and
    temperature_chart is not None
    and
    solar_bar_chart is not None
):

    st.success(
        """
        🎉 REAL SOLAR GRAPH TEST PASSED

        The complete pipeline is working:

        📍 Coordinates
             ↓
        📡 Solar Resource
             ↓
        🧮 Solar Analytics
             ↓
        📊 Graph Visualization

        The visualization system is ready to be
        integrated into the main Solar PV Designer
        Pro application.
        """
    )

else:

    st.warning(
        """
        ⚠️ Solar resource data was retrieved, but
        one or more graphs could not be generated.

        We will correct the affected visualization
        component before integrating it into main.py.
        """
    )


# ==========================================================
# SECTION 17 - FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    Real Solar Graph Integration Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)

