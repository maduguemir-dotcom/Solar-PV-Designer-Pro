# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Appliance Energy Calculator Test
# Version: 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Test appliance energy-demand calculations for v2.4.
# ==========================================================

import streamlit as st

from appliance_energy import (
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_total_power,
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar PV Designer Pro - Appliance Energy Test",
    page_icon="🔌",
    layout="wide",
)


# ==========================================================
# HEADER
# ==========================================================

st.title("🔌 Appliance Energy Calculator Test")

st.write(
    """
    This test application verifies the appliance-energy
    calculation module for Solar PV Designer Pro Africa™ v2.4.
    """
)


# ==========================================================
# APPLIANCE INPUT
# ==========================================================

st.subheader("➕ Add Appliance")

col1, col2, col3, col4 = st.columns(4)

with col1:
    appliance_name = st.text_input(
        "Appliance Name",
        value="TV",
    )

with col2:
    wattage = st.number_input(
        "Wattage (W)",
        min_value=1.0,
        value=100.0,
        step=10.0,
    )

with col3:
    hours_per_day = st.number_input(
        "Hours / Day",
        min_value=0.0,
        max_value=24.0,
        value=5.0,
        step=0.5,
    )

with col4:
    quantity = st.number_input(
        "Quantity",
        min_value=1,
        value=1,
        step=1,
    )


# ==========================================================
# CALCULATE APPLIANCE
# ==========================================================

if st.button(
    "Calculate Appliance Energy",
    type="primary",
):

    try:

        result = calculate_appliance_energy(
            wattage=wattage,
            hours_per_day=hours_per_day,
            quantity=quantity,
        )

        st.success("✅ Appliance calculation successful.")

        result_col1, result_col2, result_col3 = st.columns(3)

        with result_col1:
            st.metric(
                "Appliance",
                appliance_name,
            )

        with result_col2:
            st.metric(
                "Total Power",
                f"{result['total_power_watts']:.0f} W",
            )

        with result_col3:
            st.metric(
                "Daily Energy",
                f"{result['daily_energy_kwh']:.2f} kWh",
            )

    except Exception as error:

        st.error(
            f"❌ Appliance calculation failed: {error}"
        )


# ==========================================================
# SAMPLE APPLIANCES
# ==========================================================

st.divider()

st.subheader("📋 Sample Appliance Load")

sample_appliances = [

    {
        "name": "TV",
        "wattage": 100,
        "hours_per_day": 5,
        "quantity": 1,
    },

    {
        "name": "Ceiling Fan",
        "wattage": 75,
        "hours_per_day": 8,
        "quantity": 2,
    },

    {
        "name": "Refrigerator",
        "wattage": 150,
        "hours_per_day": 10,
        "quantity": 1,
    },

    {
        "name": "LED Bulb",
        "wattage": 10,
        "hours_per_day": 6,
        "quantity": 6,
    },

    {
        "name": "Laptop",
        "wattage": 65,
        "hours_per_day": 6,
        "quantity": 1,
    },
]


# ==========================================================
# DISPLAY SAMPLE CALCULATIONS
# ==========================================================

sample_results = []

for appliance in sample_appliances:

    try:

        result = calculate_appliance_energy(
            wattage=appliance["wattage"],
            hours_per_day=appliance["hours_per_day"],
            quantity=appliance["quantity"],
        )

        sample_results.append(
            {
                "Appliance": appliance["name"],
                "Quantity": appliance["quantity"],
                "Wattage (W)": appliance["wattage"],
                "Hours / Day": appliance["hours_per_day"],
                "Total Power (W)": result["total_power_watts"],
                "Daily Energy (kWh)": result["daily_energy_kwh"],
            }
        )

    except Exception as error:

        st.error(
            f"Error calculating {appliance['name']}: {error}"
        )


if sample_results:

    st.dataframe(
        sample_results,
        use_container_width=True,
    )


# ==========================================================
# TOTAL DAILY ENERGY
# ==========================================================

st.divider()

st.subheader("⚡ Total Energy Demand")

try:

    total_energy = calculate_total_daily_energy(
        sample_appliances
    )

    total_power = calculate_total_power(
        sample_appliances
    )

    total_col1, total_col2 = st.columns(2)

    with total_col1:

        st.metric(
            "Total Connected Load",
            f"{total_power:.0f} W",
        )

    with total_col2:

        st.metric(
            "Total Daily Energy Demand",
            f"{total_energy:.2f} kWh/day",
        )

    st.success(
        f"✅ Calculated daily energy demand: "
        f"{total_energy:.2f} kWh/day"
    )

except Exception as error:

    st.error(
        f"❌ Total energy calculation failed: {error}"
    )


# ==========================================================
# FORMULA
# ==========================================================

st.divider()

st.subheader("📐 Calculation Formula")

st.write(
    """
    **Daily Energy (kWh/day)**

    Daily Energy =
    Appliance Wattage × Quantity × Hours Used ÷ 1000

    This calculation provides the preliminary daily
    electrical energy demand that can subsequently be
    supplied to the Solar PV Designer Pro sizing engine.
    """
)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.4.0

    Appliance Energy Calculator Test

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
)
