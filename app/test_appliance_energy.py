# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Appliance Energy Test
# Version: 2.4.0
#
# ==========================================================

import streamlit as st

from appliance_energy import (
    create_appliance,
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_total_monthly_energy,
    calculate_total_connected_load,
    create_energy_summary
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Appliance Energy Test",
    page_icon="🔌",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "🔌 Appliance Energy Calculator"
)

st.subheader(
    "Solar PV Designer Pro Africa™ — v2.4"
)

st.write(
    """
    This test demonstrates how appliance wattage,
    quantity and daily operating hours are converted
    into electricity demand.
    """
)


# ==========================================================
# TEST APPLIANCES
# ==========================================================

appliances = [

    create_appliance(
        name="LED Lights",
        wattage=20,
        hours_per_day=6,
        quantity=5
    ),

    create_appliance(
        name="Television",
        wattage=100,
        hours_per_day=5,
        quantity=1
    ),

    create_appliance(
        name="Standing Fan",
        wattage=75,
        hours_per_day=8,
        quantity=2
    ),

    create_appliance(
        name="Refrigerator",
        wattage=150,
        hours_per_day=10,
        quantity=1
    ),

    create_appliance(
        name="Laptop",
        wattage=65,
        hours_per_day=6,
        quantity=1
    )

]


# ==========================================================
# CALCULATE APPLIANCE RESULTS
# ==========================================================

rows = []

for appliance in appliances:

    daily_energy = (
        calculate_appliance_energy(
            appliance
        )
    )

    load = (
        appliance["wattage"]
        *
        appliance["quantity"]
    )

    rows.append({

        "Appliance":
            appliance["name"],

        "Quantity":
            appliance["quantity"],

        "Power (W)":
            appliance["wattage"],

        "Hours/Day":
            appliance["hours_per_day"],

        "Connected Load (W)":
            load,

        "Daily Energy (kWh)":
            round(
                daily_energy,
                3
            )

    })


# ==========================================================
# DISPLAY TABLE
# ==========================================================

st.header(
    "📋 Appliance Energy Schedule"
)

st.dataframe(
    rows,
    use_container_width=True,
    hide_index=True
)


# ==========================================================
# SUMMARY
# ==========================================================

summary = create_energy_summary(
    appliances
)


daily_energy = (
    summary[
        "daily_energy_kwh"
    ]
)

monthly_energy = (
    summary[
        "monthly_energy_kwh"
    ]
)

connected_load = (
    summary[
        "connected_load_w"
    ]
)


# ==========================================================
# METRICS
# ==========================================================

st.divider()

st.header(
    "📊 Energy Demand Summary"
)

col1, col2, col3 = st.columns(3)


col1.metric(
    "Daily Energy",
    f"{daily_energy:.2f} kWh/day"
)

col2.metric(
    "Monthly Energy",
    f"{monthly_energy:.2f} kWh/month"
)

col3.metric(
    "Connected Load",
    f"{connected_load:.0f} W"
)


# ==========================================================
# ENGINEERING TEST
# ==========================================================

st.divider()

st.header(
    "🧪 Test Status"
)


if daily_energy > 0:

    st.success(
        "✅ Appliance Energy Module is working correctly."
    )

else:

    st.error(
        "❌ Appliance Energy Module returned zero energy."
    )


# ==========================================================
# FORMULA
# ==========================================================

st.info(
    """
    **Energy calculation**

    Daily Energy (kWh/day) =
    Wattage × Quantity × Hours per Day ÷ 1000
    """
)


# ==========================================================
# RAW DATA
# ==========================================================

with st.expander(
    "🔧 View Raw Appliance Data"
):

    st.json(
        appliances
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.4.0

    Appliance Energy Module

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
