# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.2
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# v2.2 Features:
# - Existing solar database
# - Worldwide place search
# - Global coordinate input
# - OpenStreetMap/Nominatim geocoding
# - NASA POWER solar-resource integration
# - PV sizing
# - Battery sizing
# - Inverter sizing
# - Carbon reduction estimation
# - AI Solar Advisor
# - PDF report generation
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st


# ----------------------------------------------------------
# Engineering calculations
# ----------------------------------------------------------

from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_carbon
)


# ----------------------------------------------------------
# Solar database
# ----------------------------------------------------------

from data_loader import (
    load_solar_database,
    get_location_data
)


# ----------------------------------------------------------
# AI Solar Advisor
# ----------------------------------------------------------

from ai import (
    generate_ai_recommendations
)


# ----------------------------------------------------------
# PDF Report Generator
# ----------------------------------------------------------

from reports import (
    create_pdf_report
)


# ----------------------------------------------------------
# Utility functions
# ----------------------------------------------------------

from utils import (
    format_currency
)


# ----------------------------------------------------------
# Global Location Engine
# ----------------------------------------------------------

from location_engine import (
    get_location_solar_resource,
    get_location_summary
)


# ----------------------------------------------------------
# Worldwide Location Search
# ----------------------------------------------------------

from location_search import (
    search_location,
    format_search_result
)


# ==========================================================
# SECTION 2 - APPLICATION CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar PV Designer Pro Africa",
    page_icon="☀️",
    layout="wide"
)


# ==========================================================
# SECTION 3 - APPLICATION HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "AI-Ready Renewable Energy Design Platform"
)

st.write(
    """
    Solar PV Designer Pro Africa™ is a renewable energy
    engineering platform designed to support preliminary
    photovoltaic system sizing, battery analysis, cost
    estimation, environmental assessment and AI-assisted
    recommendations.
    """
)


# ==========================================================
# SECTION 4 - LOAD SOLAR DATABASE
# ==========================================================

try:

    solar_database = load_solar_database()

except Exception as error:

    st.error(
        f"Unable to load solar database: {error}"
    )

    st.stop()


# ==========================================================
# SECTION 5 - SIDEBAR
# ==========================================================

st.sidebar.header(
    "⚙️ System Design Inputs"
)


# ==========================================================
# SECTION 6 - LOCATION SOURCE
# ==========================================================

st.sidebar.subheader(
    "📍 Project Location"
)

location_source = st.sidebar.radio(
    "Choose location method:",
    [
        "Solar Database",
        "Search for a Place",
        "Enter Coordinates"
    ]
)


# ==========================================================
# SECTION 7 - INITIAL LOCATION VARIABLES
# ==========================================================

location_description = "Not selected"

latitude = None
longitude = None

sun_hours = None
temperature = None

solar_data = None
solar_summary = None
location_summary = None


# ==========================================================
# SECTION 8 - SOLAR DATABASE LOCATION
# ==========================================================

if location_source == "Solar Database":

    location = st.sidebar.selectbox(
        "Select Location",
        solar_database["Location"].tolist()
    )


    location_data = get_location_data(
        solar_database,
        location
    )


    if location_data is None:

        st.error(
            "Selected location could not be found."
        )

        st.stop()


    sun_hours = float(
        location_data["Peak_Sun_Hours"]
    )


    temperature = float(
        location_data["Average_Temperature"]
    )


    latitude = None
    longitude = None

    location_description = location


# ==========================================================
# SECTION 9 - WORLDWIDE PLACE SEARCH
# ==========================================================

