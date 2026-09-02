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
#
# IMPORTANT:
# The current appliance_energy.py uses the v2.4 interface:
#
#     display_appliance_calculator(st)
#
# It does NOT expose the old functions:
#
#     create_appliance
#     calculate_total_daily_energy
#     calculate_total_monthly_energy
#     calculate_total_connected_load
#
# Therefore we import only the function that actually exists.
# ==========================================================

try:

    from appliance_energy import (
        display_appliance_calculator,
    )

    APPLIANCE_MODULE_AVAILABLE = True
    APPLIANCE_MODULE_IMPORT_ERROR = None

except Exception as error:

    APPLIANCE_MODULE_AVAILABLE = False
    APPLIANCE_MODULE_IMPORT_ERROR = error


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

    "design_results": None,

    "appliance_loads": [],

    "use_appliance_demand": False,

    "cost_diary": [],

}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# SECTION 5 - APPLICATION SIDEBAR
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
# MODULE STATUS
# ==========================================================

with st.sidebar.expander(
    "🔧 Module Status",
    expanded=False,
):

    if APPLIANCE_MODULE_AVAILABLE:

        st.success(
            "✅ Appliance Energy"
        )

    else:

        st.error(
            "❌ Appliance Energy"
        )

    if COST_DIARY_AVAILABLE:

        st.success(
            "✅ Cost Diary"
        )

    else:

        st.error(
            "❌ Cost Diary"
        )

    if PRODUCT_LIBRARY_AVAILABLE:

        st.success(
            "✅ Product Library"
        )

    else:

        st.error(
            "❌ Product Library"
        )

    if PRODUCT_MANAGEMENT_AVAILABLE:

        st.success(
            "✅ Product Management"
        )

    else:

        st.error(
            "❌ Product Management"
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

        "💰 Cost Diary",

    ],

    key="main_application_navigation",

)


# ==========================================================
# SECTION 7 - PRODUCT LIBRARY PAGE
# ==========================================================

if app_page == "📦 Product Library":

    st.title(
        "📦 Solar PV Product Library"
    )

    st.caption(
        "Create, store, search, edit and manage "
        "Solar PV components."
    )

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

    st.title(
        "🛠️ Product Library Management"
    )

    st.caption(
        "Inspect, search, edit and safely delete "
        "products from your Solar PV Product Library."
    )

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
# SECTION 9 - COST DIARY PAGE
# ==========================================================

if app_page == "💰 Cost Diary":

    st.title(
        "💰 Solar PV Project Cost Diary"
    )

    st.caption(
        "Record actual local-market equipment and "
        "project costs in their respective currencies."
    )

    if COST_DIARY_AVAILABLE:

        try:

            display_cost_diary(st)

        except Exception as error:

            st.error(
                "The Cost Diary encountered an error."
            )

            st.exception(error)

    else:

        st.error(
            "The Cost Diary module could not be loaded."
        )

        if COST_DIARY_IMPORT_ERROR:

            st.exception(
                COST_DIARY_IMPORT_ERROR
            )

    st.stop()


# ==========================================================
# SECTION 10 - MAIN SOLAR PV DESIGNER
# ==========================================================

st.title(
    "☀️ SOLAR PV DESIGNER PRO AFRICA™"
)

st.caption(
    "Professional Solar PV System Design, "
    "Solar Resource Assessment, Sizing and "
    "Decision Support"
)


st.info(
    """
    Welcome to Solar PV Designer Pro Africa™.

    Select a location, assess the available solar resource,
    build your appliance energy demand, size the PV array,
    estimate battery and inverter requirements, assess
    carbon reduction, obtain AI-assisted recommendations,
    review project costs and generate a professional report.
    """
)


# ==========================================================
# SECTION 11 - LOCATION SELECTION
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
                        "No locations found."
                    )

            except Exception as error:

                st.error(
                    "Location search failed."
                )

                st.exception(error)


    search_results = st.session_state[
        "location_search_results"
    ]


    if search_results:

        st.markdown(
            "### 📍 Search Results"
        )

        result_labels = []

        for result in search_results:

            try:

                result_labels.append(
                    format_search_result(
                        result
                    )
                )

            except Exception:

                result_labels.append(
                    str(result)
                )


        selected_index = st.selectbox(

            "Select a location",

            range(
                len(
                    search_results
                )
            ),

            format_func=lambda i:
                result_labels[i],

            key="selected_search_location",

        )


        if st.button(

            "✅ Use Selected Location",

            use_container_width=True,

            key="use_selected_location",

        ):

            selected = search_results[
                selected_index
            ]

            latitude = selected.get(
                "latitude"
            )

            longitude = selected.get(
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
                ] = selected.get(
                    "display_name",
                    selected.get(
                        "name",
                        "Selected Location"
                    )
                )

                st.session_state[
                    "location_source"
                ] = "Worldwide Search"

                st.session_state[
                    "location_ready"
                ] = True

                st.success(
                    "Location selected successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Selected location does not contain "
                    "valid coordinates."
                )


