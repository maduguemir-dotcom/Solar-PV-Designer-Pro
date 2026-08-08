# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.0
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


# Engineering calculations
from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_cost,
    calculate_carbon
)


# Solar database
from data_loader import (
    load_solar_database,
    get_location_data
)


# AI Solar Advisor
from ai import (
    generate_ai_recommendations
)


# PDF Report Generator
from reports import (
    create_pdf_report
)


# Utility functions
from utils import (
    format_currency
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
    estimation, environmental assessment and AI-assisted
    recommendations.
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


# ----------------------------------------------------------
# Location
# ----------------------------------------------------------

location = st.sidebar.selectbox(
    "📍 Select Location",
    solar_data["Location"].tolist()
)


# Get selected location information

location_data = get_location_data(
    solar_data,
    location
)


if location_data is None:

    st.error(
        "Selected location could not be found."
    )

    st.stop()


# Solar resource

sun_hours = float(
    location_data["Peak_Sun_Hours"]
)


temperature = float(
    location_data["Average_Temperature"]
)


# ----------------------------------------------------------
# Energy demand
# ----------------------------------------------------------

energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    min_value=0.1,
    value=5.0,
    step=0.5
)


# ----------------------------------------------------------
# System efficiency
# ----------------------------------------------------------

efficiency_percent = st.sidebar.slider(
    "Overall System Efficiency (%)",
    min_value=50,
    max_value=100,
    value=80
)


efficiency = (
    efficiency_percent / 100
)


# ----------------------------------------------------------
# Battery
# ----------------------------------------------------------

battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


# ----------------------------------------------------------
# Autonomy
# ----------------------------------------------------------

days = st.sidebar.number_input(
    "Battery Backup / Autonomy (Days)",
    min_value=1,
    max_value=30,
    value=3
)


# ----------------------------------------------------------
# Solar panel
# ----------------------------------------------------------

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
# SECTION 7 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary"
)


# ==========================================================
# SECTION 8 - ENGINEERING CALCULATIONS
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
    # Cost components
    # ------------------------------------------------------

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
    # SECTION 9 - DISPLAY ENGINEERING RESULTS
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
    # SECTION 10 - EQUIPMENT RECOMMENDATION
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
    # SECTION 11 - AI SOLAR ADVISOR
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
    # SECTION 12 - PDF REPORT DATA
    # ======================================================

    report_data = {

        "location": location,

        "energy": energy,

        "sun_hours": sun_hours,

        "temperature": temperature,

        "battery_type": battery_type,

        "days": days,

        "pv": pv_size,

        "panels": panels,

        "panel_rating": panel_rating,

        "battery": battery_capacity,

        "inverter": inverter_size,

        "controller": controller_current,

        "panel_cost": panel_cost,

        "battery_cost": battery_cost,

        "inverter_cost": inverter_cost,

        "installation_cost": installation_cost,

        "cost": total_cost,

        "carbon": carbon_reduction
    }


    # ======================================================
    # SECTION 13 - PDF REPORT
    # ======================================================

    st.divider()


    st.header(
        "📄 Solar Design Report"
    )


    pdf_report = create_pdf_report(
        data=report_data,
        recommendations=recommendations
    )


    st.download_button(

        label="📥 Download Professional PDF Report",

        data=pdf_report,

        file_name=(
            "Solar_PV_Design_Report.pdf"
        ),

        mime="application/pdf"
    )


# ==========================================================
# SECTION 14 - FOOTER
# ==========================================================

st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™ v2.0

    AI-Ready Renewable Energy Design Platform

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
