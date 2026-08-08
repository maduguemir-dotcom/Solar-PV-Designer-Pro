# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.2.1
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# v2.2.1 Features:
# - Existing solar database
# - Worldwide place search
# - Global coordinate input
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


from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_carbon
)


from data_loader import (
    load_solar_database,
    get_location_data
)


from ai import (
    generate_ai_recommendations
)


from reports import (
    create_pdf_report
)


from utils import (
    format_currency
)


from location_engine import (
    get_location_solar_resource,
    get_location_summary
)


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
# SECTION 5 - INITIAL VARIABLES
# ==========================================================

location_description = None

latitude = None

longitude = None

sun_hours = None

temperature = None

solar_data = None

solar_summary = None

location_summary = None

location_ready = False


# ==========================================================
# SECTION 6 - SIDEBAR
# ==========================================================

st.sidebar.header(
    "⚙️ System Design Inputs"
)


# ==========================================================
# SECTION 7 - LOCATION SOURCE
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
# SECTION 8 - SOLAR DATABASE
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


    if location_data is not None:

        try:

            sun_hours = float(
                location_data[
                    "Peak_Sun_Hours"
                ]
            )

            temperature = float(
                location_data[
                    "Average_Temperature"
                ]
            )

            location_description = location

            location_ready = True

        except (
            TypeError,
            ValueError,
            KeyError
        ):

            st.sidebar.error(
                "The selected location contains "
                "invalid solar-resource data."
            )

    else:

        st.sidebar.error(
            "Selected location could not be found."
        )


# ==========================================================
# SECTION 9 - WORLDWIDE PLACE SEARCH
# ==========================================================

elif location_source == "Search for a Place":

    st.sidebar.info(
        """
        Search for a city, town or place anywhere
        in the world.

        Examples:

        Kano, Nigeria

        Kampala, Uganda

        London, UK

        Dubai, UAE

        Tokyo, Japan
        """
    )


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
    # Perform search
    # ------------------------------------------------------

    if search_button:

        if not search_query.strip():

            st.sidebar.warning(
                "Please enter a location."
            )

            st.session_state[
                "location_search_results"
            ] = []

        else:

            with st.sidebar:

                with st.spinner(
                    "Searching worldwide..."
                ):

                    results = search_location(
                        search_query,
                        limit=5
                    )


            st.session_state[
                "location_search_results"
            ] = results


    # ------------------------------------------------------
    # Retrieve stored results
    # ------------------------------------------------------

    search_results = st.session_state.get(
        "location_search_results",
        []
    )


    # ------------------------------------------------------
    # Display results
    # ------------------------------------------------------

    if search_results:

        result_labels = [
            format_search_result(
                result
            )
            for result in search_results
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
            search_results[
                selected_index
            ]
        )


        try:

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

        except (
            TypeError,
            ValueError,
            KeyError
        ):

            st.sidebar.error(
                "The selected location has invalid "
                "coordinates."
            )

            latitude = None

            longitude = None


        if (
            latitude is not None
            and longitude is not None
        ):

            location_name = (
                selected_location.get(
                    "name",
                    "Selected Location"
                )
            )


            country = (
                selected_location.get(
                    "country",
                    ""
                )
            )


            # --------------------------------------------------
            # NASA POWER
            # --------------------------------------------------

            with st.sidebar:

                with st.spinner(
                    "Retrieving NASA POWER data..."
                ):

                    try:

                        location_result = (
                            get_location_solar_resource(

                                latitude=latitude,

                                longitude=longitude,

                                location_name=location_name,

                                country=country

                            )
                        )

                    except Exception as error:

                        location_result = {

                            "success": False,

                            "message": str(error)

                        }


            if (
                not location_result
                or not location_result.get(
                    "success",
                    False
                )
            ):

                st.sidebar.error(
                    "NASA POWER lookup failed."
                )


                message = (
                    location_result.get(
                        "message",
                        "No additional information."
                    )
                    if location_result
                    else
                    "No response received."
                )


                st.sidebar.caption(
                    str(message)
                )

            else:

                # ----------------------------------------------
                # Extract summary
                # ----------------------------------------------

                try:

                    location_summary = (
                        get_location_summary(
                            location_result
                        )
                    )

                except Exception:

                    location_summary = {}


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


                if not location_summary:

                    location_summary = {}


                # ----------------------------------------------
                # Extract solar values safely
                # ----------------------------------------------

                raw_sun_hours = (
                    location_summary.get(
                        "peak_sun_hours"
                    )
                )


                raw_temperature = (
                    location_summary.get(
                        "average_temperature"
                    )
                )


                try:

                    if raw_sun_hours is not None:

                        sun_hours = float(
                            raw_sun_hours
                        )

                except (
                    TypeError,
                    ValueError
                ):

                    sun_hours = None


                try:

                    if raw_temperature is not None:

                        temperature = float(
                            raw_temperature
                        )

                except (
                    TypeError,
                    ValueError
                ):

                    temperature = None


                # ----------------------------------------------
                # Location description
                # ----------------------------------------------

                location_description = (
                    location_summary.get(
                        "location"
                    )
                    or
                    selected_location.get(
                        "display_name",
                        "Selected Location"
                    )
                )


                # ----------------------------------------------
                # Validate solar resource
                # ----------------------------------------------

                if sun_hours is None:

                    st.sidebar.warning(
                        "Location found, but NASA POWER "
                        "did not provide a usable solar "
                        "resource value."
                    )

                elif sun_hours <= 0:

                    st.sidebar.warning(
                        "NASA POWER returned an invalid "
                        "solar-resource value."
                    )

                    sun_hours = None

                else:

                    if temperature is None:

                        temperature = 25.0


                    location_ready = True


                    st.sidebar.success(
                        "🌍 Location connected to NASA POWER."
                    )


    else:

        st.sidebar.info(
            "Search for a location to continue."
        )


