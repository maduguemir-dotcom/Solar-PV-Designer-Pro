import streamlit as st

from appliance_energy import (
    create_appliance_record,
    calculate_appliance_energy,
    calculate_appliance_contributions,
    calculate_total_energy_demand,
    analyze_appliance_load,
    calculate_category_summary,
    sort_appliances_by_energy
)


st.set_page_config(
    page_title="Appliance Energy Test",
    page_icon="🔌",
    layout="wide"
)


st.title("🔌 Appliance Energy Calculator")

st.write(
    """
    Test environment for the Solar PV Designer Pro V2.4
    appliance energy calculation engine.
    """
)


# ==========================================================
# TEST APPLIANCES
# ==========================================================

appliances = [

    create_appliance_record(
        name="Ceiling Fan",
        wattage=75,
        quantity=2,
        hours_per_day=8
    ),

    create_appliance_record(
        name="Television",
        wattage=120,
        quantity=1,
        hours_per_day=5
    ),

    create_appliance_record(
        name="Refrigerator",
        wattage=180,
        quantity=1,
        hours_per_day=10
    ),

    create_appliance_record(
        name="LED Bulb",
        wattage=12,
        quantity=6,
        hours_per_day=6
    )

]


# ==========================================================
# DISPLAY APPLIANCES
# ==========================================================

st.subheader("📋 Appliance Load")

st.dataframe(
    appliances,
    use_container_width=True
)


# ==========================================================
# CALCULATE APPLIANCE ENERGY
# ==========================================================

st.subheader("⚡ Appliance Energy Consumption")

energy_results = []

for appliance in appliances:

    try:

        energy = calculate_appliance_energy(
            appliance
        )

    except TypeError:

        try:

            energy = calculate_appliance_energy(
                wattage=appliance["wattage"],
                quantity=appliance["quantity"],
                hours_per_day=appliance["hours_per_day"]
            )

        except Exception as error:

            energy = None

            st.error(
                f"Could not calculate "
                f"{appliance.get('name', 'appliance')}: "
                f"{error}"
            )

    energy_results.append({

        "Appliance":
            appliance.get("name"),

        "Wattage (W)":
            appliance.get("wattage"),

        "Quantity":
            appliance.get("quantity"),

        "Hours/Day":
            appliance.get("hours_per_day"),

        "Daily Energy (kWh)":
            energy

    })


st.dataframe(
    energy_results,
    use_container_width=True
)


# ==========================================================
# TOTAL ENERGY DEMAND
# ==========================================================

st.subheader("🔋 Total Daily Energy Demand")

try:

    total_energy = calculate_total_energy_demand(
        appliances
    )

except Exception as error:

    st.error(
        f"Unable to calculate total energy demand: {error}"
    )

    total_energy = 0


st.metric(
    "Daily Energy Demand",
    f"{total_energy:.2f} kWh/day"
)


# ==========================================================
# MONTHLY ENERGY
# ==========================================================

monthly_energy = (
    total_energy * 30
)


st.metric(
    "Estimated Monthly Energy",
    f"{monthly_energy:.2f} kWh/month"
)


# ==========================================================
# APPLIANCE CONTRIBUTIONS
# ==========================================================

st.subheader("📊 Appliance Contributions")

try:

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    st.write(contributions)

except Exception as error:

    st.warning(
        f"Contribution analysis unavailable: {error}"
    )


# ==========================================================
# LOAD ANALYSIS
# ==========================================================

st.subheader("🔎 Appliance Load Analysis")

try:

    analysis = analyze_appliance_load(
        appliances
    )

    st.json(analysis)

except Exception as error:

    st.warning(
        f"Load analysis unavailable: {error}"
    )


# ==========================================================
# CATEGORY SUMMARY
# ==========================================================

st.subheader("📂 Category Summary")

try:

    category_summary = (
        calculate_category_summary(
            appliances
        )
    )

    st.write(category_summary)

except Exception as error:

    st.warning(
        f"Category analysis unavailable: {error}"
    )


# ==========================================================
# SORT BY ENERGY CONSUMPTION
# ==========================================================

st.subheader(
    "🏆 Appliances Ranked by Energy Consumption"
)

try:

    ranked = sort_appliances_by_energy(
        appliances
    )

    st.dataframe(
        ranked,
        use_container_width=True
    )

except Exception as error:

    st.warning(
        f"Ranking unavailable: {error}"
    )


# ==========================================================
# ENGINEERING APPLICATION
# ==========================================================

st.divider()

st.subheader(
    "☀️ Solar PV Design Application"
)

st.write(
    f"""
    The appliance load produces an estimated daily
    electrical energy requirement of:

    **{total_energy:.2f} kWh/day**

    This value can subsequently be passed directly
    into the Solar PV Designer Pro sizing engine for:

    - Solar PV capacity
    - Battery capacity
    - Inverter sizing
    - Charge controller sizing
    - System cost estimation
    - Carbon reduction estimation
    """
)


st.success(
    "✅ Appliance energy engine test completed."
)
