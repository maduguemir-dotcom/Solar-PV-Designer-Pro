import streamlit as st

from appliance_energy import (
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_monthly_energy,
    calculate_appliance_summary
)


st.set_page_config(
    page_title="Appliance Energy Test",
    page_icon="🔌",
    layout="wide"
)


st.title("🔌 Appliance Energy Calculator Test")

st.write(
    """
    This test demonstrates the appliance-energy calculation
    engine before it is integrated into Solar PV Designer Pro.
    """
)


# ==========================================================
# TEST APPLIANCES
# ==========================================================

appliances = [

    {
        "name": "Ceiling Fan",
        "wattage": 75,
        "quantity": 2,
        "hours_per_day": 8
    },

    {
        "name": "Television",
        "wattage": 120,
        "quantity": 1,
        "hours_per_day": 5
    },

    {
        "name": "Refrigerator",
        "wattage": 180,
        "quantity": 1,
        "hours_per_day": 10
    },

    {
        "name": "LED Bulb",
        "wattage": 12,
        "quantity": 6,
        "hours_per_day": 6
    }

]


# ==========================================================
# DISPLAY INPUT DATA
# ==========================================================

st.subheader("📋 Test Appliance List")

st.dataframe(
    appliances,
    use_container_width=True
)


# ==========================================================
# CALCULATE EACH APPLIANCE
# ==========================================================

results = []


for appliance in appliances:

    energy = calculate_appliance_energy(

        wattage=appliance["wattage"],

        quantity=appliance["quantity"],

        hours_per_day=appliance["hours_per_day"]

    )

    results.append({

        "Appliance":
            appliance["name"],

        "Wattage (W)":
            appliance["wattage"],

        "Quantity":
            appliance["quantity"],

        "Hours/Day":
            appliance["hours_per_day"],

        "Daily Energy (kWh)":
            energy

    })


# ==========================================================
# RESULTS
# ==========================================================

st.subheader("⚡ Daily Appliance Energy")

st.dataframe(
    results,
    use_container_width=True
)


# ==========================================================
# TOTAL DAILY ENERGY
# ==========================================================

total_daily_energy = calculate_total_daily_energy(
    results
)


st.metric(
    "Total Daily Energy Demand",
    f"{total_daily_energy:.2f} kWh/day"
)


# ==========================================================
# MONTHLY ENERGY
# ==========================================================

monthly_energy = calculate_monthly_energy(
    total_daily_energy
)


st.metric(
    "Estimated Monthly Energy",
    f"{monthly_energy:.2f} kWh/month"
)


# ==========================================================
# SUMMARY
# ==========================================================

summary = calculate_appliance_summary(
    results
)


st.subheader("📊 Appliance Energy Summary")

st.json(summary)


# ==========================================================
# ENGINEERING INTERPRETATION
# ==========================================================

st.subheader("🔎 Engineering Interpretation")

st.write(
    f"""
    The appliances in this test consume approximately

    **{total_daily_energy:.2f} kWh/day**

    of electrical energy.

    The estimated monthly consumption is approximately

    **{monthly_energy:.2f} kWh/month**.

    This value can later be used automatically by
    Solar PV Designer Pro to determine the required:

    - ☀️ Solar PV capacity
    - 🔋 Battery capacity
    - 🔌 Inverter capacity
    - ⚡ Charge controller
    - 💰 System cost
    """
)
