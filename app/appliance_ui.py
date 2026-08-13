# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Appliance Energy Designer UI
# Version 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
# ==========================================================

import streamlit as st

from appliance_energy import (
    DEFAULT_APPLIANCES,
    analyze_appliance_load,
    calculate_appliance_energy,
    calculate_category_summary,
    calculate_total_energy_demand,
    get_appliance_names,
    get_default_appliance,
)


# ==========================================================
# SECTION 1 - SAFE NUMBER CONVERSION
# ==========================================================

def safe_float(value, default=0.0):
    """Safely convert a value to float."""

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


# ==========================================================
# SECTION 2 - APPLIANCE SESSION STATE
# ==========================================================

def initialize_appliance_state():
    """
    Initialize persistent appliance list in Streamlit
    session state.
    """

    if "appliance_loads" not in st.session_state:
        st.session_state["appliance_loads"] = []


# ==========================================================
# SECTION 3 - DEFAULT APPLIANCE INFORMATION
# ==========================================================

def get_appliance_options():
    """
    Return available appliance names.

    Supports both dictionary-based and list-based
    DEFAULT_APPLIANCES structures.
    """

    try:
        names = get_appliance_names()

        if names:
            return list(names)

    except Exception:
        pass

    try:
        if isinstance(DEFAULT_APPLIANCES, dict):
            return list(DEFAULT_APPLIANCES.keys())

        if isinstance(DEFAULT_APPLIANCES, list):
            return [
                item.get("name")
                for item in DEFAULT_APPLIANCES
                if isinstance(item, dict)
                and item.get("name")
            ]

    except Exception:
        pass

    return []


# ==========================================================
# SECTION 4 - GET DEFAULT APPLIANCE DATA
# ==========================================================

def get_appliance_defaults(appliance_name):
    """
    Retrieve default information for an appliance.
    """

    try:
        result = get_default_appliance(appliance_name)

        if isinstance(result, dict):
            return result

    except Exception:
        pass

    try:

        if isinstance(DEFAULT_APPLIANCES, dict):

            result = DEFAULT_APPLIANCES.get(
                appliance_name
            )

            if isinstance(result, dict):
                return result

        elif isinstance(DEFAULT_APPLIANCES, list):

            for item in DEFAULT_APPLIANCES:

                if (
                    isinstance(item, dict)
                    and item.get("name") == appliance_name
                ):

                    return item

    except Exception:
        pass

    return {}


# ==========================================================
# SECTION 5 - CALCULATE ENERGY
# ==========================================================

def calculate_record_energy(record):
    """
    Calculate daily energy for one appliance.

    Energy = quantity × wattage × hours / 1000
    """

    quantity = safe_float(
        record.get("quantity", 1)
    )

    wattage = safe_float(
        record.get("wattage", 0)
    )

    hours = safe_float(
        record.get("hours_per_day", 0)
    )

    return (
        quantity
        * wattage
        * hours
        / 1000
    )


# ==========================================================
# SECTION 6 - ADD APPLIANCE
# ==========================================================

def add_appliance(
    name,
    category,
    quantity,
    wattage,
    hours
):
    """
    Add an appliance to the current load profile.
    """

    energy = calculate_record_energy(
        {
            "quantity": quantity,
            "wattage": wattage,
            "hours_per_day": hours
        }
    )

    record = {

        "name": name,

        "category": category,

        "quantity": quantity,

        "wattage": wattage,

        "hours_per_day": hours,

        "daily_energy": energy
    }

    st.session_state[
        "appliance_loads"
    ].append(record)


# ==========================================================
# SECTION 7 - REMOVE APPLIANCE
# ==========================================================

def remove_appliance(index):
    """Remove appliance by index."""

    if (
        0 <= index
        < len(
            st.session_state[
                "appliance_loads"
            ]
        )
    ):

        st.session_state[
            "appliance_loads"
        ].pop(index)


# ==========================================================
# SECTION 8 - APPLIANCE ENERGY DESIGNER
# ==========================================================

