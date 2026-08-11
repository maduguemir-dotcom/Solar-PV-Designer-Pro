# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Appliance Energy Test Module
# Version: 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Test appliance energy calculations before integration
# into the main Solar PV Designer Pro dashboard.
#
# ==========================================================

import streamlit as st

from appliance_energy import (
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_total_monthly_energy,
    create_appliance
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
    "🔌 Appliance Energy Calculator — Test"
)

st.subheader(
    "Solar PV Designer Pro Africa™ v2.4"
)

st.write(
    """
    This test application demonstrates how household and
    commercial appliances can be used to calculate daily
    electricity demand.
    """
)


# ==========================================================
# SECTION 1 - TEST APPLIANCES
# ==========================================================

st.header("📋 Test Appliance Load")


test_appliances = [

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
# SECTION 2 - CALCULATE INDIVIDUAL APPLIANCES
# ==========================================================

results = []


for appliance in test_appliances:

    energy = calculate_appliance_energy(
        appliance
    )

    results.append({

        "Appliance":
            appliance["name"],

        "Quantity":
            appliance["quantity"],

        "Power (W)":
            appliance["wattage"],

        "Hours/Day":
            appliance["hours_per_day"],

        "Daily Energy (kWh)":
            energy

    })


# ==========================================================
# SECTION 3 - DISPLAY TABLE
# ==========================================================

st.dataframe(
    results,
    use_container_width=True
)


# ==========================================================
# SECTION 4 - TOTAL DAILY ENERGY
# ==========================================================

total_daily_energy = (
    calculate_total_daily_energy(
        test_appliances
    )
)


# ==========================================================
# SECTION 5 - TOTAL MONTHLY ENERGY
# ==========================================================

total_monthly_energy = (
    calculate_total_monthly_energy(
        test_appliances
    )
)


# ==========================================================
# SECTION 6 - RESULTS
# ==========================================================

st.divider()

st.header(
    "📊 Energy Demand Results"
)


result_col1, result_col2 = st.columns(2)


result_col1.metric(
    "Daily Energy Demand",
    f"{total_daily_energy:.2f} kWh/day"
)


result_col2.metric(
    "Monthly Energy Demand",
    f"{total_monthly_energy:.2f} kWh/month"
)


# ==========================================================
# SECTION 7 - ENGINEERING CHECK
# ==========================================================

st.divider()

st.header(
    "🧪 Engineering Test"
)


if total_daily_energy > 0:

    st.success(
        "✅ Appliance energy calculation is working correctly."
    )

    st.write(
        f"""
        The test appliance group produces an estimated
        daily energy demand of:

        **{total_daily_energy:.2f} kWh/day**

        This value can now be passed to the Solar PV
        sizing engine.
        """
    )

else:

    st.error(
        "❌ Appliance energy calculation returned zero."
    )


# ==========================================================
# SECTION 8 - DEBUG INFORMATION
# ==========================================================

with st.expander(
    "🔧 View Raw Test Data"
):

    st.write(
        test_appliances
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.4.0

    Appliance Energy Module Test

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
