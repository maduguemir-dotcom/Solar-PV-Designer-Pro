# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# APPLIANCE ENERGY PLANNER
#
# Version: 1.1
#
# Compatible with:
#   main.py
#   test_appliance_energy.py
#   product_engine.py
#   solar sizing modules
#
# ==========================================================

from __future__ import annotations

from copy import deepcopy
from typing import Any, Dict, List, Optional


# ==========================================================
# DEFAULT APPLIANCE LIBRARY
# ==========================================================

DEFAULT_APPLIANCES: List[Dict[str, Any]] = [

    # ------------------------------------------------------
    # LIGHTING
    # ------------------------------------------------------

    {
        "name": "LED Bulb",
        "category": "Lighting",
        "power_w": 10,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical LED household lighting.",
    },

    {
        "name": "LED Bulb 15W",
        "category": "Lighting",
        "power_w": 15,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Higher-output LED bulb.",
    },

    {
        "name": "Fluorescent Lamp",
        "category": "Lighting",
        "power_w": 40,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical fluorescent lamp.",
    },

    # ------------------------------------------------------
    # ENTERTAINMENT
    # ------------------------------------------------------

    {
        "name": "LED Television",
        "category": "Entertainment",
        "power_w": 100,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical LED television.",
    },

    {
        "name": "Decoder / Satellite Receiver",
        "category": "Entertainment",
        "power_w": 25,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Satellite or digital TV decoder.",
    },

    {
        "name": "Radio",
        "category": "Entertainment",
        "power_w": 15,
        "quantity": 1,
        "hours_per_day": 4,
        "description": "Small household radio.",
    },

    {
        "name": "Laptop",
        "category": "Entertainment",
        "power_w": 60,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical laptop computer.",
    },

    {
        "name": "Phone Charger",
        "category": "Entertainment",
        "power_w": 10,
        "quantity": 1,
        "hours_per_day": 3,
        "description": "Mobile phone charging.",
    },

    # ------------------------------------------------------
    # COOLING
    # ------------------------------------------------------

    {
        "name": "Ceiling Fan",
        "category": "Cooling",
        "power_w": 80,
        "quantity": 1,
        "hours_per_day": 8,
        "description": "Typical ceiling fan.",
    },

    {
        "name": "Standing Fan",
        "category": "Cooling",
        "power_w": 60,
        "quantity": 1,
        "hours_per_day": 8,
        "description": "Typical standing fan.",
    },

    {
        "name": "Air Conditioner",
        "category": "Cooling",
        "power_w": 1200,
        "quantity": 1,
        "hours_per_day": 5,
        "description": "Typical residential air conditioner.",
    },

    # ------------------------------------------------------
    # KITCHEN
    # ------------------------------------------------------

    {
        "name": "Refrigerator",
        "category": "Kitchen",
        "power_w": 150,
        "quantity": 1,
        "hours_per_day": 8,
        "description": "Average running power estimate.",
    },

    {
        "name": "Electric Kettle",
        "category": "Kitchen",
        "power_w": 1500,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical electric kettle.",
    },

    {
        "name": "Microwave Oven",
        "category": "Kitchen",
        "power_w": 1200,
        "quantity": 1,
        "hours_per_day": 0.5,
        "description": "Typical microwave oven.",
    },

    {
        "name": "Electric Cooker",
        "category": "Kitchen",
        "power_w": 2000,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical electric cooker.",
    },

    {
        "name": "Blender",
        "category": "Kitchen",
        "power_w": 500,
        "quantity": 1,
        "hours_per_day": 0.5,
        "description": "Typical household blender.",
    },

    # ------------------------------------------------------
    # LAUNDRY
    # ------------------------------------------------------

    {
        "name": "Washing Machine",
        "category": "Laundry",
        "power_w": 500,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical washing machine.",
    },

    {
        "name": "Electric Iron",
        "category": "Laundry",
        "power_w": 1000,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical household iron.",
    },

    # ------------------------------------------------------
    # OFFICE
    # ------------------------------------------------------

    {
        "name": "Desktop Computer",
        "category": "Office",
        "power_w": 200,
        "quantity": 1,
        "hours_per_day": 6,
        "description": "Desktop computer including monitor.",
    },

    {
        "name": "Printer",
        "category": "Office",
        "power_w": 50,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical office printer.",
    },

    {
        "name": "Wi-Fi Router",
        "category": "Office",
        "power_w": 15,
        "quantity": 1,
        "hours_per_day": 24,
        "description": "Typical home or office router.",
    },

    # ------------------------------------------------------
    # WATER / OTHER
    # ------------------------------------------------------

    {
        "name": "Water Pump",
        "category": "Water",
        "power_w": 750,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical small water pump.",
    },

    {
        "name": "Electric Water Heater",
        "category": "Other",
        "power_w": 2000,
        "quantity": 1,
        "hours_per_day": 1,
        "description": "Typical domestic water heater.",
    },
]


