# Complete `app/main.py`

```python
# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Main Streamlit Application
# Version: 2.4.1
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# v2.4.1
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
#
# IMPORTANT:
# Product Library and Product Management are launched from
# this same Streamlit application.
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd


# ----------------------------------------------------------
# Engineering calculations
# ----------------------------------------------------------

from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_carbon,
)


# ----------------------------------------------------------
# Solar database
# ----------------------------------------------------------

from data_loader import (
    load_solar_database,
    get_location_data,
)


# ----------------------------------------------------------
# AI Solar Advisor
# ----------------------------------------------------------

from ai import (
    generate_ai_recommendations,
)


# ----------------------------------------------------------
# PDF Report Generator
# ----------------------------------------------------------

from reports import (
    create_pdf_report,
)


# ----------------------------------------------------------
# Utility functions
# ----------------------------------------------------------

from utils import (
    format_currency,
)


# ----------------------------------------------------------
# Location engine
# ----------------------------------------------------------

from location_engine import (
    get_location_solar_resource,
    get_location_summary,
)


# ----------------------------------------------------------
# Worldwide location search
# ----------------------------------------------------------

from location_search import (
    search_location,
    format_search_result,
)


# ----------------------------------------------------------
# Interactive map
# ----------------------------------------------------------

from map_location import (
    display_location_map,
    format_coordinates,
)


# ----------------------------------------------------------
# Solar analytics
# ----------------------------------------------------------

from solar_analytics import (
    analyze_solar_resource,
)


# ----------------------------------------------------------
# Appliance Energy Planner
# ----------------------------------------------------------

from appliance_energy import (
    create_appliance,
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_total_monthly_energy,
    calculate_total_connected_load,
)


# ----------------------------------------------------------
# Cost Diary
# ----------------------------------------------------------

try:

    from costing import (
        display_cost_diary,
    )

    COST_DIARY_AVAILABLE = True

except Exception:

    COST_DIARY_AVAILABLE = False


# ----------------------------------------------------------
# Product Library
# ----------------------------------------------------------

try:

    from product_ui import (
        display_product_library_ui,
    )

    PRODUCT_LIBRARY_AVAILABLE = True

except Exception as error:

    PRODUCT_LIBRARY_AVAILABLE = False
    PRODUCT_LIBRARY_IMPORT_ERROR = error


# ----------------------------------------------------------
# Product Management
# ----------------------------------------------------------

try:

    from product_management_ui import (
        display_product_management_ui,
    )

    PRODUCT_MANAGEMENT_AVAILABLE = True

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
# SECTION 3 - SESSION STATE
# ==========================================================

DEFAULT_STATE = {

    "location_ready": False,

    "location_description": None,

    "latitude": None,

    "longitude": None,

    "sun_hours": None,

    "temperature": None,

    "solar_data": None,

    "solar_summary": None,

    "location_summary": None,

    "location_source": None,

    "location_search_results": [],

    "selected_map_location": None,

    "appliances": [],

    "energy_source": "Appliance Planner",

    "design_results": None,

}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# SECTION 4 - APPLICATION NAVIGATION
# ==========================================================

st.sidebar.title(
    "☀️ Solar PV Designer Pro Africa™"
)


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
# SECTION 5 - PRODUCT LIBRARY PAGE
# ==========================================================

if app_page == "📦 Product Library":

    if PRODUCT_LIBRARY_AVAILABLE:

        display_product_library_ui()

    else:

        st.error(
            "The Product Library module could not be loaded."
        )

        if "PRODUCT_LIBRARY_IMPORT_ERROR" in globals():

            st.exception(
                PRODUCT_LIBRARY_IMPORT_ERROR
            )

    st.stop()


# ==========================================================
# SECTION 6 - PRODUCT MANAGEMENT PAGE
# ==========================================================

if app_page == "🛠️ Product Management":

    if PRODUCT_MANAGEMENT_AVAILABLE:

        display_product_management_ui()

    else:

        st.error(
            "The Product Management module could not be loaded."
        )

        if "PRODUCT_MANAGEMENT_IMPORT_ERROR" in globals():

            st.exception(
                PRODUCT_MANAGEMENT_IMPORT_ERROR
            )

    st.stop()


# ==========================================================
# SECTION 7 - SOLAR PV DESIGNER PAGE
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)


st.caption(
    "Professional solar photovoltaic system design, "
    "location-based solar analysis and component sizing."
)


# ==========================================================
# SECTION 8 - LOAD SOLAR DATABASE
# ==========================================================

try:

    solar_database = load_solar_database()

except Exception as error:

    solar_database = None

    st.warning(
        f"Solar database could not be loaded: {error}"
    )


# ==========================================================
# SECTION 9 - SIDEBAR LOCATION SETTINGS
# ==========================================================

st.sidebar.header(
    "📍 Location & Solar Resource"
)


location_source = st.sidebar.selectbox(
    "Location Source",
    [
        "Solar Database",
        "Search for a Place",
        "Select on Map",
        "Enter Coordinates",
    ],
)


# ==========================================================
# SECTION 10 - SOLAR DATABASE LOCATION
# ==========================================================

if location_source == "Solar Database":

    if solar_database is not None:

        try:

            location_names = sorted(
                solar_database[
                    "location"
                ].dropna().unique().tolist()
            )

        except Exception:

            location_names = []

        if location_names:

            selected_location = st.sidebar.selectbox(
                "Select Location",
                location_names,
            )

            if st.sidebar.button(
                "Load Location Data",
                use_container_width=True,
            ):

                try:

                    location_data = get_location_data(
                        solar_database,
                        selected_location,
                    )

                    if location_data:

                        st.session_state[
                            "location_description"
                        ] = selected_location

                        st.session_state[
                            "location_source"
                        ] = "Solar Database"

                        st.session_state[
                            "latitude"
                        ] = location_data.get(
                            "latitude"
                        )

                        st.session_state[
                            "longitude"
                        ] = location_data.get(
                            "longitude"
                        )

                        st.session_state[
                            "sun_hours"
                        ] = location_data.get(
                            "peak_sun_hours"
                        )

                        st.session_state[
                            "temperature"
                        ] = location_data.get(
                            "average_temperature"
                        )

                        st.session_state[
                            "location_ready"
                        ] = True

                        st.success(
                            "Location loaded successfully."
                        )

                except Exception as error:

                    st.error(
                        f"Unable to load location: {error}"
                    )

        else:

            st.info(
                "No locations were found in the Solar Database."
            )


# ==========================================================
# SECTION 11 - SEARCH FOR A PLACE
# ==========================================================

elif location_source == "Search for a Place":

    search_query = st.sidebar.text_input(
        "Search for a City or Location",
        placeholder="Example: Kampala, Uganda",
    )


    if st.sidebar.button(
        "🔍 Search Location",
        use_container_width=True,
    ):

        if search_query.strip():

            try:

                results = search_location(
                    search_query
                )

                st.session_state[
                    "location_search_results"
                ] = results or []

            except Exception as error:

                st.error(
                    f"Location search failed: {error}"
                )


    search_results = st.session_state.get(
        "location_search_results",
        []
    )


    if search_results:

        formatted_results = [

            format_search_result(
                result
            )

            for result in search_results

        ]


        selected_result = st.sidebar.selectbox(
            "Select Search Result",
            formatted_results,
        )


        if st.sidebar.button(
            "📍 Use Selected Location",
            use_container_width=True,
        ):

            try:

                selected_index = (
                    formatted_results.index(
                        selected_result
                    )
                )

                result = search_results[
                    selected_index
                ]

                latitude = result.get(
                    "latitude"
                )

                longitude = result.get(
                    "longitude"
                )

                location_name = (
                    result.get(
                        "display_name",
                        selected_result,
                    )
                )


                solar_resource = (
                    get_location_solar_resource(
                        latitude,
                        longitude,
                        location_name,
                    )
                )


                summary = get_location_summary(
                    solar_resource
                )


                st.session_state[
                    "location_description"
                ] = location_name

                st.session_state[
                    "latitude"
                ] = latitude

                st.session_state[
                    "longitude"
                ] = longitude

                st.session_state[
                    "sun_hours"
                ] = summary.get(
                    "peak_sun_hours"
                )

                st.session_state[
                    "temperature"
                ] = summary.get(
                    "average_temperature"
                )

                st.session_state[
                    "solar_data"
                ] = solar_resource

                st.session_state[
                    "location_summary"
                ] = summary

                st.session_state[
                    "location_source"
                ] = "Worldwide Search"

                st.session_state[
                    "location_ready"
                ] = True

                st.success(
                    "Location solar resource loaded."
                )

            except Exception as error:

                st.error(
                    f"Unable to load solar resource: {error}"
                )


# ==========================================================
# SECTION 12 - SELECT ON MAP
# ==========================================================

elif location_source == "Select on Map":

    st.sidebar.info(
        "Select a location using the interactive map."
    )


# ==========================================================
# SECTION 13 - MANUAL COORDINATES
# ==========================================================

elif location_source == "Enter Coordinates":

    latitude = st.sidebar.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=0.3476,
        format="%.6f",
    )


    longitude = st.sidebar.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=32.5825,
        format="%.6f",
    )


    manual_location_name = st.sidebar.text_input(
        "Location Name",
        value="Custom Location",
    )


    if st.sidebar.button(
        "☀️ Get Solar Resource",
        use_container_width=True,
    ):

        try:

            solar_resource = (
                get_location_solar_resource(
                    latitude,
                    longitude,
                    manual_location_name,
                )
            )


            summary = get_location_summary(
                solar_resource
            )


            st.session_state[
                "location_description"
            ] = manual_location_name

            st.session_state[
                "latitude"
            ] = latitude

            st.session_state[
                "longitude"
            ] = longitude

            st.session_state[
                "sun_hours"
            ] = summary.get(
                "peak_sun_hours"
            )

            st.session_state[
                "temperature"
            ] = summary.get(
                "average_temperature"
            )

            st.session_state[
                "solar_data"
            ] = solar_resource

            st.session_state[
                "location_summary"
            ] = summary

            st.session_state[
                "location_source"
            ] = "Manual Coordinates"

            st.session_state[
                "location_ready"
            ] = True


            st.success(
                "Solar resource loaded successfully."
            )

        except Exception as error:

            st.error(
                f"Unable to retrieve solar resource: {error}"
            )


# ==========================================================
# SECTION 14 - INTERACTIVE MAP
# ==========================================================

if location_source == "Select on Map":

    try:

        map_result = display_location_map()

        if map_result:

            latitude = map_result.get(
                "latitude"
            )

            longitude = map_result.get(
                "longitude"
            )

            if (
                latitude is not None
                and longitude is not None
            ):

                st.session_state[
                    "selected_map_location"
                ] = map_result

                st.session_state[
                    "latitude"
                ] = latitude

                st.session_state[
                    "longitude"
                ] = longitude

    except Exception as error:

        st.warning(
            f"Interactive map unavailable: {error}"
        )


# ==========================================================
# SECTION 15 - CURRENT LOCATION SUMMARY
# ==========================================================

if st.session_state.get(
    "location_ready"
):

    st.subheader(
        "📍 Selected Location"
    )


    location_col1, location_col2, location_col3 = (
        st.columns(3)
    )


    with location_col1:

        st.metric(
            "Location",
            st.session_state.get(
                "location_description"
            )
            or "Selected Location",
        )


    with location_col2:

        sun_hours = (
            st.session_state.get(
                "sun_hours"
            )
        )

        if sun_hours is not None:

            st.metric(
                "Peak Sun Hours",
                f"{float(sun_hours):.2f}",
            )

        else:

            st.metric(
                "Peak Sun Hours",
                "Not Available",
            )


    with location_col3:

        temperature = (
            st.session_state.get(
                "temperature"
            )
        )

        if temperature is not None:

            st.metric(
                "Average Temperature",
                f"{float(temperature):.1f} °C",
            )

        else:

            st.metric(
                "Average Temperature",
                "Not Available",
            )


    latitude = st.session_state.get(
        "latitude"
    )

    longitude = st.session_state.get(
        "longitude"
    )


    if (
        latitude is not None
        and longitude is not None
    ):

        st.caption(
            f"Coordinates: "
            f"{format_coordinates(latitude, longitude)}"
        )


# ==========================================================
# SECTION 16 - APPLIANCE ENERGY PLANNER
# ==========================================================

st.divider()


st.header(
    "🔌 Appliance Energy Planner"
)


st.caption(
    "Add electrical appliances to automatically calculate "
    "daily energy demand and connected load."
)


with st.form(
    "appliance_entry_form",
    clear_on_submit=True,
):

    appliance_col1, appliance_col2, appliance_col3, appliance_col4 = (
        st.columns(4)
    )


    with appliance_col1:

        appliance_name = st.text_input(
            "Appliance Name",
            placeholder="Example: LED TV",
        )


    with appliance_col2:

        appliance_wattage = st.number_input(
            "Power Rating (W)",
            min_value=0.0,
            value=100.0,
        )


    with appliance_col3:

        appliance_quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
        )


    with appliance_col4:

        appliance_hours = st.number_input(
            "Hours per Day",
            min_value=0.0,
            max_value=24.0,
            value=1.0,
        )


    add_appliance = st.form_submit_button(
        "➕ Add Appliance",
        use_container_width=True,
    )


if add_appliance:

    if appliance_name.strip():

        appliance = create_appliance(
            appliance_name,
            appliance_wattage,
            appliance_quantity,
            appliance_hours,
        )


        st.session_state[
            "appliances"
        ].append(
            appliance
        )


        st.success(
            f"{appliance_name} added successfully."
        )

        st.rerun()

    else:

        st.warning(
            "Please enter an appliance name."
        )


appliances = st.session_state.get(
    "appliances",
    []
)


if appliances:

    appliance_rows = []

    for appliance in appliances:

        try:

            daily_energy = (
                calculate_appliance_energy(
                    appliance
                )
            )

        except Exception:

            daily_energy = 0


        appliance_rows.append({

            "Appliance":
                appliance.get(
                    "name",
                    ""
                ),

            "Power (W)":
                appliance.get(
                    "wattage",
                    appliance.get(
                        "power",
                        0,
                    ),
                ),

            "Quantity":
                appliance.get(
                    "quantity",
                    1,
                ),

            "Hours/Day":
                appliance.get(
                    "hours",
                    appliance.get(
                        "hours_per_day",
                        0,
                    ),
                ),

            "Daily Energy (Wh)":
                daily_energy,

        })


    st.dataframe(
        pd.DataFrame(
            appliance_rows
        ),
        use_container_width=True,
        hide_index=True,
    )


    try:

        total_daily_energy = (
            calculate_total_daily_energy(
                appliances
            )
        )

    except Exception:

        total_daily_energy = 0


    try:

        total_monthly_energy = (
            calculate_total_monthly_energy(
                appliances
            )
        )

    except Exception:

        total_monthly_energy = 0


    try:

        total_connected_load = (
            calculate_total_connected_load(
                appliances
            )
        )

    except Exception:

        total_connected_load = 0


    energy_col1, energy_col2, energy_col3 = (
        st.columns(3)
    )


    with energy_col1:

        st.metric(
            "Daily Energy",
            f"{float(total_daily_energy):.2f} kWh",
        )


    with energy_col2:

        st.metric(
            "Monthly Energy",
            f"{float(total_monthly_energy):.2f} kWh",
        )


    with energy_col3:

        st.metric(
            "Connected Load",
            f"{float(total_connected_load):.0f} W",
        )


    if st.button(
        "🗑️ Clear Appliance List"
    ):

        st.session_state[
            "appliances"
        ] = []

        st.rerun()


# ==========================================================
# SECTION 17 - SYSTEM DESIGN INPUTS
# ==========================================================

st.divider()


st.header(
    "⚙️ Solar PV System Design Inputs"
)


energy_source = st.radio(
    "Daily Energy Source",
    [
        "Appliance Planner",
        "Manual Input",
    ],
    horizontal=True,
)


if (
    energy_source == "Appliance Planner"
    and appliances
):

    energy = float(
        total_daily_energy
    )


    st.success(
        f"Using Appliance Planner demand: "
        f"{energy:.2f} kWh/day"
    )


else:

    energy = st.number_input(
        "Daily Energy Consumption (kWh/day)",
        min_value=0.1,
        value=5.0,
        step=0.1,
    )


design_col1, design_col2, design_col3 = (
    st.columns(3)
)


with design_col1:

    panel_power = st.number_input(
        "Solar Panel Rating (W)",
        min_value=50.0,
        value=550.0,
        step=10.0,
    )


    system_efficiency = st.number_input(
        "System Efficiency",
        min_value=0.50,
        max_value=1.00,
        value=0.80,
        step=0.01,
    )


with design_col2:

    battery_voltage = st.selectbox(
        "Battery System Voltage (V)",
        [
            12,
            24,
            48,
        ],
        index=2,
    )


    battery_dod = st.number_input(
        "Battery Depth of Discharge",
        min_value=0.10,
        max_value=1.00,
        value=0.80,
        step=0.05,
    )


with design_col3:

    autonomy_days = st.number_input(
        "Days of Autonomy",
        min_value=1,
        value=1,
        step=1,
    )


    inverter_safety_factor = st.number_input(
        "Inverter Safety Factor",
        min_value=1.0,
        value=1.25,
        step=0.05,
    )


# ==========================================================
# SECTION 18 - DESIGN SYSTEM BUTTON
# ==========================================================

st.divider()


design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary",
    use_container_width=True,
)


if design_button:

    sun_hours = st.session_state.get(
        "sun_hours"
    )


    if (
        sun_hours is None
        or float(sun_hours) <= 0
    ):

        st.error(
            "Please select a location and obtain "
            "solar resource data first."
        )


    else:

        try:

            pv_size = calculate_pv_size(
                energy,
                float(sun_hours),
                system_efficiency,
            )


            number_of_panels = calculate_panels(
                pv_size,
                panel_power,
            )


            battery_result = calculate_battery(
                energy,
                autonomy_days,
                battery_voltage,
                battery_dod,
            )


            inverter_result = calculate_inverter(
                total_connected_load
                if appliances
                else energy * 1000 / 5,
                inverter_safety_factor,
            )


            carbon_result = calculate_carbon(
                energy
            )


            design_results = {

                "daily_energy_kwh":
                    energy,

                "sun_hours":
                    float(sun_hours),

                "pv_size":
                    pv_size,

                "number_of_panels":
                    number_of_panels,

                "panel_power_w":
                    panel_power,

                "battery":
                    battery_result,

                "inverter":
                    inverter_result,

                "carbon":
                    carbon_result,

                "location":
                    st.session_state.get(
                        "location_description"
                    ),

            }


            st.session_state[
                "design_results"
            ] = design_results


            st.success(
                "Solar PV system design completed successfully."
            )


        except Exception as error:

            st.error(
                f"System design failed: {error}"
            )


# ==========================================================
# SECTION 19 - DESIGN RESULTS
# ==========================================================

design_results = st.session_state.get(
    "design_results"
)


if design_results:

    st.divider()


    st.header(
        "📊 Solar PV System Results"
    )


    result_col1, result_col2, result_col3 = (
        st.columns(3)
    )


    with result_col1:

        st.metric(
            "Daily Energy",
            f"{design_results['daily_energy_kwh']:.2f} kWh/day",
        )


        st.metric(
            "PV Array Size",
            f"{float(design_results['pv_size']):.2f} kW",
        )


    with result_col2:

        st.metric(
            "Number of Panels",
            int(
                design_results[
                    "number_of_panels"
                ]
            ),
        )


        st.metric(
            "Panel Rating",
            f"{design_results['panel_power_w']:.0f} W",
        )


    with result_col3:

        st.metric(
            "Peak Sun Hours",
            f"{design_results['sun_hours']:.2f}",
        )


        st.metric(
            "Location",
            design_results.get(
                "location"
            )
            or "Custom Location",
        )


    st.subheader(
        "🔋 Battery System"
    )


    st.write(
        design_results[
            "battery"
        ]
    )


    st.subheader(
        "⚡ Inverter System"
    )


    st.write(
        design_results[
            "inverter"
        ]
    )


    st.subheader(
        "🌱 Carbon Reduction"
    )


    st.write(
        design_results[
            "carbon"
        ]
    )


# ==========================================================
# SECTION 20 - SOLAR ANALYTICS
# ==========================================================

solar_data = st.session_state.get(
    "solar_data"
)


if solar_data:

    st.divider()


    st.header(
        "📈 Solar Resource Analytics"
    )


    try:

        analytics_result = (
            analyze_solar_resource(
                solar_data
            )
        )


        if analytics_result:

            st.write(
                analytics_result
            )

    except Exception as error:

        st.warning(
            f"Solar analytics could not be generated: {error}"
        )


# ==========================================================
# SECTION 21 - AI SOLAR ADVISOR
# ==========================================================

if design_results:

    st.divider()


    st.header(
        "🤖 AI Solar Advisor"
    )


    if st.button(
        "Generate AI Recommendations",
        use_container_width=True,
    ):

        try:

            recommendations = (
                generate_ai_recommendations(
                    design_results
                )
            )


            st.session_state[
                "ai_recommendations"
            ] = recommendations

        except Exception as error:

            st.error(
                f"AI recommendation failed: {error}"
            )


    if (
        "ai_recommendations"
        in st.session_state
    ):

        st.write(
            st.session_state[
                "ai_recommendations"
            ]
        )


# ==========================================================
# SECTION 22 - PROJECT COST DIARY
# ==========================================================

if COST_DIARY_AVAILABLE:

    st.divider()


    display_cost_diary(st)


# ==========================================================
# SECTION 23 - PDF REPORT
# ==========================================================

if design_results:

    st.divider()


    st.header(
        "📄 Design Report"
    )


    if st.button(
        "Generate PDF Report",
        use_container_width=True,
    ):

        try:

            pdf_data = create_pdf_report(
                design_results
            )


            if pdf_data:

                st.download_button(
                    label="⬇️ Download Solar PV Design Report",
                    data=pdf_data,
                    file_name=(
                        "solar_pv_design_report.pdf"
                    ),
                    mime="application/pdf",
                    use_container_width=True,
                )

        except Exception as error:

            st.error(
                f"PDF report generation failed: {error}"
            )


# ==========================================================
# SECTION 24 - FOOTER
# ==========================================================

st.divider()


st.caption(
    "Solar PV Designer Pro Africa™ v2.4.1 | "
    "Developed by Engr. Prof. Ibrahim Sani Madugu"
)
```
