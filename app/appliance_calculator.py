# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Appliance & Load Calculator
# Version: 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Calculate household/project electrical energy demand
# from individual appliances.
#
# Features:
# - Appliance name
# - Quantity
# - Appliance wattage
# - Hours of use per day
# - Days of use per week
# - Daily energy consumption
# - Weekly energy consumption
# - Monthly energy consumption
# - Total connected load
# - Total daily energy demand
# - Total monthly energy demand
#
# ==========================================================


# ==========================================================
# SECTION 1 - DEFAULT APPLIANCE DATABASE
# ==========================================================

DEFAULT_APPLIANCES = [

    {
        "Appliance": "LED Bulb",
        "Typical_Wattage": 10
    },

    {
        "Appliance": "Ceiling Fan",
        "Typical_Wattage": 75
    },

    {
        "Appliance": "Standing Fan",
        "Typical_Wattage": 60
    },

    {
        "Appliance": "Television",
        "Typical_Wattage": 100
    },

    {
        "Appliance": "Refrigerator",
        "Typical_Wattage": 150
    },

    {
        "Appliance": "Freezer",
        "Typical_Wattage": 200
    },

    {
        "Appliance": "Laptop",
        "Typical_Wattage": 65
    },

    {
        "Appliance": "Desktop Computer",
        "Typical_Wattage": 200
    },

    {
        "Appliance": "Phone Charger",
        "Typical_Wattage": 10
    },

    {
        "Appliance": "Wi-Fi Router",
        "Typical_Wattage": 15
    },

    {
        "Appliance": "Electric Iron",
        "Typical_Wattage": 1200
    },

    {
        "Appliance": "Electric Kettle",
        "Typical_Wattage": 1500
    },

    {
        "Appliance": "Microwave",
        "Typical_Wattage": 1200
    },

    {
        "Appliance": "Washing Machine",
        "Typical_Wattage": 500
    },

    {
        "Appliance": "Air Conditioner",
        "Typical_Wattage": 1200
    },

    {
        "Appliance": "Water Pump",
        "Typical_Wattage": 750
    },

    {
        "Appliance": "Electric Cooker",
        "Typical_Wattage": 2000
    },

    {
        "Appliance": "Other",
        "Typical_Wattage": 100
    }

]