# ==========================================================
# SAFE CONVERSION FUNCTIONS
# ==========================================================

def safe_float(
    value: Any,
    default: float = 0.0,
) -> float:

    try:

        if value is None:
            return default

        return float(value)

    except (
        TypeError,
        ValueError,
    ):

        return default


def safe_int(
    value: Any,
    default: int = 0,
) -> int:

    try:

        if value is None:
            return default

        return int(float(value))

    except (
        TypeError,
        ValueError,
    ):

        return default


# ==========================================================
# CREATE APPLIANCE RECORD
# ==========================================================

def create_appliance_record(
    name: str = "",
    category: str = "Other",
    power_w: float = 0,
    quantity: int = 1,
    hours_per_day: float = 0,
    description: str = "",
    **kwargs: Any,
) -> Dict[str, Any]:

    record = {

        "name": str(name),

        "category": str(category),

        "power_w": safe_float(
            power_w
        ),

        "quantity": max(
            safe_int(
                quantity,
                1
            ),
            1
        ),

        "hours_per_day": max(
            safe_float(
                hours_per_day
            ),
            0
        ),

        "description": str(
            description
        ),
    }

    record.update(
        kwargs
    )

    return record


# ==========================================================
# NORMALIZE APPLIANCE
# ==========================================================

def normalize_appliance(
    appliance: Optional[Dict[str, Any]],
) -> Dict[str, Any]:

    if appliance is None:

        appliance = {}

    appliance = dict(
        appliance
    )

    return create_appliance_record(

        name=appliance.get(
            "name",
            appliance.get(
                "appliance",
                ""
            )
        ),

        category=appliance.get(
            "category",
            "Other"
        ),

        power_w=appliance.get(
            "power_w",
            appliance.get(
                "power",
                0
            )
        ),

        quantity=appliance.get(
            "quantity",
            1
        ),

        hours_per_day=appliance.get(
            "hours_per_day",
            appliance.get(
                "hours",
                0
            )
        ),

        description=appliance.get(
            "description",
            ""
        ),
    )


# ==========================================================
# GET DEFAULT APPLIANCE
# ==========================================================

def get_default_appliance(
    name: str,
) -> Optional[Dict[str, Any]]:

    target = str(
        name
    ).strip().lower()

    for appliance in DEFAULT_APPLIANCES:

        if (
            appliance["name"]
            .strip()
            .lower()
            == target
        ):

            return deepcopy(
                appliance
            )

    return None


# ==========================================================
# GET APPLIANCE NAMES
# ==========================================================

def get_appliance_names() -> List[str]:

    return [
        appliance["name"]
        for appliance
        in DEFAULT_APPLIANCES
    ]


# ==========================================================
# CALCULATE APPLIANCE ENERGY
#
# IMPORTANT:
#
# This function accepts MULTIPLE formats.
#
# Format 1:
# calculate_appliance_energy({
#     "power_w": 100,
#     "quantity": 2,
#     "hours_per_day": 5
# })
#
# Format 2:
# calculate_appliance_energy(
#     100,
#     2,
#     5
# )
#
# Format 3:
# calculate_appliance_energy(
#     power_w=100,
#     quantity=2,
#     hours_per_day=5
# )
#
# Format 4:
# calculate_appliance_energy(
#     power=100,
#     quantity=2,
#     hours=5
# )
# ==========================================================

