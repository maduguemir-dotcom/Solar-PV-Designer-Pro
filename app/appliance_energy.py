# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# APPLIANCE ENERGY PLANNER
#
# Complete, clean and backward-compatible module
#
# Version: 1.2
# ==========================================================

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional


# ==========================================================
# DEFAULT APPLIANCE DATABASE
# ==========================================================

DEFAULT_APPLIANCES: List[Dict[str, Any]] = [
    {
        "name": "LED Bulb",
        "category": "Lighting",
        "power_w": 10,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical LED household bulb",
    },
    {
        "name": "LED Bulb 15W",
        "category": "Lighting",
        "power_w": 15,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "15 W LED bulb",
    },
    {
        "name": "Fluorescent Lamp",
        "category": "Lighting",
        "power_w": 40,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical fluorescent lamp",
    },
    {
        "name": "LED Television",
        "category": "Entertainment",
        "power_w": 100,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical LED television",
    },
    {
        "name": "Satellite Decoder",
        "category": "Entertainment",
        "power_w": 25,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Satellite or digital television decoder",
    },
    {
        "name": "Radio",
        "category": "Entertainment",
        "power_w": 15,
        "quantity": 1,
        "hours_per_day": 4,
        "description": "Small household radio",
    },
    {
        "name": "Laptop",
        "category": "Office",
        "power_w": 60,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical laptop computer",
    },
    {
        "name": "Phone Charger",
        "category": "Electronics",
        "power_w": 10,
        "quantity": 1,
        "hours_per_day": 3,
        "description": "Mobile phone charger",
    },
    {
        "name": "Ceiling Fan",
        "category": "Cooling",
        "power_w": 80,
        "quantity": 1,
        "hours_per_day": 8,
        "description": "Typical ceiling fan",
    },
    {
        "name": "Standing Fan",
        "category": "Cooling",
        "power_w": 60,
        "quantity": 1,
        "hours_per_day": 8,
        "description": "Typical standing fan",
    },
    {
        "name": "Air Conditioner",
        "category": "Cooling",
        "power_w": 1200,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical residential air conditioner",
    },
    {
        "name": "Refrigerator",
        "category": "Kitchen",
        "power_w": 150,
        "quantity": 1,
        "hours_per_day": 8,
        "description": "Typical refrigerator running load",
    },
    {
        "name": "Electric Kettle",
        "category": "Kitchen",
        "power_w": 1500,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical electric kettle",
    },
    {
        "name": "Microwave Oven",
        "category": "Kitchen",
        "power_w": 1200,
        "quantity": 1,
        "hours_per_day": 0.5,
        "description": "Typical microwave oven",
    },
    {
        "name": "Electric Cooker",
        "category": "Kitchen",
        "power_w": 2000,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical electric cooker",
    },
    {
        "name": "Blender",
        "category": "Kitchen",
        "power_w": 500,
        "quantity": 1,
        "hours_per_day": 0.5,
        "description": "Typical household blender",
    },
    {
        "name": "Washing Machine",
        "category": "Laundry",
        "power_w": 500,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical washing machine",
    },
    {
        "name": "Electric Iron",
        "category": "Laundry",
        "power_w": 1000,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical electric iron",
    },
    {
        "name": "Desktop Computer",
        "category": "Office",
        "power_w": 200,
        "quantity": 1,
        "hours_per_day": 6,
        "description": "Desktop computer and monitor",
    },
    {
        "name": "Printer",
        "category": "Office",
        "power_w": 50,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical office printer",
    },
    {
        "name": "Wi-Fi Router",
        "category": "Office",
        "power_w": 15,
        "quantity": 1,
        "hours_per_day": 24,
        "description": "Typical Wi-Fi router",
    },
    {
        "name": "Water Pump",
        "category": "Water",
        "power_w": 750,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical small water pump",
    },
    {
        "name": "Electric Water Heater",
        "category": "Water Heating",
        "power_w": 2000,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical domestic water heater",
    },
]


