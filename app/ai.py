# ==========================================================
# Solar PV Designer Pro Africa™
# AI Solar Advisor Module
# Version 2.0
# ==========================================================


# ==========================================================
# SECTION 1 - AI SOLAR ADVISOR
# ==========================================================

def generate_ai_recommendations(
    location,
    battery_type,
    pv_size,
    battery_capacity,
    inverter_size,
    energy,
    carbon_reduction
):
    """
    Generate engineering recommendations
    based on the calculated solar system.

    Parameters:
        location: Selected geographical location
        battery_type: Selected battery technology
        pv_size: Required PV capacity in kW
        battery_capacity: Required battery capacity in kWh
        inverter_size: Recommended inverter size in kW
        energy: Daily energy consumption in kWh
        carbon_reduction: Estimated annual CO2 reduction

    Returns:
        A list of recommendations.
    """

    recommendations = []


    # ======================================================
    # SECTION 2 - LOCATION RECOMMENDATION
    # ======================================================

    recommendations.append(
        f"The proposed system has been designed for {location}."
    )


    # ======================================================
    # SECTION 3 - SYSTEM SIZE ANALYSIS
    # ======================================================

    if pv_size < 2:

        recommendations.append(
            "The proposed PV capacity is suitable for "
            "a small household, office or similar low-energy application."
        )

    elif pv_size < 5:

        recommendations.append(
            "The proposed PV capacity is suitable for "
            "a medium-sized household, small business or office."
        )

    elif pv_size < 10:

        recommendations.append(
            "The proposed PV capacity is suitable for "
            "a relatively large household, business or institutional application."
        )

    else:

        recommendations.append(
            "The proposed PV capacity indicates a relatively large "
            "commercial or institutional energy requirement."
        )


    # ======================================================
    # SECTION 4 - BATTERY RECOMMENDATION
    # ======================================================

    if battery_type == "Lithium-ion":

        recommendations.append(
            "Lithium-ion storage is recommended where higher usable "
            "capacity, deeper discharge and longer service life are priorities."
        )

    else:

        recommendations.append(
            "Lead-acid storage can provide a lower initial cost, "
            "but its usable capacity and expected service life are generally "
            "lower than lithium-ion technology."
        )


    # ======================================================
    # SECTION 5 - INVERTER ANALYSIS
    # ======================================================

    if inverter_size < 3:

        recommendations.append(
            "The calculated inverter capacity is appropriate for "
            "a relatively small solar installation."
        )

    elif inverter_size < 10:

        recommendations.append(
            "The calculated inverter capacity is appropriate for "
            "a medium-scale solar installation."
        )

    else:

        recommendations.append(
            "The calculated inverter capacity indicates a larger "
            "commercial or institutional installation."
        )


    # ======================================================
    # SECTION 6 - ENERGY DEMAND ANALYSIS
    # ======================================================

    if energy <= 5:

        recommendations.append(
            "The estimated daily energy demand is relatively modest. "
            "Energy-efficiency measures can further reduce the required "
            "PV and battery capacity."
        )

    elif energy <= 15:

        recommendations.append(
            "The energy demand is moderate. Consider prioritizing "
            "energy-efficient appliances and load management."
        )

    else:

        recommendations.append(
            "The energy demand is relatively high. A detailed load "
            "assessment and hourly consumption profile are recommended."
        )


    # ======================================================
    # SECTION 7 - BATTERY CAPACITY ANALYSIS
    # ======================================================

    if battery_capacity > 20:

        recommendations.append(
            "The required battery storage is relatively large. "
            "Consider modular battery banks to simplify future expansion "
            "and maintenance."
        )

    else:

        recommendations.append(
            "The calculated battery capacity is suitable for the "
            "specified autonomy requirement, subject to final load verification."
        )


    # ======================================================
    # SECTION 8 - SYSTEM VOLTAGE RECOMMENDATION
    # ======================================================

    if pv_size <= 2:

        recommendations.append(
            "A 24 V or 48 V architecture may be considered depending "
            "on the final battery and inverter configuration."
        )

    else:

        recommendations.append(
            "A 48 V battery architecture is recommended for improved "
            "efficiency and reduced DC current in larger systems."
        )


    # ======================================================
    # SECTION 9 - ENVIRONMENTAL IMPACT
    # ======================================================

    recommendations.append(
        f"The estimated annual CO₂ reduction is approximately "
        f"{carbon_reduction:,.0f} kg/year."
    )


    # ======================================================
    # SECTION 10 - ENGINEERING SAFETY NOTE
    # ======================================================

    recommendations.append(
        "The AI recommendations are preliminary engineering guidance. "
        "Final equipment selection, protection, wiring, structural design "
        "and installation should be verified by a qualified solar engineer."
    )


    return recommendations