elif location_source == "Search for a Place":

    st.sidebar.info(
        """
        Search for almost any city, town or place
        in the world.

        Example:
        Kano, Nigeria
        Kampala, Uganda
        London, UK
        Dubai, UAE
        Tokyo, Japan
        """
    )


    # ------------------------------------------------------
    # Search box
    # ------------------------------------------------------

    search_query = st.sidebar.text_input(
        "🔎 Search for a location",
        value="Kano, Nigeria",
        placeholder="Example: Kano, Nigeria"
    )


    search_button = st.sidebar.button(
        "🔎 Search",
        use_container_width=True
    )


    # ------------------------------------------------------
    # Search results
    # ------------------------------------------------------

    search_results = []


    if search_button:

        if not search_query.strip():

            st.sidebar.warning(
                "Please enter a location to search."
            )

        else:

            with st.sidebar:

                with st.spinner(
                    "Searching worldwide..."
                ):

                    search_results = search_location(
                        search_query,
                        limit=5
                    )


            if not search_results:

                st.sidebar.error(
                    "No locations were found."
                )


    # ------------------------------------------------------
    # Store results in session state
    # ------------------------------------------------------

    if search_results:

        st.session_state[
            "location_search_results"
        ] = search_results


    saved_results = st.session_state.get(
        "location_search_results",
        []
    )


    # ------------------------------------------------------
    # Display available results
    # ------------------------------------------------------

    if saved_results:

        result_labels = [
            format_search_result(
                result
            )
            for result in saved_results
        ]


        selected_label = st.sidebar.selectbox(
            "Select a search result",
            result_labels
        )


        selected_index = (
            result_labels.index(
                selected_label
            )
        )


        selected_location = (
            saved_results[
                selected_index
            ]
        )


        # --------------------------------------------------
        # Coordinates from search
        # --------------------------------------------------

        latitude = float(
            selected_location[
                "latitude"
            ]
        )


        longitude = float(
            selected_location[
                "longitude"
            ]
        )


        location_name = (
            selected_location.get(
                "name",
                ""
            )
        )


        country = (
            selected_location.get(
                "country",
                ""
            )
        )


        # --------------------------------------------------
        # Connect selected location to NASA POWER
        # --------------------------------------------------

        with st.spinner(
            "Retrieving NASA POWER solar data..."
        ):

            location_result = (
                get_location_solar_resource(

                    latitude=latitude,

                    longitude=longitude,

                    location_name=location_name,

                    country=country

                )
            )


        if not location_result["success"]:

            st.sidebar.error(
                "NASA POWER lookup failed: "
                + str(
                    location_result[
                        "message"
                    ]
                )
            )

            st.stop()


        # --------------------------------------------------
        # Extract NASA summary
        # --------------------------------------------------

        location_summary = (
            get_location_summary(
                location_result
            )
        )


        solar_data = (
            location_result.get(
                "solar"
            )
        )


        solar_summary = (
            location_result.get(
                "summary"
            )
        )


        sun_hours = (
            location_summary.get(
                "peak_sun_hours"
            )
        )


        temperature = (
            location_summary.get(
                "average_temperature"
            )
        )


        if sun_hours is None:

            st.sidebar.error(
                "NASA POWER did not return usable "
                "solar-resource data."
            )

            st.stop()


        if temperature is None:

            temperature = 25.0


        location_description = (
            location_summary.get(
                "location",
                selected_location.get(
                    "display_name",
                    "Selected Location"
                )
            )
        )


        st.sidebar.success(
            "🌍 Location connected to NASA POWER."
        )


    else:

        # --------------------------------------------------
        # No search result selected yet
        # --------------------------------------------------

        latitude = None
        longitude = None

        location_description = (
            "Search for a location"
        )


# ==========================================================
# SECTION 10 - GLOBAL COORDINATE LOCATION
# ==========================================================

else:

    st.sidebar.info(
        """
        Enter the geographical coordinates of your
        project site.

        Latitude: -90 to +90

        Longitude: -180 to +180

        NASA POWER will provide solar-resource
        information for the selected location.
        """
    )


    latitude = st.sidebar.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=0.3476,
        step=0.0001,
        format="%.4f"
    )


    longitude = st.sidebar.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=32.5825,
        step=0.0001,
        format="%.4f"
    )


    location_name = st.sidebar.text_input(
        "Location Name",
        value="Kampala"
    )


    country = st.sidebar.text_input(
        "Country",
        value="Uganda"
    )


    # ------------------------------------------------------
    # NASA POWER
    # ------------------------------------------------------

    with st.spinner(
        "Connecting coordinates to NASA POWER..."
    ):

        location_result = (
            get_location_solar_resource(

                latitude=latitude,

                longitude=longitude,

                location_name=location_name,

                country=country

            )
        )


    if not location_result["success"]:

        st.sidebar.error(
            "NASA POWER location lookup failed: "
            + str(
                location_result[
                    "message"
                ]
            )
        )

        st.stop()


    location_summary = (
        get_location_summary(
            location_result
        )
    )


    solar_data = (
        location_result.get(
            "solar"
        )
    )


    solar_summary = (
        location_result.get(
            "summary"
        )
    )


    sun_hours = (
        location_summary.get(
            "peak_sun_hours"
        )
    )


    temperature = (
        location_summary.get(
            "average_temperature"
        )
    )


    if sun_hours is None:

        st.sidebar.error(
            "NASA POWER did not return usable "
            "solar-resource data."
        )

        st.stop()


    if temperature is None:

        temperature = 25.0


    location_description = (
        location_summary.get(
            "location",
            f"{latitude:.4f}°, "
            f"{longitude:.4f}°"
        )
    )


    st.sidebar.success(
        "🌍 Coordinates connected to NASA POWER."
    )


# ==========================================================
# SECTION 11 - ENERGY DEMAND
# ==========================================================

energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    min_value=0.1,
    value=5.0,
    step=0.5
)


# ==========================================================
# SECTION 12 - SYSTEM EFFICIENCY
# ==========================================================

