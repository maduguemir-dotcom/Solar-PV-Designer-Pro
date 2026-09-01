# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# MAIN STREAMLIT APPLICATION
#
# Version: 2.4.2
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# ==========================================================
#
# INTEGRATED MODULES
# ----------------------------------------------------------
# - Solar PV System Designer
# - Worldwide Location Search
# - Interactive Map
# - Manual Coordinates
# - NASA POWER Solar Resource Integration
# - Solar Analytics
# - Appliance Energy Planner
# - PV Sizing
# - Battery Sizing
# - Inverter Sizing
# - Carbon Reduction
# - AI Solar Advisor
# - PDF Report
# - Project Cost Diary
# - Product Library
# - Product Management
# - Central SQLite Product Database
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd


# ==========================================================
# ENGINEERING CALCULATIONS
# ==========================================================

from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_carbon,
)


# ==========================================================
# SOLAR DATABASE
# ==========================================================

from data_loader import (
    load_solar_database,
    get_location_data,
)


# ==========================================================
# AI SOLAR ADVISOR
# ==========================================================

from ai import (
    generate_ai_recommendations,
)


# ==========================================================
# PDF REPORT GENERATOR
# ==========================================================

from reports import (
    create_pdf_report,
)


# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

from utils import (
    format_currency,
)


# ==========================================================
# LOCATION ENGINE
# ==========================================================

from location_engine import (
    get_location_solar_resource,
    get_location_summary,
)


# ==========================================================
# WORLDWIDE LOCATION SEARCH
# ==========================================================

from location_search import (
    search_location,
    format_search_result,
)


# ==========================================================
# INTERACTIVE MAP
# ==========================================================

from map_location import (
    display_location_map,
    format_coordinates,
)


# ==========================================================
# SOLAR ANALYTICS
# ==========================================================

from solar_analytics import (
    analyze_solar_resource,
)


# ==========================================================
# APPLIANCE ENERGY PLANNER
# ==========================================================

from appliance_energy import (
    create_appliance,
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_total_monthly_energy,
    calculate_total_connected_load,
)


# ==========================================================
# COST DIARY
# ==========================================================

try:

    from costing import (
        display_cost_diary,
    )

    COST_DIARY_AVAILABLE = True

except Exception as error:

    COST_DIARY_AVAILABLE = False
    COST_DIARY_IMPORT_ERROR = error


# ==========================================================
# CENTRAL PRODUCT DATABASE
# ==========================================================
#
# IMPORTANT:
#
# Product Library and Product Management must use the same
# SQLite database.
#
# Database:
#
# app/data/solar_pv_library.db
#
# This prevents one module from creating/using a different
# product database.
# ==========================================================

try:

    from library_store import (
        initialize_database,
    )

    PRODUCT_DATABASE_AVAILABLE = True
    PRODUCT_DATABASE_IMPORT_ERROR = None

except Exception as error:

    PRODUCT_DATABASE_AVAILABLE = False
    PRODUCT_DATABASE_IMPORT_ERROR = error


# ==========================================================
# PRODUCT LIBRARY
# ==========================================================

try:

    from product_ui import (
        display_product_library_ui,
    )

    PRODUCT_LIBRARY_AVAILABLE = True
    PRODUCT_LIBRARY_IMPORT_ERROR = None

except Exception as error:

    PRODUCT_LIBRARY_AVAILABLE = False
    PRODUCT_LIBRARY_IMPORT_ERROR = error


# ==========================================================
# PRODUCT MANAGEMENT
# ==========================================================

try:

    from product_management_ui import (
        display_product_management_ui,
    )

    PRODUCT_MANAGEMENT_AVAILABLE = True
    PRODUCT_MANAGEMENT_IMPORT_ERROR = None

except Exception as error:

    PRODUCT_MANAGEMENT_AVAILABLE = False
    PRODUCT_MANAGEMENT_IMPORT_ERROR = error


# ==========================================================
# SECTION 2 - APPLICATION CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="Solar PV Designer Pro Africa",

    page_icon="☀️",

    layout="wide",

)


# ==========================================================
# SECTION 3 - CENTRAL PRODUCT DATABASE INITIALIZATION
# ==========================================================

if PRODUCT_DATABASE_AVAILABLE:

    try:

        initialize_database()

    except Exception as error:

        st.warning(
            "Product database initialization warning: "
            f"{error}"
        )

else:

    st.warning(
        "Central Product Database module could not be loaded."
    )


# ==========================================================
# SECTION 4 - SESSION STATE
# ==========================================================

