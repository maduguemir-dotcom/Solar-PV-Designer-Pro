
def calculate_cost(
    pv_size,
    battery_capacity,
    inverter_size
):

    panel_cost = pv_size * 800

    battery_cost = battery_capacity * 300

    inverter_cost = inverter_size * 250


    installation = (
        panel_cost +
        battery_cost +
        inverter_cost
    ) * 0.15


    total = (
        panel_cost +
        battery_cost +
        inverter_cost +
        installation
    )


    return total
