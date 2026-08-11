```python
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
# v2.4.0
#
# NEW:
# - Appliance Energy Planner
# - Multiple appliance entry
# - Appliance wattage
# - Appliance quantity
# - Daily operating hours
# - Automatic daily energy calculation
# - Monthly energy calculation
# - Total connected load
# - Automatic transfer of appliance demand
#   into PV sizing
# - Manual energy-demand option
#
# RETAINED FROM v2.3:
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
# - Cost estimation
# - Carbon reduction
# - AI Solar Advisor
# - PDF report
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
    display_location_map,
    format_coordinates
)


# ----------------------------------------------------------
# Solar analytics
# ----------------------------------------------------------

from solar_analytics import (
    analyze_solar_resource
)


# ----------------------------------------------------------
# Appliance energy engine
# ----------------------------------------------------------

from appliance_energy import (
    create_appliance,
    calculate_appliance_energy,
    calculate_total_daily_energy,
    calculate_total_monthly_energy,
    calculate_total_connected_load
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

    "appliances": [],

    "energy_source": "Appliance Planner",

    "design_results": None

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
    battery sizing, cost estimation, environmental
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
                "The selected location contains invalid "
                "solar-resource data."
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
        placeholder="Example: Kano, Nigeria"
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

                            location_name="Map Selected Location",

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
                        "retrieved."
                    )

                else:

                    st.warning(
                        "NASA POWER returned no usable "
                        "solar-resource values."
                    )

            else:

                st.error(
                    "NASA POWER request failed."
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

    manual_latitude = st.sidebar.number_input(
        "Latitude",
        min_value=-90.0,
        max_value=90.0,
        value=0.3476,
        step=0.0001,
        format="%.4f"
    )

    manual_longitude = st.sidebar.number_input(
        "Longitude",
        min_value=-180.0,
        max_value=180.0,
        value=32.5825,
        step=0.0001,
        format="%.4f"
    )

    manual_location_name = st.sidebar.text_input(
        "Location Name",
        value="Kampala"
    )

    manual_country = st.sidebar.text_input(
        "Country",
        value="Uganda"
    )

    retrieve_manual_data = st.sidebar.button(
        "☀️ Get Solar Data",
        use_container_width=True
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

location_ready = st.session_state[
    "location_ready"
]

location_description = st.session_state[
    "location_description"
]

latitude = st.session_state[
    "latitude"
]

longitude = st.session_state[
    "longitude"
]

sun_hours = st.session_state[
    "sun_hours"
]

temperature = st.session_state[
    "temperature"
]

solar_data = st.session_state[
    "solar_data"
]

solar_summary = st.session_state[
    "solar_summary"
]

location_summary = st.session_state[
    "location_summary"
]


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
    and st.session_state[
        "location_source"
    ] != "Solar Database"
    and solar_data is not None
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

        analytics = analyze_solar_resource(
            solar_data
        )

    except Exception as error:

        analytics = {}

        st.warning(
            f"Solar analytics could not be calculated: {error}"
        )


    solar_statistics = analytics.get(
        "solar_statistics",
        {}
    )

    temperature_statistics = analytics.get(
        "temperature_statistics",
        {}
    )

    seasonal_analysis = analytics.get(
        "seasonal_analysis",
        {}
    )

    monthly_solar = analytics.get(
        "monthly_solar",
        []
    )

    monthly_temperature = analytics.get(
        "monthly_temperature",
        []
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

    annual_average = solar_statistics.get(
        "annual_average"
    )

    maximum = solar_statistics.get(
        "maximum"
    )

    minimum = solar_statistics.get(
        "minimum"
    )


    solar_col1.metric(
        "Annual Average",
        (
            f"{float(annual_average):.2f} kWh/m²/day"
            if annual_average is not None
            else "N/A"
        )
    )

    solar_col2.metric(
        "Maximum",
        (
            f"{float(maximum):.2f} kWh/m²/day"
            if maximum is not None
            else "N/A"
        )
    )

    solar_col3.metric(
        "Minimum",
        (
            f"{float(minimum):.2f} kWh/m²/day"
            if minimum is not None
            else "N/A"
        )
    )


    best_month = solar_statistics.get(
        "best_month"
    )

    lowest_month = solar_statistics.get(
        "lowest_month"
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

    if monthly_solar:

        solar_chart_data = pd.DataFrame(
            monthly_solar
        )

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

        st.subheader(
            "☀️ Monthly Solar Resource"
        )

        st.line_chart(
            solar_chart_data,
            use_container_width=True
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

    temp_col1, temp_col2, temp_col3 = (
        st.columns(3)
    )

    temp_average = temperature_statistics.get(
        "annual_average"
    )

    temp_maximum = temperature_statistics.get(
        "maximum"
    )

    temp_minimum = temperature_statistics.get(
        "minimum"
    )


    temp_col1.metric(
        "Annual Average",
        (
            f"{float(temp_average):.1f} °C"
            if temp_average is not None
            else "N/A"
        )
    )

    temp_col2.metric(
        "Maximum",
        (
            f"{float(temp_maximum):.1f} °C"
            if temp_maximum is not None
            else "N/A"
        )
    )

    temp_col3.metric(
        "Minimum",
        (
            f"{float(temp_minimum):.1f} °C"
            if temp_minimum is not None
            else "N/A"
        )
    )


    hottest_month = temperature_statistics.get(
        "hottest_month"
    )

    coolest_month = temperature_statistics.get(
        "coolest_month"
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

    if monthly_temperature:

        temperature_chart_data = pd.DataFrame(
            monthly_temperature
        )

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

        temperature_chart_data.columns = [
            "Temperature (°C)"
        ]

        st.subheader(
            "🌡️ Monthly Temperature"
        )

        st.line_chart(
            temperature_chart_data,
            use_container_width=True
        )

    else:

        st.info(
            "No monthly temperature data available for graphing."
        )


    # ------------------------------------------------------
    # Seasonal analysis
    # ------------------------------------------------------

    st.subheader(
        "🌤️ Seasonal Solar Analysis"
    )

    high_months = seasonal_analysis.get(
        "high_solar_months",
        []
    )

    medium_months = seasonal_analysis.get(
        "medium_solar_months",
        []
    )

    low_months = seasonal_analysis.get(
        "low_solar_months",
        []
    )


    seasonal_col1, seasonal_col2, seasonal_col3 = (
        st.columns(3)
    )


    with seasonal_col1:

        st.markdown(
            "**🟢 High Solar Months**"
        )

        if high_months:

            st.write(
                ", ".join(
                    high_months
                )
            )

        else:

            st.write(
                "No months classified"
            )


    with seasonal_col2:

        st.markdown(
            "**🟡 Medium Solar Months**"
        )

        if medium_months:

            st.write(
                ", ".join(
                    medium_months
                )
            )

        else:

            st.write(
                "No months classified"
            )


    with seasonal_col3:

        st.markdown(
            "**🔴 Low Solar Months**"
        )

        if low_months:

            st.write(
                ", ".join(
                    low_months
                )
            )

        else:

            st.write(
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
    Build your electricity demand from the appliances
    used at the project site. The calculated daily energy
    demand can be transferred automatically into the
    solar PV sizing engine.
    """
)


# ----------------------------------------------------------
# Common appliance presets
# ----------------------------------------------------------

APPLIANCE_PRESETS = {

    "LED Light": 20,

    "Fan": 75,

    "Television": 100,

    "Refrigerator": 150,

    "Freezer": 200,

    "Air Conditioner": 1200,

    "Laptop": 65,

    "Desktop Computer": 200,

    "Water Pump": 750,

    "Electric Iron": 1000,

    "Microwave": 1200,

    "Washing Machine": 500,

    "Phone Charger": 10,

    "Electric Kettle": 1500,

    "Custom Appliance": 0

}


# ----------------------------------------------------------
# Add appliance controls
# ----------------------------------------------------------

with st.expander(
    "➕ Add Appliance",
    expanded=True
):

    appliance_col1, appliance_col2 = (
        st.columns(2)
    )

    with appliance_col1:

        appliance_name = st.selectbox(
            "Appliance",
            list(
                APPLIANCE_PRESETS.keys()
            ),
            key="new_appliance_name"
        )

        if appliance_name == "Custom Appliance":

            custom_name = st.text_input(
                "Custom Appliance Name",
                value="My Appliance"
            )

            selected_name = custom_name

        else:

            selected_name = appliance_name


    with appliance_col2:

        default_wattage = (
            APPLIANCE_PRESETS[
                appliance_name
            ]
        )

        appliance_wattage = st.number_input(
            "Power Rating (Watts)",
            min_value=0.0,
            value=float(
                default_wattage
            ),
            step=10.0,
            key="new_appliance_wattage"
        )


    appliance_col3, appliance_col4 = (
        st.columns(2)
    )

    with appliance_col3:

        appliance_quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
            key="new_appliance_quantity"
        )

    with appliance_col4:

        appliance_hours = st.number_input(
            "Hours Used per Day",
            min_value=0.0,
            max_value=24.0,
            value=5.0,
            step=0.5,
            key="new_appliance_hours"
        )


    add_appliance = st.button(
        "➕ Add Appliance to Energy Schedule",
        type="primary",
        use_container_width=True
    )


    if add_appliance:

        new_appliance = create_appliance(

            name=selected_name,

            wattage=appliance_wattage,

            hours_per_day=appliance_hours,

            quantity=appliance_quantity

        )

        st.session_state[
            "appliances"
        ].append(
            new_appliance
        )

        st.success(
            f"✅ {selected_name} added to the energy schedule."
        )

        st.rerun()


# ==========================================================
# SECTION 17 - APPLIANCE ENERGY TABLE
# ==========================================================

appliances = st.session_state[
    "appliances"
]


if appliances:

    st.subheader(
        "📋 Appliance Energy Schedule"
    )

    appliance_rows = []


    for index, appliance in enumerate(
        appliances
    ):

        daily_energy = (
            calculate_appliance_energy(
                appliance
            )
        )

        connected_load = (
            appliance["wattage"]
            *
            appliance["quantity"]
        )

        appliance_rows.append({

            "No.":
                index + 1,

            "Appliance":
                appliance["name"],

            "Quantity":
                appliance["quantity"],

            "Power (W)":
                appliance["wattage"],

            "Hours/Day":
                appliance["hours_per_day"],

            "Connected Load (W)":
                connected_load,

            "Daily Energy (kWh)":
                round(
                    daily_energy,
                    3
                )

        })


    st.dataframe(
        appliance_rows,
        use_container_width=True,
        hide_index=True
    )


    # ------------------------------------------------------
    # Appliance totals
    # ------------------------------------------------------

    total_daily_energy = (
        calculate_total_daily_energy(
            appliances
        )
    )

    total_monthly_energy = (
        calculate_total_monthly_energy(
            appliances
        )
    )

    total_connected_load = (
        calculate_total_connected_load(
            appliances
        )
    )


    energy_col1, energy_col2, energy_col3 = (
        st.columns(3)
    )


    energy_col1.metric(
        "☀️ Daily Energy Demand",
        f"{total_daily_energy:.2f} kWh/day"
    )

    energy_col2.metric(
        "📅 Monthly Energy",
        f"{total_monthly_energy:.2f} kWh/month"
    )

    energy_col3.metric(
        "⚡ Connected Load",
        f"{total_connected_load:.0f} W"
    )


    # ------------------------------------------------------
    # Remove appliance
    # ------------------------------------------------------

    st.subheader(
        "🗑️ Appliance Management"
    )

    remove_options = [

        f"{index + 1}. "
        f"{appliance['name']}"

        for index, appliance
        in enumerate(appliances)

    ]


    remove_selection = st.selectbox(
        "Select appliance to remove",
        remove_options,
        key="remove_appliance_selection"
    )


    remove_button = st.button(
        "🗑️ Remove Selected Appliance"
    )


    if remove_button:

        remove_index = (
            remove_options.index(
                remove_selection
            )
        )

        removed_appliance = (
            st.session_state[
                "appliances"
            ].pop(
                remove_index
            )
        )

        st.success(
            f"Removed {removed_appliance['name']}."
        )

        st.rerun()


    clear_button = st.button(
        "🧹 Clear All Appliances"
    )


    if clear_button:

        st.session_state[
            "appliances"
        ] = []

        st.rerun()


else:

    st.info(
        """
        No appliances have been added yet.

        Add appliances above to automatically calculate
        your electricity demand.
        """
    )


# ==========================================================
# SECTION 18 - ENERGY DEMAND SOURCE
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

    if appliances:

        energy = st.number_input(
            "Calculated Daily Energy Demand (kWh/day)",
            min_value=0.1,
            value=float(
                total_daily_energy
            ),
            step=0.1,
            disabled=True
        )

        st.success(
            f"Appliance planner demand of "
            f"**{total_daily_energy:.2f} kWh/day** "
            f"will be used for PV sizing."
        )

    else:

        energy = 0.0

        st.warning(
            "Add at least one appliance before designing "
            "the solar PV system."
        )

else:

    energy = st.number_input(
        "Daily Energy Demand (kWh/day)",
        min_value=0.1,
        value=5.0,
        step=0.5
    )


# ==========================================================
# SECTION 19 - SYSTEM DESIGN PARAMETERS
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
# SECTION 20 - DESIGN BUTTON
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
# SECTION 21 - ENGINEERING CALCULATIONS
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
    # Carbon reduction
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
            carbon_reduction

    }


# ==========================================================
# SECTION 22 - DISPLAY DESIGN RESULTS
# ==========================================================

results = st.session_state.get(
    "design_results"
)


if results:

    pv_size = results[
        "pv"
    ]

    panels = results[
        "panels"
    ]

    battery_capacity = results[
        "battery"
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

    st.divider()

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

            **💰 Estimated System Cost**

            {format_currency(total_cost)}
            """
        )


    st.success(
        f"Estimated annual CO₂ reduction: "
        f"{carbon_reduction:,.0f} kg/year"
    )


    # ======================================================
    # SECTION 23 - AI SOLAR ADVISOR
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
    # SECTION 24 - PDF REPORT DATA
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
            st.session_state[
                "location_source"
            ],

        "energy_source":
            energy_source,

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
    # SECTION 25 - PDF REPORT
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
# SECTION 26 - FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.4.0

    Appliance Energy Planner + Worldwide Location Search
    + Interactive Map + NASA POWER + Solar Analytics

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
```