DEFAULT_STATE = {

    "location_ready":
        False,

    "location_description":
        None,

    "latitude":
        None,

    "longitude":
        None,

    "sun_hours":
        None,

    "temperature":
        None,

    "solar_data":
        None,

    "solar_summary":
        None,

    "location_summary":
        None,

    "location_source":
        None,

    "location_search_results":
        [],

    "selected_map_location":
        None,

    "appliances":
        [],

    "energy_source":
        "Appliance Planner",

    "design_results":
        None,

}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# SECTION 5 - APPLICATION HEADER
# ==========================================================

st.sidebar.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.sidebar.caption(
    "Professional Solar PV Design & Analysis Platform"
)


# ==========================================================
# DATABASE STATUS
# ==========================================================

if PRODUCT_DATABASE_AVAILABLE:

    st.sidebar.success(
        "🗄️ Product Database: SQLite"
    )

else:

    st.sidebar.warning(
        "🗄️ Product Database: Unavailable"
    )


# ==========================================================
# SECTION 6 - APPLICATION NAVIGATION
# ==========================================================

app_page = st.sidebar.radio(

    "Application Menu",

    [

        "☀️ Solar PV Designer",

        "📦 Product Library",

        "🛠️ Product Management",

    ],

    key="main_application_navigation",

)


# ==========================================================
# SECTION 7 - PRODUCT LIBRARY PAGE
# ==========================================================

if app_page == "📦 Product Library":

    if PRODUCT_LIBRARY_AVAILABLE:

        try:

            display_product_library_ui()

        except Exception as error:

            st.error(
                "The Product Library encountered an error."
            )

            st.exception(error)

    else:

        st.error(
            "The Product Library module could not be loaded."
        )

        if PRODUCT_LIBRARY_IMPORT_ERROR:

            st.exception(
                PRODUCT_LIBRARY_IMPORT_ERROR
            )

    st.stop()


# ==========================================================
# SECTION 8 - PRODUCT MANAGEMENT PAGE
# ==========================================================

if app_page == "🛠️ Product Management":

    if PRODUCT_MANAGEMENT_AVAILABLE:

        try:

            display_product_management_ui()

        except Exception as error:

            st.error(
                "The Product Management module encountered "
                "an error."
            )

            st.exception(error)

    else:

        st.error(
            "The Product Management module could not be loaded."
        )

        if PRODUCT_MANAGEMENT_IMPORT_ERROR:

            st.exception(
                PRODUCT_MANAGEMENT_IMPORT_ERROR
            )

    st.stop()


# ==========================================================
# SECTION 9 - MAIN SOLAR PV DESIGNER
# ==========================================================

st.title(
    "☀️ SOLAR PV DESIGNER PRO AFRICA™"
)

st.caption(
    "Professional Solar PV System Design, Resource "
    "Assessment, Sizing and Decision Support"
)


# ==========================================================
# MAIN APPLICATION INFORMATION
# ==========================================================

st.info(
    """
    Welcome to Solar PV Designer Pro Africa™.

    Use the sidebar to select a location, assess solar
    resources, plan appliances, size your PV system,
    estimate batteries and inverters, assess carbon
    reduction, obtain AI-assisted recommendations and
    generate a professional PDF report.
    """
)


# ==========================================================
# SECTION 10 - LOCATION SELECTION
# ==========================================================

st.header(
    "📍 Solar Resource Location"
)


location_method = st.radio(

    "Choose location input method",

    [

        "🌍 Search for a Place",

        "🗺️ Select on Map",

        "📐 Enter Coordinates",

        "☀️ Solar Database",

    ],

    horizontal=True,

    key="location_input_method",

)


# ==========================================================
# WORLDWIDE LOCATION SEARCH
# ==========================================================