# ==========================================================
# MAP LOCATION
# ==========================================================

elif location_method == "🗺️ Select on Map":

    st.subheader(
        "🗺️ Select Location on Interactive Map"
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

            else:

                try:

                    latitude, longitude = map_result

                except Exception:

                    latitude = None
                    longitude = None


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
                ] = (
                    f"Map Location "
                    f"({float(latitude):.5f}, "
                    f"{float(longitude):.5f})"
                )

                st.session_state[
                    "location_source"
                ] = "Interactive Map"

                st.session_state[
                    "location_ready"
                ] = True

    except Exception as error:

        st.error(
            "Interactive map could not be displayed."
        )

        st.exception(error)


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

            value=float(
                st.session_state[
                    "latitude"
                ]
                if st.session_state[
                    "latitude"
                ] is not None
                else 0.0
            ),

            step=0.0001,

            format="%.5f",

            key="manual_latitude",

        )

    with col2:

        longitude = st.number_input(

            "Longitude",

            min_value=-180.0,

            max_value=180.0,

            value=float(
                st.session_state[
                    "longitude"
                ]
                if st.session_state[
                    "longitude"
                ] is not None
                else 0.0
            ),

            step=0.0001,

            format="%.5f",

            key="manual_longitude",

        )


    if st.button(

        "📍 Use These Coordinates",

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
            f"Coordinates "
            f"({latitude:.5f}, {longitude:.5f})"
        )

        st.session_state[
            "location_source"
        ] = "Manual Coordinates"

        st.session_state[
            "location_ready"
        ] = True

        st.success(
            "Coordinates saved."
        )


# ==========================================================
# SOLAR DATABASE
# ==========================================================

elif location_method == "☀️ Solar Database":

    st.subheader(
        "☀️ Solar Database"
    )

    try:

        solar_database = (
            load_solar_database()
        )

        if solar_database is None:

            st.warning(
                "Solar database returned no data."
            )

        else:

            if isinstance(
                solar_database,
                pd.DataFrame
            ):

                database_df = solar_database

            else:

                database_df = pd.DataFrame(
                    solar_database
                )


            if database_df.empty:

                st.warning(
                    "No solar database records found."
                )

            else:

                st.dataframe(
                    database_df,
                    use_container_width=True,
                    hide_index=True,
                )


                location_column = None

                for candidate in [

                    "Location",
                    "location",
                    "City",
                    "city",
                    "Name",
                    "name",

                ]:

                    if candidate in database_df.columns:

                        location_column = candidate

                        break


                if location_column:

                    location_names = (
                        database_df[
                            location_column
                        ]
                        .dropna()
                        .astype(str)
                        .tolist()
                    )

                    selected_name = st.selectbox(

                        "Select location",

                        location_names,

                        key="database_location_select",

                    )


                    if st.button(

                        "✅ Use Database Location",

                        use_container_width=True,

                        key="use_database_location",

                    ):

                        matching = database_df[
                            database_df[
                                location_column
                            ].astype(str)
                            == selected_name
                        ]

                        if not matching.empty:

                            row = matching.iloc[
                                0
                            ]

                            latitude = None
                            longitude = None


                            for candidate in [

                                "Latitude",
                                "latitude",
                                "Lat",
                                "lat",

                            ]:

                                if candidate in row.index:

                                    latitude = row[
                                        candidate
                                    ]

                                    break


                            for candidate in [

                                "Longitude",
                                "longitude",
                                "Lon",
                                "lon",

                            ]:

                                if candidate in row.index:

                                    longitude = row[
                                        candidate
                                    ]

                                    break


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
                                ] = selected_name

                                st.session_state[
                                    "location_source"
                                ] = "Solar Database"

                                st.session_state[
                                    "location_ready"
                                ] = True

                                st.success(
                                    "Database location selected."
                                )

                            else:

                                st.warning(
                                    "This database record does not "
                                    "contain usable coordinates."
                                )

    except Exception as error:

        st.error(
            "Solar database could not be loaded."
        )

        st.exception(error)


# ==========================================================
# CURRENT LOCATION STATUS
# ==========================================================

