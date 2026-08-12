# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Appliance Energy Calculator
# Version: 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Calculate household/business energy demand from
# individual appliances and prepare the results for
# integration with the Solar PV Designer Pro dashboard.
#
# ==========================================================


# ==========================================================
# SECTION 1 - DEFAULT APPLIANCE LIBRARY
# ==========================================================

DEFAULT_APPLIANCES = [
    {
        "name": "LED Light",
        "category": "Lighting",
        "default_wattage": 10
    },
    {
        "name": "Ceiling Fan",
        "category": "Cooling",
        "default_wattage": 60
    },
    {
        "name": "Standing Fan",
        "category": "Cooling",
        "default_wattage": 75
    },
    {
        "name": "Television",
        "category": "Entertainment",
        "default_wattage": 100
    },
    {
        "name": "Refrigerator",
        "category": "Kitchen",
        "default_wattage": 150
    },
    {
        "name": "Freezer",
        "category": "Kitchen",
        "default_wattage": 200
    },
    {
        "name": "Laptop",
        "category": "Office",
        "default_wattage": 65
    },
    {
        "name": "Desktop Computer",
        "category": "Office",
        "default_wattage": 200
    },
    {
        "name": "Phone Charger",
        "category": "Electronics",
        "default_wattage": 10
    },
    {
        "name": "Wi-Fi Router",
        "category": "Electronics",
        "default_wattage": 15
    },
    {
        "name": "Electric Iron",
        "category": "Kitchen",
        "default_wattage": 1200
    },
    {
        "name": "Electric Kettle",
        "category": "Kitchen",
        "default_wattage": 1500
    },
    {
        "name": "Microwave",
        "category": "Kitchen",
        "default_wattage": 1200
    },
    {
        "name": "Washing Machine",
        "category": "Laundry",
        "default_wattage": 500
    },
    {
        "name": "Water Pump",
        "category": "Water",
        "default_wattage": 750
    },
    {
        "name": "Air Conditioner",
        "category": "Cooling",
        "default_wattage": 1200
    },
    {
        "name": "Electric Cooker",
        "category": "Kitchen",
        "default_wattage": 2000
    },
    {
        "name": "Printer",
        "category": "Office",
        "default_wattage": 100
    }
]


