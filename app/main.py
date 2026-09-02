# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# MAIN STREAMLIT APPLICATION
#
# Version: 2.4.3
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
# IMPORTANT
# ----------------------------------------------------------
# Product Library and Product Management use the same
# central SQLite database:
#
# app/data/solar_pv_library.db
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
#
# IMPORTANT:
# Only import functions that actually exist in the current
# appliance_energy.py.
# ==========================================================

try:

    from appliance_energy import (
        display_appliance_calculator,
    )

    APPLIANCE_MODULE_AVAILABLE = True
    APPLIANCE_IMPORT_ERROR = None

except Exception as error:

    APPLIANCE_MODULE_AVAILABLE = False
    APPLIANCE_IMPORT_ERROR = error


# ==========================================================
# COST DIARY
# ==========================================================

try:

    from costing import (
        display_cost_diary,
    )

    COST_DIARY_AVAILABLE = True
    COST_DIARY_IMPORT_ERROR = None

except Exception as error:

    COST_DIARY_AVAILABLE = False
    COST_DIARY_IMPORT_ERROR = error


# ==========================================================
# CENTRAL PRODUCT DATABASE
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
# SECTION 2 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(

    page_title="Solar PV Designer Pro Africa",

    page_icon="☀️",

    layout="wide",

    initial_sidebar_state="expanded",

)


# ==========================================================
# SECTION 3 - APPLICATION SESSION STATE
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

    "appliance_loads": [],

    "energy_source": "Appliance Planner",

    "design_results": None,

    "ai_recommendations": None,

    "cost_diary": [],

}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# SECTION 4 - CENTRAL DATABASE INITIALIZATION
# ==========================================================

if PRODUCT_DATABASE_AVAILABLE:

    try:

        initialize_database()

    except Exception as error:

        st.sidebar.warning(
            "Product database initialization warning."
        )

        st.sidebar.caption(
            str(error)
        )

else:

    st.sidebar.warning(
        "Central Product Database unavailable."
    )


# ==========================================================
# SECTION 5 - SIDEBAR HEADER
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
# APPLICATION NAVIGATION
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
# SECTION 6 - PRODUCT LIBRARY PAGE
# ==========================================================

if app_page == "📦 Product Library":

    st.title(
        "📦 Solar PV Product Library"
    )

    st.caption(
        "Create, store, search, compare and manage "
        "solar PV products using the central SQLite database."
    )

    if PRODUCT_DATABASE_AVAILABLE:

        try:

            initialize_database()

        except Exception as error:

            st.error(
                "Unable to initialize the product database."
            )

            st.exception(error)

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
# SECTION 7 - PRODUCT MANAGEMENT PAGE
# ==========================================================

if app_page == "🛠️ Product Management":

    st.title(
        "🛠️ Product Library Management"
    )

    st.caption(
        "Inspect, edit and safely delete products "
        "from the central Solar PV Product Library."
    )

    if PRODUCT_DATABASE_AVAILABLE:

        try:

            initialize_database()

        except Exception as error:

            st.error(
                "Unable to initialize the product database."
            )

            st.exception(error)

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
# SECTION 8 - MAIN SOLAR PV DESIGNER
# ==========================================================

st.title(
    "☀️ SOLAR PV DESIGNER PRO AFRICA™"
)

st.caption(
    "Professional Solar PV System Design, Resource "
    "Assessment, Sizing and Decision Support"
)


st.info(
    """
    Welcome to Solar PV Designer Pro Africa™.

    This platform supports solar-resource assessment,
    appliance energy analysis, PV sizing, battery sizing,
    inverter sizing, carbon-reduction assessment,
    AI-assisted recommendations and professional reporting.
    """
)


