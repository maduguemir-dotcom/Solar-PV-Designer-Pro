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
# Calculate daily and monthly electrical energy demand
# from household, institutional and commercial appliances.
#
# ==========================================================


# ==========================================================
# SECTION 1 - STANDARD APPLIANCE LIBRARY
# ==========================================================

DEFAULT_APPLIANCES = [

    {
        "name": "LED Light",
        "category": "Lighting",
        "wattage": 10
    },

    {
        "name": "CFL Light",
        "category": "Lighting",
        "wattage": 20
    },

    {
        "name": "Ceiling Fan",
        "category": "Cooling",
        "wattage": 75
    },

    {
        "name": "Standing Fan",
        "category": "Cooling",
        "wattage": 60
    },

    {
        "name": "Television",
        "category": "Entertainment",
        "wattage": 100
    },

    {
        "name": "Decoder / Set-top Box",
        "category": "Entertainment",
        "wattage": 25
    },

    {
        "name": "Refrigerator",
        "category": "Kitchen",
        "wattage": 150
    },

    {
        "name": "Freezer",
        "category": "Kitchen",
        "wattage": 200
    },

    {
        "name": "Electric Iron",
        "category": "Household",
        "wattage": 1000
    },

    {
        "name": "Electric Kettle",
        "category": "Kitchen",
        "wattage": 1500
    },

    {
        "name": "Microwave Oven",
        "category": "Kitchen",
        "wattage": 1200
    },

    {
        "name": "Electric Cooker",
        "category": "Kitchen",
        "wattage": 2000
    },

    {
        "name": "Air Conditioner",
        "category": "Cooling",
        "wattage": 1500
    },

    {
        "name": "Water Pump",
        "category": "Water",
        "wattage": 750
    },

    {
        "name": "Laptop",
        "category": "ICT",
        "wattage": 65
    },

    {
        "name": "Desktop Computer",
        "category": "ICT",
        "wattage": 250
    },

    {
        "name": "Wi-Fi Router",
        "category": "ICT",
        "wattage": 15
    },

    {
        "name": "Printer",
        "category": "ICT",
        "wattage": 100
    },

    {
        "name": "Phone Charger",
        "category": "ICT",
        "wattage": 10
    },

    {
        "name": "Washing Machine",
        "category": "Laundry",
        "wattage": 500
    },

    {
        "name": "Hair Dryer",
        "category": "Personal Care",
        "wattage": 1200
    },

    {
        "name": "Other / Custom Appliance",
        "category": "Custom",
        "wattage": 100
    }

]


# ==========================================================
# SECTION 2 - SAFE NUMERIC CONVERSION
# ==========================================================

def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        number = float(value)

        if number < 0:
            return default

        return number

    except (TypeError, ValueError):

        return default


# ==========================================================
# SECTION 3 - CALCULATE APPLIANCE ENERGY
# ==========================================================

def calculate_appliance_energy(
    wattage,
    hours_per_day,
    quantity=1
):
    """
    Calculate energy consumed by an appliance.

    Formula:

        Daily Wh =
            Wattage × Hours × Quantity

        Daily kWh =
            Daily Wh / 1000

        Monthly kWh =
            Daily kWh × 30
    """

    wattage = safe_float(wattage)
    hours_per_day = safe_float(hours_per_day)
    quantity = safe_float(quantity, 1)

    daily_wh = (
        wattage
        *
        hours_per_day
        *
        quantity
    )

    daily_kwh = (
        daily_wh / 1000
    )

    monthly_kwh = (
        daily_kwh * 30
    )

    return {

        "daily_wh": daily_wh,

        "daily_kwh": daily_kwh,

        "monthly_kwh": monthly_kwh

    }


# ==========================================================
# SECTION 4 - CREATE APPLIANCE RECORD
# ==========================================================

def create_appliance_record(
    name,
    category,
    wattage,
    hours_per_day,
    quantity=1
):

    energy = calculate_appliance_energy(

        wattage=wattage,

        hours_per_day=hours_per_day,

        quantity=quantity

    )

    return {

        "appliance": str(name),

        "category": str(category),

        "quantity": safe_float(
            quantity,
            1
        ),

        "wattage_w": safe_float(
            wattage
        ),

        "hours_per_day": safe_float(
            hours_per_day
        ),

        "daily_wh": energy[
            "daily_wh"
        ],

        "daily_kwh": energy[
            "daily_kwh"
        ],

        "monthly_kwh": energy[
            "monthly_kwh"
        ]

    }