# ==========================================================
# SECTION 2 - SAFE NUMBER CONVERSION
# ==========================================================

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.

    Returns default if conversion fails.
    """

    try:

        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):

        return default


# ==========================================================
# SECTION 3 - SAFE INTEGER CONVERSION
# ==========================================================

def safe_int(value, default=0):
    """
    Safely convert a value to integer.
    """

    try:

        if value is None:
            return default

        return int(value)

    except (TypeError, ValueError):

        return default


# ==========================================================
# SECTION 4 - CALCULATE APPLIANCE ENERGY
# ==========================================================

def calculate_appliance_energy(
    wattage,
    quantity,
    hours_per_day,
    days_per_week=7
):
    """
    Calculate energy consumption for one appliance.

    Formula:

        Daily Energy (kWh)
        =
        Wattage × Quantity × Hours / 1000

    Weekly Energy (kWh)
        =
        Daily Energy × Days per Week

    Monthly Energy (kWh)
        =
        Weekly Energy × 52 / 12
    """

    wattage = safe_float(wattage)

    quantity = safe_float(
        quantity,
        default=1
    )

    hours_per_day = safe_float(
        hours_per_day
    )

    days_per_week = safe_float(
        days_per_week,
        default=7
    )

    # ------------------------------------------------------
    # Prevent negative values
    # ------------------------------------------------------

    wattage = max(
        wattage,
        0
    )

    quantity = max(
        quantity,
        0
    )

    hours_per_day = max(
        hours_per_day,
        0
    )

    days_per_week = max(
        min(days_per_week, 7),
        0
    )

    # ------------------------------------------------------
    # Connected load
    # ------------------------------------------------------

    connected_load_watts = (
        wattage
        *
        quantity
    )

    # ------------------------------------------------------
    # Daily energy
    # ------------------------------------------------------

    daily_energy_kwh = (
        connected_load_watts
        *
        hours_per_day
        /
        1000
    )

    # ------------------------------------------------------
    # Weekly energy
    # ------------------------------------------------------

    weekly_energy_kwh = (
        daily_energy_kwh
        *
        days_per_week
    )

    # ------------------------------------------------------
    # Monthly energy
    #
    # 52 weeks / 12 months ≈ 4.333 weeks/month
    # ------------------------------------------------------

    monthly_energy_kwh = (
        weekly_energy_kwh
        *
        52
        /
        12
    )

    # ------------------------------------------------------
    # Annual energy
    # ------------------------------------------------------

    annual_energy_kwh = (
        weekly_energy_kwh
        *
        52
    )

    return {

        "connected_load_watts":
            connected_load_watts,

        "daily_energy_kwh":
            daily_energy_kwh,

        "weekly_energy_kwh":
            weekly_energy_kwh,

        "monthly_energy_kwh":
            monthly_energy_kwh,

        "annual_energy_kwh":
            annual_energy_kwh

    }


# ==========================================================
# SECTION 5 - CREATE APPLIANCE RECORD
# ==========================================================

def create_appliance_record(
    appliance,
    wattage,
    quantity=1,
    hours_per_day=1,
    days_per_week=7
):
    """
    Create a complete appliance energy record.
    """

    energy = calculate_appliance_energy(

        wattage=wattage,

        quantity=quantity,

        hours_per_day=hours_per_day,

        days_per_week=days_per_week

    )

    return {

        "Appliance":
            str(appliance).strip(),

        "Wattage_W":
            safe_float(wattage),

        "Quantity":
            safe_float(
                quantity,
                default=1
            ),

        "Hours_per_Day":
            safe_float(
                hours_per_day
            ),

        "Days_per_Week":
            safe_float(
                days_per_week,
                default=7
            ),

        "Connected_Load_W":
            energy[
                "connected_load_watts"
            ],

        "Daily_Energy_kWh":
            energy[
                "daily_energy_kwh"
            ],

        "Weekly_Energy_kWh":
            energy[
                "weekly_energy_kwh"
            ],

        "Monthly_Energy_kWh":
            energy[
                "monthly_energy_kwh"
            ],

        "Annual_Energy_kWh":
            energy[
                "annual_energy_kwh"
            ]

    }


# ==========================================================
# SECTION 6 - CALCULATE TOTAL LOAD
# ==========================================================

def calculate_total_load(
    appliances
):
    """
    Calculate total connected load and energy demand
    from a list of appliance records.
    """

    if not appliances:

        return {

            "total_connected_load_w":
                0.0,

            "total_daily_energy_kwh":
                0.0,

            "total_weekly_energy_kwh":
                0.0,

            "total_monthly_energy_kwh":
                0.0,

            "total_annual_energy_kwh":
                0.0

        }

    total_connected_load = 0.0

    total_daily_energy = 0.0

    total_weekly_energy = 0.0

    total_monthly_energy = 0.0

    total_annual_energy = 0.0

    for appliance in appliances:

        if not isinstance(
            appliance,
            dict
        ):
            continue

        total_connected_load += safe_float(
            appliance.get(
                "Connected_Load_W",
                0
            )
        )

        total_daily_energy += safe_float(
            appliance.get(
                "Daily_Energy_kWh",
                0
            )
        )

        total_weekly_energy += safe_float(
            appliance.get(
                "Weekly_Energy_kWh",
                0
            )
        )

        total_monthly_energy += safe_float(
            appliance.get(
                "Monthly_Energy_kWh",
                0
            )
        )

        total_annual_energy += safe_float(
            appliance.get(
                "Annual_Energy_kWh",
                0
            )
        )

    return {

        "total_connected_load_w":
            total_connected_load,

        "total_daily_energy_kwh":
            total_daily_energy,

        "total_weekly_energy_kwh":
            total_weekly_energy,

        "total_monthly_energy_kwh":
            total_monthly_energy,

        "total_annual_energy_kwh":
            total_annual_energy

    }


# ==========================================================
# SECTION 7 - CALCULATE PEAK LOAD
# ==========================================================

def calculate_peak_load(
    appliances
):
    """
    Calculate the total connected load.

    This represents the theoretical maximum load if all
    listed appliances operate simultaneously.
    """

    result = calculate_total_load(
        appliances
    )

    return result[
        "total_connected_load_w"
    ]


# ==========================================================
# SECTION 8 - CALCULATE AVERAGE DAILY LOAD
# ==========================================================

def calculate_average_daily_load(
    appliances
):
    """
    Calculate average daily energy demand in kWh/day.
    """

    result = calculate_total_load(
        appliances
    )

    return result[
        "total_daily_energy_kwh"
    ]


# ==========================================================
# SECTION 9 - GET DEFAULT APPLIANCE DATABASE
# ==========================================================

def get_default_appliances():
    """
    Return a copy of the default appliance database.

    A copy is returned so that the original database
    cannot accidentally be modified.
    """

    return [

        item.copy()

        for item in DEFAULT_APPLIANCES

    ]


# ==========================================================
# SECTION 10 - FIND DEFAULT APPLIANCE
# ==========================================================

def get_typical_wattage(
    appliance_name
):
    """
    Return typical wattage for a known appliance.

    Returns None if the appliance is not found.
    """

    if not appliance_name:

        return None

    target = (
        str(
            appliance_name
        )
        .strip()
        .lower()
    )

    for item in DEFAULT_APPLIANCES:

        name = (
            str(
                item.get(
                    "Appliance",
                    ""
                )
            )
            .strip()
            .lower()
        )

        if name == target:

            return item.get(
                "Typical_Wattage"
            )

    return None


# ==========================================================
# SECTION 11 - VALIDATE APPLIANCE RECORD
# ==========================================================

def validate_appliance_record(
    appliance
):
    """
    Validate an appliance record.

    Returns:

        {
            "valid": True/False,
            "message": "..."
        }
    """

    if not isinstance(
        appliance,
        dict
    ):

        return {

            "valid": False,

            "message":
                "Appliance record must be a dictionary."

        }

    appliance_name = (
        str(
            appliance.get(
                "Appliance",
                ""
            )
        ).strip()
    )

    if not appliance_name:

        return {

            "valid": False,

            "message":
                "Appliance name is required."

        }

    wattage = safe_float(
        appliance.get(
            "Wattage_W"
        ),
        default=-1
    )

    if wattage < 0:

        return {

            "valid": False,

            "message":
                "Wattage cannot be negative."

        }

    quantity = safe_float(
        appliance.get(
            "Quantity"
        ),
        default=-1
    )

    if quantity <= 0:

        return {

            "valid": False,

            "message":
                "Quantity must be greater than zero."

        }

    hours = safe_float(
        appliance.get(
            "Hours_per_Day"
        ),
        default=-1
    )

    if hours < 0 or hours > 24:

        return {

            "valid": False,

            "message":
                "Hours per day must be between 0 and 24."

        }

    days = safe_float(
        appliance.get(
            "Days_per_Week"
        ),
        default=-1
    )

    if days < 0 or days > 7:

        return {

            "valid": False,

            "message":
                "Days per week must be between 0 and 7."

        }

    return {

        "valid": True,

        "message":
            "Appliance record is valid."

    }


# ==========================================================
# SECTION 12 - BUILD LOAD SUMMARY
# ==========================================================

def build_load_summary(
    appliances
):
    """
    Produce a user-friendly engineering summary.
    """

    totals = calculate_total_load(
        appliances
    )

    return {

        "number_of_appliances":
            len(appliances)
            if appliances
            else 0,

        "total_connected_load_w":
            totals[
                "total_connected_load_w"
            ],

        "total_connected_load_kw":
            totals[
                "total_connected_load_w"
            ] / 1000,

        "daily_energy_kwh":
            totals[
                "total_daily_energy_kwh"
            ],

        "weekly_energy_kwh":
            totals[
                "total_weekly_energy_kwh"
            ],

        "monthly_energy_kwh":
            totals[
                "total_monthly_energy_kwh"
            ],

        "annual_energy_kwh":
            totals[
                "total_annual_energy_kwh"
            ]

    }
