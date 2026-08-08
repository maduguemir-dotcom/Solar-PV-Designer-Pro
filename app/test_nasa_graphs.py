# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Real NASA POWER Graph Integration Test
# Version: 2.3.0
#
# Purpose:
# Test the complete pipeline:
#
# Location
#     ↓
# Coordinates
#     ↓
# NASA POWER API
#     ↓
# Solar Analytics
#     ↓
# Graph Visualization
#
# This is a TEST PAGE.
# It does NOT modify main.py.
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st

from solar_api import (
    get_nasa_power_data
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
# SECTION 2 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NASA POWER Graph Test",
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
    "Real NASA POWER → Analytics → Graph Test"
)

st.write(
    """
    This test retrieves real monthly solar-resource and
    temperature data from NASA POWER using geographical
    coordinates, processes the data and displays
    interactive graphs.
    """
)


# ==========================================================
# SECTION 4 - LOCATION INPUT
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
# SECTION 5 - RETRIEVE NASA POWER DATA
# ==========================================================

st.header(
    "📡 NASA POWER Data"
)


get_data_button = st.button(
    "🚀 Retrieve NASA POWER Data",
    type="primary"
)


if get_data_button:

    with st.spinner(
        "Connecting to NASA POWER..."
    ):

        try:

            nasa_data = get_nasa_power_data(
                latitude,
                longitude
            )

        except Exception as error:

            st.error(
                f"""
                ❌ NASA POWER request failed.

                Error:

                {error}
                """
            )

            st.stop()


    # ======================================================
    # NASA RESPONSE VALIDATION
    # ======================================================

    if not nasa_data:

        st.error(
            "NASA POWER returned no data."
        )

        st.stop()


    st.success(
        "✅ NASA POWER data retrieved successfully."
    )


    # ======================================================
    # LOCATION INFORMATION
    # ======================================================

    location_col1, location_col2 = (
        st.columns(2)
    )


    location_col1.metric(
        "Latitude",
        f"{latitude:.4f}°"
    )


    location_col2.metric(
        "Longitude",
        f"{longitude:.4f}°"
    )


    # ======================================================
    # RAW NASA DATA
    # ======================================================

    with st.expander(
        "🔍 View Raw NASA POWER Response"
    ):

        st.json(
            nasa_data
        )


    # ======================================================
    # SECTION 6 - ANALYZE NASA DATA
    # ======================================================

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
            ❌ Solar analytics failed.

            Error:

            {error}
            """
        )

        st.stop()


    monthly_solar = analytics[
        "monthly_solar"
    ]


    monthly_temperature = analytics[
        "monthly_temperature"
    ]


    # ======================================================
    # VALIDATE MONTHLY DATA
    # ======================================================

    solar_count = len(
        monthly_solar
    )


    temperature_count = len(
        monthly_temperature
    )


    validation_col1, validation_col2 = (
        st.columns(2)
    )


    with validation_col1:

        if solar_count > 0:

            st.success(
                f"""
                ✅ Solar data detected.

                {solar_count} monthly values found.
                """
            )

        else:

            st.error(
                "❌ No monthly solar values found."
            )


    with validation_col2:

        if temperature_count > 0:

            st.success(
                f"""
                ✅ Temperature data detected.

                {temperature_count} monthly values found.
                """
            )

        else:

            st.error(
                "❌ No monthly temperature values found."
            )


    # ======================================================
    # STOP IF NO USABLE DATA
    # ======================================================

    if (
        solar_count == 0
        and
        temperature_count == 0
    ):

        st.error(
            """
            NASA POWER responded, but the Solar Analytics
            module could not find usable monthly values.

            The raw NASA response above can be inspected
            to determine the returned data structure.
            """
        )

        st.stop()


    # ======================================================
    # SECTION 7 - SOLAR STATISTICS
    # ======================================================

    st.header(
        "☀️ Solar Resource Summary"
    )


    solar_stats = analytics[
        "solar_statistics"
    ]


    solar_col1, solar_col2, solar_col3, solar_col4 = (
        st.columns(4)
    )


    if solar_stats[
        "annual_average"
    ] is not None:

        solar_col1.metric(
            "Annual Average",
            f"{solar_stats['annual_average']:.2f}"
        )

    else:

        solar_col1.metric(
            "Annual Average",
            "Unavailable"
        )


    if solar_stats[
        "maximum"
    ] is not None:

        solar_col2.metric(
            "Maximum",
            f"{solar_stats['maximum']:.2f}"
        )

    else:

        solar_col2.metric(
            "Maximum",
            "Unavailable"
        )


    solar_col3.metric(
        "Best Month",
        solar_stats[
            "best_month"
        ]
        or
        "Unavailable"
    )


    solar_col4.metric(
        "Lowest Month",
        solar_stats[
            "lowest_month"
        ]
        or
        "Unavailable"
    )


    # ======================================================
    # SECTION 8 - TEMPERATURE SUMMARY
    # ======================================================

    st.header(
        "🌡️ Temperature Summary"
    )


    temperature_stats = analytics[
        "temperature_statistics"
    ]


    temp_col1, temp_col2, temp_col3, temp_col4 = (
        st.columns(4)
    )


    if temperature_stats[
        "annual_average"
    ] is not None:

        temp_col1.metric(
            "Annual Average",
            (
                f"{temperature_stats['annual_average']:.1f} °C"
            )
        )

    else:

        temp_col1.metric(
            "Annual Average",
            "Unavailable"
        )


    if temperature_stats[
        "maximum"
    ] is not None:

        temp_col2.metric(
            "Maximum",
            (
                f"{temperature_stats['maximum']:.1f} °C"
            )
        )

    else:

        temp_col2.metric(
            "Maximum",
            "Unavailable"
        )


    temp_col3.metric(
        "Hottest Month",
        temperature_stats[
            "hottest_month"
        ]
        or
        "Unavailable"
    )


    temp_col4.metric(
        "Coolest Month",
        temperature_stats[
            "coolest_month"
        ]
        or
        "Unavailable"
    )


    # ======================================================
    # SECTION 9 - SOLAR RESOURCE GRAPH
    # ======================================================

    st.header(
        "☀️ Real Monthly Solar Resource"
    )


    solar_chart = create_solar_resource_chart(
        monthly_solar
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


    # ======================================================
    # SECTION 10 - TEMPERATURE GRAPH
    # ======================================================

    st.header(
        "🌡️ Real Monthly Temperature"
    )


    temperature_chart = create_temperature_chart(
        monthly_temperature
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


    # ======================================================
    # SECTION 11 - SOLAR BAR GRAPH
    # ======================================================

    st.header(
        "📊 Monthly Solar Resource — Bar Chart"
    )


    solar_bar_chart = create_solar_bar_chart(
        monthly_solar
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


    # ======================================================
    # SECTION 12 - COMBINED DATA
    # ======================================================

    st.header(
        "📋 Monthly Solar & Temperature Data"
    )


    combined_data = create_combined_dataframe(
        monthly_solar,
        monthly_temperature
    )


    if not combined_data.empty:

        st.dataframe(
            combined_data,
            use_container_width=True
        )

    else:

        st.warning(
            "Combined monthly data could not be created."
        )


    # ======================================================
    # SECTION 13 - SEASONAL ANALYSIS
    # ======================================================

    st.header(
        "📅 Seasonal Solar Analysis"
    )


    seasonal = analytics[
        "seasonal_analysis"
    ]


    seasonal_col1, seasonal_col2, seasonal_col3 = (
        st.columns(3)
    )


    with seasonal_col1:

        st.subheader(
            "☀️ High Solar"
        )

        high_months = seasonal[
            "high_solar_months"
        ]

        if high_months:

            st.write(
                ", ".join(
                    high_months
                )
            )

        else:

            st.write(
                "None identified"
            )


    with seasonal_col2:

        st.subheader(
            "☀️ Medium Solar"
        )

        medium_months = seasonal[
            "medium_solar_months"
        ]

        if medium_months:

            st.write(
                ", ".join(
                    medium_months
                )
            )

        else:

            st.write(
                "None identified"
            )


    with seasonal_col3:

        st.subheader(
            "☁️ Low Solar"
        )

        low_months = seasonal[
            "low_solar_months"
        ]

        if low_months:

            st.write(
                ", ".join(
                    low_months
                )
            )

        else:

            st.write(
                "None identified"
            )


    # ======================================================
    # SECTION 14 - FINAL TEST STATUS
    # ======================================================

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

            The complete data pipeline is working:

            📍 Coordinates
                    ↓
            📡 NASA POWER
                    ↓
            🧮 Solar Analytics
                    ↓
            📊 Interactive Graphs

            The real NASA POWER data is now successfully
            being processed and visualized.
            """
        )

    else:

        st.warning(
            """
            ⚠️ NASA POWER DATA WAS RETRIEVED, BUT ONE OR
            MORE GRAPHS COULD NOT BE GENERATED.

            We will troubleshoot the affected component
            before integrating it into main.py.
            """
        )


# ==========================================================
# SECTION 15 - INSTRUCTIONS
# ==========================================================

else:

    st.info(
        """
        👈 Enter or modify the latitude and longitude
        in the sidebar, then click:

        **🚀 Retrieve NASA POWER Data**

        Suggested test location:

        Kampala, Uganda

        Latitude: **0.3476**

        Longitude: **32.5825**
        """
    )


# ==========================================================
# SECTION 16 - FOOTER
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

