import streamlit as st


# ==========================================
# Solar PV Designer Pro v1.0
# Single File Edition
# Developed for Renewable Energy Design
# ==========================================


# Page configuration

st.set_page_config(
    page_title="Solar PV Designer Pro",
    page_icon="☀️",
    layout="wide"
)


# Title

st.title("☀️ Solar PV Designer Pro v1.0")

st.write(
    """
    An intelligent solar photovoltaic system sizing
    application for engineers, researchers and students.
    """
)


# ==========================================
# Sidebar Inputs
# ==========================================

st.sidebar.header("System Design Inputs")


energy = st.sidebar.number_input(
    "Daily Energy Consumption (kWh/day)",
    min_value=0.1,
    value=5.0,
    step=0.5
)


sun_hours = st.sidebar.number_input(
    "Peak Sun Hours per Day",
    min_value=1.0,
    value=4.0,
    step=0.5
)


efficiency = st.sidebar.slider(
    "Overall System Efficiency (%)",
    min_value=50,
    max_value=100,
    value=80
)


autonomy_days = st.sidebar.number_input(
    "Battery Autonomy (Days)",
    min_value=1,
    value=3
)


battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


panel_rating = st.sidebar.selectbox(
    "Solar Panel Rating (Watts)",
    [
        450,
        550,
        600
    ]
)


system_voltage = st.sidebar.selectbox(
    "System Voltage",
    [
        "12 V",
        "24 V",
        "48 V"
    ]
)


# ==========================================
# Engineering Calculations
# ==========================================


if st.button("🚀 Design Solar PV System"):


    # PV Size Calculation

    efficiency_factor = efficiency / 100

    pv_size = energy / (
        sun_hours *
        efficiency_factor
    )


    # Number of Panels

    panel_kw = panel_rating / 1000

    number_of_panels = round(
        pv_size / panel_kw
    )


    # Battery Calculation

    if battery_type == "Lithium-ion":

        depth_of_discharge = 0.90

    else:

        depth_of_discharge = 0.50


    battery_capacity = (
        energy *
        autonomy_days
    ) / depth_of_discharge



    # Inverter Calculation

    inverter_size = pv_size * 1.25



    # Charge Controller

    controller_current = (
        pv_size * 1000
    ) / int(system_voltage.replace(" V",""))


    # Cost Estimation

    panel_cost = pv_size * 800

    battery_cost = battery_capacity * 300

    inverter_cost = inverter_size * 250


    installation_cost = (
        panel_cost +
        battery_cost +
        inverter_cost
    ) * 0.15


    total_cost = (
        panel_cost +
        battery_cost +
        inverter_cost +
        installation_cost
    )



    # ======================================
    # Display Results
    # ======================================

    st.header("📊 Solar System Design Results")


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "PV System Size",
        f"{pv_size:.2f} kW"
    )


    col2.metric(
        "Battery Capacity",
        f"{battery_capacity:.2f} kWh"
    )


    col3.metric(
        "Inverter Size",
        f"{inverter_size:.2f} kW"
    )


    st.divider()


    st.subheader("Equipment Recommendation")


    st.write(
        f"""
        ☀️ Solar Panels:
        **{number_of_panels} panels**
        ({panel_rating} W each)

        🔋 Battery:
        **{battery_type}**

        ⚡ Charge Controller:
        Approximately
        **{controller_current:.1f} A**

        🔌 System Voltage:
        **{system_voltage}**

        💰 Estimated Project Cost:
        **${total_cost:,.0f}**
        """
    )


    st.success(
        "Solar PV system design completed successfully!"
    )


# Footer

st.divider()

st.caption(
    """
    Solar PV Designer Pro v1.0 |
    Renewable Energy Engineering Prototype |
    Developed for education and research
    """
    )
