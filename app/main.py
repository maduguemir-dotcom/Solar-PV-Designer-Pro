import streamlit as st


# =========================================
# Solar PV Designer Pro Africa
# Version 1.1 Dashboard Edition
# =========================================


st.set_page_config(
    page_title="Solar PV Designer Pro Africa",
    page_icon="☀️",
    layout="wide"
)


# Sidebar Navigation

st.sidebar.title("☀️ Solar PV Designer Pro")

page = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Dashboard",
        "⚡ PV System Design",
        "🔋 Battery Analysis",
        "💰 Cost Estimation",
        "🌱 Environmental Impact",
        "ℹ️ About Project"
    ]
)


# =========================================
# Dashboard
# =========================================

if page == "🏠 Dashboard":

    st.title(
        "☀️ Solar PV Designer Pro Africa™"
    )

    st.subheader(
        "AI-Driven Renewable Energy Design Platform"
    )


    st.write(
        """
        Welcome to Solar PV Designer Pro Africa.

        This platform is designed to help:
        
        - Engineers
        - Researchers
        - Students
        - Renewable energy professionals

        design optimized solar photovoltaic systems.
        """
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Version",
        "1.1"
    )

    col2.metric(
        "Technology",
        "Python + AI Ready"
    )

    col3.metric(
        "Region",
        "Africa"
    )



# =========================================
# PV Design
# =========================================

elif page == "⚡ PV System Design":


    st.title(
        "⚡ Solar PV System Design"
    )


    energy = st.number_input(
        "Daily Energy Consumption (kWh/day)",
        value=5.0
    )


    sun_hours = st.number_input(
        "Peak Sun Hours",
        value=4.0
    )


    efficiency = st.slider(
        "System Efficiency (%)",
        50,
        100,
        80
    )


    if st.button("Calculate PV Size"):


        pv_size = energy / (
            sun_hours *
            efficiency/100
        )


        panels = round(
            pv_size / 0.55
        )


        inverter = pv_size * 1.25


        st.success(
            f"Required PV Capacity: {pv_size:.2f} kW"
        )


        st.success(
            f"Recommended Panels: {panels} × 550W"
        )


        st.success(
            f"Inverter Size: {inverter:.2f} kW"
        )



# =========================================
# Battery Analysis
# =========================================

elif page == "🔋 Battery Analysis":


    st.title(
        "🔋 Battery Storage Analysis"
    )


    energy = st.number_input(
        "Daily Energy (kWh/day)",
        value=5.0
    )


    days = st.number_input(
        "Backup Days",
        value=3
    )


    battery = st.selectbox(
        "Battery Type",
        [
            "Lithium-ion",
            "Lead Acid"
        ]
    )


    if battery == "Lithium-ion":

        dod = 0.9

    else:

        dod = 0.5



    capacity = (
        energy * days
    ) / dod


    st.info(
        f"Required Battery Capacity: {capacity:.2f} kWh"
    )



# =========================================
# Cost Estimation
# =========================================

elif page == "💰 Cost Estimation":


    st.title(
        "💰 Solar System Cost Estimation"
    )


    pv = st.number_input(
        "PV Size (kW)",
        value=3.0
    )


    battery = st.number_input(
        "Battery Capacity (kWh)",
        value=10.0
    )


    inverter = st.number_input(
        "Inverter Size (kW)",
        value=3.0
    )


    cost = (
        pv*800 +
        battery*300 +
        inverter*250
    )


    st.success(
        f"Estimated Equipment Cost: ${cost:,.0f}"
    )



# =========================================
# Environmental Impact
# =========================================

elif page == "🌱 Environmental Impact":


    st.title(
        "🌱 Environmental Benefits"
    )


    energy_saved = st.number_input(
        "Solar Energy Generated (kWh/year)",
        value=3000
    )


    carbon = energy_saved * 0.45


    st.success(
        f"Estimated CO₂ Reduction: {carbon:,.0f} kg/year"
    )



# =========================================
# About
# =========================================

elif page == "ℹ️ About Project":


    st.title(
        "ℹ️ About Solar PV Designer Pro Africa™"
    )


    st.write(
        """
        Developed as a renewable energy engineering
        and artificial intelligence demonstration project.

        Developer:
        
        Engr. Prof. Ibrahim Sani Madugu

        Future developments:

        ✓ AI solar prediction
        ✓ GIS solar mapping
        ✓ Weather integration
        ✓ Automated engineering reports
        """
    )