# ==========================================================
# SAFE CONVERSION UTILITIES
# ==========================================================

def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:
    """Safely convert a value to float."""

    try:
        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):
        return default


def safe_int(
    value: Any,
    default: int = 0,
) -> int:
    """Safely convert a value to integer."""

    try:
        if value is None:
            return default

        return int(float(value))

    except (TypeError, ValueError):
        return default


# ==========================================================
# CREATE APPLIANCE RECORD
# ==========================================================

def create_appliance_record(
    name: str = "",
    category: str = "Other",
    power_w: float = 0.0,
    quantity: int = 1,
    hours_per_day: float = 0.0,
    description: str = "",
    **kwargs: Any,
) -> Dict[str, Any]:
    """Create a standardized appliance record."""

    record = {
        "name": str(name),
        "category": str(category),
        "power_w": safe_float(power_w),
        "quantity": max(
            safe_int(quantity, 1),
            1,
        ),
        "hours_per_day": max(
            safe_float(hours_per_day),
            0.0,
        ),
        "description": str(description),
    }

    record.update(kwargs)

    return record


# ==========================================================
# NORMALIZE APPLIANCE
# ==========================================================

def normalize_appliance(
    appliance: Optional[Dict[str, Any]],
) -> Dict[str, Any]:
    """Normalize different appliance dictionary formats."""

    if appliance is None:
        appliance = {}

    appliance = dict(appliance)

    return create_appliance_record(
        name=appliance.get(
            "name",
            appliance.get(
                "appliance",
                "",
            ),
        ),
        category=appliance.get(
            "category",
            "Other",
        ),
        power_w=appliance.get(
            "power_w",
            appliance.get(
                "power",
                appliance.get(
                    "watts",
                    0,
                ),
            ),
        ),
        quantity=appliance.get(
            "quantity",
            appliance.get(
                "qty",
                1,
            ),
        ),
        hours_per_day=appliance.get(
            "hours_per_day",
            appliance.get(
                "hours",
                appliance.get(
                    "operating_hours",
                    0,
                ),
            ),
        ),
        description=appliance.get(
            "description",
            appliance.get(
                "notes",
                "",
            ),
        ),
    )


# ==========================================================
# GET DEFAULT APPLIANCE
# ==========================================================

def get_default_appliance(
    name: str,
) -> Optional[Dict[str, Any]]:
    """Return a copy of a default appliance by name."""

    target = str(name).strip().lower()

    for appliance in DEFAULT_APPLIANCES:

        if (
            appliance["name"]
            .strip()
            .lower()
            == target
        ):
            return deepcopy(appliance)

    return None


# ==========================================================
# GET APPLIANCE NAMES
# ==========================================================

def get_appliance_names() -> List[str]:
    """Return names of all standard appliances."""

    return [
        appliance["name"]
        for appliance in DEFAULT_APPLIANCES
    ]


# ==========================================================
# GET APPLIANCE CATEGORIES
# ==========================================================

def get_appliance_categories() -> List[str]:
    """Return unique appliance categories."""

    categories = {
        appliance["category"]
        for appliance in DEFAULT_APPLIANCES
    }

    return sorted(categories)


# ==========================================================
# CALCULATE INDIVIDUAL APPLIANCE ENERGY
# ==========================================================