# ==========================================================
# SECTION 10 - MANUAL COORDINATES
# ==========================================================

else:

    st.sidebar.info(
        """
        Enter the geographical coordinates of your
        project site.

        Latitude: -90 to +90

        Longitude: -180 to +180
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

    with st.sidebar:

        with st.spinner(
            "Connecting to NASA POWER..."
        ):

            try:

                location_result = (
                    get_location_solar_resource(

                        latitude=latitude,

                        longitude=longitude,

                        location_name=location_name,

                        country=country

                    )
                )

            except Exception as error:

                location_result = {

                    "success": False,

                    "message": str(error)

                }


    if (
        not location_result
        or not location_result.get(
            "success",
            False
        )
    ):

        st.sidebar.error(
            "NASA POWER connection failed."
        )


        message = (
            location_result.get(
                "message",
                "No additional information."
            )
            if location_result
            else
            "No response received."
        )


        st.sidebar.caption(
            str(message)
        )

    else:

        try:

            location_summary = (
                get_location_summary(
                    location_result
                )
            )

        except Exception:

            location_summary = {}


        if not location_summary:

            location_summary = {}


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


        raw_sun_hours = (
            location_summary.get(
                "peak_sun_hours"
            )
        )


        raw_temperature = (
            location_summary.get(
                "average_temperature"
            )
        )


        try:

            sun_hours = float(
                raw_sun_hours
            )

        except (
            TypeError,
            ValueError
        ):

            sun_hours = None


        try:

            temperature = float(
                raw_temperature
            )

        except (
            TypeError,
            ValueError
        ):

            temperature = None


        if (
            sun_hours is not None
            and sun_hours > 0
        ):

            if temperature is None:

                temperature = 25.0


            location_description = (
                location_summary.get(
                    "location"
                )
                or
                f"{location_name}, {country}"
            )


            location_ready = True


            st.sidebar.success(
                "🌍 Coordinates connected to NASA POWER."
            )

        else:

            st.sidebar.warning(
                "NASA POWER did not return a usable "
                "solar-resource value."
            )


# ==========================================================
# SECTION 11 - SYSTEM DESIGN INPUTS
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader(
    "🔋 System Design"
)


energy = st.sidebar.number_input(
    "Daily Energy Demand (kWh/day)",
    min_value=0.1,
    value=5.0,
    step=0.5
)


efficiency_percent = st.sidebar.slider(
    "Overall System Efficiency (%)",
    min_value=50,
    max_value=100,
    value=80
)


efficiency = (
    efficiency_percent / 100
)


battery_type = st.sidebar.selectbox(
    "Battery Technology",
    [
        "Lithium-ion",
        "Lead Acid"
    ]
)


days = st.sidebar.number_input(
    "Battery Backup / Autonomy (Days)",
    min_value=1,
    max_value=30,
    value=3
)


panel_rating = st.sidebar.selectbox(
    "Solar Panel Rating (Watts)",
    [
        450,
        550,
        600
    ]
)


# ==========================================================
# SECTION 12 - LOCATION INFORMATION
# ==========================================================

st.header(
    "📍 Solar Resource Information"
)


if location_ready:

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


    # ------------------------------------------------------
    # Solar resource metrics
    # ------------------------------------------------------

    resource_col1, resource_col2, resource_col3 = (
        st.columns(3)
    )


    resource_col1.metric(
        "☀️ Peak Sun Hours",
        f"{sun_hours:.2f} h/day"
    )


    resource_col2.metric(
        "🌡️ Average Temperature",
        f"{temperature:.1f} °C"
    )


    resource_col3.metric(
        "📡 Data Source",
        (
            "Solar Database"
            if location_source ==
            "Solar Database"
            else
            "NASA POWER"
        )
    )


else:

    st.warning(
        """
        📍 **Location not ready**

        Please select a location from the Solar Database,
        search for a place, or provide coordinates before
        designing the solar PV system.
        """
    )


# ==========================================================
# SECTION 13 - NASA DATA
# ==========================================================

if (
    location_ready
    and location_source != "Solar Database"
    and solar_data is not None
):

    with st.expander(
        "☀️ View NASA POWER Solar Data"
    ):

        monthly_display = []

        if isinstance(
            solar_data,
            dict
        ):

            monthly_display = (
                solar_data.get(
                    "monthly_display",
                    []
                )
            )


        if monthly_display:

            st.dataframe(
                monthly_display,
                use_container_width=True
            )

        else:

            st.json(
                solar_data
            )


# ==========================================================
# SECTION 14 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary",
    disabled=not location_ready
)


# ==========================================================
# SECTION 15 - ENGINEERING CALCULATIONS
# ==========================================================

if design_button and location_ready:

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
    # SECTION 16 - ENGINEERING RESULTS
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
    # SECTION 17 - EQUIPMENT RECOMMENDATION
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
    # SECTION 18 - AI SOLAR ADVISOR
    # ======================================================

    st.divider()


    st.header(
        "🤖 AI Solar Advisor"
    )


    try:

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

    except Exception as error:

        recommendations = [

            "AI recommendation service "
            "could not be generated: "
            f"{error}"

        ]


    for recommendation in recommendations:

        st.success(
            recommendation
        )


    # ======================================================
    # SECTION 19 - PDF REPORT DATA
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
    # Add coordinates
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
    # Add NASA information
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
    # SECTION 20 - PDF REPORT
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
# SECTION 21 - FOOTER
# ==========================================================

st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™ v2.2.1

    Worldwide Location Search + NASA POWER

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
