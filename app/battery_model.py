
def calculate_battery_capacity(
    energy,
    autonomy_days,
    depth_of_discharge
):
    """
    Calculate battery storage requirement
    """

    battery = (
        energy * autonomy_days
    ) / (depth_of_discharge / 100)

    return battery
