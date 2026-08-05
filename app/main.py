import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet

def ai_recommendation(
    location,
    battery_type,
    pv_size,
    battery_capacity,
    carbon
):

    advice = []

    advice.append(
        f"Location: {location} has suitable solar resources."
    )

    if battery_type == "Lithium-ion":

        advice.append(
            "Lithium-ion batteries are recommended because they offer higher usable capacity and a longer service life."
        )

    else:

        advice.append(
            "Lead-acid batteries have a lower initial cost but require more maintenance and have a shorter lifespan."
        )

    if pv_size < 2:

        advice.append(
            "This system is appropriate for a small household or office."
        )

    elif pv_size < 5:

        advice.append(
            "This system is suitable for medium-sized homes or small businesses."
        )

    else:

        advice.append(
            "This design is suitable for commercial facilities or institutions."
        )

    advice.append(
        "A 48 V DC system is recommended for improved efficiency and future expansion."
    )

    advice.append(
        f"Estimated annual CO₂ reduction is approximately {carbon:.0f} kg."
    )

    return advice
# ==========================================
# Solar PV Designer Pro Africa™
# Version 1.3
# PDF Report Edition
# ==========================================


st.set_page_config(
    page_title="Solar PV Designer Pro Africa",
    page_icon="☀️",
    layout="wide"
)


# ==========================================
# PDF REPORT FUNCTION
# ==========================================


def create_pdf_report(data):

    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer
    )

    styles = getSampleStyleSheet()

    content = []


    title = Paragraph(
        "Solar PV Designer Pro Africa™<br/>"
        "Renewable Energy System Design Report",
        styles["Title"]
    )

    content.append(title)

    content.append(
        Spacer(1, 20)
    )


    content.append(
        Paragraph(
            f"Prepared by: Engr. Prof. Ibrahim Sani Madugu<br/>"
            f"Report Date: {date.today()}",
            styles["Normal"]
        )
    )


    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            "1. Project Summary",
            styles["Heading2"]
        )
    )


    summary = [

        ["Parameter","Value"],

        ["Location", data["location"]],

        ["Energy Demand",
         f'{data["energy"]} kWh/day'],

        ["Battery Type",
         data["battery_type"]],

        ["Autonomy",
         f'{data["days"]} days']

    ]


    table = Table(summary)


    table.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None)
            ]
        )
    )


    content.append(table)


    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            "2. Technical Design Results",
            styles["Heading2"]
        )
    )


    technical = [

        ["Design Parameter","Result"],

        ["PV Capacity",
         f'{data["pv"]:.2f} kW'],

        ["Solar Panels",
         f'{data["panels"]} panels'],

        ["Battery Capacity",
         f'{data["battery"]:.2f} kWh'],

        ["Inverter Size",
         f'{data["inverter"]:.2f} kW']

    ]


    table2 = Table(
        technical
    )


    table2.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None)
            ]
        )
    )


    content.append(table2)


    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            "3. Economic and Environmental Analysis",
            styles["Heading2"]
        )
    )


    economic = [

        ["Item","Value"],

        ["Estimated Cost",
         f'${data["cost"]:,.0f}'],

        ["Annual CO₂ Reduction",
         f'{data["carbon"]:,.0f} kg/year']

    ]


    table3 = Table(
        economic
    )


    table3.setStyle(
        TableStyle(
            [
                ("GRID",(0,0),(-1,-1),0.5,None)
            ]
        )
    )


    content.append(table3)


    content.append(
        Spacer(1,20)
    )


    content.append(
        Paragraph(
            "Engineering Note: "
            "This preliminary design should be verified "
            "by a qualified solar engineer before installation.",
            styles["Normal"]
        )
    )


    document.build(
        content
    )


    buffer.seek(0)

    return buffer



# ==========================================
# APPLICATION INTERFACE
# ==========================================


st.title(
    "☀️ Solar PV Designer Pro Africa™ v1.3"
)


st.subheader(
    "Intelligent Solar Design and Reporting Platform"
)


try:

    solar_data = pd.read_csv(
        "data/solar_locations.csv"
    )


