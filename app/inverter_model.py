def calculate_inverter_size(
    pv_size
):
    """
    Recommended inverter capacity
    """

    inverter = pv_size * 1.25

    return inverter
