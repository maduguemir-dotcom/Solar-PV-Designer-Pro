# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Appliance Energy Module Test
# Version: 2.4.0
#
# ==========================================================

import streamlit as st

from appliance_energy import (
    calculate_appliance_energy,
    calculate_total_energy,
    calculate_appliance_contributions,
    sort_appliances_by_energy,
    analyze_appliance_energy,
    get_daily_energy_demand,
    get_default_appliances,
    get_default_appliance,
    format_energy_summary
)


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Appliance Energy Test",
    page_icon="⚡",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "⚡ Appliance Energy Calculator Test"
)

st.subheader(
    "Solar PV Designer Pro Africa™ v2.4"
)

st.write(
    """
    This page tests the appliance-energy calculation
    engine before it is integrated into the main
    Solar PV Designer Pro dashboard.
    """
)


# ==========================================================
# TEST 1 - SINGLE APPLIANCE
# ==========================================================

st.header(
    "1️⃣ Single Appliance Test"
)

single = calculate_appliance_energy(
    name="Television",
    quantity=1,
    wattage=100,
    hours_per_day=5
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Daily Energy",
    f"{single['daily_kwh']:.2f} kWh"
)

col2.metric(
    "Daily Energy",
    f"{single['daily_wh']:.0f} Wh"
)

col3.metric(
    "Monthly Energy",
    f"{single['monthly_kwh']:.2f} kWh"
)

st.json(
    single
)


# ==========================================================
# TEST 2 - MULTIPLE APPLIANCES
# ==========================================================

st.header(
    "2️⃣ Multiple Appliance Test"
)

appliances = []


appliances.append(
    calculate_appliance_energy(
        name="LED Lights",
        quantity=10,
        wattage=10,
        hours_per_day=6
    )
)


appliances.append(
    calculate_appliance_energy(
        name="Television",
        quantity=1,
        wattage=100,
        hours_per_day=5
    )
)


appliances.append(
    calculate_appliance_energy(
        name="Ceiling Fans",
        quantity=3,
        wattage=60,
        hours_per_day=8
    )
)


appliances.append(
    calculate_appliance_energy(
        name="Refrigerator",
        quantity=1,
        wattage=150,
        hours_per_day=10
    )
)


appliances.append(
    calculate_appliance_energy(
        name="Laptop",
        quantity=2,
        wattage=65,
        hours_per_day=6
    )
)


st.dataframe(
    appliances,
    use_container_width=True
)


# ==========================================================
# TEST 3 - TOTAL ENERGY
# ==========================================================

st.header(
    "3️⃣ Total Energy Demand"
)

totals = calculate_total_energy(
    appliances
)

col1, col2, col3 = st.columns(3)

col1.metric(
    "Daily Energy",
    f"{totals['total_daily_kwh']:.2f} kWh/day"
)

col2.metric(
    "Daily Energy",
    f"{totals['total_daily_wh']:.0f} Wh/day"
)

col3.metric(
    "Monthly Energy",
    f"{totals['total_monthly_kwh']:.2f} kWh/month"
)


# ==========================================================
# TEST 4 - CONTRIBUTIONS
# ==========================================================

st.header(
    "4️⃣ Appliance Contribution"
)

contributions = (
    calculate_appliance_contributions(
        appliances
    )
)

st.dataframe(
    contributions,
    use_container_width=True
)


# ==========================================================
# TEST 5 - SORTING
# ==========================================================

st.header(
    "5️⃣ Appliances Ranked by Energy Consumption"
)

sorted_appliances = (
    sort_appliances_by_energy(
        appliances
    )
)

st.dataframe(
    sorted_appliances,
    use_container_width=True
)


# ==========================================================
# TEST 6 - COMPLETE ANALYSIS
# ==========================================================

st.header(
    "6️⃣ Complete Energy Analysis"
)

analysis = analyze_appliance_energy(
    appliances
)

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Appliances",
    analysis[
        "number_of_appliances"
    ]
)

col2.metric(
    "Daily Demand",
    f"{analysis['total_daily_kwh']:.2f} kWh"
)

col3.metric(
    "Monthly Demand",
    f"{analysis['total_monthly_kwh']:.2f} kWh"
)

if analysis[
    "highest_consumer"
]:

    col4.metric(
        "Largest Consumer",
        analysis[
            "highest_consumer"
        ]["name"]
    )

else:

    col4.metric(
        "Largest Consumer",
        "None"
    )


# ==========================================================
# TEST 7 - PV SIZING INPUT
# ==========================================================

st.header(
    "7️⃣ PV Sizing Energy Input"
)

daily_demand = get_daily_energy_demand(
    appliances
)

st.success(
    f"""
    Calculated daily energy demand:

    **{daily_demand:.2f} kWh/day**

    This value can be passed directly to the
    existing Solar PV sizing engine.
    """
)


# ==========================================================
# TEST 8 - DEFAULT APPLIANCE LIBRARY
# ==========================================================

st.header(
    "8️⃣ Default Appliance Library"
)

default_appliances = (
    get_default_appliances()
)

st.dataframe(
    default_appliances,
    use_container_width=True
)


# ==========================================================
# TEST 9 - FIND APPLIANCE
# ==========================================================

st.header(
    "9️⃣ Appliance Lookup"
)

selected_appliance = get_default_appliance(
    "Refrigerator"
)

if selected_appliance:

    st.success(
        f"""
        Refrigerator default wattage:

        **{selected_appliance['default_wattage']} W**
        """
    )

else:

    st.warning(
        "Appliance not found."
    )


# ==========================================================
# TEST 10 - SUMMARY
# ==========================================================

st.header(
    "🔟 Energy Summary"
)

summary = format_energy_summary(
    appliances
)

summary_col1, summary_col2 = st.columns(2)

with summary_col1:

    st.write(
        f"""
        **Number of appliances:**
        {summary['number_of_appliances']}

        **Daily energy demand:**
        {summary['total_daily_kwh']:.2f} kWh/day

        **Monthly energy demand:**
        {summary['total_monthly_kwh']:.2f} kWh/month
        """
    )

with summary_col2:

    st.write(
        f"""
        **Largest energy consumer:**

        {summary['highest_consumer']}
        """
    )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.4

    Appliance Energy Calculation Engine

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