# ==========================================================
# SECTION 5 - CALCULATE TOTAL ENERGY DEMAND
# ==========================================================

def calculate_total_energy_demand(
    appliances
):

    if not appliances:

        return {

            "total_daily_wh": 0.0,

            "total_daily_kwh": 0.0,

            "total_monthly_kwh": 0.0

        }

    total_daily_wh = 0.0

    total_monthly_kwh = 0.0

    for appliance in appliances:

        total_daily_wh += safe_float(
            appliance.get(
                "daily_wh"
            )
        )

        total_monthly_kwh += safe_float(
            appliance.get(
                "monthly_kwh"
            )
        )

    return {

        "total_daily_wh":
            total_daily_wh,

        "total_daily_kwh":
            total_daily_wh / 1000,

        "total_monthly_kwh":
            total_monthly_kwh

    }


# ==========================================================
# SECTION 6 - CALCULATE APPLIANCE CONTRIBUTIONS
# ==========================================================

def calculate_appliance_contributions(
    appliances
):

    totals = calculate_total_energy_demand(
        appliances
    )

    total_daily_wh = totals[
        "total_daily_wh"
    ]

    results = []

    for appliance in appliances:

        daily_wh = safe_float(
            appliance.get(
                "daily_wh"
            )
        )

        if total_daily_wh > 0:

            contribution = (
                daily_wh
                /
                total_daily_wh
                *
                100
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
# SECTION 7 - SORT APPLIANCES BY ENERGY
# ==========================================================

def sort_appliances_by_energy(
    appliances,
    descending=True
):

    return sorted(

        appliances,

        key=lambda item:
            safe_float(
                item.get(
                    "daily_wh"
                )
            ),

        reverse=descending

    )


# ==========================================================
# SECTION 8 - CATEGORY SUMMARY
# ==========================================================

def calculate_category_summary(
    appliances
):

    category_totals = {}

    for appliance in appliances:

        category = appliance.get(
            "category",
            "Other"
        )

        daily_kwh = safe_float(
            appliance.get(
                "daily_kwh"
            )
        )

        if category not in category_totals:

            category_totals[
                category
            ] = 0.0

        category_totals[
            category
        ] += daily_kwh

    return category_totals


# ==========================================================
# SECTION 9 - COMPLETE LOAD ANALYSIS
# ==========================================================

def analyze_appliance_load(
    appliances
):

    totals = calculate_total_energy_demand(
        appliances
    )

    contribution_data = (
        calculate_appliance_contributions(
            appliances
        )
    )

    category_summary = (
        calculate_category_summary(
            appliances
        )
    )

    sorted_appliances = (
        sort_appliances_by_energy(
            contribution_data
        )
    )

    return {

        "appliances":
            contribution_data,

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

        "category_summary":
            category_summary,

        "highest_consuming_appliances":
            sorted_appliances

    }


# ==========================================================
# SECTION 10 - VALIDATE APPLIANCE
# ==========================================================

def validate_appliance(
    wattage,
    hours_per_day,
    quantity
):

    errors = []

    wattage = safe_float(
        wattage
    )

    hours_per_day = safe_float(
        hours_per_day
    )

    quantity = safe_float(
        quantity
    )

    if wattage <= 0:

        errors.append(
            "Wattage must be greater than zero."
        )

    if hours_per_day <= 0:

        errors.append(
            "Hours per day must be greater than zero."
        )

    if hours_per_day > 24:

        errors.append(
            "Hours per day cannot exceed 24."
        )

    if quantity <= 0:

        errors.append(
            "Quantity must be greater than zero."
        )

    return {

        "valid":
            len(errors) == 0,

        "errors":
            errors

    }


# ==========================================================
# SECTION 11 - DEFAULT APPLIANCE LOOKUP
# ==========================================================

def get_default_appliance(
    appliance_name
):

    for appliance in DEFAULT_APPLIANCES:

        if (
            appliance["name"]
            ==
            appliance_name
        ):

            return dict(
                appliance
            )

    return None


# ==========================================================
# SECTION 12 - APPLIANCE NAMES
# ==========================================================

def get_appliance_names():

    return [

        appliance["name"]

        for appliance
        in DEFAULT_APPLIANCES

    ]
