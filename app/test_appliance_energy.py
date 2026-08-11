# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Appliance Energy Calculator
# Version: 2.4.1
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
# ==========================================================

"""
Appliance-based daily energy-demand calculator for
Solar PV Designer Pro Africa™ v2.4.

Functions provided:

1. calculate_appliance_energy()
2. calculate_daily_demand()
3. calculate_total_daily_energy()
4. calculate_total_power()
5. add_appliance_record()
6. display_appliance_calculator()
"""

# ==========================================================
# SECTION 1 - DEFAULT APPLIANCES
# ==========================================================

DEFAULT_APPLIANCES = [
    {
        "Appliance": "LED Bulb",
        "Quantity": 6,
        "Wattage (W)": 10,
        "Hours/day": 6,
    },
    {
        "Appliance": "Fan",
        "Quantity": 2,
        "Wattage (W)": 60,
        "Hours/day": 8,
    },
    {
        "Appliance": "Television",
        "Quantity": 1,
        "Wattage (W)": 100,
        "Hours/day": 5,
    },
    {
        "Appliance": "Refrigerator",
        "Quantity": 1,
        "Wattage (W)": 150,
        "Hours/day": 8,
    },
]


# ==========================================================
# SECTION 2 - SAFE NUMBER CONVERSION
# ==========================================================

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """

    try:
        return float(value)

    except (TypeError, ValueError):
        return default


# ==========================================================
# SECTION 3 - SINGLE APPLIANCE ENERGY
# ==========================================================

def calculate_appliance_energy(
    quantity,
    wattage,
    hours_per_day,
):
    """
    Calculate daily energy consumption for one
    appliance category.

    Formula:

        Energy (kWh/day)
        =
        Quantity × Wattage × Hours/day ÷ 1000
    """

    quantity = max(
        safe_float(quantity),
        0.0,
    )

    wattage = max(
        safe_float(wattage),
        0.0,
    )

    hours_per_day = max(
        safe_float(hours_per_day),
        0.0,
    )

    total_power_watts = (
        quantity
        * wattage
    )

    daily_energy_kwh = (
        total_power_watts
        * hours_per_day
        / 1000.0
    )

    return {
        "quantity": quantity,
        "wattage": wattage,
        "hours_per_day": hours_per_day,
        "total_power_watts": total_power_watts,
        "daily_energy_kwh": daily_energy_kwh,
    }


# ==========================================================
# SECTION 4 - TOTAL DAILY ENERGY
# ==========================================================

def calculate_total_daily_energy(appliances):
    """
    Calculate total daily energy demand from
    a list of appliances.

    Returns:
        kWh/day
    """

    if not appliances:
        return 0.0

    total_energy = 0.0

    for appliance in appliances:

        result = calculate_appliance_energy(
            quantity=appliance.get(
                "quantity",
                appliance.get(
                    "Quantity",
                    0,
                ),
            ),
            wattage=appliance.get(
                "wattage",
                appliance.get(
                    "Wattage (W)",
                    0,
                ),
            ),
            hours_per_day=appliance.get(
                "hours_per_day",
                appliance.get(
                    "Hours/day",
                    0,
                ),
            ),
        )

        total_energy += result[
            "daily_energy_kwh"
        ]

    return total_energy


# ==========================================================
# SECTION 5 - TOTAL CONNECTED POWER
# ==========================================================

def calculate_total_power(appliances):
    """
    Calculate total connected appliance load.

    Returns:
        Watts
    """

    if not appliances:
        return 0.0

    total_power = 0.0

    for appliance in appliances:

        result = calculate_appliance_energy(
            quantity=appliance.get(
                "quantity",
                appliance.get(
                    "Quantity",
                    0,
                ),
            ),
            wattage=appliance.get(
                "wattage",
                appliance.get(
                    "Wattage (W)",
                    0,
                ),
            ),
            hours_per_day=appliance.get(
                "hours_per_day",
                appliance.get(
                    "Hours/day",
                    0,
                ),
            ),
        )

        total_power += result[
            "total_power_watts"
        ]

    return total_power


# ==========================================================
# SECTION 6 - DAILY DEMAND ALIAS
# ==========================================================

def calculate_daily_demand(appliances):
    """
    Backward-compatible alias for total daily energy.

    Returns:
        kWh/day
    """

    return calculate_total_daily_energy(
        appliances
    )


# ==========================================================
# SECTION 7 - CREATE APPLIANCE RECORD
# ==========================================================

def add_appliance_record(
    name,
    quantity,
    wattage,
    hours_per_day,
):
    """
    Create a normalized appliance record.
    """

    quantity = max(
        safe_float(quantity),
        0.0,
    )

    wattage = max(
        safe_float(wattage),
        0.0,
    )

    hours_per_day = max(
        safe_float(hours_per_day),
        0.0,
    )

    result = calculate_appliance_energy(
        quantity=quantity,
        wattage=wattage,
        hours_per_day=hours_per_day,
    )

    return {
        "Appliance":
            str(name).strip()
            or "Unnamed Appliance",

        "Quantity":
            quantity,

        "Wattage (W)":
            wattage,

        "Hours/day":
            hours_per_day,

        "Daily Energy (kWh)":
            result[
                "daily_energy_kwh"
            ],
    }


# ==========================================================
# SECTION 8 - STREAMLIT APPLIANCE CALCULATOR
# ==========================================================

def display_appliance_calculator(st):
    """
    Display the interactive appliance calculator.

    Returns:

        appliances,
        total_daily_energy
    """

    # ------------------------------------------------------
    # Initialize session state
    # ------------------------------------------------------

    if "appliance_loads" not in st.session_state:

        st.session_state[
            "appliance_loads"
        ] = [
            dict(item)
            for item in DEFAULT_APPLIANCES
        ]

    appliances = (
        st.session_state[
            "appliance_loads"
        ]
    )

    # ------------------------------------------------------
    # Header
    # ------------------------------------------------------

    st.subheader(
        "🔌 Appliance Energy Demand Calculator"
    )

    st.caption(
        """
        Enter the appliances used at the project site.
        The system calculates daily energy demand from
        appliance quantity, wattage and operating hours.
        """
    )

    # ------------------------------------------------------
    # Add appliance form
    # ------------------------------------------------------

    with st.form(
        "appliance_form",
        clear_on_submit=True,
    ):

        col1, col2, col3, col4 = (
            st.columns(4)
        )

        with col1:

            name = st.text_input(
                "Appliance",
                placeholder="e.g. Water Pump",
            )

        with col2:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                step=1,
            )

        with col3:

            wattage = st.number_input(
                "Wattage (W)",
                min_value=1.0,
                value=100.0,
                step=10.0,
            )

        with col4:

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

    # ------------------------------------------------------
    # Add appliance
    # ------------------------------------------------------

    if add:

        if not name.strip():

            st.warning(
                "Please enter the appliance name."
            )

        else:

            appliances.append(
                add_appliance_record(
                    name=name,
                    quantity=quantity,
                    wattage=wattage,
                    hours_per_day=hours,
                )
            )

            st.session_state[
                "appliance_loads"
            ] = appliances

            st.success(
                f"✅ {name} added successfully."
            )

    # ------------------------------------------------------
    # Recalculate stored records
    # ------------------------------------------------------

    for row in appliances:

        row[
            "Daily Energy (kWh)"
        ] = calculate_appliance_energy(

            quantity=row.get(
                "Quantity",
                0,
            ),

            wattage=row.get(
                "Wattage (W)",
                0,
            ),

            hours_per_day=row.get(
                "Hours/day",
                0,
            ),
        )[
            "daily_energy_kwh"
        ]

    # ------------------------------------------------------
    # Display table
    # ------------------------------------------------------

    if appliances:

        import pandas as pd

        dataframe = pd.DataFrame(
            appliances
        )

        st.markdown(
            "#### 📋 Appliance Load Schedule"
        )

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True,
        )

        # --------------------------------------------------
        # Totals
        # --------------------------------------------------

        total_energy = (
            calculate_total_daily_energy(
                appliances
            )
        )

        total_power = (
            calculate_total_power(
                appliances
            )
        )

        col1, col2, col3 = (
            st.columns(3)
        )

        col1.metric(
            "Connected Load",
            f"{total_power:.0f} W",
        )

        col2.metric(
            "Daily Energy Demand",
            f"{total_energy:.2f} kWh/day",
        )

        col3.metric(
            "Monthly Estimate",
            f"{total_energy * 30:.1f} kWh/month",
        )

        st.metric(
            "Annual Estimate",
            f"{total_energy * 365:.0f} kWh/year",
        )

        # --------------------------------------------------
        # Use demand for PV sizing
        # --------------------------------------------------

        use_load = st.checkbox(
            "Use this calculated demand for PV sizing",
            value=False,
            key="use_appliance_demand",
        )

        if use_load:

            st.success(
                f"""
                PV sizing demand set to
                {total_energy:.2f} kWh/day.
                """
            )

        # --------------------------------------------------
        # Controls
        # --------------------------------------------------

        col1, col2 = (
            st.columns(2)
        )

        with col1:

            if st.button(
                "🗑️ Clear Appliance List",
                use_container_width=True,
                key="clear_appliance_loads",
            ):

                st.session_state[
                    "appliance_loads"
                ] = []

                st.session_state[
                    "use_appliance_demand"
                ] = False

                st.rerun()

        with col2:

            csv_data = (
                dataframe
                .to_csv(
                    index=False
                )
                .encode("utf-8")
            )

            st.download_button(
                "📥 Download Appliance Schedule CSV",
                data=csv_data,
                file_name=(
                    "solar_pv_appliance_schedule.csv"
                ),
                mime="text/csv",
                use_container_width=True,
            )

        return (
            appliances,
            total_energy,
        )

    # ------------------------------------------------------
    # Empty state
    # ------------------------------------------------------

    st.info(
        "No appliances have been added yet."
    )

    return (
        [],
        0.0,
    )
