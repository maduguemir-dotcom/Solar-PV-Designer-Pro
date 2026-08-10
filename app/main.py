# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Main Streamlit Application
# Version: 2.3.0
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# v2.3.0
# - Persistent Streamlit session state
# - Interactive world map
# - NASA POWER integration
# - Worldwide location search
# - Global coordinates
# - PV sizing
# - Battery sizing
# - Inverter sizing
# - Cost estimation
# - Carbon analysis
# - AI Solar Advisor
# - PDF report generation
# - Solar-resource analytics
# - Monthly solar graphs
# - Temperature graphs
# - Seasonal solar analysis
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st
import pandas as pd


# Engineering calculations
from calculations import (
    calculate_pv_size,
    calculate_panels,
    calculate_battery,
    calculate_inverter,
    calculate_carbon
)


# Solar database
from data_loader import (
    load_solar_database,
    get_location_data
)


# AI Solar Advisor
from ai import (
    generate_ai_recommendations
)


# PDF Report Generator
from reports import (
    create_pdf_report
)


# Utility functions
from utils import (
    format_currency
)


# Global location engine
from location_engine import (
    get_location_solar_resource,
    get_location_summary
)


# Worldwide location search
from location_search import (
    search_location,
    format_search_result
)


# Interactive map
from map_location import (
    display_location_map,
    format_coordinates
)


# Solar analytics
from solar_analytics import (
    analyze_solar_resource
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
# SECTION 3 - SESSION STATE INITIALIZATION
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

    "analytics": None,

    "recommendations": [],

}


for key, value in DEFAULT_STATE.items():

    if key not in st.session_state:

        st.session_state[key] = value