# ==========================================================
# SECTION 9 - LOCATION SELECTION
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

                else:

                    st.warning(
                        "No locations were found."
                    )

            except Exception as error:

                st.error(
                    f"Location search failed: {error}"
                )


    search_results = st.session_state.get(
        "location_search_results",
        []
    )


    if search_results:

        st.markdown(
            "### 📍 Search Results"
        )


        labels = []

        for result in search_results:

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

            range(
                len(search_results)
            ),

            format_func=lambda index:
                labels[index],

            key="selected_search_location",

        )


        if st.button(

            "✅ Use Selected Location",

            use_container_width=True,

            key="use_selected_search_location",

        ):

            selected = search_results[
                selected_index
            ]


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

            except Exception:

                latitude = None
                longitude = None


            if (
                latitude is not None
                and longitude is not None
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
                    selected.get(
                        "display_name"
                    )
                    or selected.get(
                        "name"
                    )
                    or "Selected Location"
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

                st.rerun()


# ==========================================================
# MAP LOCATION
# ==========================================================

if location_method == "🗺️ Select on Map":

    st.subheader(
        "🗺️ Select Location on Map"
    )

    try:

        map_result = display_location_map()

        if map_result:

            if isinstance(
                map_result,
                dict
            ):

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
                        "latitude"
                    ] = float(latitude)

                    st.session_state[
                        "longitude"
                    ] = float(longitude)

                    st.session_state[
                        "location_description"
                    ] = "Map Selected Location"

                    st.session_state[
                        "location_source"
                    ] = "Interactive Map"

    except Exception as error:

        st.warning(
            f"Interactive map could not be loaded: {error}"
        )


# ==========================================================
# MANUAL COORDINATES
# ==========================================================

if location_method == "📐 Enter Coordinates":

    st.subheader(
        "📐 Enter Geographic Coordinates"
    )


    coordinate_col1, coordinate_col2 = (
        st.columns(2)
    )


    with coordinate_col1:

        latitude_input = st.number_input(

            "Latitude",

            min_value=-90.0,

            max_value=90.0,

            value=float(
                st.session_state.get(
                    "latitude"
                )
                or 0.0
            ),

            step=0.01,

            key="manual_latitude",

        )


    with coordinate_col2:

        longitude_input = st.number_input(

            "Longitude",

            min_value=-180.0,

            max_value=180.0,

            value=float(
                st.session_state.get(
                    "longitude"
                )
                or 0.0
            ),

            step=0.01,

            key="manual_longitude",

        )


    location_name = st.text_input(

        "Location Name",

        value=(
            st.session_state.get(
                "location_description"
            )
            or ""
        ),

        placeholder="e.g. Kampala, Uganda",

        key="manual_location_name",

    )


    if st.button(

        "📍 Use These Coordinates",

        use_container_width=True,

        key="use_manual_coordinates",

    ):

        st.session_state[
            "latitude"
        ] = latitude_input

        st.session_state[
            "longitude"
        ] = longitude_input

        st.session_state[
            "location_description"
        ] = (
            location_name.strip()
            or "Custom Coordinates"
        )

        st.session_state[
            "location_source"
        ] = "Manual Coordinates"

        st.session_state[
            "location_ready"
        ] = True

        st.success(
            "Coordinates accepted."
        )


# ==========================================================
# SOLAR DATABASE
# ==========================================================

if location_method == "☀️ Solar Database":

    st.subheader(
        "☀️ Solar Resource Database"
    )


    try:

        database = load_solar_database()


        if database is None:

            st.warning(
                "Solar database is unavailable."
            )

        elif isinstance(
            database,
            pd.DataFrame
        ):

            if database.empty:

                st.warning(
                    "The solar database contains no records."
                )

            else:

                st.dataframe(

                    database,

                    use_container_width=True,

                    hide_index=True,

                )


                st.info(
                    "Select a location using the database "
                    "interface provided by the current data module."
                )

        elif isinstance(
            database,
            list
        ):

            if not database:

                st.warning(
                    "The solar database contains no records."
                )

            else:

                df_database = pd.DataFrame(
                    database
                )

                st.dataframe(

                    df_database,

                    use_container_width=True,

                    hide_index=True,

                )

    except Exception as error:

        st.error(
            f"Solar database could not be loaded: {error}"
        )


# ==========================================================
# LOCATION STATUS
# ==========================================================

latitude = st.session_state.get(
    "latitude"
)

longitude = st.session_state.get(
    "longitude"
)


if latitude is not None and longitude is not None:

    st.session_state[
        "location_ready"
    ] = True


if st.session_state.get(
    "location_ready"
):

    st.success(

        f"""
        📍 Location:

        **{st.session_state.get(
            "location_description"
        ) or "Selected Location"}**

        Coordinates:

        **{float(latitude):.5f},
        {float(longitude):.5f}**
        """

    )


# ==========================================================
# NASA POWER SOLAR RESOURCE
# ==========================================================