def calculate_appliance_energy(
    appliance: Any = None,
    quantity: Any = None,
    hours_per_day: Any = None,
    power_w: Any = None,
    **kwargs: Any,
) -> float:
    """
    Calculate daily appliance energy consumption in kWh.

    Supported calling styles:

        calculate_appliance_energy({
            "power_w": 100,
            "quantity": 2,
            "hours_per_day": 5
        })

        calculate_appliance_energy(
            100,
            2,
            5
        )

        calculate_appliance_energy(
            power_w=100,
            quantity=2,
            hours_per_day=5
        )

        calculate_appliance_energy(
            power=100,
            quantity=2,
            hours=5
        )

    Formula:

        Energy (kWh/day)
        = Power(W) × Quantity × Hours/day / 1000
    """

    # ------------------------------------------------------
    # Dictionary input
    # ------------------------------------------------------

    if isinstance(appliance, dict):

        record = dict(appliance)

        if power_w is not None:
            record["power_w"] = power_w

        if quantity is not None:
            record["quantity"] = quantity

        if hours_per_day is not None:
            record["hours_per_day"] = hours_per_day

        if "power" in kwargs:
            record["power_w"] = kwargs["power"]

        if "watts" in kwargs:
            record["power_w"] = kwargs["watts"]

        if "hours" in kwargs:
            record["hours_per_day"] = kwargs["hours"]

        if "operating_hours" in kwargs:
            record["hours_per_day"] = kwargs[
                "operating_hours"
            ]

        normalized = normalize_appliance(
            record
        )

        power = safe_float(
            normalized.get(
                "power_w",
                0,
            )
        )

        qty = safe_int(
            normalized.get(
                "quantity",
                1,
            ),
            1,
        )

        hours = safe_float(
            normalized.get(
                "hours_per_day",
                0,
            )
        )

        return round(
            power * qty * hours / 1000.0,
            4,
        )

    # ------------------------------------------------------
    # Numeric input
    # ------------------------------------------------------

    if power_w is not None:

        power = safe_float(
            power_w
        )

    else:

        power = safe_float(
            appliance
        )

    if quantity is None:

        quantity = kwargs.get(
            "qty",
            1,
        )

    if hours_per_day is None:

        hours_per_day = kwargs.get(
            "hours",
            kwargs.get(
                "operating_hours",
                0,
            ),
        )

    qty = safe_int(
        quantity,
        1,
    )

    hours = safe_float(
        hours_per_day,
        0,
    )

    return round(
        power * qty * hours / 1000.0,
        4,
    )


# ==========================================================
# CALCULATE APPLIANCE CONTRIBUTIONS
# ==========================================================

def calculate_appliance_contributions(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
) -> List[Dict[str, Any]]:
    """Calculate energy contribution of every appliance."""

    if appliances is None:
        appliances = []

    contributions = []

    for appliance in appliances:

        normalized = normalize_appliance(
            appliance
        )

        energy = calculate_appliance_energy(
            normalized
        )

        load = (
            normalized["power_w"]
            * normalized["quantity"]
        )

        item = dict(
            normalized
        )

        item["load_w"] = round(
            load,
            2,
        )

        item["energy_kwh"] = round(
            energy,
            4,
        )

        item["daily_energy_kwh"] = round(
            energy,
            4,
        )

        item["daily_energy_wh"] = round(
            energy * 1000,
            2,
        )

        contributions.append(
            item
        )

    return contributions


# ==========================================================
# TOTAL DAILY ENERGY
# ==========================================================

def calculate_total_energy_demand(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
) -> float:
    """Calculate total daily appliance energy demand."""

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    total = sum(
        safe_float(
            item.get(
                "daily_energy_kwh",
                0,
            )
        )
        for item in contributions
    )

    return round(
        total,
        4,
    )


# ==========================================================
# BACKWARD-COMPATIBLE DAILY DEMAND
# ==========================================================

def calculate_daily_demand(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
) -> float:
    """Alias for total daily energy demand."""

    return calculate_total_energy_demand(
        appliances
    )


# ==========================================================
# TOTAL CONNECTED LOAD
# ==========================================================

def calculate_total_load(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
) -> float:
    """Calculate total connected electrical load in watts."""

    if appliances is None:
        return 0.0

    total = 0.0

    for appliance in appliances:

        normalized = normalize_appliance(
            appliance
        )

        total += (
            normalized["power_w"]
            * normalized["quantity"]
        )

    return round(
        total,
        2,
    )


# ==========================================================
# CATEGORY SUMMARY
# ==========================================================

