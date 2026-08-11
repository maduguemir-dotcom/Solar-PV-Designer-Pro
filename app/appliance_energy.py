# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Appliance Energy Calculation Engine
# Version: 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Calculate electricity consumption from appliances
# and determine total daily and monthly energy demand.
#
# ==========================================================


# ==========================================================
# SECTION 1 - CREATE APPLIANCE
# ==========================================================

def create_appliance(
    name,
    wattage,
    hours_per_day,
    quantity=1
):
    """
    Create a standardized appliance record.

    Parameters:
        name           Appliance name
        wattage        Power rating in watts
        hours_per_day  Daily operating hours
        quantity       Number of appliances

    Returns:
        Dictionary containing appliance information.
    """

    try:
        wattage = float(wattage)
    except (TypeError, ValueError):
        wattage = 0.0

    try:
        hours_per_day = float(hours_per_day)
    except (TypeError, ValueError):
        hours_per_day = 0.0

    try:
        quantity = int(quantity)
    except (TypeError, ValueError):
        quantity = 1

    if wattage < 0:
        wattage = 0.0

    if hours_per_day < 0:
        hours_per_day = 0.0

    if hours_per_day > 24:
        hours_per_day = 24.0

    if quantity < 1:
        quantity = 1

    return {
        "name": str(name).strip(),
        "wattage": wattage,
        "hours_per_day": hours_per_day,
        "quantity": quantity
    }


# ==========================================================
# SECTION 2 - CALCULATE APPLIANCE ENERGY
# ==========================================================

def calculate_appliance_energy(appliance):
    """
    Calculate daily energy consumption of one appliance.

    Formula:

        Energy (kWh/day)
        =
        Wattage × Hours × Quantity / 1000
    """

    if not isinstance(appliance, dict):
        return 0.0

    try:
        wattage = float(
            appliance.get(
                "wattage",
                0
            )
        )

        hours = float(
            appliance.get(
                "hours_per_day",
                0
            )
        )

        quantity = float(
            appliance.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):
        return 0.0

    if wattage < 0:
        wattage = 0.0

    if hours < 0:
        hours = 0.0

    if quantity < 0:
        quantity = 0.0

    daily_energy = (
        wattage
        *
        hours
        *
        quantity
        /
        1000
    )

    return daily_energy


# ==========================================================
# SECTION 3 - CALCULATE TOTAL DAILY ENERGY
# ==========================================================

def calculate_total_daily_energy(appliances):
    """
    Calculate total daily energy consumption.

    Parameters:
        appliances:
            List of appliance dictionaries.

    Returns:
        Total kWh/day.
    """

    if not isinstance(
        appliances,
        list
    ):
        return 0.0

    total = 0.0

    for appliance in appliances:

        total += calculate_appliance_energy(
            appliance
        )

    return total


# ==========================================================
# SECTION 4 - CALCULATE TOTAL MONTHLY ENERGY
# ==========================================================

def calculate_total_monthly_energy(
    appliances,
    days_per_month=30
):
    """
    Calculate total monthly energy consumption.

    Default:
        30 days/month.

    Returns:
        Total kWh/month.
    """

    daily_energy = (
        calculate_total_daily_energy(
            appliances
        )
    )

    try:
        days = float(
            days_per_month
        )
    except (TypeError, ValueError):
        days = 30.0

    if days < 0:
        days = 0.0

    return (
        daily_energy
        *
        days
    )


# ==========================================================
# SECTION 5 - CALCULATE APPLIANCE LOAD
# ==========================================================

def calculate_appliance_load(appliance):
    """
    Calculate the instantaneous power demand
    of an appliance.

    Formula:

        Load (W)
        =
        Wattage × Quantity
    """

    if not isinstance(
        appliance,
        dict
    ):
        return 0.0

    try:

        wattage = float(
            appliance.get(
                "wattage",
                0
            )
        )

        quantity = float(
            appliance.get(
                "quantity",
                1
            )
        )

    except (TypeError, ValueError):

        return 0.0

    return (
        wattage
        *
        quantity
    )


# ==========================================================
# SECTION 6 - CALCULATE TOTAL CONNECTED LOAD
# ==========================================================

def calculate_total_connected_load(
    appliances
):
    """
    Calculate total connected appliance load.

    Returns:
        Total watts.
    """

    if not isinstance(
        appliances,
        list
    ):
        return 0.0

    total_load = 0.0

    for appliance in appliances:

        total_load += (
            calculate_appliance_load(
                appliance
            )
        )

    return total_load


# ==========================================================
# SECTION 7 - CREATE ENERGY SUMMARY
# ==========================================================

def create_energy_summary(
    appliances
):
    """
    Create a complete appliance-energy summary.
    """

    daily_energy = (
        calculate_total_daily_energy(
            appliances
        )
    )

    monthly_energy = (
        calculate_total_monthly_energy(
            appliances
        )
    )

    connected_load = (
        calculate_total_connected_load(
            appliances
        )
    )

    return {

        "daily_energy_kwh":
            daily_energy,

        "monthly_energy_kwh":
            monthly_energy,

        "connected_load_w":
            connected_load,

        "connected_load_kw":
            connected_load / 1000

    }


# ==========================================================
# SECTION 8 - MODULE TEST
# ==========================================================

def test_appliance_energy():
    """
    Basic internal test for the appliance-energy engine.
    """

    appliances = [

        create_appliance(
            name="TV",
            wattage=100,
            hours_per_day=5,
            quantity=1
        ),

        create_appliance(
            name="Fan",
            wattage=75,
            hours_per_day=8,
            quantity=2
        )

    ]

    summary = create_energy_summary(
        appliances
    )

    return summary
