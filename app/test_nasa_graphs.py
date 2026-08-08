# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Real NASA POWER → Analytics → Graph Test
# Version: 2.3.0
#
# IMPORTANT:
# This test does NOT modify solar_api.py or main.py.
#
# ==========================================================

import streamlit as st
import inspect


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
    "Real NASA POWER → Analytics → Graph Test"
)


st.write(
    """
    This page tests the complete pipeline:

    Coordinates → NASA POWER → Solar Analytics → Graphs
    """
)


# ==========================================================
# LOAD MODULES
# ==========================================================

try:

    import solar_api

except Exception as error:

    st.error(
        f"""
        ❌ Could not load solar_api.py

        Error:

        {error}
        """
    )

    st.stop()


try:

    from solar_analytics import (
        analyze_solar_resource
    )

except Exception as error:

    st.error(
        f"""
        ❌ Could not load solar_analytics.py

        Error:

        {error}
        """
    )

    st.stop()


try:

    from graph_visualization import (
        create_solar_resource_chart,
        create_temperature_chart,
        create_solar_bar_chart,
        create_combined_dataframe
    )

except Exception as error:

    st.error(
        f"""
        ❌ Could not load graph_visualization.py

        Error:

        {error}
        """
    )

    st.stop()


# ==========================================================
# SECTION 1 - DETECT NASA FUNCTIONS
# ==========================================================

st.header(
    "🔎 NASA POWER Module Check"
)


available_functions = []


for name in dir(solar_api):

    if name.startswith("_"):
        continue

    try:

        attribute = getattr(
            solar_api,
            name
        )

        if callable(attribute):

            available_functions.append(
                name
            )

    except Exception:

        pass


if available_functions:

    st.success(
        "✅ solar_api.py loaded successfully."
    )

    with st.expander(
        "View functions available in solar_api.py"
    ):

        st.write(
            available_functions
        )

else:

    st.warning(
        "No callable functions were detected in solar_api.py."
    )


# ==========================================================
# FIND LIKELY NASA FUNCTION
# ==========================================================

preferred_names = [

    "fetch_nasa_power_data",

    "get_nasa_power_data",

    "get_nasa_power",

    "fetch_nasa_power",

    "request_nasa_power",

    "get_solar_data",

    "fetch_solar_data",

    "get_power_data",

    "fetch_power_data",

    "get_nasa_data",

    "fetch_nasa_data"

]


nasa_function = None

nasa_function_name = None


for function_name in preferred_names:

    if hasattr(
        solar_api,
        function_name
    ):

        possible_function = getattr(
            solar_api,
            function_name
        )

        if callable(
            possible_function
        ):

            nasa_function = (
                possible_function
            )

            nasa_function_name = (
                function_name
            )

            break


# ==========================================================
# IF NO FUNCTION FOUND
# ==========================================================

if nasa_function is None:

    st.error(
        """
        ❌ No compatible NASA POWER function was
        automatically identified.

        Your solar_api.py is loaded successfully,
        but its NASA function has a different name.
        """
    )


    st.info(
        """
        Please look at the function list above.

        We will use the exact function already present
        in your working solar_api.py.
        """
    )


    st.stop()


st.success(
    f"NASA POWER function detected: `{nasa_function_name}()`"
)


# ==========================================================
# FUNCTION SIGNATURE
# ==========================================================

try:

    function_signature = inspect.signature(
        nasa_function
    )

    with st.expander(
        "🔍 View NASA function signature"
    ):

        st.code(
            f"{nasa_function_name}{function_signature}"
        )

except Exception:

    pass


# ==========================================================
# SECTION 2 - LOCATION
# ==========================================================