def calculate_category_summary(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
) -> Dict[str, float]:
    """Calculate daily energy by appliance category."""

    summary: Dict[str, float] = {}

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    for appliance in contributions:

        category = (
            appliance.get(
                "category"
            )
            or "Other"
        )

        energy = safe_float(
            appliance.get(
                "daily_energy_kwh",
                0,
            )
        )

        summary[category] = round(
            summary.get(
                category,
                0.0,
            )
            + energy,
            4,
        )

    return summary


# ==========================================================
# COMPLETE LOAD ANALYSIS
# ==========================================================

def analyze_appliance_load(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
) -> Dict[str, Any]:
    """
    Complete appliance load analysis.

    Several compatibility aliases are deliberately returned
    because different parts of the Solar PV Designer project
    may use different names for the same values.
    """

    if appliances is None:
        appliances = []

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    total_energy = (
        calculate_total_energy_demand(
            appliances
        )
    )

    total_load = (
        calculate_total_load(
            appliances
        )
    )

    category_summary = (
        calculate_category_summary(
            appliances
        )
    )

    if contributions:

        highest = max(
            contributions,
            key=lambda item: safe_float(
                item.get(
                    "daily_energy_kwh",
                    0,
                )
            ),
        )

    else:

        highest = None

    analysis = {

        # --------------------------------------------------
        # DAILY ENERGY
        # --------------------------------------------------

        "total_daily_kwh":
            total_energy,

        "total_daily_energy_kwh":
            total_energy,

        "total_energy_kwh":
            total_energy,

        "daily_energy_kwh":
            total_energy,

        # --------------------------------------------------
        # LOAD
        # --------------------------------------------------

        "total_load_w":
            total_load,

        "total_load_kw":
            round(
                total_load / 1000.0,
                4,
            ),

        "connected_load_w":
            total_load,

        "connected_load_kw":
            round(
                total_load / 1000.0,
                4,
            ),

        # --------------------------------------------------
        # APPLIANCE DETAILS
        # --------------------------------------------------

        "appliance_contributions":
            contributions,

        "appliances":
            contributions,

        # --------------------------------------------------
        # CATEGORY SUMMARY
        # --------------------------------------------------

        "category_summary":
            category_summary,

        "energy_by_category":
            category_summary,

        # --------------------------------------------------
        # HIGHEST CONSUMER
        # --------------------------------------------------

        "highest_energy_appliance":
            highest,

        "highest_consuming_appliance":
            highest,
    }

    return analysis


# ==========================================================
# SORT BY ENERGY
# ==========================================================

def sort_appliances_by_energy(
    appliances: Optional[
        List[Dict[str, Any]]
    ],
    descending: bool = True,
) -> List[Dict[str, Any]]:
    """Sort appliances by daily energy consumption."""

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    return sorted(
        contributions,
        key=lambda item: safe_float(
            item.get(
                "daily_energy_kwh",
                0,
            )
        ),
        reverse=descending,
    )


# ==========================================================
# VALIDATE APPLIANCE
# ==========================================================

def validate_appliance(
    appliance: Dict[str, Any],
) -> Dict[str, Any]:
    """Validate an appliance record."""

    normalized = normalize_appliance(
        appliance
    )

    errors: List[str] = []

    if not normalized["name"].strip():

        errors.append(
            "Appliance name is required."
        )

    if normalized["power_w"] < 0:

        errors.append(
            "Power rating cannot be negative."
        )

    if normalized["quantity"] < 1:

        errors.append(
            "Quantity must be at least 1."
        )

    if normalized["hours_per_day"] < 0:

        errors.append(
            "Operating hours cannot be negative."
        )

    if normalized["hours_per_day"] > 24:

        errors.append(
            "Operating hours cannot exceed 24 hours/day."
        )

    return {

        "valid":
            len(errors) == 0,

        "errors":
            errors,

        "appliance":
            normalized,
    }