efficiency_percent = st.sidebar.slider(
    "Overall System Efficiency (%)",
    min_value=50,
    max_value=100,
    value=80
)


efficiency = (
    efficiency_percent / 100
)


# ==========================================================
# SECTION 13 - BATTERY
# ==========================================================

battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


# ==========================================================
# SECTION 14 - BATTERY AUTONOMY
# ==========================================================

days = st.sidebar.number_input(
    "Battery Backup / Autonomy (Days)",
    min_value=1,
    max_value=30,
    value=3
)


# ==========================================================
# SECTION 15 - SOLAR PANEL
# ==========================================================

panel_rating = st.sidebar.selectbox(
    "Solar Panel Rating (Watts)",
    [
        450,
        550,
        600
    ]
)


# ==========================================================
# SECTION 16 - SOLAR RESOURCE INFORMATION
# ==========================================================

st.header(
    "📍 Solar Resource Information"
)


location_col1, location_col2, location_col3 = (
    st.columns(3)
)


location_col1.metric(
    "Location",
    location_description
)


if latitude is None:

    latitude_display = "Database"

else:

    latitude_display = (
        f"{latitude:.4f}°"
    )


location_col2.metric(
    "Latitude",
    latitude_display
)


if longitude is None:

    longitude_display = "Database"

else:

    longitude_display = (
        f"{longitude:.4f}°"
    )


location_col3.metric(
    "Longitude",
    longitude_display
)


# ==========================================================
# SECTION 17 - SOLAR RESOURCE METRICS
# ==========================================================

solar_info_col1, solar_info_col2, solar_info_col3 = (
    st.columns(3)
)


solar_info_col1.metric(
    "☀️ Peak Sun Hours",
    f"{sun_hours:.2f} h/day"
)


solar_info_col2.metric(
    "🌡️ Average Temperature",
    f"{temperature:.1f} °C"
)


if location_source == "Solar Database":

    solar_info_col3.metric(
        "📡 Data Source",
        "Solar Database"
    )

else:

    solar_info_col3.metric(
        "📡 Data Source",
        "NASA POWER"
    )


# ==========================================================
# SECTION 18 - SOLAR DATA INFORMATION
# ==========================================================

if location_source == "Solar Database":

    st.info(
        f"""
        **Solar Resource**

        Peak Sun Hours:
        {sun_hours:.2f} hours/day

        Average Temperature:
        {temperature:.1f} °C

        Source:
        Existing Solar Database
        """
    )


else:

    climatology_period = (
        location_summary.get(
            "climatology_period",
            "NASA POWER"
        )
        if location_summary
        else "NASA POWER"
    )


    st.info(
        f"""
        **Live Solar Resource**

        Peak Sun Hours:
        {sun_hours:.2f} hours/day

        Average Temperature:
        {temperature:.1f} °C

        Source:
        NASA POWER

        Climatology:
        {climatology_period}
        """
    )


# ==========================================================
# SECTION 19 - NASA MONTHLY DATA
# ==========================================================

if (
    location_source != "Solar Database"
    and solar_data is not None
):

    with st.expander(
        "☀️ View NASA POWER Solar Data"
    ):

        # ----------------------------------------------
        # Try to display monthly data
        # ----------------------------------------------

        monthly_display = (
            solar_data.get(
                "monthly_display",
                []
            )
            if isinstance(
                solar_data,
                dict
            )
            else []
        )


        if monthly_display:

            st.dataframe(
                monthly_display,
                use_container_width=True
            )

        else:

            # ------------------------------------------
            # Show complete data if monthly display
            # is not available.
            # ------------------------------------------

            st.json(
                solar_data
            )


# ==========================================================
# SECTION 20 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary"
)


# ==========================================================
# SECTION 21 - ENGINEERING CALCULATIONS
# ==========================================================

