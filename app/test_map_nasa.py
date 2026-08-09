# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# REAL NASA POWER → ANALYTICS → GRAPHS
# Version: 2.3.0
#
# Uses the EXISTING:
#     get_solar_resource()
#
# This test does NOT modify main.py or solar_api.py.
#
# ==========================================================

import streamlit as st
import inspect

from solar_api import (
    get_solar_resource
)

from solar_analytics import (
    analyze_solar_resource
)

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
    page_title="NASA Solar Graph Test",
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
    "Real NASA POWER → Analytics → Graph Test"
)

st.write(
    """
    This test uses the existing solar-resource engine
    to retrieve real location data and send it through
    the Solar Analytics and Graph Visualization modules.
    """
)


# ==========================================================
# FUNCTION INFORMATION
# ==========================================================

with st.expander(
    "🔎 View get_solar_resource() function"
):

    try:

        st.code(
            str(
                inspect.signature(
                    get_solar_resource
                )
            )
        )

    except Exception:

        st.write(
            "Function signature unavailable."
        )


# ==========================================================
# LOCATION INPUT
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

    Longitude: {longitude:.4f}°
    """
)


# ==========================================================
# RETRIEVE SOLAR RESOURCE
# ==========================================================

run_test = st.button(
    "🚀 Get Real Solar Resource",
    type="primary"
)


if not run_test:

    st.info(
        """
        Enter coordinates and click:

        **🚀 Get Real Solar Resource**

        Suggested test:

        Kampala, Uganda

        Latitude: 0.3476

        Longitude: 32.5825
        """
    )

    st.stop()


# ==========================================================
# NASA POWER / SOLAR RESOURCE
# ==========================================================

st.header(
    "📡 Solar Resource Retrieval"
)


try:

    solar_resource = (
        get_solar_resource(
            latitude,
            longitude
        )
    )


except TypeError:

    try:

        solar_resource = (
            get_solar_resource(
                latitude=latitude,
                longitude=longitude
            )
        )

    except Exception as error:

        st.error(
            f"""
            ❌ get_solar_resource() could not be called.

            Error:

            {error}
            """
        )

        st.stop()


except Exception as error:

    st.error(
        f"""
        ❌ Solar resource request failed.

        Error:

        {error}
        """
    )

    st.stop()


# ==========================================================
# VALIDATE RESPONSE
# ==========================================================

if solar_resource is None:

    st.error(
        """
        ❌ get_solar_resource() returned no data.
        """
    )

    st.stop()


st.success(
    "✅ Solar resource retrieved successfully."
)


# ==========================================================
# DISPLAY RAW RESPONSE
# ==========================================================

with st.expander(
    "🔍 View Solar Resource Response"
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
# ANALYTICS
# ==========================================================

st.header(
    "🧮 Solar Analytics"
)


try:

    analytics = (
        analyze_solar_resource(
            solar_resource
        )
    )


except Exception as error:

    st.error(
        f"""
        ❌ Solar Analytics could not process the
        returned solar-resource data.

        Error:

        {error}
        """
    )

    st.stop()


# ==========================================================
# EXTRACT MONTHLY DATA
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
# DATA STATUS
# ==========================================================

status_col1, status_col2 = (
    st.columns(2)
)


with status_col1:

    if solar_count:

        st.success(
            f"""
            ☀️ Solar data available

            {solar_count} monthly values
            """
        )

    else:

        st.error(
            "❌ No monthly solar data found."
        )


with status_col2:

    if temperature_count:

        st.success(
            f"""
            🌡️ Temperature data available

            {temperature_count} monthly values
            """
        )

    else:

        st.warning(
            "⚠️ No monthly temperature data found."
        )


# ==========================================================
# SOLAR GRAPH
# ==========================================================

st.header(
    "☀️ Monthly Solar Resource"
)


try:

    solar_chart = (
        create_solar_resource_chart(
            monthly_solar
        )
    )

except Exception as error:

    solar_chart = None

    st.error(
        f"Solar graph error: {error}"
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
# TEMPERATURE GRAPH
# ==========================================================

st.header(
    "🌡️ Monthly Temperature"
)


try:

    temperature_chart = (
        create_temperature_chart(
            monthly_temperature
        )
    )

except Exception as error:

    temperature_chart = None

    st.error(
        f"Temperature graph error: {error}"
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
# SOLAR BAR CHART
# ==========================================================

st.header(
    "📊 Solar Resource — Bar Chart"
)


try:

    solar_bar_chart = (
        create_solar_bar_chart(
            monthly_solar
        )
    )

except Exception as error:

    solar_bar_chart = None

    st.error(
        f"Solar bar chart error: {error}"
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
# DATA TABLE
# ==========================================================

st.header(
    "📋 Monthly Solar & Temperature Data"
)


try:

    combined_data = (
        create_combined_dataframe(
            monthly_solar,
            monthly_temperature
        )
    )

except Exception as error:

    combined_data = None

    st.error(
        f"Data table error: {error}"
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
        "Combined data table is unavailable."
    )


# ==========================================================
# FINAL TEST RESULT
# ==========================================================

st.divider()


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

        Complete pipeline:

        📍 Coordinates
             ↓
        📡 Solar Resource
             ↓
        🧮 Solar Analytics
             ↓
        📊 Interactive Graphs

        The graph system is ready for integration
        into the main application.
        """
    )

else:

    st.warning(
        """
        ⚠️ Solar data was retrieved, but one or more
        visualization components still need adjustment.
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    Real Solar Graph Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)