if location_method == "🌍 Search for a Place":

    st.subheader(
        "🌍 Worldwide Location Search"
    )

    location_query = st.text_input(

        "Enter city, town or location",

        placeholder="e.g. Kampala, Uganda",

        key="location_search_query",

    )


    if st.button(

        "🔎 Search Location",

        use_container_width=True,

        key="search_location_button",

    ):

        if not location_query.strip():

            st.warning(
                "Please enter a location."
            )

        else:

            try:

                results = search_location(
                    location_query
                )

                if results:

                    st.session_state[
                        "location_search_results"
                    ] = results

                    st.success(
                        f"{len(results)} location(s) found."
                    )

                else:

                    st.warning(
                        "No matching locations found."
                    )

            except Exception as error:

                st.error(
                    f"Location search failed: {error}"
                )


    results = st.session_state.get(
        "location_search_results",
        [],
    )


    if results:

        labels = []

        for result in results:

            try:

                labels.append(
                    format_search_result(
                        result
                    )
                )

            except Exception:

                labels.append(
                    str(result)
                )


        selected_index = st.selectbox(

            "Select a location",

            range(len(results)),

            format_func=lambda i: labels[i],

            key="selected_search_location",

        )


        selected = results[
            selected_index
        ]


        if st.button(

            "✅ Use Selected Location",

            use_container_width=True,

            key="use_selected_location",

        ):

            try:

                latitude = float(
                    selected.get(
                        "latitude"
                    )
                )

                longitude = float(
                    selected.get(
                        "longitude"
                    )
                )

                st.session_state[
                    "latitude"
                ] = latitude

                st.session_state[
                    "longitude"
                ] = longitude

                st.session_state[
                    "location_description"
                ] = selected.get(
                    "display_name",
                    selected.get(
                        "name",
                        "Selected Location",
                    ),
                )

                st.session_state[
                    "location_source"
                ] = "Worldwide Location Search"

                st.session_state[
                    "location_ready"
                ] = True

                st.success(
                    "Location selected successfully."
                )

            except Exception as error:

                st.error(
                    f"Could not use selected location: "
                    f"{error}"
                )


# ==========================================================
# MAP LOCATION
# ==========================================================

elif location_method == "🗺️ Select on Map":

    st.subheader(
        "🗺️ Interactive Location Map"
    )

    try:

        selected_location = display_location_map()

        if selected_location:

            st.session_state[
                "selected_map_location"
            ] = selected_location

    except Exception as error:

        st.error(
            f"Map interface failed: {error}"
        )


# ==========================================================
# MANUAL COORDINATES
# ==========================================================

elif location_method == "📐 Enter Coordinates":

    st.subheader(
        "📐 Enter Geographic Coordinates"
    )

    col1, col2 = st.columns(2)

    with col1:

        latitude = st.number_input(

            "Latitude",

            min_value=-90.0,

            max_value=90.0,

            value=0.0,

            step=0.0001,

            format="%.4f",

            key="manual_latitude",

        )

    with col2:

        longitude = st.number_input(

            "Longitude",

            min_value=-180.0,

            max_value=180.0,

            value=0.0,

            step=0.0001,

            format="%.4f",

            key="manual_longitude",

        )


    location_name = st.text_input(

        "Location Name",

        placeholder="e.g. Kampala, Uganda",

        key="manual_location_name",

    )


    if st.button(

        "📍 Use Coordinates",

        type="primary",

        use_container_width=True,

        key="use_manual_coordinates",

    ):

        st.session_state[
            "latitude"
        ] = latitude

        st.session_state[
            "longitude"
        ] = longitude

        st.session_state[
            "location_description"
        ] = (
            location_name.strip()
            or "Manual Coordinates"
        )

        st.session_state[
            "location_source"
        ] = "Manual Coordinates"

        st.session_state[
            "location_ready"
        ] = True

        st.success(
            "Coordinates saved successfully."
        )


# ==========================================================
# SOLAR DATABASE
# ==========================================================

elif location_method == "☀️ Solar Database":

    st.subheader(
        "☀️ Solar Database"
    )

    try:

        solar_database = load_solar_database()

        if solar_database is None:

            solar_database = pd.DataFrame()


        if isinstance(
            solar_database,
            pd.DataFrame,
        ):

            st.dataframe(

                solar_database,

                use_container_width=True,

                hide_index=True,

            )

            st.caption(
                f"{len(solar_database)} "
                "location record(s)"
            )

        else:

            st.write(
                solar_database
            )

    except Exception as error:

        st.error(
            f"Solar database could not be loaded: "
            f"{error}"
        )


# ==========================================================
# LOCATION STATUS
# ==========================================================

if st.session_state.get(
    "location_ready",
    False,
):

    st.success(
        "📍 Location is ready for solar-resource analysis."
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Latitude",
            f"{st.session_state.get('latitude', 0):.4f}",
        )

    with col2:

        st.metric(
            "Longitude",
            f"{st.session_state.get('longitude', 0):.4f}",
        )

    with col3:

        st.metric(
            "Source",
            st.session_state.get(
                "location_source",
                "Unknown",
            ),
        )


# ==========================================================
# NASA POWER SOLAR RESOURCE
# ==========================================================

