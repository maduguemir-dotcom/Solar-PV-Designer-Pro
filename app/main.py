import streamlit as st


# Solar PV Designer Pro v1.0

st.title("☀️ Solar PV Designer Pro v1.0")

st.write(
    "Intelligent Solar PV System Sizing Tool "
    "for Engineers, Researchers and Students"
)


# User Inputs

energy = st.number_input(
    "Daily Energy Consumption (kWh/day)",
    min_value=0.1,
    value=5.0
)

sun_hours = st.number_input(
    "Peak Sun Hours per Day",
    min_value=1.0,
    value=4.0
)

efficiency = st.slider(
    "System Efficiency (%)",
    50,
    100,
    80
)

days = st.number_input(
    "Battery Autonomy Days",
    min_value=1,
    value=3
)

dod = st.slider(
    "Battery Depth of Discharge (%)",
    20,
    100,
    50
)


# Calculations

if st.button("Calculate Solar System"):

    efficiency_factor = efficiency / 100

    # Solar panel size

    pv_size = energy / (
        sun_hours * efficiency_factor
    )


    # Battery size

    battery_capacity = (
        energy * days
    ) / (dod / 100)


    # Inverter size

    inverter_size = pv_size * 1.25


    st.subheader("Design Results")

    st.success(
        f"Solar Panel Size: {pv_size:.2f} kW"
    )

    st.success(
        f"Battery Capacity Required: "
        f"{battery_capacity:.2f} kWh"
    )

    st.success(
        f"Recommended Inverter Size: "
        f"{inverter_size:.2f} kW"
    )


st.caption(
    "Developed for renewable energy education and research"
)
