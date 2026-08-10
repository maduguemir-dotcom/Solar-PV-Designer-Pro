# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Appliance Energy Calculator - Version 2.4.0
# Developed by: Engr. Prof. Ibrahim Sani Madugu
# ==========================================================

"""Appliance-based daily energy-demand calculator for v2.4."""

DEFAULT_APPLIANCES = [
    {"Appliance": "LED Bulb", "Quantity": 6, "Wattage (W)": 10, "Hours/day": 6},
    {"Appliance": "Fan", "Quantity": 2, "Wattage (W)": 60, "Hours/day": 8},
    {"Appliance": "Television", "Quantity": 1, "Wattage (W)": 100, "Hours/day": 5},
    {"Appliance": "Refrigerator", "Quantity": 1, "Wattage (W)": 150, "Hours/day": 8},
]


def calculate_appliance_energy(quantity, wattage, hours_per_day):
    """Return daily energy in kWh for one appliance line."""
    try:
        return (
            max(float(quantity), 0.0)
            * max(float(wattage), 0.0)
            * max(float(hours_per_day), 0.0)
            / 1000.0
        )
    except (TypeError, ValueError):
        return 0.0


def calculate_daily_demand(appliances):
    """Return total daily energy demand in kWh/day."""
    return sum(
        calculate_appliance_energy(
            item.get("Quantity", 0),
            item.get("Wattage (W)", 0),
            item.get("Hours/day", 0),
        )
        for item in appliances or []
    )


def add_appliance_record(name, quantity, wattage, hours_per_day):
    """Create a normalized appliance record."""
    energy = calculate_appliance_energy(
        quantity,
        wattage,
        hours_per_day,
    )
    return {
        "Appliance": str(name).strip() or "Unnamed Appliance",
        "Quantity": float(quantity),
        "Wattage (W)": float(wattage),
        "Hours/day": float(hours_per_day),
        "Daily Energy (kWh)": energy,
    }


def display_appliance_calculator(st):
    """Render the appliance energy calculator.

    Returns:
        tuple(list_of_appliances, total_daily_kwh)
    """
    if "appliance_loads" not in st.session_state:
        st.session_state["appliance_loads"] = list(DEFAULT_APPLIANCES)

    appliances = st.session_state["appliance_loads"]

    st.subheader("🔌 Appliance Energy Demand Calculator")
    st.caption(
        "Enter the appliances used at the project site. "
        "The app calculates daily energy demand from quantity, "
        "wattage and daily operating hours."
    )

    with st.form("appliance_form", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)

        with c1:
            name = st.text_input(
                "Appliance",
                placeholder="e.g. Water Pump",
            )

        with c2:
            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1,
            )

        with c3:
            wattage = st.number_input(
                "Wattage (W)",
                min_value=1.0,
                value=100.0,
                step=10.0,
            )

        with c4:
            hours = st.number_input(
                "Hours/day",
                min_value=0.0,
                max_value=24.0,
                value=5.0,
                step=0.5,
            )

        add = st.form_submit_button(
            "➕ Add Appliance",
            use_container_width=True,
        )

    if add:
        if not name.strip():
            st.warning("Please enter the appliance name.")
        else:
            appliances.append(
                add_appliance_record(
                    name,
                    quantity,
                    wattage,
                    hours,
                )
            )
            st.session_state["appliance_loads"] = appliances
            st.success("Appliance added.")

    import pandas as pd

    if appliances:
        # Recalculate all rows in case a stored record came from an older version.
        for row in appliances:
            row["Daily Energy (kWh)"] = calculate_appliance_energy(
                row.get("Quantity", 0),
                row.get("Wattage (W)", 0),
                row.get("Hours/day", 0),
            )

        df = pd.DataFrame(appliances)

        st.markdown("#### 📋 Appliance Load Schedule")
        st.dataframe(df, use_container_width=True, hide_index=True)

        total = calculate_daily_demand(appliances)

        a, b, c = st.columns(3)
        a.metric("Daily Energy Demand", f"{total:.2f} kWh/day")
        b.metric("Monthly Estimate", f"{total * 30:.1f} kWh/month")
        c.metric("Annual Estimate", f"{total * 365:.0f} kWh/year")

        use_load = st.checkbox(
            "Use this calculated demand for PV sizing",
            value=False,
            key="use_appliance_demand",
        )

        if use_load:
            st.success(
                f"PV sizing demand set to {total:.2f} kWh/day."
            )

        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                "🗑️ Clear Appliance List",
                use_container_width=True,
                key="clear_appliance_loads",
            ):
                st.session_state["appliance_loads"] = []
                st.session_state["use_appliance_demand"] = False
                st.rerun()

        with c2:
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Appliance Schedule CSV",
                data=csv_data,
                file_name="solar_pv_appliance_schedule.csv",
                mime="text/csv",
                use_container_width=True,
            )

        return appliances, total

    st.info("No appliances have been added yet.")
    return [], 0.0
