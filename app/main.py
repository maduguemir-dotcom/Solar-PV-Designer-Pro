# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.4.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# ==========================================================
#
# V2.4.0 FEATURES
#
# NEW:
# - Appliance Energy Planner
# - Appliance quantity
# - Appliance wattage
# - Daily operating hours
# - Automatic daily energy calculation
# - Monthly energy estimate
# - Annual energy estimate
# - Appliance demand transfer to PV sizing
# - Project Cost Diary
# - Multiple currencies
# - Supplier and quotation notes
#
# RETAINED:
# - Worldwide location search
# - Interactive map
# - Manual coordinates
# - NASA POWER integration
# - Solar-resource statistics
# - Monthly solar graph
# - Monthly temperature graph
# - PV sizing
# - Battery sizing
# - Inverter sizing
# - Charge controller
# - Cost estimation
# - Carbon reduction
# - AI Solar Advisor
# - Professional PDF report
#
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
# PDF report
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
# Location engine
# ----------------------------------------------------------

from location_engine import (
    get_location_solar_resource,
    get_location_summary
)


# ----------------------------------------------------------
# Worldwide location search
# ----------------------------------------------------------

from location_search import (
    search_location,
    format_search_result
)


# ----------------------------------------------------------
# Interactive map
# ----------------------------------------------------------

from map_location import (
    display_location_map
)


# ----------------------------------------------------------
# Solar analytics
# ----------------------------------------------------------

from solar_analytics import (
    analyze_solar_resource
)


# ----------------------------------------------------------
# V2.4 Appliance Energy Module
# ----------------------------------------------------------

from appliance_energy import (
    display_appliance_calculator
)


# ----------------------------------------------------------
# V2.4 Cost Diary Module
# ----------------------------------------------------------

from costing import (
    display_cost_diary
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

    "design_results": None,

    "appliance_loads": [],

    "use_appliance_demand": False,

    "cost_diary": []

}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# SECTION 4 - HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "AI-Ready Renewable Energy Design Platform"
)

st.write(
    """
    Solar PV Designer Pro Africa™ is a renewable-energy
    engineering platform designed for preliminary
    photovoltaic system sizing, energy-demand analysis,
    battery sizing, project cost recording, environmental
    assessment and AI-assisted recommendations.
    """
)


# ==========================================================
# SECTION 5 - LOAD SOLAR DATABASE
# ==========================================================

try:

    solar_database = load_solar_database()

except Exception as error:

    st.error(
        f"Unable to load solar database: {error}"
    )

    st.stop()


# ==========================================================
# SECTION 6 - SIDEBAR
# ==========================================================

st.sidebar.header(
    "⚙️ Solar PV System Design"
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
        "Select on Map",
        "Enter Coordinates"
    ],
    key="location_source_selector"
)


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

            st.session_state[
                "location_description"
            ] = location

            st.session_state[
                "latitude"
            ] = None

            st.session_state[
                "longitude"
            ] = None

            st.session_state[
                "sun_hours"
            ] = sun_hours

            st.session_state[
                "temperature"
            ] = temperature

            st.session_state[
                "solar_data"
            ] = location_data

            st.session_state[
                "solar_summary"
            ] = None

            st.session_state[
                "location_summary"
            ] = None

            st.session_state[
                "location_ready"
            ] = True

            st.session_state[
                "location_source"
            ] = "Solar Database"

        except (
            TypeError,
            ValueError,
            KeyError
        ):

            st.session_state[
                "location_ready"
            ] = False

            st.sidebar.error(
                "The selected location contains "
                "invalid solar-resource data."
            )

    else:

        st.session_state[
            "location_ready"
        ] = False

        st.sidebar.error(
            "Selected location could not be found."
        )