if st.session_state[
    "location_ready"
]:

    st.success(

        f"""
        📍 **Selected Location**

        {st.session_state["location_description"]}

        Latitude:
        `{st.session_state["latitude"]:.5f}`

        Longitude:
        `{st.session_state["longitude"]:.5f}`

        Source:
        `{st.session_state["location_source"]}`
        """
    )


# ==========================================================
# SECTION 12 - SOLAR RESOURCE ASSESSMENT
# ==========================================================

if st.session_state[
    "location_ready"
]:

    st.header(
        "☀️ Solar Resource Assessment"
    )

    latitude = st.session_state[
        "latitude"
    ]

    longitude = st.session_state[
        "longitude"
    ]


    if st.button(

        "☀️ Assess Solar Resource",

        type="primary",

        use_container_width=True,

        key="assess_solar_resource",

    ):

        try:

            solar_result = (
                get_location_solar_resource(

                    latitude,

                    longitude,

                    st.session_state[
                        "location_description"
                    ],

                )
            )

            st.session_state[
                "solar_data"
            ] = solar_result

            summary = get_location_summary(
                solar_result
            )

            st.session_state[
                "solar_summary"
            ] = summary

            if summary:

                st.session_state[
                    "sun_hours"
                ] = summary.get(
                    "peak_sun_hours",
                    summary.get(
                        "sun_hours"
                    )
                )

                st.session_state[
                    "temperature"
                ] = summary.get(
                    "average_temperature",
                    summary.get(
                        "temperature"
                    )
                )

            st.success(
                "Solar resource assessment completed."
            )

        except Exception as error:

            st.error(
                "Solar resource assessment failed."
            )

            st.exception(error)


    solar_summary = st.session_state[
        "solar_summary"
    ]


    if solar_summary:

        c1, c2, c3 = st.columns(3)

        with c1:

            sun_hours = solar_summary.get(
                "peak_sun_hours"
            )

            if sun_hours is not None:

                st.metric(
                    "Peak Sun Hours",
                    f"{float(sun_hours):.2f} h/day",
                )

        with c2:

            temperature = solar_summary.get(
                "average_temperature"
            )

            if temperature is not None:

                st.metric(
                    "Average Temperature",
                    f"{float(temperature):.1f} °C",
                )

        with c3:

            st.metric(
                "Location",
                st.session_state[
                    "location_description"
                ],
            )


# ==========================================================
# SECTION 13 - SOLAR ANALYTICS
# ==========================================================

if st.session_state[
    "solar_data"
]:

    st.header(
        "📊 Solar Analytics"
    )

    try:

        analytics_result = (
            analyze_solar_resource(
                st.session_state[
                    "solar_data"
                ]
            )
        )

        if analytics_result:

            if isinstance(
                analytics_result,
                pd.DataFrame
            ):

                st.dataframe(
                    analytics_result,
                    use_container_width=True,
                )

            elif isinstance(
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
            "Solar analytics could not be displayed."
        )

        st.exception(error)


# ==========================================================
# SECTION 14 - APPLIANCE ENERGY PLANNER
# ==========================================================

st.header(
    "🔌 Appliance Energy Demand"
)

st.caption(
    "Build the project's daily electricity demand "
    "from the actual appliances used at the site."
)


if APPLIANCE_MODULE_AVAILABLE:

    try:

        appliance_records, appliance_total = (
            display_appliance_calculator(st)
        )

    except Exception as error:

        st.error(
            "The Appliance Energy Planner encountered "
            "an error."
        )

        st.exception(error)

        appliance_records = (
            st.session_state.get(
                "appliance_loads",
                []
            )
        )

        appliance_total = 0.0

else:

    st.error(
        "The Appliance Energy Planner module "
        "could not be loaded."
    )

    if APPLIANCE_MODULE_IMPORT_ERROR:

        st.exception(
            APPLIANCE_MODULE_IMPORT_ERROR
        )

    appliance_records = (
        st.session_state.get(
            "appliance_loads",
            []
        )
    )

    appliance_total = 0.0


# ==========================================================
# DETERMINE ENERGY DEMAND
# ==========================================================

manual_energy = st.number_input(

    "Manual Daily Energy Demand (kWh/day)",

    min_value=0.0,

    value=5.0,

    step=0.1,

    key="manual_energy_demand",

)


use_appliance_demand = st.session_state.get(

    "use_appliance_demand",

    False,

)


