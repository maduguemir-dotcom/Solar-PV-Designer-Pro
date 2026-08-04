def calculate_battery_capacity(
    energy,
    autonomy_days,
    battery_type
):

    if battery_type == "Lithium":

        dod = 0.90

    else:

        dod = 0.50


    battery = (
        energy * autonomy_days
    ) / dod


    return battery