if st.session_state.get(
    "location_ready"
):

    st.divider()

    st.header(
        "☀️ Solar Resource Assessment"
    )


    if st.button(

        "🌞 Retrieve Solar Resource Data",

        use_container_width=True,

        key="retrieve_solar_resource",

    ):

        try:

            resource = get_location_solar_resource(

                latitude=float(
                    st.session_state[
                        "latitude"
                    ]
                ),

                longitude=float(
                    st.session_state[
                        "longitude"
                    ]
                ),

                location_name=(
                    st.session_state.get(
                        "location_description"
                    )
                    or "Selected Location"
                ),

            )


            if resource:

                st.session_state[
                    "solar_data"
                ] = resource


                try:

                    summary = get_location_summary(
                        resource
                    )

                except Exception:

                    summary = None


                st.session_state[
                    "location_summary"
                ] = summary


                if isinstance(
                    summary,
                    dict
                ):

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


                if (
                    st.session_state.get(
                        "sun_hours"
                    ) is not None
                ):

                    st.success(
                        "Solar resource data retrieved successfully."
                    )

                else:

                    st.warning(
                        "Solar resource was retrieved, "
                        "but peak-sun-hour data was not available."
                    )

            else:

                st.warning(
                    "No solar resource data was returned."
                )

        except Exception as error:

            st.error(
                f"Solar resource retrieval failed: {error}"
            )


# ==========================================================
# DISPLAY SOLAR RESOURCE SUMMARY
# ==========================================================

solar_summary = st.session_state.get(
    "location_summary"
)


if isinstance(
    solar_summary,
    dict
):

    st.subheader(
        "📊 Solar Resource Summary"
    )


    summary_col1, summary_col2, summary_col3 = (
        st.columns(3)
    )


    with summary_col1:

        value = solar_summary.get(
            "peak_sun_hours"
        )

        st.metric(

            "Peak Sun Hours",

            (
                f"{float(value):.2f}"
                if value is not None
                else "N/A"
            ),

        )


    with summary_col2:

        value = solar_summary.get(
            "average_temperature"
        )

        st.metric(

            "Average Temperature",

            (
                f"{float(value):.1f} °C"
                if value is not None
                else "N/A"
            ),

        )


    with summary_col3:

        st.metric(

            "Location",

            st.session_state.get(
                "location_description"
            )
            or "Selected Location",

        )


# ==========================================================
# APPLIANCE ENERGY PLANNER
# ==========================================================

st.divider()

st.header(
    "🔌 Appliance Energy Planner"
)

st.write(
    """
    Build the project's electricity demand from the
    appliances that will be used at the site.

    The planner calculates daily energy demand from
    appliance quantity, wattage and operating hours.
    """
)


appliance_records = []
appliance_daily_energy = 0.0


if APPLIANCE_MODULE_AVAILABLE:

    try:

        appliance_result = (
            display_appliance_calculator(st)
        )


        if isinstance(
            appliance_result,
            tuple
        ):

            appliance_records = (
                appliance_result[0]
                or []
            )

            appliance_daily_energy = float(
                appliance_result[1]
                or 0.0
            )

        else:

            appliance_records = (
                appliance_result
                or []
            )


            appliance_daily_energy = 0.0


    except Exception as error:

        st.error(
            "The Appliance Energy Planner encountered "
            f"an error: {error}"
        )

else:

    st.error(
        "The Appliance Energy Planner could not be loaded."
    )

    if APPLIANCE_IMPORT_ERROR:

        st.exception(
            APPLIANCE_IMPORT_ERROR
        )


# ==========================================================
# ENERGY DEMAND SOURCE
# ==========================================================

st.divider()

st.subheader(
    "⚡ Energy Demand for PV Design"
)


energy_source = st.radio(

    "Choose the source of daily energy demand",

    [

        "Appliance Planner",

        "Manual Input",

    ],

    horizontal=True,

    key="energy_source_selector",

)


if (
    energy_source == "Appliance Planner"
):

    if (
        appliance_records
        and appliance_daily_energy > 0
    ):

        energy = float(
            appliance_daily_energy
        )


        st.success(

            f"""
            Appliance Planner demand:

            **{energy:.2f} kWh/day**

            This value will be used for PV sizing.
            """

        )

    else:

        energy = 0.0


        st.warning(

            """
            No appliance demand is currently available.

            Add appliances above or select **Manual Input**.
            """

        )

else:

    energy = st.number_input(

        "Daily Energy Consumption (kWh/day)",

        min_value=0.1,

        value=5.0,

        step=0.1,

        key="manual_energy_demand",

    )


# ==========================================================
# SYSTEM DESIGN INPUTS
# ==========================================================

st.divider()

