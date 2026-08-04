import streamlit as st

from solar_calculator import calculate_pv_size
from battery_model import calculate_battery_capacity
#from inverter_model import calculate_inverter_size
from inverter_model import calculate_inverter_size
from solar_calculator import calculate_number_of_panels
from cost_estimator import calculate_cost

st.set_page_config(
    page_title="Solar PV Designer Pro",
    page_icon="☀️"
)


st.title(
    "☀️ Solar PV Designer Pro v1.0"
)

st.write(
    "Professional Solar Energy System Design Platform"
)


st.sidebar.header(
    "System Inputs"
)


energy = st.sidebar.number_input(
    "Daily Energy (kWh/day)",
    value=5.0
)


sun_hours = st.sidebar.number_input(
    "Peak Sun Hours",
    value=4.0
)


efficiency = st.sidebar.slider(
    "System Efficiency %",
    50,
    100,
    80
)


days = st.sidebar.number_input(
    "Battery Autonomy Days",
    value=3
)


dod = st.sidebar.slider(
    "Battery Depth of Discharge %",
    20,
    100,
    50
)



if st.button("Design Solar System"):

    pv = calculate_pv_size(
        energy,
        sun_hours,
        efficiency
    )


    battery = calculate_battery_capacity(
        energy,
        days,
        dod
    )


    inverter = calculate_inverter_size(
        pv
    )


    st.header(
        "Design Results"
    )


    col1, col2, col3 = st.columns(3)


    col1.metric(
        "PV Size",
        f"{pv:.2f} kW"
    )


    col2.metric(
        "Battery",
        f"{battery:.2f} kWh"
    )


    col3.metric(
        "Inverter",
        f"{inverter:.2f} kW"
    )


st.info(
    "Solar PV Designer Pro - Research Prototype"
)