if use_appliance_demand and appliance_total > 0:

    energy_demand = appliance_total

    energy_source = (
        "Appliance Energy Planner"
    )

    st.success(

        f"""
        🔌 Appliance demand is being used for
        PV sizing:

        **{energy_demand:.2f} kWh/day**
        """
    )

else:

    energy_demand = manual_energy

    energy_source = "Manual Input"

    st.info(

        f"""
        Manual energy demand is being used:

        **{energy_demand:.2f} kWh/day**
        """
    )


st.session_state[
    "energy_source"
] = energy_source


# ==========================================================
# SECTION 15 - SYSTEM DESIGN INPUTS
# ==========================================================

st.header(
    "⚙️ Solar PV System Design Inputs"
)


col1, col2, col3 = st.columns(3)


with col1:

    sun_hours_input = st.number_input(

        "Peak Sun Hours",

        min_value=0.1,

        max_value=12.0,

        value=float(
            st.session_state[
                "sun_hours"
            ]
            if st.session_state[
                "sun_hours"
            ] is not None
            else 4.5
        ),

        step=0.1,

        key="design_sun_hours",

    )


with col2:

    autonomy_days = st.number_input(

        "Battery Autonomy (days)",

        min_value=0.0,

        max_value=10.0,

        value=2.0,

        step=0.5,

        key="design_autonomy_days",

    )


with col3:

    system_voltage = st.selectbox(

        "System Voltage",

        [12, 24, 48],

        index=2,

        key="design_system_voltage",

    )


# ==========================================================
# DERATING
# ==========================================================

col1, col2, col3 = st.columns(3)


with col1:

    system_derating = st.number_input(

        "System Derating Factor",

        min_value=0.50,

        max_value=1.00,

        value=0.80,

        step=0.01,

        key="system_derating",

    )


with col2:

    battery_efficiency = st.number_input(

        "Battery Efficiency",

        min_value=0.50,

        max_value=1.00,

        value=0.90,

        step=0.01,

        key="battery_efficiency",

    )


with col3:

    depth_of_discharge = st.number_input(

        "Depth of Discharge",

        min_value=0.10,

        max_value=1.00,

        value=0.80,

        step=0.01,

        key="depth_of_discharge",

    )


# ==========================================================
# SECTION 16 - PV SYSTEM DESIGN
# ==========================================================

if st.button(

    "🚀 Calculate Solar PV System",

    type="primary",

    use_container_width=True,

    key="calculate_system",

):

    if energy_demand <= 0:

        st.error(
            "Daily energy demand must be greater than zero."
        )

    elif sun_hours_input <= 0:

        st.error(
            "Peak Sun Hours must be greater than zero."
        )

    else:

        try:

            # --------------------------------------------------
            # PV SIZE
            # --------------------------------------------------

            pv_size = calculate_pv_size(

                energy_demand,

                sun_hours_input,

                system_derating,

            )


            # --------------------------------------------------
            # PANEL COUNT
            # --------------------------------------------------

            panel_result = calculate_panels(

                pv_size,

                550,

            )


            # --------------------------------------------------
            # BATTERY
            # --------------------------------------------------

            battery_result = calculate_battery(

                energy_demand,

                autonomy_days,

                system_voltage,

                depth_of_discharge,

                battery_efficiency,

            )


            # --------------------------------------------------
            # INVERTER
            # --------------------------------------------------

            inverter_result = calculate_inverter(

                energy_demand,

                system_voltage,

            )


            # --------------------------------------------------
            # CARBON
            # --------------------------------------------------

            carbon_result = calculate_carbon(

                energy_demand,

            )


            st.session_state[
                "design_results"
            ] = {

                "energy_demand":
                    energy_demand,

                "energy_source":
                    energy_source,

                "sun_hours":
                    sun_hours_input,

                "pv_size":
                    pv_size,

                "panel_result":
                    panel_result,

                "battery_result":
                    battery_result,

                "inverter_result":
                    inverter_result,

                "carbon_result":
                    carbon_result,

            }


            st.success(
                "Solar PV system calculation completed."
            )


        except Exception as error:

            st.error(
                "Solar PV calculation failed."
            )

            st.exception(error)


# ==========================================================
# SECTION 17 - DISPLAY DESIGN RESULTS
# ==========================================================

results = st.session_state[
    "design_results"
]