except:

    st.error(
        "Solar database missing. Check data/solar_locations.csv"
    )

    st.stop()



# Sidebar

st.sidebar.header(
    "System Inputs"
)


location = st.sidebar.selectbox(
    "Select Location",
    solar_data["Location"]
)


location_data = solar_data[
    solar_data["Location"] == location
]


sun_hours = float(
    location_data["Peak_Sun_Hours"].values[0]
)


temperature = float(
    location_data["Average_Temperature"].values[0]
)


energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    value=5.0
)


battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


days = st.sidebar.number_input(
    "Battery Backup Days",
    value=3
)


efficiency = st.sidebar.slider(
    "System Efficiency (%)",
    50,
    100,
    80
)


panel_rating = st.sidebar.selectbox(
    "Panel Rating (Watts)",
    [450,550,600]
)# ==========================================
# SYSTEM CALCULATION
# ==========================================


if st.button(
    "🚀 Design Solar PV System"
):


    # Temperature correction

    temperature_factor = 1


    if temperature > 25:

        temperature_factor = (
            1 +
            ((temperature - 25) * 0.005)
        )



    # PV Calculation

    pv_size = energy / (
        sun_hours *
        (efficiency / 100)
    )


    pv_size = (
        pv_size *
        temperature_factor
    )



    # Number of panels

    panel_kw = (
        panel_rating / 1000
    )


    panels = round(
        pv_size /
        panel_kw
    )



    # Battery Calculation


    if battery_type == "Lithium-ion":

        dod = 0.90

    else:

        dod = 0.50



    battery_capacity = (
        energy *
        days
    ) / dod



    # Inverter

    inverter_size = (
        pv_size *
        1.25
    )



    # Charge Controller

    controller = (
        pv_size *
        1000 /
        48
    )



    # Cost Calculation


    panel_cost = (
        pv_size *
        800
    )


    battery_cost = (
        battery_capacity *
        300
    )


    inverter_cost = (
        inverter_size *
        250
    )


    installation_cost = (
        panel_cost +
        battery_cost +
        inverter_cost
    ) * 0.15



    total_cost = (
        panel_cost +
        battery_cost +
        inverter_cost +
        installation_cost
    )



    # Carbon Reduction

    carbon_reduction = (
        energy *
        365 *
        0.45
    )



    # ======================================
    # DISPLAY RESULTS
    # ======================================


    st.header(
        "📊 Solar System Design Results"
    )


    c1,c2,c3 = st.columns(3)


    c1.metric(
        "PV Capacity",
        f"{pv_size:.2f} kW"
    )


    c2.metric(
        "Battery",
        f"{battery_capacity:.2f} kWh"
    )


    c3.metric(
        "Inverter",
        f"{inverter_size:.2f} kW"
    )



    st.divider()



    st.subheader(
        "Recommended Equipment"
    )


    st.write(
        f"""
        ☀️ Solar Panels:

        **{panels} × {panel_rating}W panels**


        🔋 Battery:

        **{battery_type}**


        ⚡ Charge Controller:

        **{controller:.1f} A**


        📍 Location:

        **{location}**


        🌡️ Temperature:

        **{temperature} °C**


        💰 Estimated Cost:

        **${total_cost:,.0f}**
        """
    )



    st.success(
        f"Annual CO₂ Reduction: {carbon_reduction:,.0f} kg/year"
    )



    # ======================================
    # CREATE PDF REPORT
    # ======================================


    report_data = {

        "location": location,

        "energy": energy,

        "battery_type": battery_type,

        "days": days,

        "pv": pv_size,

        "panels": panels,

        "battery": battery_capacity,

        "inverter": inverter_size,

        "cost": total_cost,

        "carbon": carbon_reduction

    }



    pdf = create_pdf_report(
        report_data
    )



    st.download_button(

        label="📄 Download Solar Design Report (PDF)",

        data=pdf,

        file_name=
        "Solar_PV_Design_Report.pdf",

        mime=
        "application/pdf"

    )



# ==========================================
# Footer
# ==========================================


st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™ v1.3

    Intelligent Renewable Energy Design Platform

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
    )
