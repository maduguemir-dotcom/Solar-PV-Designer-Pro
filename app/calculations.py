# ==========================================================
# Solar PV Designer Pro Africa™
# Engineering Calculations
# Version 2.0
# ==========================================================


from config import (
    TEMPERATURE_REFERENCE,
    TEMPERATURE_COEFFICIENT,
    PANEL_COST_PER_KW,
    BATTERY_COST_PER_KWH,
    INVERTER_COST_PER_KW,
    CO2_FACTOR
)



def calculate_pv_size(
        energy,
        sun_hours,
        efficiency,
        temperature):

    """
    Calculate required PV capacity
    """

    pv = energy / (
        sun_hours *
        efficiency
    )


    if temperature > TEMPERATURE_REFERENCE:

        factor = 1 + (
            (temperature -
             TEMPERATURE_REFERENCE)
            *
            TEMPERATURE_COEFFICIENT
        )

        pv *= factor


    return pv



def calculate_panels(
        pv_size,
        panel_rating):

    panel_kw = panel_rating / 1000

    return round(
        pv_size / panel_kw
    )



def calculate_battery(
        energy,
        days,
        battery_type):


    if battery_type == "Lithium-ion":

        dod = 0.90

    else:

        dod = 0.50


    return (
        energy *
        days
    ) / dod



def calculate_inverter(
        pv_size):

    return pv_size * 1.25



def calculate_cost(
        pv,
        battery,
        inverter):


    cost = (

        pv *
        PANEL_COST_PER_KW

        +

        battery *
        BATTERY_COST_PER_KWH

        +

        inverter *
        INVERTER_COST_PER_KW

    )


    installation = cost * 0.15


    return cost + installation



def calculate_carbon(
        energy):

    return (
        energy *
        365 *
        CO2_FACTOR
    )
