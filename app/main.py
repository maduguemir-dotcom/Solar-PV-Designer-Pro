```python
# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.1.6
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# v2.1.6 Updates:
# - Global coordinate input
# - Existing solar database retained
# - NASA POWER live solar-resource integration
# - Global Location Engine integration
# - Live peak sun hours from NASA POWER
# - Live average temperature from NASA POWER
# - Cleaner modular application architecture
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st


# ----------------------------------------------------------
# Engineering calculations
# ----------------------------------------------------------

from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_carbon
)


# ----------------------------------------------------------
# Solar database
# ----------------------------------------------------------

from data_loader import (
    load_solar_database,
    get_location_data
)


# ----------------------------------------------------------
# AI Solar Advisor
# ----------------------------------------------------------

from ai import (
    generate_ai_recommendations
)


# ----------------------------------------------------------
# PDF Report Generator
# ----------------------------------------------------------

from reports import (
    create_pdf_report
)


# ----------------------------------------------------------
# Utility functions
# ----------------------------------------------------------

from utils import (
    format_currency
)


# ----------------------------------------------------------
# Global Location Engine
# ----------------------------------------------------------

from location_engine import (
    get_location_solar_resource,
    get_location_summary
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

    solar_database = load_solar_database()

except Exception as error:

    st.error(
        f"Unable to load solar database: {error}"
    )

    st.stop()


# ==========================================================
# SECTION 5 - SIDEBAR
# ==========================================================

st.sidebar.header(
    "⚙️ System Design Inputs"
)


# ==========================================================
# SECTION 6 - LOCATION SOURCE
# ==========================================================

st.sidebar.subheader(
    "📍 Project Location"
)

location_source = st.sidebar.radio(
    "Choose location method:",
    [
        "Solar Database",
        "Enter Coordinates"
    ]
)


# ==========================================================
# SECTION 7 - INITIAL LOCATION VARIABLES
# ==========================================================

location_description = "Not selected"

latitude = None
longitude = None

sun_hours = None
temperature = None

solar_data = None
solar_summary = None

location_summary = None


# ==========================================================
# SECTION 8 - SOLAR DATABASE LOCATION
# ==========================================================

if location_source == "Solar Database":

    # ------------------------------------------------------
    # Existing database location
    # ------------------------------------------------------

    location = st.sidebar.selectbox(
        "Select Location",
        solar_database["Location"].tolist()
    )


    location_data = get_location_data(
        solar_database,
        location
    )


    if location_data is None:

        st.error(
            "Selected location could not be found."
        )

        st.stop()


    # ------------------------------------------------------
    # Existing database solar values
    # ------------------------------------------------------

    sun_hours = float(
        location_data["Peak_Sun_Hours"]
    )


    temperature = float(
        location_data["Average_Temperature"]
    )


    # ------------------------------------------------------
    # Database locations do not necessarily have
    # coordinates in the current database.
    # ------------------------------------------------------

    latitude = None
    longitude = None


    location_description = location


# ==========================================================
# SECTION 9 - GLOBAL COORDINATE LOCATION
# ==========================================================

else:

    st.sidebar.info(
        """
        Enter the geographical coordinates of your
        project site.

        Latitude: -90 to +90

        Longitude: -180 to +180

        NASA POWER will provide the solar-resource
        information for the selected location.
        """
    )


    # ------------------------------------------------------
    # Latitude
    # ------------------------------------------------------

    latitude = st.sidebar.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=0.3476,
        step=0.0001,
        format="%.4f"
    )


    # ------------------------------------------------------
    # Longitude
    # ------------------------------------------------------

    longitude = st.sidebar.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=32.5825,
        step=0.0001,
        format="%.4f"
    )


    # ------------------------------------------------------
    # Optional location name
    # ------------------------------------------------------

    location_name = st.sidebar.text_input(
        "Location Name",
        value="Kampala"
    )


    # ------------------------------------------------------
    # Optional country
    # ------------------------------------------------------

    country = st.sidebar.text_input(
        "Country",
        value="Uganda"
    )


    # ------------------------------------------------------
    # Connect location to NASA POWER
    # ------------------------------------------------------

    location_result = get_location_solar_resource(

        latitude=latitude,

        longitude=longitude,

        location_name=location_name,

        country=country

    )


    # ------------------------------------------------------
    # Check result
    # ------------------------------------------------------

    if not location_result["success"]:

        st.sidebar.error(
            "NASA POWER location lookup failed: "
            + str(
                location_result["message"]
            )
        )

        st.stop()


    # ------------------------------------------------------
    # Extract location summary
    # ------------------------------------------------------

    location_summary = get_location_summary(
        location_result
    )


    # ------------------------------------------------------
    # Extract live NASA POWER data
    # ------------------------------------------------------

    solar_data = location_result.get(
        "solar"
    )


    solar_summary = location_result.get(
        "summary"
    )


    # ------------------------------------------------------
    # Use NASA POWER solar values
    # ------------------------------------------------------

    sun_hours = location_summary.get(
        "peak_sun_hours"
    )


    temperature = location_summary.get(
        "average_temperature"
    )


    # ------------------------------------------------------
    # Safety check
    # ------------------------------------------------------

    if sun_hours is None:

        st.sidebar.error(
            "NASA POWER did not return usable "
            "solar-resource data."
        )

        st.stop()


    if temperature is None:

        temperature = 25.0


    # ------------------------------------------------------
    # Location description
    # ------------------------------------------------------

    location_description = (
        location_summary.get(
            "location",
            f"{latitude:.4f}°, {longitude:.4f}°"
        )
    )


    # ------------------------------------------------------
    # Confirmation
    # ------------------------------------------------------

    st.sidebar.success(
        "🌍 Location connected to NASA POWER."
    )


# ==========================================================
# SECTION 10 - ENERGY DEMAND
# ==========================================================

energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    min_value=0.1,
    value=5.0,
    step=0.5
)


# ==========================================================
# SECTION 11 - SYSTEM EFFICIENCY
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
# SECTION 12 - BATTERY
# ==========================================================

battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


# ==========================================================
# SECTION 13 - BATTERY AUTONOMY
# ==========================================================

days = st.sidebar.number_input(
    "Battery Backup / Autonomy (Days)",
    min_value=1,
    max_value=30,
    value=3
)


# ==========================================================
# SECTION 14 - SOLAR PANEL
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
# SECTION 15 - SOLAR RESOURCE INFORMATION
# ==========================================================

st.header(
    "📍 Solar Resource Information"
)


location_col1, location_col2, location_col3 = (
    st.columns(3)
)


# ----------------------------------------------------------
# Location
# ----------------------------------------------------------

location_col1.metric(
    "Location",
    location_description
)


# ----------------------------------------------------------
# Latitude
# ----------------------------------------------------------

if latitude is None:

    latitude_display = "Database"

else:

    latitude_display = (
        f"{latitude:.4f}°"
    )


location_col2.metric(
    "Latitude",
    latitude_display
)


# ----------------------------------------------------------
# Longitude
# ----------------------------------------------------------

if longitude is None:

    longitude_display = "Database"

else:

    longitude_display = (
        f"{longitude:.4f}°"
    )


location_col3.metric(
    "Longitude",
    longitude_display
)


# ==========================================================
# SECTION 16 - SOLAR RESOURCE DETAILS
# ==========================================================

solar_info_col1, solar_info_col2, solar_info_col3 = (
    st.columns(3)
)


solar_info_col1.metric(
    "☀️ Peak Sun Hours",
    f"{sun_hours:.2f} h/day"
)


solar_info_col2.metric(
    "🌡️ Average Temperature",
    f"{temperature:.1f} °C"
)


if location_source == "Enter Coordinates":

    solar_info_col3.metric(
        "📡 Data Source",
        "NASA POWER"
    )

else:

    solar_info_col3.metric(
        "📡 Data Source",
        "Solar Database"
    )


# ==========================================================
# SECTION 17 - DATA SOURCE INFORMATION
# ==========================================================

if location_source == "Enter Coordinates":

    climatology_period = (
        location_summary.get(
            "climatology_period",
            "2001-2020"
        )
        if location_summary
        else "2001-2020"
    )


    st.info(
        f"""
        **Live Solar Resource**

        Source: NASA POWER

        Climatology period: {climatology_period}

        Coordinates: {latitude:.4f}°,
        {longitude:.4f}°
        """
    )

else:

    st.info(
        f"""
        **Solar Resource Inputs**

        Peak Sun Hours: {sun_hours:.2f} hours/day

        Average Temperature: {temperature:.1f} °C

        Source: Existing Solar Database
        """
    )


# ==========================================================
# SECTION 18 - OPTIONAL NASA MONTHLY DATA
# ==========================================================

if (
    location_source == "Enter Coordinates"
    and solar_data is not None
):

    with st.expander(
        "☀️ View NASA POWER Monthly Solar Resource"
    ):

        monthly_display = solar_data.get(
            "monthly_display",
            []
        )


        if monthly_display:

            st.dataframe(
                monthly_display,
                use_container_width=True
            )

        else:

            st.warning(
                "No monthly solar-resource data "
                "is available for display."
            )


# ==========================================================
# SECTION 19 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary"
)


# ==========================================================
# SECTION 20 - ENGINEERING CALCULATIONS
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
    # ------------------------------------------------------

    controller_current = (
        pv_size * 1000 / 48
    )


    # ------------------------------------------------------
    # Cost estimation
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
    # SECTION 21 - ENGINEERING RESULTS
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
    # SECTION 22 - EQUIPMENT RECOMMENDATION
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
    # SECTION 23 - AI SOLAR ADVISOR
    # ======================================================

    st.divider()


    st.header(
        "🤖 AI Solar Advisor"
    )


    recommendations = generate_ai_recommendations(

        location=location_description,

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
    # SECTION 24 - PDF REPORT DATA
    # ======================================================

    report_data = {

        "location":
            location_description,

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

        "panel_cost":
            panel_cost,

        "battery_cost":
            battery_cost,

        "inverter_cost":
            inverter_cost,

        "installation_cost":
            installation_cost,

        "cost":
            total_cost,

        "carbon":
            carbon_reduction

    }


    # ------------------------------------------------------
    # Add coordinates to report where available
    # ------------------------------------------------------

    if latitude is not None:

        report_data["latitude"] = latitude


    if longitude is not None:

        report_data["longitude"] = longitude


    if location_source == "Enter Coordinates":

        report_data["data_source"] = (
            "NASA POWER"
        )

        report_data["climatology_period"] = (
            location_summary.get(
                "climatology_period",
                "2001-2020"
            )
        )

    else:

        report_data["data_source"] = (
            "Solar Database"
        )


    # ======================================================
    # SECTION 25 - PDF REPORT
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

            label=(
                "📥 Download Professional PDF Report"
            ),

            data=pdf_report,

            file_name=(
                "Solar_PV_Design_Report.pdf"
            ),

            mime="application/pdf"

        )

    except Exception as error:

        st.error(
            "Unable to generate PDF report: "
            f"{error}"
        )


# ==========================================================
# SECTION 26 - FOOTER
# ==========================================================

st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™ v2.1.6

    Global Location Engine + NASA POWER

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
```
