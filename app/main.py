```python
# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.3
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# AI-ready solar photovoltaic system design platform
# for engineering, research, education and demonstration.
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st


# ==========================================================
# ENGINEERING CALCULATIONS
# ==========================================================

from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_cost,
    calculate_carbon
)


# ==========================================================
# SOLAR DATABASE
# ==========================================================

from data_loader import (
    load_solar_database,
    get_location_data,
    get_location_coordinates
)


# ==========================================================
# AI SOLAR ADVISOR
# ==========================================================

from ai import (
    generate_ai_recommendations
)


# ==========================================================
# PDF REPORT GENERATOR
# ==========================================================

from reports import (
    create_pdf_report
)


# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

from utils import (
    format_currency
)


# ==========================================================
# NASA POWER SOLAR RESOURCE
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
# SECTION 2 - APPLICATION CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar PV Designer Pro Africa",
    page_icon="☀️",
    layout="wide"
)


# ==========================================================
# SECTION 3 - APPLICATION HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "AI-Ready Renewable Energy Design Platform"
)

st.write(
    """
    Solar PV Designer Pro Africa™ is a renewable energy
    engineering platform designed to support preliminary
    photovoltaic system sizing, battery analysis, cost
    estimation, environmental assessment, solar-resource
    analytics and AI-assisted recommendations.
    """
)


# ==========================================================
# SECTION 4 - LOAD SOLAR DATABASE
# ==========================================================

try:

    solar_data = load_solar_database()

except Exception as error:

    st.error(
        f"Unable to load solar database: {error}"
    )

    st.stop()


# ==========================================================
# SECTION 5 - SIDEBAR / USER INPUTS
# ==========================================================

st.sidebar.header(
    "⚙️ System Design Inputs"
)


# ==========================================================
# LOCATION
# ==========================================================

location = st.sidebar.selectbox(
    "📍 Select Location",
    solar_data["Location"].tolist()
)


# ==========================================================
# GET SELECTED LOCATION INFORMATION
# ==========================================================

location_data = get_location_data(
    solar_data,
    location
)


if location_data is None:

    st.error(
        "Selected location could not be found."
    )

    st.stop()


# ==========================================================
# SOLAR RESOURCE FROM DATABASE
# ==========================================================

try:

    sun_hours = float(
        location_data["Peak_Sun_Hours"]
    )

except (
    KeyError,
    TypeError,
    ValueError
):

    sun_hours = 5.0


try:

    temperature = float(
        location_data["Average_Temperature"]
    )

except (
    KeyError,
    TypeError,
    ValueError
):

    temperature = 25.0


# ==========================================================
# LOCATION COORDINATES
# ==========================================================

latitude, longitude = (
    get_location_coordinates(
        location_data
    )
)


# ==========================================================
# NASA POWER RESOURCE VARIABLES
# ==========================================================

solar_resource = None

solar_analytics = None

nasa_error = None


# ==========================================================
# NASA POWER RETRIEVAL
# ==========================================================

if (
    latitude is not None
    and
    longitude is not None
):

    try:

        solar_resource = get_solar_resource(
            latitude,
            longitude
        )

        if solar_resource is not None:

            solar_analytics = (
                analyze_solar_resource(
                    solar_resource
                )
            )

    except Exception as error:

        nasa_error = str(error)

        solar_resource = None

        solar_analytics = None


# ==========================================================
# ENERGY DEMAND
# ==========================================================

energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    min_value=0.1,
    value=5.0,
    step=0.5
)


# ==========================================================
# SYSTEM EFFICIENCY
# ==========================================================

efficiency_percent = st.sidebar.slider(
    "Overall System Efficiency (%)",
    min_value=50,
    max_value=100,
    value=80
)

efficiency = (
    efficiency_percent / 100
)


# ==========================================================
# BATTERY
# ==========================================================

battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


# ==========================================================
# AUTONOMY
# ==========================================================

days = st.sidebar.number_input(
    "Battery Backup / Autonomy (Days)",
    min_value=1,
    max_value=30,
    value=3
)


# ==========================================================
# SOLAR PANEL
# ==========================================================

panel_rating = st.sidebar.selectbox(
    "Solar Panel Rating (Watts)",
    [
        450,
        550,
        600
    ]
)


# ==========================================================
# SECTION 6 - LOCATION INFORMATION
# ==========================================================

st.header(
    "📍 Solar Resource Information"
)


location_col1, location_col2, location_col3 = (
    st.columns(3)
)


location_col1.metric(
    "Location",
    location
)


location_col2.metric(
    "Peak Sun Hours",
    f"{sun_hours:.1f} h/day"
)


location_col3.metric(
    "Average Temperature",
    f"{temperature:.1f} °C"
)


# ==========================================================
# COORDINATES
# ==========================================================

if (
    latitude is not None
    and
    longitude is not None
):

    coordinate_col1, coordinate_col2 = (
        st.columns(2)
    )

    coordinate_col1.metric(
        "Latitude",
        f"{latitude:.4f}°"
    )

    coordinate_col2.metric(
        "Longitude",
        f"{longitude:.4f}°"
    )

else:

    st.info(
        """
        📍 Geographic coordinates are not available
        for this database location.

        The application will continue using the existing
        solar-resource database.
        """
    )


# ==========================================================
# SECTION 7 - NASA POWER SOLAR ANALYTICS
# ==========================================================

st.divider()

st.header(
    "📡 NASA POWER Solar Analytics"
)


if solar_analytics is not None:

    st.success(
        "✅ NASA POWER solar-resource data retrieved successfully."
    )


    # ======================================================
    # MONTHLY SOLAR DATA
    # ======================================================

    monthly_solar = solar_analytics.get(
        "monthly_solar",
        []
    )


    # ======================================================
    # MONTHLY TEMPERATURE DATA
    # ======================================================

    monthly_temperature = solar_analytics.get(
        "monthly_temperature",
        []
    )


    # ======================================================
    # ANALYTICS METRICS
    # ======================================================

    analytics_col1, analytics_col2 = (
        st.columns(2)
    )


    analytics_col1.metric(
        "Monthly Solar Values",
        len(monthly_solar)
    )


    analytics_col2.metric(
        "Monthly Temperature Values",
        len(monthly_temperature)
    )


    # ======================================================
    # SOLAR RESOURCE GRAPH
    # ======================================================

    if monthly_solar:

        st.subheader(
            "☀️ Monthly Solar Resource"
        )

        try:

            solar_chart = (
                create_solar_resource_chart(
                    monthly_solar
                )
            )

            if solar_chart is not None:

                st.plotly_chart(
                    solar_chart,
                    use_container_width=True
                )

        except Exception as error:

            st.warning(
                f"Solar resource graph unavailable: {error}"
            )


    # ======================================================
    # TEMPERATURE GRAPH
    # ======================================================

    if monthly_temperature:

        st.subheader(
            "🌡️ Monthly Temperature"
        )

        try:

            temperature_chart = (
                create_temperature_chart(
                    monthly_temperature
                )
            )

            if temperature_chart is not None:

                st.plotly_chart(
                    temperature_chart,
                    use_container_width=True
                )

        except Exception as error:

            st.warning(
                f"Temperature graph unavailable: {error}"
            )


    # ======================================================
    # SOLAR BAR CHART
    # ======================================================

    if monthly_solar:

        st.subheader(
            "📊 Monthly Solar Resource — Bar Chart"
        )

        try:

            solar_bar_chart = (
                create_solar_bar_chart(
                    monthly_solar
                )
            )

            if solar_bar_chart is not None:

                st.plotly_chart(
                    solar_bar_chart,
                    use_container_width=True
                )

        except Exception as error:

            st.warning(
                f"Solar bar chart unavailable: {error}"
            )


    # ======================================================
    # COMBINED DATA TABLE
    # ======================================================

    try:

        combined_data = (
            create_combined_dataframe(
                monthly_solar,
                monthly_temperature
            )
        )

        if (
            combined_data is not None
            and
            not combined_data.empty
        ):

            with st.expander(
                "📋 View Monthly Solar & Temperature Data"
            ):

                st.dataframe(
                    combined_data,
                    use_container_width=True
                )

    except Exception as error:

        st.warning(
            f"Monthly data table unavailable: {error}"
        )


else:

    if nasa_error:

        st.warning(
            f"""
            ⚠️ NASA POWER data is temporarily unavailable.

            The application will continue using the
            existing solar-resource database.

            Technical message:
            {nasa_error}
            """
        )

    elif (
        latitude is None
        or
        longitude is None
    ):

        st.info(
            """
            📍 NASA POWER analytics require latitude and
            longitude for this location.

            The existing database values will continue
            to be used for PV system sizing.
            """
        )

    else:

        st.info(
            """
            📡 NASA POWER analytics are not currently
            available for this location.

            The existing solar-resource database will
            continue to be used.
            """
        )


# ==========================================================
# SECTION 8 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary"
)


# ==========================================================
# SECTION 9 - ENGINEERING CALCULATIONS
# ==========================================================

if design_button:

    # ------------------------------------------------------
    # PV capacity
    # ------------------------------------------------------

    pv_size = calculate_pv_size(
        energy=energy,
        sun_hours=sun_hours,
        efficiency=efficiency,
        temperature=temperature
    )


    # ------------------------------------------------------
    # Solar panels
    # ------------------------------------------------------

    panels = calculate_panels(
        pv_size=pv_size,
        panel_rating=panel_rating
    )


    # ------------------------------------------------------
    # Battery
    # ------------------------------------------------------

    battery_capacity = calculate_battery(
        energy=energy,
        days=days,
        battery_type=battery_type
    )


    # ------------------------------------------------------
    # Inverter
    # ------------------------------------------------------

    inverter_size = calculate_inverter(
        pv_size
    )


    # ------------------------------------------------------
    # Charge controller
    #
    # Preliminary estimate using a 48 V architecture.
    # ------------------------------------------------------

    controller_current = (
        pv_size * 1000 / 48
    )


    # ------------------------------------------------------
    # Cost calculation
    # ------------------------------------------------------

    try:

        total_cost = calculate_cost(
            pv_size=pv_size,
            battery_capacity=battery_capacity,
            inverter_size=inverter_size
        )

    except Exception:

        panel_cost = (
            pv_size * 800
        )

        battery_cost = (
            battery_capacity * 300
        )

        inverter_cost = (
            inverter_size * 250
        )

        equipment_cost = (
            panel_cost
            +
            battery_cost
            +
            inverter_cost
        )

        installation_cost = (
            equipment_cost * 0.15
        )

        total_cost = (
            equipment_cost
            +
            installation_cost
        )


    # ------------------------------------------------------
    # Environmental impact
    # ------------------------------------------------------

    carbon_reduction = calculate_carbon(
        energy
    )


    # ======================================================
    # SECTION 10 - DISPLAY ENGINEERING RESULTS
    # ======================================================

    st.header(
        "📊 Solar PV Design Results"
    )


    result_col1, result_col2, result_col3 = (
        st.columns(3)
    )


    result_col1.metric(
        "PV Capacity",
        f"{pv_size:.2f} kW"
    )


    result_col2.metric(
        "Battery Capacity",
        f"{battery_capacity:.2f} kWh"
    )


    result_col3.metric(
        "Inverter",
        f"{inverter_size:.2f} kW"
    )


    st.divider()


    # ======================================================
    # SECTION 11 - EQUIPMENT RECOMMENDATION
    # ======================================================

    st.subheader(
        "⚡ Recommended Equipment"
    )


    equipment_col1, equipment_col2 = (
        st.columns(2)
    )


    with equipment_col1:

        st.write(
            f"""
            **☀️ Solar Array**

            {panels} × {panel_rating} W panels

            **🔋 Battery**

            {battery_type}

            {battery_capacity:.2f} kWh
            """
        )


    with equipment_col2:

        st.write(
            f"""
            **🔌 Inverter**

            {inverter_size:.2f} kW

            **⚡ Charge Controller**

            Approximately {controller_current:.1f} A

            **💰 Estimated System Cost**

            {format_currency(total_cost)}
            """
        )


    st.success(
        f"Estimated annual CO₂ reduction: "
        f"{carbon_reduction:,.0f} kg/year"
    )


    # ======================================================
    # SECTION 12 - AI SOLAR ADVISOR
    # ======================================================

    st.divider()

    st.header(
        "🤖 AI Solar Advisor"
    )


    recommendations = generate_ai_recommendations(

        location=location,

        battery_type=battery_type,

        pv_size=pv_size,

        battery_capacity=battery_capacity,

        inverter_size=inverter_size,

        energy=energy,

        carbon_reduction=carbon_reduction
    )


    for recommendation in recommendations:

        st.success(
            recommendation
        )


    # ======================================================
    # SECTION 13 - PDF REPORT DATA
    # ======================================================

    report_data = {

        "location":
            location,

        "energy":
            energy,

        "sun_hours":
            sun_hours,

        "temperature":
            temperature,

        "battery_type":
            battery_type,

        "days":
            days,

        "pv":
            pv_size,

        "panels":
            panels,

        "panel_rating":
            panel_rating,

        "battery":
            battery_capacity,

        "inverter":
            inverter_size,

        "controller":
            controller_current,

        "cost":
            total_cost,

        "carbon":
            carbon_reduction
    }


    # ======================================================
    # ADD NASA INFORMATION TO REPORT DATA
    # ======================================================

    if (
        latitude is not None
        and
        longitude is not None
    ):

        report_data[
            "latitude"
        ] = latitude

        report_data[
            "longitude"
        ] = longitude


    # ======================================================
    # SECTION 14 - PDF REPORT
    # ======================================================

    st.divider()

    st.header(
        "📄 Solar Design Report"
    )


    try:

        pdf_report = create_pdf_report(
            data=report_data,
            recommendations=recommendations
        )


        st.download_button(

            label=
                "📥 Download Professional PDF Report",

            data=
                pdf_report,

            file_name=
                "Solar_PV_Design_Report.pdf",

            mime=
                "application/pdf"
        )

    except Exception as error:

        st.error(
            f"PDF report generation failed: {error}"
        )


# ==========================================================
# SECTION 15 - FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.3

    AI-Ready Renewable Energy Design Platform

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
```