if design_button:

    # ------------------------------------------------------
    # PV capacity
    # ------------------------------------------------------

    pv_size = calculate_pv_size(

        energy=energy,

        sun_hours=sun_hours,

        efficiency=efficiency,

        temperature=temperature

    )


    # ------------------------------------------------------
    # Solar panels
    # ------------------------------------------------------

    panels = calculate_panels(

        pv_size=pv_size,

        panel_rating=panel_rating

    )


    # ------------------------------------------------------
    # Battery
    # ------------------------------------------------------

    battery_capacity = calculate_battery(

        energy=energy,

        days=days,

        battery_type=battery_type

    )


    # ------------------------------------------------------
    # Inverter
    # ------------------------------------------------------

    inverter_size = calculate_inverter(
        pv_size
    )


    # ------------------------------------------------------
    # Charge controller
    # ------------------------------------------------------

    controller_current = (
        pv_size * 1000 / 48
    )


    # ------------------------------------------------------
    # Cost estimation
    # ------------------------------------------------------

    panel_cost = (
        pv_size * 800
    )


    battery_cost = (
        battery_capacity * 300
    )


    inverter_cost = (
        inverter_size * 250
    )


    equipment_cost = (
        panel_cost
        +
        battery_cost
        +
        inverter_cost
    )


    installation_cost = (
        equipment_cost * 0.15
    )


    total_cost = (
        equipment_cost
        +
        installation_cost
    )


    # ------------------------------------------------------
    # Environmental impact
    # ------------------------------------------------------

    carbon_reduction = calculate_carbon(
        energy
    )


    # ======================================================
    # SECTION 22 - ENGINEERING RESULTS
    # ======================================================

    st.header(
        "📊 Solar PV Design Results"
    )


    result_col1, result_col2, result_col3 = (
        st.columns(3)
    )


    result_col1.metric(
        "PV Capacity",
        f"{pv_size:.2f} kW"
    )


    result_col2.metric(
        "Battery Capacity",
        f"{battery_capacity:.2f} kWh"
    )


    result_col3.metric(
        "Inverter",
        f"{inverter_size:.2f} kW"
    )


    st.divider()


    # ======================================================
    # SECTION 23 - EQUIPMENT RECOMMENDATION
    # ======================================================

    st.subheader(
        "⚡ Recommended Equipment"
    )


    equipment_col1, equipment_col2 = (
        st.columns(2)
    )


    with equipment_col1:

        st.write(
            f"""
            **☀️ Solar Array**

            {panels} × {panel_rating} W panels

            **🔋 Battery**

            {battery_type}

            {battery_capacity:.2f} kWh
            """
        )


    with equipment_col2:

        st.write(
            f"""
            **🔌 Inverter**

            {inverter_size:.2f} kW

            **⚡ Charge Controller**

            Approximately {controller_current:.1f} A

            **💰 Estimated System Cost**

            {format_currency(total_cost)}
            """
        )


    st.success(
        f"Estimated annual CO₂ reduction: "
        f"{carbon_reduction:,.0f} kg/year"
    )


    # ======================================================
    # SECTION 24 - AI SOLAR ADVISOR
    # ======================================================

    st.divider()


    st.header(
        "🤖 AI Solar Advisor"
    )


    recommendations = (
        generate_ai_recommendations(

            location=location_description,

            battery_type=battery_type,

            pv_size=pv_size,

            battery_capacity=battery_capacity,

            inverter_size=inverter_size,

            energy=energy,

            carbon_reduction=carbon_reduction

        )
    )


    for recommendation in recommendations:

        st.success(
            recommendation
        )


    # ======================================================
    # SECTION 25 - PDF REPORT DATA
    # ======================================================

    report_data = {

        "location":
            location_description,

        "energy":
            energy,

        "sun_hours":
            sun_hours,

        "temperature":
            temperature,

        "battery_type":
            battery_type,

        "days":
            days,

        "pv":
            pv_size,

        "panels":
            panels,

        "panel_rating":
            panel_rating,

        "battery":
            battery_capacity,

        "inverter":
            inverter_size,

        "controller":
            controller_current,

        "panel_cost":
            panel_cost,

        "battery_cost":
            battery_cost,

        "inverter_cost":
            inverter_cost,

        "installation_cost":
            installation_cost,

        "cost":
            total_cost,

        "carbon":
            carbon_reduction,

        "data_source":
            (
                "Solar Database"
                if location_source ==
                "Solar Database"
                else
                "NASA POWER"
            )

    }


    # ------------------------------------------------------
    # Coordinates
    # ------------------------------------------------------

    if latitude is not None:

        report_data[
            "latitude"
        ] = latitude


    if longitude is not None:

        report_data[
            "longitude"
        ] = longitude


    # ------------------------------------------------------
    # NASA climatology
    # ------------------------------------------------------

    if (
        location_source !=
        "Solar Database"
        and location_summary
    ):

        report_data[
            "climatology_period"
        ] = location_summary.get(
            "climatology_period"
        )


    # ======================================================
    # SECTION 26 - PDF REPORT
    # ======================================================

    st.divider()


    st.header(
        "📄 Solar Design Report"
    )


    try:

        pdf_report = create_pdf_report(

            data=report_data,

            recommendations=recommendations

        )


        st.download_button(

            label=(
                "📥 Download Professional PDF Report"
            ),

            data=pdf_report,

            file_name=(
                "Solar_PV_Design_Report.pdf"
            ),

            mime="application/pdf"

        )

    except Exception as error:

        st.error(
            "Unable to generate PDF report: "
            f"{error}"
        )


# ==========================================================
# SECTION 27 - FOOTER
# ==========================================================

st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™ v2.2

    Worldwide Location Search + NASA POWER

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
