import streamlit as st
import pandas as pd


# ==========================================
# Solar PV Designer Pro Africa™
# Version 1.2
# Location Intelligent Edition
# ==========================================


st.set_page_config(
    page_title="Solar PV Designer Pro Africa",
    page_icon="☀️",
    layout="wide"
)


# Title

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "Location Intelligent Renewable Energy Design Platform"
)


st.write(
    """
    This application designs solar photovoltaic systems
    using energy demand, solar resource and environmental
    conditions.
    """
)


# ==========================================
# Load Solar Database
# ==========================================

try:

    solar_data = pd.read_csv(
        "data/solar_locations.csv"
    )

except:

    st.error(
        "Solar database not found. Please check data/solar_locations.csv"
    )

    st.stop()



# ==========================================
# Sidebar Inputs
# ==========================================


st.sidebar.header(
    "⚙️ System Design Parameters"
)



location = st.sidebar.selectbox(
    "📍 Select Location",
    solar_data["Location"]
)



selected_location = solar_data[
    solar_data["Location"] == location
]



sun_hours = float(
    selected_location[
        "Peak_Sun_Hours"
    ].values[0]
)



temperature = float(
    selected_location[
        "Average_Temperature"
    ].values[0]
)



energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    min_value=0.5,
    value=5.0
)



efficiency = st.sidebar.slider(
    "System Efficiency (%)",
    50,
    100,
    80
)



battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)



autonomy_days = st.sidebar.number_input(
    "Battery Backup Days",
    min_value=1,
    value=3
)



panel_rating = st.sidebar.selectbox(
    "Solar Panel Rating (Watts)",
    [
        450,
        550,
        600
    ]
)



# ==========================================
# Location Information
# ==========================================


st.header(
    "📍 Solar Resource Information"
)



col1, col2, col3 = st.columns(3)


col1.metric(
    "Location",
    location
)


col2.metric(
    "Peak Sun Hours",
    f"{sun_hours} h/day"
)


col3.metric(
    "Temperature",
    f"{temperature} °C"
)



# ==========================================
# Calculation Button
# ==========================================


if st.button(
    "🚀 Design Solar PV System"
):


    # Temperature correction

    temperature_factor = 1


    if temperature > 25:

        temperature_factor = (
            1 +
            ((temperature - 25) * 0.005)
        )



    # PV Size Calculation


    pv_size = energy / (
        sun_hours *
        (efficiency / 100)
    )



    pv_size = (
        pv_size *
        temperature_factor
    )



    # Panel Number


    panel_kw = (
        panel_rating /
        1000
    )


    number_of_panels = round(
        pv_size /
        panel_kw
    )



    # Battery Calculation


    if battery_type == "Lithium-ion":

        dod = 0.90

    else:

        dod = 0.50



    battery_capacity = (
        energy *
        autonomy_days
    ) / dod



    # Inverter Calculation


    inverter_size = (
        pv_size *
        1.25
    )



    # Charge Controller


    controller_current = (
        pv_size *
        1000 /
        48
    )



    # Cost Estimation


    panel_cost = (
        pv_size *
        800
    )


    battery_cost = (
        battery_capacity *
        300
    )


    inverter_cost = (
        inverter_size *
        250
    )


    installation = (
        panel_cost +
        battery_cost +
        inverter_cost
    ) * 0.15



    total_cost = (
        panel_cost +
        battery_cost +
        inverter_cost +
        installation
    )



    # ======================================
    # Results
    # ======================================


    st.header(
        "📊 System Design Results"
    )


    c1, c2, c3 = st.columns(3)


    c1.metric(
        "PV Capacity",
        f"{pv_size:.2f} kW"
    )


    c2.metric(
        "Battery",
        f"{battery_capacity:.2f} kWh"
    )


    c3.metric(
        "Inverter",
        f"{inverter_size:.2f} kW"
    )



    st.divider()



    st.subheader(
        "Equipment Recommendation"
    )


    st.write(
        f"""
        ☀️ Solar Panels:

        **{number_of_panels} × {panel_rating}W panels**


        🔋 Battery System:

        **{battery_type}**
        

        ⚡ Charge Controller:

        Approximately **{controller_current:.1f} A**


        💰 Estimated Project Cost:

        **${total_cost:,.0f}**
        """
    )



    # Environmental benefit


    carbon = (
        energy *
        365 *
        0.45
    )


    st.success(
        f"Estimated Annual CO₂ Reduction: {carbon:,.0f} kg/year"
    )



# ==========================================
# About Section
# ==========================================


st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™ v1.2

    Developed as an AI-ready renewable energy
    engineering platform.

    Developer:
    Engr. Prof. Ibrahim Sani Madugu
    """
)