st.header(
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
    Latitude: {latitude:.4f}°

    Longitude: {longitude:.4f}°
    """
)


# ==========================================================
# SECTION 3 - RETRIEVE NASA DATA
# ==========================================================

run_test = st.button(
    "🚀 Retrieve NASA POWER Data",
    type="primary"
)


if not run_test:

    st.info(
        """
        Enter the coordinates and click:

        **🚀 Retrieve NASA POWER Data**

        Suggested test:

        Kampala, Uganda

        Latitude: 0.3476

        Longitude: 32.5825
        """
    )

    st.stop()


# ==========================================================
# CALL NASA FUNCTION
# ==========================================================

st.header(
    "📡 NASA POWER Connection"
)


try:

    # ------------------------------------------------------
    # First attempt:
    # latitude, longitude
    # ------------------------------------------------------

    try:

        nasa_data = nasa_function(
            latitude,
            longitude
        )

    except TypeError:

        # --------------------------------------------------
        # Second attempt:
        # keyword arguments
        # --------------------------------------------------

        try:

            nasa_data = nasa_function(
                latitude=latitude,
                longitude=longitude
            )

        except TypeError:

            # ----------------------------------------------
            # Third attempt:
            # lat/lon
            # ----------------------------------------------

            nasa_data = nasa_function(
                lat=latitude,
                lon=longitude
            )


except Exception as error:

    st.error(
        f"""
        ❌ NASA POWER request failed.

        Function used:

        `{nasa_function_name}()`

        Error:

        {error}
        """
    )

    st.stop()


# ==========================================================
# NASA DATA VALIDATION
# ==========================================================

if nasa_data is None:

    st.error(
        """
        ❌ NASA POWER function returned None.
        """
    )

    st.stop()


st.success(
    "✅ NASA POWER data retrieved successfully."
)


# ==========================================================
# RAW DATA
# ==========================================================

with st.expander(
    "🔍 View Raw NASA POWER Data"
):

    st.json(
        nasa_data
    )


# ==========================================================
# SECTION 4 - SOLAR ANALYTICS
# ==========================================================

st.header(
    "🧮 Solar Analytics"
)


try:

    analytics = analyze_solar_resource(
        nasa_data
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
# EXTRACT DATA
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
# DATA VALIDATION
# ==========================================================

validation_col1, validation_col2 = (
    st.columns(2)
)


with validation_col1:

    if solar_count > 0:

        st.success(
            f"☀️ {solar_count} solar values detected."
        )

    else:

        st.error(
            "❌ No solar values detected."
        )


with validation_col2:

    if temperature_count > 0:

        st.success(
            f"🌡️ {temperature_count} temperature values detected."
        )

    else:

        st.error(
            "❌ No temperature values detected."
        )


# ==========================================================
# STOP IF NO DATA
# ==========================================================

if (
    solar_count == 0
    and
    temperature_count == 0
):

    st.error(
        """
        NASA POWER returned data, but
        solar_analytics.py could not extract
        monthly solar or temperature values.
        """
    )

    st.stop()


# ==========================================================
# SECTION 5 - SOLAR GRAPH
# ==========================================================

st.header(
    "☀️ Real Monthly Solar Resource"
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
# SECTION 6 - TEMPERATURE GRAPH
# ==========================================================

st.header(
    "🌡️ Real Monthly Temperature"
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
# SECTION 7 - SOLAR BAR GRAPH
# ==========================================================

st.header(
    "📊 Monthly Solar Resource — Bar Chart"
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
# SECTION 8 - DATA TABLE
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
        f"Combined data error: {error}"
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
        "Combined data table could not be generated."
    )


# ==========================================================
# SECTION 9 - FINAL STATUS
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
        🎉 REAL NASA POWER GRAPH TEST PASSED

        The complete pipeline is working:

        📍 Coordinates
             ↓
        📡 NASA POWER
             ↓
        🧮 Solar Analytics
             ↓
        📊 Interactive Graphs

        The system is ready for integration
        into the main Solar PV Designer Pro application.
        """
    )

else:

    st.warning(
        """
        ⚠️ NASA POWER data was retrieved, but
        one or more graphs could not be generated.
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    Real NASA POWER Graph Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)