st.header(
    "⚙️ Solar PV System Design Inputs"
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

        key="design_panel_power",

    )


    system_efficiency = st.number_input(

        "Overall System Efficiency",

        min_value=0.50,

        max_value=1.00,

        value=0.80,

        step=0.01,

        key="design_system_efficiency",

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

        key="design_battery_voltage",

    )


    battery_dod = st.number_input(

        "Battery Depth of Discharge",

        min_value=0.10,

        max_value=1.00,

        value=0.80,

        step=0.05,

        key="design_battery_dod",

    )


with design_col3:

    autonomy_days = st.number_input(

        "Days of Autonomy",

        min_value=1,

        max_value=30,

        value=1,

        step=1,

        key="design_autonomy_days",

    )


    inverter_safety_factor = st.number_input(

        "Inverter Safety Factor",

        min_value=1.0,

        max_value=2.0,

        value=1.25,

        step=0.05,

        key="design_inverter_safety_factor",

    )


# ==========================================================
# DESIGN BUTTON
# ==========================================================

design_button = st.button(

    "🚀 Design Solar PV System",

    type="primary",

    use_container_width=True,

    disabled=(

        not st.session_state.get(
            "location_ready",
            False
        )

        or energy <= 0

    ),

)


# ==========================================================
# ENGINEERING DESIGN
# ==========================================================

if design_button:

    sun_hours = st.session_state.get(
        "sun_hours"
    )


    temperature = st.session_state.get(
        "temperature"
    )


    if (
        sun_hours is None
        or float(sun_hours) <= 0
    ):

        st.error(
            "Please retrieve valid solar-resource data "
            "before designing the system."
        )

    else:

        try:

            # ------------------------------------------------
            # PV ARRAY
            # ------------------------------------------------

            try:

                pv_size = calculate_pv_size(

                    energy,

                    float(sun_hours),

                    system_efficiency,

                )

            except TypeError:

                pv_size = calculate_pv_size(

                    energy=energy,

                    sun_hours=float(
                        sun_hours
                    ),

                    efficiency=system_efficiency,

                    temperature=temperature,

                )


            # ------------------------------------------------
            # NUMBER OF PANELS
            # ------------------------------------------------

            try:

                number_of_panels = calculate_panels(

                    pv_size,

                    panel_power,

                )

            except TypeError:

                number_of_panels = (
                    float(pv_size)
                    * 1000
                    / float(panel_power)
                )

                number_of_panels = int(
                    -(-number_of_panels // 1)
                )


            # ------------------------------------------------
            # BATTERY
            # ------------------------------------------------

            battery_result = calculate_battery(

                energy,

                autonomy_days,

                battery_voltage,

                battery_dod,

            )


            # ------------------------------------------------
            # CONNECTED LOAD
            # ------------------------------------------------

            connected_load = 0.0


            if appliance_records:

                for appliance in appliance_records:

                    try:

                        quantity = float(
                            appliance.get(
                                "Quantity",
                                0
                            )
                        )

                        wattage = float(
                            appliance.get(
                                "Wattage (W)",
                                0
                            )
                        )

                        connected_load += (
                            quantity
                            * wattage
                        )

                    except Exception:

                        pass


            if connected_load <= 0:

                connected_load = (
                    energy
                    * 1000
                    / max(
                        float(sun_hours),
                        1.0
                    )
                )


            # ------------------------------------------------
            # INVERTER
            # ------------------------------------------------

            inverter_result = calculate_inverter(

                connected_load,

                inverter_safety_factor,

            )


            # ------------------------------------------------
            # CARBON
            # ------------------------------------------------

            carbon_result = calculate_carbon(
                energy
            )


            # ------------------------------------------------
            # DESIGN RESULTS
            # ------------------------------------------------

            design_results = {

                "daily_energy_kwh":
                    float(energy),

                "sun_hours":
                    float(sun_hours),

                "temperature":
                    temperature,

                "pv_size":
                    float(pv_size),

                "number_of_panels":
                    int(
                        number_of_panels
                    ),

                "panel_power_w":
                    float(panel_power),

                "battery_voltage":
                    battery_voltage,

                "battery_dod":
                    battery_dod,

                "autonomy_days":
                    autonomy_days,

                "connected_load_w":
                    connected_load,

                "battery":
                    battery_result,

                "inverter":
                    inverter_result,

                "carbon":
                    carbon_result,

                "location":
                    (
                        st.session_state.get(
                            "location_description"
                        )
                        or "Custom Location"
                    ),

                "latitude":
                    st.session_state.get(
                        "latitude"
                    ),

                "longitude":
                    st.session_state.get(
                        "longitude"
                    ),

                "location_source":
                    st.session_state.get(
                        "location_source"
                    ),

            }


            st.session_state[
                "design_results"
            ] = design_results


            st.success(
                "✅ Solar PV system design completed successfully."
            )


        except Exception as error:

            st.error(
                f"System design failed: {error}"
            )

            st.exception(error)


# ==========================================================
# DESIGN RESULTS
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

            (
                f"{float(
                    design_results[
                        'daily_energy_kwh'
                    ]
                ):.2f} kWh/day"
            ),

        )


        st.metric(

            "PV Array Size",

            (
                f"{float(
                    design_results[
                        'pv_size'
                    ]
                ):.2f} kW"
            ),

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

            (
                f"{float(
                    design_results[
                        'panel_power_w'
                    ]
                ):.0f} W"
            ),

        )


    with result_col3:

        st.metric(

            "Peak Sun Hours",

            (
                f"{float(
                    design_results[
                        'sun_hours'
                    ]
                ):.2f}"
            ),

        )


        st.metric(

            "Location",

            design_results.get(
                "location"
            )
            or "Custom Location",

        )


    # ======================================================
    # BATTERY
    # ======================================================

    st.subheader(
        "🔋 Battery System"
    )

    battery_result = design_results.get(
        "battery"
    )

    if isinstance(
        battery_result,
        dict
    ):

        st.json(
            battery_result
        )

    else:

        st.write(
            battery_result
        )


    # ======================================================
    # INVERTER
    # ======================================================

    st.subheader(
        "⚡ Inverter System"
    )

    inverter_result = design_results.get(
        "inverter"
    )

    if isinstance(
        inverter_result,
        dict
    ):

        st.json(
            inverter_result
        )

    else:

        st.write(
            inverter_result
        )


    # ======================================================
    # CARBON
    # ======================================================

    st.subheader(
        "🌱 Carbon Reduction"
    )

    carbon_result = design_results.get(
        "carbon"
    )

    if isinstance(
        carbon_result,
        dict
    ):

        st.json(
            carbon_result
        )

    else:

        st.write(
            carbon_result
        )