# ==========================================================
# SECTION 9 - WORLDWIDE LOCATION SEARCH
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
        placeholder="Example: Kampala, Uganda"
    )

    search_button = st.sidebar.button(
        "🔎 Search",
        use_container_width=True
    )

    if search_button:

        if not search_query.strip():

            st.sidebar.warning(
                "Please enter a location."
            )

        else:

            with st.sidebar:

                with st.spinner(
                    "Searching worldwide..."
                ):

                    try:

                        results = search_location(
                            search_query,
                            limit=5
                        )

                    except Exception as error:

                        results = []

                        st.error(
                            f"Location search failed: {error}"
                        )

            st.session_state[
                "location_search_results"
            ] = results


    search_results = st.session_state.get(
        "location_search_results",
        []
    )


    if search_results:

        result_labels = [

            format_search_result(
                result
            )

            for result in search_results

        ]


        selected_label = st.sidebar.selectbox(
            "Select a search result",
            result_labels,
            key="selected_search_result"
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


            retrieve_search_data = (
                st.sidebar.button(
                    "☀️ Get Solar Data",
                    use_container_width=True
                )
            )


            if retrieve_search_data:

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
                    location_result
                    and location_result.get(
                        "success",
                        False
                    )
                ):

                    try:

                        summary = (
                            get_location_summary(
                                location_result
                            )
                        )

                    except Exception:

                        summary = {}


                    try:

                        retrieved_sun_hours = float(
                            summary.get(
                                "peak_sun_hours"
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        retrieved_sun_hours = None


                    try:

                        retrieved_temperature = float(
                            summary.get(
                                "average_temperature"
                            )
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        retrieved_temperature = 25.0


                    if (
                        retrieved_sun_hours is not None
                        and retrieved_sun_hours > 0
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
                            summary.get(
                                "location"
                            )
                            or
                            selected_location.get(
                                "display_name",
                                location_name
                            )
                        )

                        st.session_state[
                            "sun_hours"
                        ] = retrieved_sun_hours

                        st.session_state[
                            "temperature"
                        ] = retrieved_temperature

                        st.session_state[
                            "solar_data"
                        ] = location_result.get(
                            "solar"
                        )

                        st.session_state[
                            "solar_summary"
                        ] = location_result.get(
                            "summary"
                        )

                        st.session_state[
                            "location_summary"
                        ] = summary

                        st.session_state[
                            "location_ready"
                        ] = True

                        st.session_state[
                            "location_source"
                        ] = "NASA POWER"

                        st.sidebar.success(
                            "✅ NASA POWER data retrieved."
                        )

                    else:

                        st.sidebar.warning(
                            "NASA POWER returned no usable "
                            "solar-resource value."
                        )

                else:

                    st.sidebar.error(
                        "NASA POWER lookup failed."
                    )


# ==========================================================
# SECTION 10 - INTERACTIVE MAP
# ==========================================================

elif location_source == "Select on Map":

    st.header(
        "🗺️ Select Project Location on Map"
    )

    st.write(
        """
        Click anywhere on the map to select the
        location of your solar PV project.
        """
    )


    selected_map_location = (
        display_location_map()
    )


    if selected_map_location:

        map_latitude = (
            selected_map_location[
                "latitude"
            ]
        )

        map_longitude = (
            selected_map_location[
                "longitude"
            ]
        )


        st.session_state[
            "selected_map_location"
        ] = selected_map_location


        st.session_state[
            "latitude"
        ] = map_latitude


        st.session_state[
            "longitude"
        ] = map_longitude


        st.session_state[
            "location_description"
        ] = "Map Selected Location"


        st.info(
            f"""
            **Selected Coordinates**

            Latitude: {map_latitude:.6f}°

            Longitude: {map_longitude:.6f}°
            """
        )


        retrieve_map_data = st.button(
            "☀️ Retrieve Solar Data for Map Location",
            type="primary"
        )


        if retrieve_map_data:

            with st.spinner(
                "Connecting to NASA POWER..."
            ):

                try:

                    location_result = (
                        get_location_solar_resource(

                            latitude=map_latitude,

                            longitude=map_longitude,

                            location_name=(
                                "Map Selected Location"
                            ),

                            country=""

                        )
                    )

                except Exception as error:

                    location_result = {

                        "success": False,

                        "message": str(error)

                    }


            if (
                location_result
                and location_result.get(
                    "success",
                    False
                )
            ):

                try:

                    summary = (
                        get_location_summary(
                            location_result
                        )
                    )

                except Exception:

                    summary = {}


                try:

                    retrieved_sun_hours = float(
                        summary.get(
                            "peak_sun_hours"
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    retrieved_sun_hours = None


                try:

                    retrieved_temperature = float(
                        summary.get(
                            "average_temperature"
                        )
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    retrieved_temperature = 25.0


                if (
                    retrieved_sun_hours is not None
                    and retrieved_sun_hours > 0
                ):

                    st.session_state[
                        "latitude"
                    ] = map_latitude

                    st.session_state[
                        "longitude"
                    ] = map_longitude

                    st.session_state[
                        "location_description"
                    ] = (
                        summary.get(
                            "location"
                        )
                        or
                        "Map Selected Location"
                    )

                    st.session_state[
                        "sun_hours"
                    ] = retrieved_sun_hours

                    st.session_state[
                        "temperature"
                    ] = retrieved_temperature

                    st.session_state[
                        "solar_data"
                    ] = location_result.get(
                        "solar"
                    )

                    st.session_state[
                        "solar_summary"
                    ] = location_result.get(
                        "summary"
                    )

                    st.session_state[
                        "location_summary"
                    ] = summary

                    st.session_state[
                        "location_ready"
                    ] = True

                    st.session_state[
                        "location_source"
                    ] = "NASA POWER"


                    st.success(
                        "✅ NASA POWER data successfully "
                        "retrieved for the selected location."
                    )

                else:

                    st.warning(
                        """
                        NASA POWER responded successfully,
                        but no usable solar-resource values
                        were found.
                        """
                    )

            else:

                st.error(
                    "NASA POWER request failed."
                )

                if location_result:

                    st.caption(
                        location_result.get(
                            "message",
                            "No additional information."
                        )
                    )


# ==========================================================
# SECTION 11 - MANUAL COORDINATES
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


    manual_latitude = (
        st.sidebar.number_input(
            "Latitude",
            min_value=-90.0,
            max_value=90.0,
            value=0.3476,
            step=0.0001,
            format="%.4f"
        )
    )


    manual_longitude = (
        st.sidebar.number_input(
            "Longitude",
            min_value=-180.0,
            max_value=180.0,
            value=32.5825,
            step=0.0001,
            format="%.4f"
        )
    )


    manual_location_name = (
        st.sidebar.text_input(
            "Location Name",
            value="Kampala"
        )
    )


    manual_country = (
        st.sidebar.text_input(
            "Country",
            value="Uganda"
        )
    )


    retrieve_manual_data = (
        st.sidebar.button(
            "☀️ Get Solar Data",
            use_container_width=True
        )
    )


    if retrieve_manual_data:

        with st.sidebar:

            with st.spinner(
                "Connecting to NASA POWER..."
            ):

                try:

                    location_result = (
                        get_location_solar_resource(

                            latitude=manual_latitude,

                            longitude=manual_longitude,

                            location_name=manual_location_name,

                            country=manual_country

                        )
                    )

                except Exception as error:

                    location_result = {

                        "success": False,

                        "message": str(error)

                    }


        if (
            location_result
            and location_result.get(
                "success",
                False
            )
        ):

            try:

                summary = (
                    get_location_summary(
                        location_result
                    )
                )

            except Exception:

                summary = {}


            try:

                retrieved_sun_hours = float(
                    summary.get(
                        "peak_sun_hours"
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                retrieved_sun_hours = None


            try:

                retrieved_temperature = float(
                    summary.get(
                        "average_temperature"
                    )
                )

            except (
                TypeError,
                ValueError
            ):

                retrieved_temperature = 25.0


            if (
                retrieved_sun_hours is not None
                and retrieved_sun_hours > 0
            ):

                st.session_state[
                    "latitude"
                ] = manual_latitude

                st.session_state[
                    "longitude"
                ] = manual_longitude

                st.session_state[
                    "location_description"
                ] = (
                    summary.get(
                        "location"
                    )
                    or
                    f"{manual_location_name}, "
                    f"{manual_country}"
                )

                st.session_state[
                    "sun_hours"
                ] = retrieved_sun_hours

                st.session_state[
                    "temperature"
                ] = retrieved_temperature

                st.session_state[
                    "solar_data"
                ] = location_result.get(
                    "solar"
                )

                st.session_state[
                    "solar_summary"
                ] = location_result.get(
                    "summary"
                )

                st.session_state[
                    "location_summary"
                ] = summary

                st.session_state[
                    "location_ready"
                ] = True

                st.session_state[
                    "location_source"
                ] = "NASA POWER"


                st.sidebar.success(
                    "✅ Solar data retrieved."
                )

            else:

                st.sidebar.warning(
                    "No usable solar-resource value "
                    "was returned."
                )

        else:

            st.sidebar.error(
                "NASA POWER connection failed."
            )


# ==========================================================
# SECTION 12 - RESTORE LOCATION VARIABLES
# ==========================================================

location_ready = (
    st.session_state[
        "location_ready"
    ]
)

location_description = (
    st.session_state[
        "location_description"
    ]
)

latitude = (
    st.session_state[
        "latitude"
    ]
)

longitude = (
    st.session_state[
        "longitude"
    ]
)

sun_hours = (
    st.session_state[
        "sun_hours"
    ]
)

temperature = (
    st.session_state[
        "temperature"
    ]
)

solar_data = (
    st.session_state[
        "solar_data"
    ]
)

solar_summary = (
    st.session_state[
        "solar_summary"
    ]
)

location_summary = (
    st.session_state[
        "location_summary"
    ]
)


# ==========================================================
# SECTION 13 - LOCATION INFORMATION
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


    if longitude is None:

        longitude_display = "Database"

    else:

        longitude_display = (
            f"{longitude:.4f}°"
        )


    location_col2.metric(
        "Latitude",
        latitude_display
    )


    location_col3.metric(
        "Longitude",
        longitude_display
    )


    resource_col1, resource_col2, resource_col3 = (
        st.columns(3)
    )


    if sun_hours is not None:

        resource_col1.metric(
            "☀️ Peak Sun Hours",
            f"{float(sun_hours):.2f} h/day"
        )

    else:

        resource_col1.metric(
            "☀️ Peak Sun Hours",
            "Unavailable"
        )


    if temperature is not None:

        resource_col2.metric(
            "🌡️ Average Temperature",
            f"{float(temperature):.1f} °C"
        )

    else:

        resource_col2.metric(
            "🌡️ Average Temperature",
            "Unavailable"
        )


    resource_col3.metric(
        "📡 Data Source",
        (
            "Solar Database"
            if st.session_state[
                "location_source"
            ] == "Solar Database"
            else
            "NASA POWER"
        )
    )


else:

    st.warning(
        """
        📍 **Location not ready**

        Please select a location from the Solar Database,
        search for a place, select a point on the map,
        or provide coordinates before designing the
        solar PV system.
        """
    )


# ==========================================================
# SECTION 14 - NASA POWER DATA
# ==========================================================

if (
    location_ready
    and
    st.session_state[
        "location_source"
    ] != "Solar Database"
    and
    solar_data is not None
):

    with st.expander(
        "☀️ View NASA POWER Solar Data"
    ):

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
                    use_container_width=True,
                    hide_index=True
                )

            else:

                st.json(
                    solar_data
                )

        else:

            st.write(
                solar_data
            )


# ==========================================================
# SECTION 15 - SOLAR ANALYTICS
# ==========================================================

if (
    location_ready
    and
    isinstance(
        solar_data,
        dict
    )
):

    st.divider()

    st.header(
        "📈 Solar Resource Analytics"
    )


    try:

        analytics = (
            analyze_solar_resource(
                solar_data
            )
        )

    except Exception as error:

        analytics = {}

        st.warning(
            "Solar analytics could not be calculated: "
            f"{error}"
        )


    solar_statistics = (
        analytics.get(
            "solar_statistics",
            {}
        )
    )


    temperature_statistics = (
        analytics.get(
            "temperature_statistics",
            {}
        )
    )


    seasonal_analysis = (
        analytics.get(
            "seasonal_analysis",
            {}
        )
    )


    monthly_solar = (
        analytics.get(
            "monthly_solar",
            []
        )
    )


    monthly_temperature = (
        analytics.get(
            "monthly_temperature",
            []
        )
    )


    # ------------------------------------------------------
    # Solar statistics
    # ------------------------------------------------------

    st.subheader(
        "☀️ Solar Resource Statistics"
    )


    solar_col1, solar_col2, solar_col3 = (
        st.columns(3)
    )


    annual_average = (
        solar_statistics.get(
            "annual_average"
        )
    )


    maximum = (
        solar_statistics.get(
            "maximum"
        )
    )


    minimum = (
        solar_statistics.get(
            "minimum"
        )
    )


    solar_col1.metric(
        "Annual Average",
        (
            f"{float(annual_average):.2f} "
            "kWh/m²/day"
            if annual_average is not None
            else "N/A"
        )
    )


    solar_col2.metric(
        "Maximum",
        (
            f"{float(maximum):.2f} "
            "kWh/m²/day"
            if maximum is not None
            else "N/A"
        )
    )


    solar_col3.metric(
        "Minimum",
        (
            f"{float(minimum):.2f} "
            "kWh/m²/day"
            if minimum is not None
            else "N/A"
        )
    )


    best_month = (
        solar_statistics.get(
            "best_month"
        )
    )


    lowest_month = (
        solar_statistics.get(
            "lowest_month"
        )
    )


    st.write(
        f"**Best Solar Month:** "
        f"{best_month or 'N/A'}"
    )


    st.write(
        f"**Lowest Solar Month:** "
        f"{lowest_month or 'N/A'}"
    )


    # ------------------------------------------------------
    # Monthly solar graph
    # ------------------------------------------------------

    st.subheader(
        "☀️ Monthly Solar Resource"
    )


    if monthly_solar:

        solar_chart_data = (
            pd.DataFrame(
                monthly_solar
            )
        )


        if {
            "month_short",
            "solar_value"
        }.issubset(
            solar_chart_data.columns
        ):

            solar_chart_data = (
                solar_chart_data[
                    [
                        "month_short",
                        "solar_value"
                    ]
                ]
                .set_index(
                    "month_short"
                )
            )


            solar_chart_data.columns = [
                "Solar Resource (kWh/m²/day)"
            ]


            st.line_chart(
                solar_chart_data,
                use_container_width=True
            )

        else:

            st.info(
                "Monthly solar data format is unavailable."
            )

    else:

        st.info(
            "No monthly solar data available for graphing."
        )


    # ------------------------------------------------------
    # Temperature statistics
    # ------------------------------------------------------

    st.subheader(
        "🌡️ Temperature Statistics"
    )


    temperature_col1, temperature_col2, temperature_col3 = (
        st.columns(3)
    )


    temperature_average = (
        temperature_statistics.get(
            "annual_average"
        )
    )


    temperature_maximum = (
        temperature_statistics.get(
            "maximum"
        )
    )


    temperature_minimum = (
        temperature_statistics.get(
            "minimum"
        )
    )


    temperature_col1.metric(
        "Annual Average",
        (
            f"{float(temperature_average):.1f} °C"
            if temperature_average is not None
            else "N/A"
        )
    )


    temperature_col2.metric(
        "Maximum",
        (
            f"{float(temperature_maximum):.1f} °C"
            if temperature_maximum is not None
            else "N/A"
        )
    )


    temperature_col3.metric(
        "Minimum",
        (
            f"{float(temperature_minimum):.1f} °C"
            if temperature_minimum is not None
            else "N/A"
        )
    )


    hottest_month = (
        temperature_statistics.get(
            "hottest_month"
        )
    )


    coolest_month = (
        temperature_statistics.get(
            "coolest_month"
        )
    )


    st.write(
        f"**Hottest Month:** "
        f"{hottest_month or 'N/A'}"
    )


    st.write(
        f"**Coolest Month:** "
        f"{coolest_month or 'N/A'}"
    )


    # ------------------------------------------------------
    # Monthly temperature graph
    # ------------------------------------------------------

    st.subheader(
        "🌡️ Monthly Temperature"
    )


    if monthly_temperature:

        temperature_chart_data = (
            pd.DataFrame(
                monthly_temperature
            )
        )


        if {
            "month_short",
            "temperature"
        }.issubset(
            temperature_chart_data.columns
        ):

            temperature_chart_data = (
                temperature_chart_data[
                    [
                        "month_short",
                        "temperature"
                    ]
                ]
                .set_index(
                    "month_short"
                )
            )


            # IMPORTANT:
            # Explicitly add Celsius to the graph axis.
            temperature_chart_data.columns = [
                "Temperature (°C)"
            ]


            st.line_chart(
                temperature_chart_data,
                use_container_width=True
            )

        else:

            st.info(
                "Monthly temperature data format is unavailable."
            )

    else:

        st.info(
            "No monthly temperature data available for graphing."
        )


    # ------------------------------------------------------
    # Seasonal analysis
    # ------------------------------------------------------

    st.subheader(
        "🌦️ Solar Resource Seasonal Classification"
    )


    high_months = (
        seasonal_analysis.get(
            "high_solar_months",
            []
        )
    )


    medium_months = (
        seasonal_analysis.get(
            "medium_solar_months",
            []
        )
    )


    low_months = (
        seasonal_analysis.get(
            "low_solar_months",
            []
        )
    )


    seasonal_col1, seasonal_col2, seasonal_col3 = (
        st.columns(3)
    )


    with seasonal_col1:

        st.markdown(
            "### 🟢 High Solar"
        )

        if high_months:

            for month in high_months:

                st.write(
                    f"• {month}"
                )

        else:

            st.info(
                "No months classified"
            )


    with seasonal_col2:

        st.markdown(
            "### 🟡 Medium Solar"
        )

        if medium_months:

            for month in medium_months:

                st.write(
                    f"• {month}"
                )

        else:

            st.info(
                "No months classified"
            )


    with seasonal_col3:

        st.markdown(
            "### 🔴 Low Solar"
        )

        if low_months:

            for month in low_months:

                st.write(
                    f"• {month}"
                )

        else:

            st.info(
                "No months classified"
            )


# ==========================================================
# SECTION 16 - APPLIANCE ENERGY PLANNER
# ==========================================================

st.divider()

st.header(
    "🔌 Appliance Energy Planner"
)

st.write(
    """
    Build the project's electricity demand from the
    appliances that will be used at the site.

    The planner calculates daily, monthly and annual
    energy demand from appliance quantity, wattage and
    operating hours.
    """
)


try:

    appliance_records, appliance_daily_energy = (
        display_appliance_calculator(st)
    )

except Exception as error:

    appliance_records = []

    appliance_daily_energy = 0.0

    st.error(
        "The Appliance Energy Planner could not be loaded: "
        f"{error}"
    )


# ==========================================================
# SECTION 17 - ENERGY DEMAND SOURCE
# ==========================================================

st.divider()

st.subheader(
    "⚡ Energy Demand for PV Design"
)


energy_source = st.radio(
    "Choose how daily energy demand should be obtained:",
    [
        "Use Appliance Planner",
        "Enter Manually"
    ],
    horizontal=True,
    key="energy_source_selector"
)


if energy_source == "Use Appliance Planner":

    if appliance_records:

        energy = float(
            appliance_daily_energy
        )


        st.success(
            f"""
            Appliance planner demand of
            **{energy:.2f} kWh/day**
            will be used for PV sizing.
            """
        )

    else:

        energy = 0.0


        st.warning(
            """
            Add at least one appliance before designing
            the solar PV system, or select **Enter Manually**.
            """
        )

else:

    energy = st.number_input(
        "Daily Energy Demand (kWh/day)",
        min_value=0.1,
        value=5.0,
        step=0.5,
        key="manual_energy_demand"
    )


# ==========================================================
# SECTION 18 - SYSTEM DESIGN PARAMETERS
# ==========================================================

st.sidebar.divider()

st.sidebar.subheader(
    "🔋 System Design"
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
# SECTION 19 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary",
    disabled=(
        not location_ready
        or energy <= 0
    )
)


# ==========================================================
# SECTION 20 - ENGINEERING CALCULATIONS
# ==========================================================

if design_button and location_ready:

    # ------------------------------------------------------
    # PV capacity
    # ------------------------------------------------------

    try:

        pv_size = calculate_pv_size(

            energy=energy,

            sun_hours=sun_hours,

            efficiency=efficiency,

            temperature=temperature

        )

    except Exception as error:

        st.error(
            f"PV sizing calculation failed: {error}"
        )

        st.stop()


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
    # Preliminary cost estimate
    #
    # NOTE:
    # These remain preliminary engineering estimates.
    # The V2.4 Cost Diary records actual market prices
    # separately.
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


    # ------------------------------------------------------
    # Store design results
    # ------------------------------------------------------

    st.session_state[
        "design_results"
    ] = {

        "energy":
            energy,

        "energy_source":
            energy_source,

        "pv":
            pv_size,

        "panels":
            panels,

        "panel_rating":
            panel_rating,

        "battery":
            battery_capacity,

        "battery_type":
            battery_type,

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

        "appliances":
            appliance_records

    }


# ==========================================================
# SECTION 21 - DISPLAY DESIGN RESULTS
# ==========================================================

results = (
    st.session_state.get(
        "design_results"
    )
)


if results:

    pv_size = results[
        "pv"
    ]

    panels = results[
        "panels"
    ]

    panel_rating = results[
        "panel_rating"
    ]

    battery_capacity = results[
        "battery"
    ]

    battery_type = results[
        "battery_type"
    ]

    inverter_size = results[
        "inverter"
    ]

    controller_current = results[
        "controller"
    ]

    panel_cost = results[
        "panel_cost"
    ]

    battery_cost = results[
        "battery_cost"
    ]

    inverter_cost = results[
        "inverter_cost"
    ]

    installation_cost = results[
        "installation_cost"
    ]

    total_cost = results[
        "cost"
    ]

    carbon_reduction = results[
        "carbon"
    ]

    energy = results[
        "energy"
    ]

    energy_source = results[
        "energy_source"
    ]

    appliances = results.get(
        "appliances",
        []
    )


    st.divider()

    st.header(
        "📊 Solar PV Design Results"
    )


    # ------------------------------------------------------
    # Main results
    # ------------------------------------------------------

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


    # ------------------------------------------------------
    # Energy demand
    # ------------------------------------------------------

    st.subheader(
        "⚡ Energy Demand"
    )


    energy_col1, energy_col2 = (
        st.columns(2)
    )


    energy_col1.metric(
        "Daily Energy Demand",
        f"{energy:.2f} kWh/day"
    )


    energy_col2.metric(
        "Energy Source",
        energy_source
    )


    # ------------------------------------------------------
    # Equipment
    # ------------------------------------------------------

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

            **💰 Preliminary System Cost**

            {format_currency(total_cost)}
            """
        )


    st.success(
        f"Estimated annual CO₂ reduction: "
        f"{carbon_reduction:,.0f} kg/year"
    )


    # ======================================================
    # SECTION 22 - APPLIANCE SUMMARY
    # ======================================================

    if appliances:

        st.divider()

        st.subheader(
            "🔌 Appliance Load Summary Used for Design"
        )


        appliance_summary_df = (
            pd.DataFrame(
                appliances
            )
        )


        st.dataframe(
            appliance_summary_df,
            use_container_width=True,
            hide_index=True
        )


    # ======================================================
    # SECTION 23 - PROJECT COST DIARY
    # ======================================================

    st.divider()

    st.header(
        "💰 Project Cost Diary"
    )


    st.write(
        """
        Record actual local-market prices for the
        equipment and services used in this project.

        Each item retains its own currency. The application
        does not invent exchange rates or combine different
        currencies into a misleading total.
        """
    )


    try:

        current_cost_records = (
            display_cost_diary(st)
        )

    except Exception as error:

        current_cost_records = []

        st.error(
            "The Cost Diary could not be loaded: "
            f"{error}"
        )


    # ======================================================
    # SECTION 24 - AI SOLAR ADVISOR
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
    # SECTION 25 - PDF REPORT DATA
    # ======================================================

    report_data = {

        "location":
            location_description,

        "energy":
            energy,

        "energy_source":
            energy_source,

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
            st.session_state[
                "location_source"
            ],

        "appliances":
            appliances

    }


    if latitude is not None:

        report_data[
            "latitude"
        ] = latitude


    if longitude is not None:

        report_data[
            "longitude"
        ] = longitude


    if location_summary:

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
    Solar PV Designer Pro Africa™ v2.4.0

    Appliance Energy Planner + Project Cost Diary
    + Worldwide Location Search + Interactive Map
    + NASA POWER + Solar Analytics

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