# ==========================================================
# STREAMLIT UI
# ==========================================================

def display_appliance_calculator(
    st,
) -> Optional[Dict[str, Any]]:
    """
    Display the Appliance Energy Planner.

    Parameters
    ----------
    st:
        Streamlit module passed by main.py.

    Returns
    -------
    dict
        Complete appliance analysis.
    """

    st.subheader(
        "🔌 Appliance Energy Planner"
    )

    st.caption(
        "Calculate daily electricity consumption "
        "from appliance power, quantity and operating hours."
    )

    # ------------------------------------------------------
    # SESSION STATE
    # ------------------------------------------------------

    if (
        "appliance_planner_items"
        not in st.session_state
    ):

        st.session_state[
            "appliance_planner_items"
        ] = []

    # ------------------------------------------------------
    # ADD APPLIANCE
    # ------------------------------------------------------

    st.markdown(
        "### ➕ Add Appliance"
    )

    names = get_appliance_names()

    appliance_name = st.selectbox(
        "Appliance",
        names,
        key="appliance_name_select",
    )

    default = get_default_appliance(
        appliance_name
    )

    if default is None:

        default = {
            "power_w": 0.0,
            "quantity": 1,
            "hours_per_day": 1.0,
            "category": "Other",
            "description": "",
        }

    col1, col2 = st.columns(
        2
    )

    with col1:

        category = st.selectbox(
            "Category",
            get_appliance_categories(),
            index=(
                get_appliance_categories().index(
                    default.get(
                        "category",
                        "Other",
                    )
                )
                if default.get(
                    "category",
                    "Other",
                )
                in get_appliance_categories()
                else 0
            ),
            key="appliance_category_select",
        )

    with col2:

        description = st.text_input(
            "Description / notes",
            value=str(
                default.get(
                    "description",
                    "",
                )
            ),
            key="appliance_description_input",
        )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        power_w = st.number_input(
            "Power rating (W)",
            min_value=0.0,
            value=float(
                default.get(
                    "power_w",
                    0,
                )
            ),
            step=1.0,
            key="appliance_power_input",
        )

    with col2:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=int(
                default.get(
                    "quantity",
                    1,
                )
            ),
            step=1,
            key="appliance_quantity_input",
        )

    with col3:

        hours_per_day = st.number_input(
            "Hours per day",
            min_value=0.0,
            max_value=24.0,
            value=float(
                default.get(
                    "hours_per_day",
                    1,
                )
            ),
            step=0.5,
            key="appliance_hours_input",
        )

    # ------------------------------------------------------
    # PREVIEW
    # ------------------------------------------------------

    preview = create_appliance_record(
        name=appliance_name,
        category=category,
        power_w=power_w,
        quantity=quantity,
        hours_per_day=hours_per_day,
        description=description,
    )

    preview_energy = (
        calculate_appliance_energy(
            preview
        )
    )

    st.info(
        "Estimated daily consumption: "
        f"**{preview_energy:.3f} kWh/day**"
    )

    # ------------------------------------------------------
    # ADD BUTTON
    # ------------------------------------------------------

    if st.button(
        "➕ Add Appliance",
        type="primary",
        use_container_width=True,
    ):

        validation = validate_appliance(
            preview
        )

        if not validation["valid"]:

            for error in validation["errors"]:

                st.error(
                    error
                )

        else:

            st.session_state[
                "appliance_planner_items"
            ].append(
                validation[
                    "appliance"
                ]
            )

            st.success(
                f"{appliance_name} added successfully."
            )

            st.rerun()

    # ------------------------------------------------------
    # SELECTED APPLIANCES
    # ------------------------------------------------------

    appliances = st.session_state[
        "appliance_planner_items"
    ]

    st.markdown(
        "### 📋 Selected Appliances"
    )

    if not appliances:

        st.warning(
            "No appliances have been added yet."
        )

        return {
            "appliances": [],
            "appliance_contributions": [],
            "total_daily_kwh": 0.0,
            "total_daily_energy_kwh": 0.0,
            "total_energy_kwh": 0.0,
            "daily_energy_kwh": 0.0,
            "total_load_w": 0.0,
            "total_load_kw": 0.0,
            "connected_load_w": 0.0,
            "connected_load_kw": 0.0,
            "category_summary": {},
            "energy_by_category": {},
            "highest_energy_appliance": None,
            "highest_consuming_appliance": None,
        }

    # ------------------------------------------------------
    # DISPLAY ITEMS
    # ------------------------------------------------------

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    for index, item in enumerate(
        contributions
    ):

        col1, col2, col3, col4, col5 = st.columns(
            [
                2.2,
                1.0,
                1.0,
                1.4,
                0.7,
            ]
        )

        with col1:

            st.write(
                f"**{item['name']}**"
            )

            st.caption(
                item.get(
                    "category",
                    "Other",
                )
            )

        with col2:

            st.write(
                f"{item['power_w']:.0f} W"
            )

        with col3:

            st.write(
                f"x {item['quantity']}"
            )

        with col4:

            st.write(
                f"{item['daily_energy_kwh']:.3f} kWh"
            )

        with col5:

            if st.button(
                "🗑️",
                key=f"remove_appliance_{index}",
            ):

                st.session_state[
                    "appliance_planner_items"
                ].pop(index)

                st.rerun()

    # ------------------------------------------------------
    # ANALYSIS
    # ------------------------------------------------------

    analysis = analyze_appliance_load(
        appliances
    )

    st.divider()

    st.markdown(
        "### 📊 Complete Load Analysis"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(
            "Daily Energy",
            f"{analysis['total_daily_kwh']:.2f} kWh",
        )

    with col2:

        st.metric(
            "Connected Load",
            f"{analysis['total_load_w']:.0f} W",
        )

    with col3:

        st.metric(
            "Connected Load",
            f"{analysis['total_load_kw']:.2f} kW",
        )

    # ------------------------------------------------------
    # CATEGORY BREAKDOWN
    # ------------------------------------------------------

    st.markdown(
        "#### Energy by Category"
    )

    for category_name, energy in sorted(
        analysis[
            "category_summary"
        ].items()
    ):

        st.write(
            f"**{category_name}:** "
            f"{energy:.2f} kWh/day"
        )

    # ------------------------------------------------------
    # HIGHEST CONSUMER
    # ------------------------------------------------------

    highest = analysis[
        "highest_energy_appliance"
    ]

    if highest:

        st.warning(
            "Highest energy consumer: "
            f"**{highest['name']}** — "
            f"{highest['daily_energy_kwh']:.2f} kWh/day"
        )

    # ------------------------------------------------------
    # CLEAR BUTTON
    # ------------------------------------------------------

    st.divider()

    if st.button(
        "🧹 Clear All Appliances",
        use_container_width=True,
    ):

        st.session_state[
            "appliance_planner_items"
        ] = []

        st.rerun()

    return analysis


# ==========================================================
# BACKWARD COMPATIBILITY ALIAS
# ==========================================================

def appliance_energy_calculator(
    st,
) -> Optional[Dict[str, Any]]:
    """Backward-compatible alias."""

    return display_appliance_calculator(
        st
    )


# ==========================================================
# MODULE EXPORTS
# ==========================================================

__all__ = [

    "DEFAULT_APPLIANCES",

    "safe_float",

    "safe_int",

    "create_appliance_record",

    "normalize_appliance",

    "get_default_appliance",

    "get_appliance_names",

    "get_appliance_categories",

    "calculate_appliance_energy",

    "calculate_appliance_contributions",

    "calculate_total_energy_demand",

    "calculate_daily_demand",

    "calculate_total_load",

    "calculate_category_summary",

    "analyze_appliance_load",

    "sort_appliances_by_energy",

    "validate_appliance",

    "display_appliance_calculator",

    "appliance_energy_calculator",

]