st.header(
    "☀️ Solar Resource Assessment"
)


if st.session_state.get(
    "location_ready",
    False,
):

    latitude = st.session_state.get(
        "latitude"
    )

    longitude = st.session_state.get(
        "longitude"
    )


    if st.button(

        "🌞 Retrieve Solar Resource",

        type="primary",

        use_container_width=True,

        key="retrieve_solar_resource",

    ):

        try:

            solar_data = (
                get_location_solar_resource(
                    latitude=latitude,
                    longitude=longitude,
                    location_name=st.session_state.get(
                        "location_description",
                        "",
                    ),
                    country="",
                )
            )


            st.session_state[
                "solar_data"
            ] = solar_data


            summary = get_location_summary(
                solar_data
            )


            st.session_state[
                "solar_summary"
            ] = summary


            st.success(
                "Solar resource data retrieved successfully."
            )

        except Exception as error:

            st.error(
                "Solar resource retrieval failed."
            )

            st.exception(error)


# ==========================================================
# DISPLAY SOLAR RESOURCE SUMMARY
# ==========================================================

solar_summary = st.session_state.get(
    "solar_summary"
)


if solar_summary:

    st.subheader(
        "Solar Resource Summary"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(

            "Peak Sun Hours",

            f"{solar_summary.get('peak_sun_hours', 0):.2f}",

        )

    with col2:

        st.metric(

            "Average Temperature",

            f"{solar_summary.get('average_temperature', 0):.1f} °C",

        )

    with col3:

        st.metric(

            "Location",

            st.session_state.get(
                "location_description",
                "Selected Location",
            ),

        )


# ==========================================================
# APPLIANCE ENERGY PLANNER
# ==========================================================

st.header(
    "🔌 Appliance Energy Planner"
)


st.caption(
    "Estimate daily energy consumption and connected load."
)


if "appliances" not in st.session_state:

    st.session_state[
        "appliances"
    ] = []


with st.form(
    "appliance_form"
):

    col1, col2, col3 = st.columns(3)

    with col1:

        appliance_name = st.text_input(
            "Appliance",
            placeholder="e.g. Refrigerator",
        )

    with col2:

        appliance_power = st.number_input(
            "Power (W)",
            min_value=0.0,
            value=100.0,
            step=10.0,
        )

    with col3:

        appliance_hours = st.number_input(
            "Hours per day",
            min_value=0.0,
            value=5.0,
            step=0.5,
        )


    add_appliance = st.form_submit_button(
        "➕ Add Appliance",
        use_container_width=True,
    )


if add_appliance:

    if not appliance_name.strip():

        st.warning(
            "Please enter an appliance name."
        )

    else:

        try:

            appliance = create_appliance(

                name=appliance_name,

                power_w=appliance_power,

                hours_per_day=appliance_hours,

            )

            st.session_state[
                "appliances"
            ].append(
                appliance
            )

            st.success(
                "Appliance added successfully."
            )

        except Exception as error:

            st.error(
                f"Could not add appliance: {error}"
            )


# ==========================================================
# DISPLAY APPLIANCES
# ==========================================================

appliances = st.session_state.get(
    "appliances",
    [],
)


if appliances:

    appliance_rows = []

    for appliance in appliances:

        try:

            energy = calculate_appliance_energy(
                appliance
            )

        except Exception:

            energy = 0


        appliance_rows.append(

            {

                "Appliance":
                    appliance.get(
                        "name",
                        "",
                    ),

                "Power (W)":
                    appliance.get(
                        "power_w",
                        0,
                    ),

                "Hours/day":
                    appliance.get(
                        "hours_per_day",
                        0,
                    ),

                "Daily Energy (kWh)":
                    energy,

            }

        )


    st.dataframe(

        pd.DataFrame(
            appliance_rows
        ),

        use_container_width=True,

        hide_index=True,

    )


    try:

        daily_energy = (
            calculate_total_daily_energy(
                appliances
            )
        )

    except Exception:

        daily_energy = 0


    try:

        monthly_energy = (
            calculate_total_monthly_energy(
                appliances
            )
        )

    except Exception:

        monthly_energy = 0


    try:

        connected_load = (
            calculate_total_connected_load(
                appliances
            )
        )

    except Exception:

        connected_load = 0


    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Daily Energy",
            f"{daily_energy:.2f} kWh",
        )

    with col2:

        st.metric(
            "Monthly Energy",
            f"{monthly_energy:.2f} kWh",
        )

    with col3:

        st.metric(
            "Connected Load",
            f"{connected_load:.0f} W",
        )