# ==========================================================
# SOLAR ANALYTICS
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

            if isinstance(
                analytics_result,
                dict
            ):

                st.json(
                    analytics_result
                )

            else:

                st.write(
                    analytics_result
                )

    except Exception as error:

        st.warning(
            "Solar analytics could not be generated: "
            f"{error}"
        )


# ==========================================================
# AI SOLAR ADVISOR
# ==========================================================

if design_results:

    st.divider()

    st.header(
        "🤖 AI Solar Advisor"
    )


    if st.button(

        "Generate AI Recommendations",

        use_container_width=True,

        key="generate_ai_recommendations",

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


    recommendations = st.session_state.get(
        "ai_recommendations"
    )


    if recommendations:

        st.write(
            recommendations
        )


# ==========================================================
# PROJECT COST DIARY
# ==========================================================

if COST_DIARY_AVAILABLE:

    st.divider()

    try:

        display_cost_diary(st)

    except Exception as error:

        st.error(
            "The Project Cost Diary encountered "
            f"an error: {error}"
        )

else:

    st.divider()

    st.warning(
        "Project Cost Diary is currently unavailable."
    )


    if COST_DIARY_IMPORT_ERROR:

        with st.expander(
            "View Cost Diary Import Error"
        ):

            st.exception(
                COST_DIARY_IMPORT_ERROR
            )


# ==========================================================
# PDF REPORT
# ==========================================================

if design_results:

    st.divider()

    st.header(
        "📄 Professional Design Report"
    )


    if st.button(

        "📄 Generate PDF Report",

        use_container_width=True,

        key="generate_pdf_report",

    ):

        try:

            pdf_data = create_pdf_report(
                design_results
            )


            if pdf_data:

                st.download_button(

                    label=(
                        "⬇️ Download Solar PV "
                        "Design Report"
                    ),

                    data=pdf_data,

                    file_name=(
                        "solar_pv_design_report.pdf"
                    ),

                    mime="application/pdf",

                    use_container_width=True,

                    key="download_pdf_report",

                )

            else:

                st.warning(
                    "The PDF generator returned no data."
                )


        except Exception as error:

            st.error(
                f"PDF report generation failed: {error}"
            )

            st.exception(error)


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    "Solar PV Designer Pro Africa™ v2.4.3 | "
    "Developed by Engr. Prof. Ibrahim Sani Madugu"
)