def render_appliance_energy_designer():
    """
    Render the complete Appliance Energy Designer.

    Returns:
        total daily energy demand in kWh/day
    """

    initialize_appliance_state()

    st.header(
        "🔌 Appliance Energy Designer"
    )

    st.write(
        """
        Build your electrical load profile by entering
        the appliances used in the project. Solar PV
        Designer Pro will calculate the daily energy
        demand automatically.
        """
    )

    # ======================================================
    # ADD APPLIANCE
    # ======================================================

    st.subheader(
        "➕ Add Appliance"
    )

    appliance_options = get_appliance_options()

    if appliance_options:

        appliance_selection = st.selectbox(
            "Appliance",
            appliance_options,
            key="v24_appliance_selection"
        )

    else:

        appliance_selection = "Custom Appliance"

    custom_appliance = st.text_input(
        "Custom appliance name",
        value="",
        placeholder="Example: Water Pump",
        key="v24_custom_appliance"
    )

    if custom_appliance.strip():

        appliance_name = (
            custom_appliance.strip()
        )

    else:

        appliance_name = appliance_selection

    defaults = get_appliance_defaults(
        appliance_selection
    )

    default_category = defaults.get(
        "category",
        "Other"
    )

    default_wattage = safe_float(
        defaults.get(
            "wattage",
            100
        ),
        100
    )

    default_hours = safe_float(
        defaults.get(
            "hours_per_day",
            5
        ),
        5
    )

    default_quantity = safe_float(
        defaults.get(
            "quantity",
            1
        ),
        1
    )

    category_options = [
        "Lighting",
        "Entertainment",
        "Cooling",
        "Kitchen",
        "Water Pumping",
        "Office",
        "Communication",
        "Security",
        "Other"
    ]

    category_default_index = 0

    if default_category in category_options:

        category_default_index = (
            category_options.index(
                default_category
            )
        )

    category = st.selectbox(
        "Category",
        category_options,
        index=category_default_index,
        key="v24_appliance_category"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        quantity = st.number_input(
            "Quantity",
            min_value=1.0,
            value=max(
                1.0,
                default_quantity
            ),
            step=1.0,
            key="v24_appliance_quantity"
        )

    with col2:

        wattage = st.number_input(
            "Power Rating (W)",
            min_value=0.0,
            value=max(
                0.0,
                default_wattage
            ),
            step=10.0,
            key="v24_appliance_wattage"
        )

    with col3:

        hours = st.number_input(
            "Hours Used / Day",
            min_value=0.0,
            max_value=24.0,
            value=min(
                24.0,
                max(
                    0.0,
                    default_hours
                )
            ),
            step=0.5,
            key="v24_appliance_hours"
        )

    estimated_energy = (
        quantity
        * wattage
        * hours
        / 1000
    )

    st.info(
        f"""
        **Estimated Daily Energy:**
        {estimated_energy:.2f} kWh/day
        """
    )

    if st.button(
        "➕ Add Appliance to Load Profile",
        type="primary",
        use_container_width=True,
        key="v24_add_appliance"
    ):

        add_appliance(
            name=appliance_name,
            category=category,
            quantity=quantity,
            wattage=wattage,
            hours=hours
        )

        st.success(
            f"{appliance_name} added successfully."
        )

        st.rerun()

    # ======================================================
    # CURRENT LOAD PROFILE
    # ======================================================

    st.divider()

    st.subheader(
        "📋 Current Appliance Load Profile"
    )

    loads = st.session_state[
        "appliance_loads"
    ]

    if not loads:

        st.info(
            """
            No appliances have been added yet.

            Add appliances above to build the
            project's energy-demand profile.
            """
        )

        return 0.0

    # ======================================================
    # DISPLAY APPLIANCES
    # ======================================================

    for index, appliance in enumerate(
        loads
    ):

        energy = calculate_record_energy(
            appliance
        )

        appliance[
            "daily_energy"
        ] = energy

        col1, col2, col3, col4, col5, col6 = (
            st.columns(
                [2, 1.5, 1, 1.2, 1.2, 0.8]
            )
        )

        with col1:

            st.write(
                f"**{appliance['name']}**"
            )

            st.caption(
                appliance["category"]
            )

        with col2:

            st.write(
                f"{appliance['quantity']:.0f} × "
                f"{appliance['wattage']:.0f} W"
            )

        with col3:

            st.write(
                f"{appliance['hours_per_day']:.1f} h"
            )

        with col4:

            st.write(
                f"{energy:.2f} kWh"
            )

        with col5:

            st.write(
                "Daily"
            )

        with col6:

            if st.button(
                "🗑️",
                key=f"v24_remove_{index}"
            ):

                remove_appliance(index)

                st.rerun()

    # ======================================================
    # ANALYSIS
    # ======================================================

    st.divider()

    st.subheader(
        "📊 Energy Demand Analysis"
    )

    total_energy = sum(
        calculate_record_energy(
            appliance
        )
        for appliance in loads
    )

    monthly_energy = (
        total_energy * 30
    )

    annual_energy = (
        total_energy * 365
    )

    metric1, metric2, metric3 = (
        st.columns(3)
    )

    metric1.metric(
        "Daily Energy Demand",
        f"{total_energy:.2f} kWh/day"
    )

    metric2.metric(
        "Monthly Energy",
        f"{monthly_energy:.1f} kWh"
    )

    metric3.metric(
        "Annual Energy",
        f"{annual_energy:.1f} kWh"
    )

    # ======================================================
    # CATEGORY SUMMARY
    # ======================================================

    st.subheader(
        "📂 Energy by Category"
    )

    try:

        category_summary = (
            calculate_category_summary(
                loads
            )
        )

    except Exception:

        category_summary = {}

        for appliance in loads:

            category = appliance.get(
                "category",
                "Other"
            )

            energy = calculate_record_energy(
                appliance
            )

            category_summary[
                category
            ] = (
                category_summary.get(
                    category,
                    0
                )
                + energy
            )

    if category_summary:

        for category, energy in (
            category_summary.items()
        ):

            percentage = (
                energy
                /
                total_energy
                * 100
                if total_energy > 0
                else 0
            )

            st.write(
                f"**{category}:** "
                f"{energy:.2f} kWh/day "
                f"({percentage:.1f}%)"
            )

    # ======================================================
    # HIGHEST ENERGY CONSUMERS
    # ======================================================

    st.subheader(
        "🏆 Highest Energy Consumers"
    )

    ranked = sorted(
        loads,
        key=lambda item:
            calculate_record_energy(item),
        reverse=True
    )

    for position, appliance in enumerate(
        ranked[:5],
        start=1
    ):

        energy = calculate_record_energy(
            appliance
        )

        st.write(
            f"**{position}. "
            f"{appliance['name']}** — "
            f"{energy:.2f} kWh/day"
        )

    # ======================================================
    # USE FOR PV DESIGN
    # ======================================================

    st.divider()

    st.subheader(
        "☀️ Solar PV Design Integration"
    )

    st.success(
        f"""
        Calculated Daily Energy Demand:

        **{total_energy:.2f} kWh/day**
        """
    )

    if st.button(
        "☀️ Use This Demand for PV Sizing",
        type="primary",
        use_container_width=True,
        key="v24_use_appliance_demand"
    ):

        st.session_state[
            "appliance_energy_demand"
        ] = total_energy

        st.session_state[
            "energy_from_appliances"
        ] = True

        st.success(
            """
            ✅ Appliance energy demand has been
            transferred to the Solar PV design engine.
            """
        )

    return total_energy