def calculate_appliance_energy(
    appliance: Any = None,
    quantity: Any = None,
    hours_per_day: Any = None,
    power_w: Any = None,
    **kwargs: Any,
) -> float:

    # ------------------------------------------------------
    # CASE 1: Dictionary / appliance record
    # ------------------------------------------------------

    if isinstance(
        appliance,
        dict
    ):

        record = dict(
            appliance
        )

        if power_w is not None:

            record[
                "power_w"
            ] = power_w

        if quantity is not None:

            record[
                "quantity"
            ] = quantity

        if hours_per_day is not None:

            record[
                "hours_per_day"
            ] = hours_per_day

        # Support aliases
        if "power" in kwargs:

            record[
                "power_w"
            ] = kwargs[
                "power"
            ]

        if "hours" in kwargs:

            record[
                "hours_per_day"
            ] = kwargs[
                "hours"
            ]

        normalized = normalize_appliance(
            record
        )

        return round(

            safe_float(
                normalized.get(
                    "power_w",
                    0
                )
            )
            *
            safe_int(
                normalized.get(
                    "quantity",
                    1
                ),
                1
            )
            *
            safe_float(
                normalized.get(
                    "hours_per_day",
                    0
                )
            )
            / 1000.0,

            4
        )

    # ------------------------------------------------------
    # CASE 2:
    #
    # calculate_appliance_energy(
    #     power_w,
    #     quantity,
    #     hours_per_day
    # )
    # ------------------------------------------------------

    if appliance is not None:

        numeric_power = safe_float(
            appliance,
            0
        )

    else:

        numeric_power = safe_float(
            power_w,
            0
        )

    # If power_w was explicitly supplied,
    # it takes priority.

    if power_w is not None:

        numeric_power = safe_float(
            power_w,
            numeric_power
        )

    numeric_quantity = safe_int(
        quantity
        if quantity is not None
        else kwargs.get(
            "qty",
            1
        ),
        1
    )

    numeric_hours = safe_float(
        hours_per_day
        if hours_per_day is not None
        else kwargs.get(
            "hours",
            0
        ),
        0
    )

    return round(

        numeric_power
        *
        numeric_quantity
        *
        numeric_hours
        / 1000.0,

        4
    )


# ==========================================================
# CALCULATE APPLIANCE CONTRIBUTIONS
# ==========================================================

def calculate_appliance_contributions(
    appliances: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:

    contributions = []

    if appliances is None:

        appliances = []

    for appliance in appliances:

        normalized = normalize_appliance(
            appliance
        )

        energy = calculate_appliance_energy(
            normalized
        )

        load_w = (
            safe_float(
                normalized.get(
                    "power_w",
                    0
                )
            )
            *
            safe_int(
                normalized.get(
                    "quantity",
                    1
                ),
                1
            )
        )

        item = dict(
            normalized
        )

        item[
            "daily_energy_kwh"
        ] = energy

        item[
            "energy_kwh"
        ] = energy

        item[
            "load_w"
        ] = round(
            load_w,
            2
        )

        contributions.append(
            item
        )

    return contributions


# ==========================================================
# TOTAL ENERGY DEMAND
# ==========================================================

def calculate_total_energy_demand(
    appliances: List[Dict[str, Any]],
) -> float:

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    total = sum(

        safe_float(
            item.get(
                "daily_energy_kwh",
                0
            )
        )

        for item
        in contributions
    )

    return round(
        total,
        4
    )


# ==========================================================
# DAILY DEMAND
# ==========================================================

def calculate_daily_demand(
    appliances: List[Dict[str, Any]],
) -> float:

    return calculate_total_energy_demand(
        appliances
    )


# ==========================================================
# TOTAL CONNECTED LOAD
# ==========================================================

def calculate_total_load(
    appliances: List[Dict[str, Any]],
) -> float:

    total = 0.0

    if appliances is None:

        return 0.0

    for appliance in appliances:

        normalized = normalize_appliance(
            appliance
        )

        total += (

            safe_float(
                normalized.get(
                    "power_w",
                    0
                )
            )

            *

            safe_int(
                normalized.get(
                    "quantity",
                    1
                ),
                1
            )
        )

    return round(
        total,
        2
    )


# ==========================================================
# CATEGORY SUMMARY
# ==========================================================

def calculate_category_summary(
    appliances: List[Dict[str, Any]],
) -> Dict[str, float]:

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
                0
            )
        )

        summary[
            category
        ] = round(

            summary.get(
                category,
                0
            )
            + energy,

            4
        )

    return summary