# ==========================================================
# SECTION 2 - SAFE NUMERIC CONVERSION
# ==========================================================

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.

    Returns default if conversion fails.
    """

    try:
        if value is None:
            return float(default)

        return float(value)

    except (TypeError, ValueError):
        return float(default)


# ==========================================================
# SECTION 3 - VALIDATE APPLIANCE INPUT
# ==========================================================

def validate_appliance(
    name,
    quantity,
    wattage,
    hours_per_day
):
    """
    Validate appliance information.

    Returns:
        {
            "valid": True/False,
            "message": "..."
        }
    """

    if not str(name).strip():

        return {
            "valid": False,
            "message": "Appliance name is required."
        }

    quantity = safe_float(quantity)
    wattage = safe_float(wattage)
    hours_per_day = safe_float(hours_per_day)

    if quantity <= 0:

        return {
            "valid": False,
            "message": "Quantity must be greater than zero."
        }

    if wattage <= 0:

        return {
            "valid": False,
            "message": "Wattage must be greater than zero."
        }

    if hours_per_day < 0:

        return {
            "valid": False,
            "message": "Hours per day cannot be negative."
        }

    if hours_per_day > 24:

        return {
            "valid": False,
            "message": "Hours per day cannot exceed 24."
        }

    return {
        "valid": True,
        "message": "Appliance data is valid."
    }


# ==========================================================
# SECTION 4 - CALCULATE APPLIANCE ENERGY
# ==========================================================

def calculate_appliance_energy(
    name,
    quantity,
    wattage,
    hours_per_day
):
    """
    Calculate energy consumption for one appliance.

    Formula:

        Daily Wh =
            Quantity × Wattage × Hours/day

        Daily kWh =
            Daily Wh / 1000

        Monthly kWh =
            Daily kWh × 30
    """

    validation = validate_appliance(
        name,
        quantity,
        wattage,
        hours_per_day
    )

    if not validation["valid"]:

        raise ValueError(
            validation["message"]
        )

    quantity = safe_float(quantity)
    wattage = safe_float(wattage)
    hours_per_day = safe_float(hours_per_day)

    daily_wh = (
        quantity
        * wattage
        * hours_per_day
    )

    daily_kwh = (
        daily_wh / 1000
    )

    monthly_kwh = (
        daily_kwh * 30
    )

    return {
        "name": str(name).strip(),
        "quantity": quantity,
        "wattage": wattage,
        "hours_per_day": hours_per_day,
        "daily_wh": daily_wh,
        "daily_kwh": daily_kwh,
        "monthly_kwh": monthly_kwh
    }


# ==========================================================
# SECTION 5 - CALCULATE TOTAL ENERGY DEMAND
# ==========================================================

def calculate_total_energy(
    appliances
):
    """
    Calculate total energy demand from an appliance list.

    Returns:

        total_daily_wh
        total_daily_kwh
        total_monthly_kwh
    """

    if not appliances:

        return {
            "total_daily_wh": 0.0,
            "total_daily_kwh": 0.0,
            "total_monthly_kwh": 0.0
        }

    total_daily_wh = 0.0

    for appliance in appliances:

        total_daily_wh += safe_float(
            appliance.get(
                "daily_wh",
                0
            )
        )

    total_daily_kwh = (
        total_daily_wh / 1000
    )

    total_monthly_kwh = (
        total_daily_kwh * 30
    )

    return {
        "total_daily_wh": total_daily_wh,
        "total_daily_kwh": total_daily_kwh,
        "total_monthly_kwh": total_monthly_kwh
    }


# ==========================================================
# SECTION 6 - ADD APPLIANCE
# ==========================================================

def add_appliance(
    appliances,
    name,
    quantity,
    wattage,
    hours_per_day
):
    """
    Calculate and append one appliance to an appliance list.

    Returns:

        updated appliance list
    """

    if appliances is None:

        appliances = []

    appliance = calculate_appliance_energy(
        name=name,
        quantity=quantity,
        wattage=wattage,
        hours_per_day=hours_per_day
    )

    appliances.append(
        appliance
    )

    return appliances


# ==========================================================
# SECTION 7 - REMOVE APPLIANCE
# ==========================================================

def remove_appliance(
    appliances,
    index
):
    """
    Remove an appliance by list index.
    """

    if not appliances:

        return []

    try:

        index = int(index)

        if 0 <= index < len(appliances):

            appliances.pop(index)

    except (
        TypeError,
        ValueError
    ):

        pass

    return appliances


# ==========================================================
# SECTION 8 - CALCULATE APPLIANCE CONTRIBUTION
# ==========================================================

def calculate_appliance_contributions(
    appliances
):
    """
    Calculate each appliance's percentage contribution
    to total daily energy consumption.
    """

    if not appliances:

        return []

    totals = calculate_total_energy(
        appliances
    )

    total_daily_kwh = totals[
        "total_daily_kwh"
    ]

    results = []

    for appliance in appliances:

        daily_kwh = safe_float(
            appliance.get(
                "daily_kwh",
                0
            )
        )

        if total_daily_kwh > 0:

            contribution = (
                daily_kwh
                / total_daily_kwh
                * 100
            )

        else:

            contribution = 0.0

        item = dict(
            appliance
        )

        item[
            "contribution_percent"
        ] = contribution

        results.append(
            item
        )

    return results


# ==========================================================
# SECTION 9 - SORT APPLIANCES BY ENERGY
# ==========================================================

def sort_appliances_by_energy(
    appliances,
    descending=True
):
    """
    Sort appliances according to daily energy consumption.
    """

    if not appliances:

        return []

    return sorted(
        appliances,
        key=lambda item: safe_float(
            item.get(
                "daily_kwh",
                0
            )
        ),
        reverse=descending
    )


# ==========================================================
# SECTION 10 - COMPLETE ENERGY ANALYSIS
# ==========================================================

def analyze_appliance_energy(
    appliances
):
    """
    Perform complete appliance-energy analysis.

    Returns a dictionary suitable for:

        Streamlit dashboard
        charts
        reports
        AI recommendations
        PV sizing
    """

    if appliances is None:

        appliances = []

    contributions = (
        calculate_appliance_contributions(
            appliances
        )
    )

    totals = calculate_total_energy(
        contributions
    )

    sorted_appliances = (
        sort_appliances_by_energy(
            contributions
        )
    )

    if sorted_appliances:

        highest_consumer = (
            sorted_appliances[0]
        )

    else:

        highest_consumer = None

    return {

        "appliances":
            contributions,

        "total_daily_wh":
            totals[
                "total_daily_wh"
            ],

        "total_daily_kwh":
            totals[
                "total_daily_kwh"
            ],

        "total_monthly_kwh":
            totals[
                "total_monthly_kwh"
            ],

        "number_of_appliances":
            len(contributions),

        "highest_consumer":
            highest_consumer,

        "sorted_appliances":
            sorted_appliances
    }


# ==========================================================
# SECTION 11 - DEFAULT APPLIANCE LIBRARY
# ==========================================================

def get_default_appliances():
    """
    Return a copy of the built-in appliance library.
    """

    return [
        dict(appliance)
        for appliance
        in DEFAULT_APPLIANCES
    ]


# ==========================================================
# SECTION 12 - FIND DEFAULT APPLIANCE
# ==========================================================

def get_default_appliance(
    name
):
    """
    Find a default appliance by name.
    """

    for appliance in DEFAULT_APPLIANCES:

        if appliance[
            "name"
        ].lower() == str(
            name
        ).strip().lower():

            return dict(
                appliance
            )

    return None


# ==========================================================
# SECTION 13 - PREPARE DATA FOR PV SIZING
# ==========================================================

def get_daily_energy_demand(
    appliances
):
    """
    Return total daily energy demand in kWh/day.

    This is the value that can be passed directly into
    the existing PV sizing calculation.
    """

    analysis = (
        analyze_appliance_energy(
            appliances
        )
    )

    return analysis[
        "total_daily_kwh"
    ]


# ==========================================================
# SECTION 14 - FORMAT SUMMARY
# ==========================================================

def format_energy_summary(
    appliances
):
    """
    Create a simple human-readable energy summary.
    """

    analysis = (
        analyze_appliance_energy(
            appliances
        )
    )

    total_daily = analysis[
        "total_daily_kwh"
    ]

    total_monthly = analysis[
        "total_monthly_kwh"
    ]

    number = analysis[
        "number_of_appliances"
    ]

    highest = analysis[
        "highest_consumer"
    ]

    if highest:

        highest_name = highest[
            "name"
        ]

        highest_energy = highest[
            "daily_kwh"
        ]

        highest_text = (
            f"{highest_name} "
            f"({highest_energy:.2f} kWh/day)"
        )

    else:

        highest_text = "None"

    return {

        "total_daily_kwh":
            total_daily,

        "total_monthly_kwh":
            total_monthly,

        "number_of_appliances":
            number,

        "highest_consumer":
            highest_text
    }
