def calculate_pv_size(
    energy,
    sun_hours,
    efficiency
):
    efficiency_factor = efficiency / 100

    pv_size = energy / (
        sun_hours * efficiency_factor
    )

    return pv_size



def calculate_number_of_panels(
    pv_size,
    panel_rating
):
    """
    Calculate number of solar panels required
    """

    panel_kw = panel_rating / 1000

    number = pv_size / panel_kw

    return round(number)