if results:

    st.header(
        "📐 Solar PV Design Results"
    )


    c1, c2, c3, c4 = st.columns(4)


    with c1:

        st.metric(

            "Daily Energy",

            f"{results['energy_demand']:.2f} kWh/day",

        )


    with c2:

        try:

            st.metric(

                "PV Array",

                f"{float(results['pv_size']):.2f} kW",

            )

        except Exception:

            st.metric(

                "PV Array",

                str(
                    results["pv_size"]
                ),

            )


    with c3:

        st.metric(

            "Energy Source",

            results[
                "energy_source"
            ],

        )


    with c4:

        st.metric(

            "Peak Sun Hours",

            f"{results['sun_hours']:.2f} h/day",

        )


    st.subheader(
        "☀️ PV Array"
    )

    st.write(
        results[
            "panel_result"
        ]
    )


    st.subheader(
        "🔋 Battery Bank"
    )

    st.write(
        results[
            "battery_result"
        ]
    )


    st.subheader(
        "⚡ Inverter"
    )

    st.write(
        results[
            "inverter_result"
        ]
    )


    st.subheader(
        "🌱 Carbon Reduction"
    )

    st.write(
        results[
            "carbon_result"
        ]
    )


# ==========================================================
# SECTION 18 - AI SOLAR ADVISOR
# ==========================================================

st.header(
    "🤖 AI Solar Advisor"
)


if st.button(

    "🤖 Generate Solar Recommendation",

    use_container_width=True,

    key="generate_ai_recommendation",

):

    try:

        recommendation = (
            generate_ai_recommendations(
                results
                if results
                else {
                    "energy_demand":
                        energy_demand,

                    "sun_hours":
                        sun_hours_input,

                    "location":
                        st.session_state.get(
                            "location_description"
                        ),
                }
            )
        )

        st.session_state[
            "ai_recommendation"
        ] = recommendation

    except Exception as error:

        st.error(
            "AI recommendation could not be generated."
        )

        st.exception(error)


if "ai_recommendation" in st.session_state:

    st.markdown(
        "### 💡 Recommendation"
    )

    st.write(
        st.session_state[
            "ai_recommendation"
        ]
    )


# ==========================================================
# SECTION 19 - COST DIARY SUMMARY
# ==========================================================

if COST_DIARY_AVAILABLE:

    st.header(
        "💰 Project Cost Diary"
    )

    with st.expander(
        "Open Project Cost Diary",
        expanded=False,
    ):

        try:

            display_cost_diary(st)

        except Exception as error:

            st.error(
                "Cost Diary could not be displayed."
            )

            st.exception(error)


# ==========================================================
# SECTION 20 - PROFESSIONAL REPORT
# ==========================================================

st.header(
    "📄 Professional Solar PV Report"
)


if st.button(

    "📄 Generate PDF Report",

    use_container_width=True,

    key="generate_pdf_report",

):

    if not results:

        st.warning(
            "Please calculate the solar PV system first."
        )

    else:

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

                "energy_demand":
                    results.get(
                        "energy_demand"
                    ),

                "energy_source":
                    results.get(
                        "energy_source"
                    ),

                "sun_hours":
                    results.get(
                        "sun_hours"
                    ),

                "pv_size":
                    results.get(
                        "pv_size"
                    ),

                "panel_result":
                    results.get(
                        "panel_result"
                    ),

                "battery_result":
                    results.get(
                        "battery_result"
                    ),

                "inverter_result":
                    results.get(
                        "inverter_result"
                    ),

                "carbon_result":
                    results.get(
                        "carbon_result"
                    ),

                "appliances":
                    appliance_records,

            }


            pdf_result = create_pdf_report(
                report_data
            )


            if pdf_result:

                if isinstance(
                    pdf_result,
                    bytes
                ):

                    st.download_button(

                        "📥 Download PDF Report",

                        data=pdf_result,

                        file_name=(
                            "solar_pv_design_report.pdf"
                        ),

                        mime="application/pdf",

                        use_container_width=True,

                    )

                else:

                    try:

                        with open(
                            pdf_result,
                            "rb"
                        ) as file:

                            st.download_button(

                                "📥 Download PDF Report",

                                data=file.read(),

                                file_name=(
                                    "solar_pv_design_report.pdf"
                                ),

                                mime="application/pdf",

                                use_container_width=True,

                            )

                    except Exception:

                        st.write(
                            pdf_result
                        )

        except Exception as error:

            st.error(
                "PDF report generation failed."
            )

            st.exception(error)


# ==========================================================
# SECTION 21 - APPLICATION FOOTER
# ==========================================================

st.divider()

st.caption(
    "SOLAR PV DESIGNER PRO AFRICA™ v2.4.2"
)

st.caption(
    "Developed by Engr. Prof. Ibrahim Sani Madugu"
)

st.caption(
    "Professional Solar PV Design, Analysis and "
    "Decision Support Platform"
)