# ==========================================================
# SECTION 4 - APPLICATION HEADER
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
    estimation, environmental assessment, solar-resource
    analytics and AI-assisted recommendations.
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
        value="",
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


            retrieve_search_data = st.sidebar.button(
                "☀️ Get Solar Data",
                use_container_width=True
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


                    raw_sun_hours = (
                        summary.get(
                            "peak_sun_hours"
                        )
                    )


                    raw_temperature = (
                        summary.get(
                            "average_temperature"
                        )
                    )


                    try:

                        retrieved_sun_hours = float(
                            raw_sun_hours
                        )

                    except (
                        TypeError,
                        ValueError
                    ):

                        retrieved_sun_hours = None


                    try:

                        retrieved_temperature = float(
                            raw_temperature
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


                raw_sun_hours = (
                    summary.get(
                        "peak_sun_hours"
                    )
                )


                raw_temperature = (
                    summary.get(
                        "average_temperature"
                    )
                )


                try:

                    retrieved_sun_hours = float(
                        raw_sun_hours
                    )

                except (
                    TypeError,
                    ValueError
                ):

                    retrieved_sun_hours = None


                try:

                    retrieved_temperature = float(
                        raw_temperature
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


            raw_sun_hours = (
                summary.get(
                    "peak_sun_hours"
                )
            )


            raw_temperature = (
                summary.get(
                    "average_temperature"
                )
            )


            try:

                retrieved_sun_hours = float(
                    raw_sun_hours
                )

            except (
                TypeError,
                ValueError
            ):

                retrieved_sun_hours = None


            try:

                retrieved_temperature = float(
                    raw_temperature
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
# SECTION 12 - RESTORE SESSION VARIABLES
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
# SECTION 13 - SYSTEM DESIGN INPUTS
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
# SECTION 14 - LOCATION INFORMATION
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
            f"{float(latitude):.4f}°"
        )


    if longitude is None:

        longitude_display = "Database"

    else:

        longitude_display = (
            f"{float(longitude):.4f}°"
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
# SECTION 15 - NASA DATA
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
                    use_container_width=True
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
# SECTION 16 - SOLAR ANALYTICS
# ==========================================================

if (
    location_ready
    and solar_data is not None
    and st.session_state[
        "location_source"
    ] != "Solar Database"
):

    st.divider()

    st.header(
        "📈 Solar Resource Analytics"
    )

    try:

        analytics = analyze_solar_resource(
            solar_data
        )

        st.session_state[
            "analytics"
        ] = analytics

    except Exception as error:

        analytics = None

        st.warning(
            "Solar analytics could not be generated: "
            f"{error}"
        )


    if analytics:

        monthly_solar = analytics.get(
            "monthly_solar",
            []
        )

        monthly_temperature = analytics.get(
            "monthly_temperature",
            []
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


        # --------------------------------------------------
        # Solar statistics
        # --------------------------------------------------

        st.subheader(
            "☀️ Solar Resource Statistics"
        )


        solar_stat_col1, solar_stat_col2, solar_stat_col3, solar_stat_col4 = (
            st.columns(4)
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

        best_month = solar_statistics.get(
            "best_month"
        )


        solar_stat_col1.metric(
            "Annual Average",
            (
                f"{float(annual_average):.2f}"
                if annual_average is not None
                else "N/A"
            )
        )


        solar_stat_col2.metric(
            "Maximum",
            (
                f"{float(maximum):.2f}"
                if maximum is not None
                else "N/A"
            )
        )


        solar_stat_col3.metric(
            "Minimum",
            (
                f"{float(minimum):.2f}"
                if minimum is not None
                else "N/A"
            )
        )


        solar_stat_col4.metric(
            "Best Month",
            best_month
            if best_month
            else "N/A"
        )


        # --------------------------------------------------
        # Temperature statistics
        # --------------------------------------------------

        st.subheader(
            "🌡️ Temperature Statistics"
        )


        temp_stat_col1, temp_stat_col2, temp_stat_col3, temp_stat_col4 = (
            st.columns(4)
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

        hottest_month = (
            temperature_statistics.get(
                "hottest_month"
            )
        )


        temp_stat_col1.metric(
            "Annual Average",
            (
                f"{float(temperature_average):.1f} °C"
                if temperature_average is not None
                else "N/A"
            )
        )


        temp_stat_col2.metric(
            "Maximum",
            (
                f"{float(temperature_maximum):.1f} °C"
                if temperature_maximum is not None
                else "N/A"
            )
        )


        temp_stat_col3.metric(
            "Minimum",
            (
                f"{float(temperature_minimum):.1f} °C"
                if temperature_minimum is not None
                else "N/A"
            )
        )


        temp_stat_col4.metric(
            "Hottest Month",
            hottest_month
            if hottest_month
            else "N/A"
        )


        # --------------------------------------------------
        # Monthly solar chart
        # --------------------------------------------------

        if monthly_solar:

            st.subheader(
                "☀️ Monthly Solar Resource"
            )


            solar_chart_data = pd.DataFrame(
                monthly_solar
            )


            if (
                "month_short" in solar_chart_data.columns
                and "solar_value" in solar_chart_data.columns
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


                st.line_chart(
                    solar_chart_data,
                    use_container_width=True
                )


                with st.expander(
                    "📋 View Monthly Solar Data"
                ):

                    st.dataframe(
                        pd.DataFrame(
                            monthly_solar
                        ),
                        use_container_width=True
                    )


        # --------------------------------------------------
        # Temperature chart
        # --------------------------------------------------

        if monthly_temperature:

            st.subheader(
                "🌡️ Monthly Average Temperature"
            )


            temperature_chart_data = pd.DataFrame(
                monthly_temperature
            )


            if (
                "month_short"
                in temperature_chart_data.columns
                and
                "temperature"
                in temperature_chart_data.columns
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


                st.line_chart(
                    temperature_chart_data,
                    use_container_width=True
                )


                with st.expander(
                    "📋 View Monthly Temperature Data"
                ):

                    st.dataframe(
                        pd.DataFrame(
                            monthly_temperature
                        ),
                        use_container_width=True
                    )


        # --------------------------------------------------
        # Seasonal analysis
        # --------------------------------------------------

        st.subheader(
            "🌦️ Seasonal Solar Analysis"
        )


        seasonal_col1, seasonal_col2, seasonal_col3 = (
            st.columns(3)
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


        with seasonal_col1:

            st.markdown(
                "### 🟢 High Solar"
            )

            if high_months:

                st.write(
                    ", ".join(
                        high_months
                    )
                )

            else:

                st.write(
                    "No months classified."
                )


        with seasonal_col2:

            st.markdown(
                "### 🟡 Medium Solar"
            )

            if medium_months:

                st.write(
                    ", ".join(
                        medium_months
                    )
                )

            else:

                st.write(
                    "No months classified."
                )


        with seasonal_col3:

            st.markdown(
                "### 🔵 Low Solar"
            )

            if low_months:

                st.write(
                    ", ".join(
                        low_months
                    )
                )

            else:

                st.write(
                    "No months classified."
                )


# ==========================================================
# SECTION 17 - DESIGN BUTTON
# ==========================================================

design_button = st.button(
    "🚀 Design Solar PV System",
    type="primary",
    disabled=not location_ready
)


# ==========================================================
# SECTION 18 - ENGINEERING CALCULATIONS
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
    # SECTION 19 - ENGINEERING RESULTS
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
    # SECTION 20 - EQUIPMENT RECOMMENDATION
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
    # SECTION 21 - AI SOLAR ADVISOR
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


    st.session_state[
        "recommendations"
    ] = recommendations


    for recommendation in recommendations:

        st.success(
            recommendation
        )


    # ======================================================
    # SECTION 22 - PDF REPORT DATA
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
            ]

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
    # SECTION 23 - ADD ANALYTICS TO REPORT
    # ======================================================

    analytics_for_report = (
        st.session_state.get(
            "analytics"
        )
    )


    if analytics_for_report:

        report_data[
            "solar_analytics"
        ] = analytics_for_report


    # ======================================================
    # SECTION 24 - PDF REPORT
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
# SECTION 25 - FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™ v2.3.0

    Worldwide Location Search + Interactive Map
    + NASA POWER + Solar Analytics

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu

    For preliminary engineering, education,
    research and demonstration purposes.
    """
)
