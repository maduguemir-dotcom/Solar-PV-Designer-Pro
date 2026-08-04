
def calculate_pv_size(
    energy,
    sun_hours,
    efficiency
):
    """
    Calculate required solar PV capacity
    """

    efficiency_factor = efficiency / 100

    pv_size = energy / (
        sun_hours * efficiency_factor
    )

    return pv_size