# ==========================================================
# SYSTEM DESIGN
# ==========================================================

st.header(
    "⚡ Solar PV System Design"
)


daily_energy_input = st.number_input(

    "Daily Energy Requirement (kWh/day)",

    min_value=0.0,

    value=5.0,

    step=0.1,

    key="design_daily_energy",

)


sun_hours_input = st.number_input(

    "Peak Sun Hours",

    min_value=0.1,

    value=float(
        st.session_state.get(
            "sun_hours"
        )
        or 4.0
    ),

    step=0.1,

    key="design_sun_hours",

)


system_voltage = st.selectbox(

    "System Voltage",

    [

        12,

        24,

        48,

    ],

    index=2,

    key="design_system_voltage",

)


if st.button(

    "⚡ Calculate Solar PV System",

    type="primary",

    use_container_width=True,

    key="calculate_system_button",

):

    try:

        pv_result = calculate_pv_size(

            daily_energy=daily_energy_input,

            sun_hours=sun_hours_input,

        )


        panel_result = calculate_panels(
            pv_result
        )


        battery_result = calculate_battery(

            daily_energy=daily_energy_input,

            system_voltage=system_voltage,

        )


        inverter_result = calculate_inverter(

            connected_load=connected_load
            if appliances
            else 0,

        )


        carbon_result = calculate_carbon(
            daily_energy_input
        )


        st.session_state[
            "design_results"
        ] = {

            "pv":
                pv_result,

            "panels":
                panel_result,

            "battery":
                battery_result,

            "inverter":
                inverter_result,

            "carbon":
                carbon_result,

        }


    except Exception as error:

        st.error(
            "System calculation failed."
        )

        st.exception(error)


# ==========================================================
# DESIGN RESULTS
# ==========================================================

design_results = st.session_state.get(
    "design_results"
)


if design_results:

    st.subheader(
        "📊 Recommended System"
    )

    st.json(
        design_results
    )


# ==========================================================
# AI SOLAR ADVISOR
# ==========================================================

st.header(
    "🤖 AI Solar Advisor"
)


if st.button(

    "🤖 Generate AI Recommendation",

    use_container_width=True,

    key="generate_ai_recommendation",

):

    try:

        recommendation = (
            generate_ai_recommendations(
                st.session_state.get(
                    "design_results",
                    {}
                )
            )
        )

        st.write(
            recommendation
        )

    except Exception as error:

        st.error(
            f"AI recommendation failed: {error}"
        )


# ==========================================================
# PROJECT COST DIARY
# ==========================================================

st.header(
    "💰 Project Cost Diary"
)


if COST_DIARY_AVAILABLE:

    try:

        display_cost_diary(st)

    except Exception as error:

        st.error(
            f"Cost Diary failed: {error}"
        )

else:

    st.info(
        "Project Cost Diary module is unavailable."
    )


# ==========================================================
# PDF REPORT
# ==========================================================

st.header(
    "📄 Professional PDF Report"
)


if st.button(

    "📄 Generate PDF Report",

    use_container_width=True,

    key="generate_pdf_report",

):

    try:

        report_data = {

            "location":
                st.session_state.get(
                    "location_description"
                ),

            "latitude":
                st.session_state.get(
                    "latitude"
                ),

            "longitude":
                st.session_state.get(
                    "longitude"
                ),

            "solar_summary":
                st.session_state.get(
                    "solar_summary"
                ),

            "appliances":
                st.session_state.get(
                    "appliances",
                    [],
                ),

            "design_results":
                st.session_state.get(
                    "design_results"
                ),

        }


        pdf_result = create_pdf_report(
            report_data
        )


        if pdf_result:

            st.success(
                "PDF report generated successfully."
            )

            try:

                with open(
                    pdf_result,
                    "rb"
                ) as pdf_file:

                    st.download_button(

                        "⬇️ Download PDF Report",

                        data=pdf_file,

                        file_name="solar_pv_report.pdf",

                        mime="application/pdf",

                        use_container_width=True,

                    )

            except Exception:

                st.write(
                    pdf_result
                )

    except Exception as error:

        st.error(
            f"PDF report generation failed: {error}"
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "SOLAR PV DESIGNER PRO AFRICA™"
)

st.caption(
    "Developed by Engr. Prof. Ibrahim Sani Madugu"
)

st.caption(
    "Professional Solar PV Design • Renewable Energy • "
    "AI-Assisted Decision Support"
)