# ==========================================================
# ANALYZE APPLIANCE LOAD
# ==========================================================
def analyze_appliance_load(
    appliances: List[Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Analyze the complete appliance load.

    Returns multiple backward-compatible key names
    for total daily energy consumption.
    """

    if appliances is None:
        appliances = []

    # Calculate individual appliance contributions
    contributions = calculate_appliance_contributions(
        appliances
    )

    # Total daily energy
    total_energy = calculate_total_energy_demand(
        appliances
    )

    # Total connected load
    total_load = calculate_total_load(
        appliances
    )

    # Category breakdown
    category_summary = calculate_category_summary(
        appliances
    )

    # Find highest energy-consuming appliance
    if contributions:

        highest_energy = max(
            contributions,
            key=lambda item: safe_float(
                item.get(
                    "daily_energy_kwh",
                    item.get(
                        "energy_kwh",
                        0
                    )
                )
            )
        )

    else:

        highest_energy = None

    # ------------------------------------------------------
    # RETURN ALL COMPATIBILITY ALIASES
    # ------------------------------------------------------

    analysis = {

        # Required by current test
        "total_daily_kwh":
            total_energy,

        # Newer naming convention
        "total_daily_energy_kwh":
            total_energy,

        # Additional compatibility names
        "total_energy_kwh":
            total_energy,

        "daily_energy_kwh":
            total_energy,

        # Connected load
        "total_load_w":
            total_load,

        "total_load_kw":
            round(
                total_load / 1000.0,
                4
            ),

        # Category information
        "category_summary":
            category_summary,

        # Appliance-level information
        "appliance_contributions":
            contributions,

        # Highest consumer
        "highest_energy_appliance":
            highest_energy,

        # Compatibility alias
        "highest_consuming_appliance":
            highest_energy,
    }

    return analysis
def test_analysis_keys():
    """
    Internal diagnostic for appliance analysis.
    """

    result = analyze_appliance_load([])

    return {
        "has_total_daily_kwh":
            "total_daily_kwh" in result,

        "keys":
            list(result.keys()),
    }

        # --------------------------------------------------
        # ENERGY TOTALS
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
                4
            ),

        # --------------------------------------------------
        # CATEGORY BREAKDOWN
        # --------------------------------------------------

        "category_summary":
            category_summary,

        # --------------------------------------------------
        # INDIVIDUAL APPLIANCES
        # --------------------------------------------------

        "appliance_contributions":
            contributions,

        # --------------------------------------------------
        # HIGHEST CONSUMER
        # --------------------------------------------------

        "highest_energy_appliance":
            highest_energy,

        # Backward-compatible alias
        "highest_consuming_appliance":
            highest_energy,

    }
    # ==========================================================
# SORT APPLIANCES BY ENERGY
# ==========================================================

def sort_appliances_by_energy(
    appliances: List[Dict[str, Any]],
    descending: bool = True,
) -> List[Dict[str, Any]]:

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    return sorted(

        contributions,

        key=lambda item:
        safe_float(
            item.get(
                "daily_energy_kwh",
                0
            )
        ),

        reverse=descending
    )


# ==========================================================
# VALIDATE APPLIANCE
# ==========================================================

def validate_appliance(
    appliance: Dict[str, Any],
) -> Dict[str, Any]:

    normalized = normalize_appliance(
        appliance
    )

    errors = []

    if not normalized[
        "name"
    ].strip():

        errors.append(
            "Appliance name is required."
        )

    if normalized[
        "power_w"
    ] < 0:

        errors.append(
            "Power cannot be negative."
        )

    if normalized[
        "quantity"
    ] < 1:

        errors.append(
            "Quantity must be at least 1."
        )

    if normalized[
        "hours_per_day"
    ] < 0:

        errors.append(
            "Hours per day cannot be negative."
        )

    if normalized[
        "hours_per_day"
    ] > 24:

        errors.append(
            "Hours per day cannot exceed 24."
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
# STREAMLIT APPLIANCE CALCULATOR
# ==========================================================

def display_appliance_calculator(
    st,
) -> Optional[Dict[str, Any]]:
    """
    Main Streamlit Appliance Energy Planner.

    Compatible with:

        display_appliance_calculator(st)
    """

    st.subheader(
        "🔌 Appliance Energy Planner"
    )

    st.caption(
        "Estimate household or facility energy "
        "consumption from appliance power ratings, "
        "quantities and daily operating hours."
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

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        appliance_name = st.selectbox(

            "Appliance",

            get_appliance_names(),

            key=
            "appliance_name_select",
        )

    with col2:

        categories = sorted(

            list(
                {
                    item[
                        "category"
                    ]

                    for item
                    in DEFAULT_APPLIANCES
                }
            )
        )

        category = st.selectbox(

            "Category",

            categories,

            key=
            "appliance_category_select",
        )

    default = (
        get_default_appliance(
            appliance_name
        )
    )

    if default is None:

        default = {

            "power_w": 0,

            "quantity": 1,

            "hours_per_day": 1,

        }

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
                    0
                )
            ),

            step=1.0,

            key=
            "appliance_power_input",
        )

    with col2:

        quantity = st.number_input(

            "Quantity",

            min_value=1,

            value=int(
                default.get(
                    "quantity",
                    1
                )
            ),

            step=1,

            key=
            "appliance_quantity_input",
        )

    with col3:

        hours_per_day = st.number_input(

            "Hours per day",

            min_value=0.0,

            max_value=24.0,

            value=float(
                default.get(
                    "hours_per_day",
                    1
                )
            ),

            step=0.5,

            key=
            "appliance_hours_input",
        )

    description = st.text_input(

        "Description / notes",

        value=str(
            default.get(
                "description",
                ""
            )
        ),

        key=
        "appliance_description_input",
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

        f"Estimated daily consumption: "
        f"**{preview_energy:.3f} kWh/day**"
    )

    # ------------------------------------------------------
    # ADD
    # ------------------------------------------------------

    if st.button(

        "➕ Add Appliance",

        type="primary",

        use_container_width=True,
    ):

        validation = validate_appliance(
            preview
        )

        if not validation[
            "valid"
        ]:

            for error in validation[
                "errors"
            ]:

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

                f"{appliance_name} "
                f"added successfully."
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

        st.info(
            "Add appliances above to calculate "
            "the total daily energy demand."
        )

        return {

            "appliances": [],

            "total_daily_energy_kwh":
                0.0,

            "total_load_w":
                0.0,

            "total_load_kw":
                0.0,

            "category_summary":
                {},

        }

    # ------------------------------------------------------
    # DISPLAY APPLIANCES
    # ------------------------------------------------------

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    for index, item in enumerate(
        contributions
    ):

        col1, col2, col3, col4, col5 = (
            st.columns(
                [
                    2.2,
                    1.0,
                    1.0,
                    1.2,
                    0.8,
                ]
            )
        )

        with col1:

            st.write(
                f"**{item['name']}**"
            )

            st.caption(
                item.get(
                    "category",
                    "Other"
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

                key=
                f"remove_appliance_{index}",
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

    total_energy = analysis[
        "total_daily_energy_kwh"
    ]

    total_load = analysis[
        "total_load_w"
    ]

    category_summary = analysis[
        "category_summary"
    ]

    st.divider()

    st.markdown(
        "### 📊 Energy Summary"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        st.metric(

            "Daily Energy Demand",

            f"{total_energy:.2f} kWh/day"
        )

    with col2:

        st.metric(

            "Connected Load",

            f"{total_load:.0f} W"
        )

    with col3:

        st.metric(

            "Connected Load",

            f"{total_load / 1000:.2f} kW"
        )

    # ------------------------------------------------------
    # CATEGORY SUMMARY
    # ------------------------------------------------------

    st.markdown(
        "#### Energy by Category"
    )

    for category_name, energy in sorted(
        category_summary.items()
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

            f"Highest energy consumer: "
            f"**{highest['name']}** "
            f"({highest['daily_energy_kwh']:.2f} "
            f"kWh/day)"
        )

    # ------------------------------------------------------
    # CLEAR
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

    # ------------------------------------------------------
    # RETURN
    # ------------------------------------------------------

    return {

        "appliances":
            deepcopy(
                appliances
            ),

        "total_daily_energy_kwh":
            total_energy,

        "total_energy_kwh":
            total_energy,

        "daily_energy_kwh":
            total_energy,

        "total_load_w":
            total_load,

        "total_load_kw":
            round(
                total_load / 1000,
                4
            ),

        "category_summary":
            category_summary,

        "analysis":
            analysis,

    }


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def appliance_energy_calculator(
    st,
) -> Optional[Dict[str, Any]]:

    return display_appliance_calculator(
        st
    )


# ==========================================================
# EXPORTS
# ==========================================================

__all__ = [

    "DEFAULT_APPLIANCES",

    "safe_float",

    "safe_int",

    "create_appliance_record",

    "normalize_appliance",

    "get_default_appliance",

    "get_appliance_names",

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
