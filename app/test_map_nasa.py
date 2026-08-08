# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Interactive Map + NASA POWER Test
# Version: 2.2.2
#
# Purpose:
# Test the complete workflow:
#
# Interactive Map
#       ↓
# Latitude / Longitude
#       ↓
# NASA POWER
#       ↓
# Solar Resource
#
# ==========================================================


# ==========================================================
# SECTION 1 - IMPORTS
# ==========================================================

import streamlit as st


from map_location import (
    display_location_map,
    format_coordinates
)


from location_engine import (
    get_location_solar_resource,
    get_location_summary
)


# ==========================================================
# SECTION 2 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Map + NASA POWER Test",
    page_icon="🌍",
    layout="wide"
)


# ==========================================================
# SECTION 3 - HEADER
# ==========================================================

st.title(
    "🌍 Solar PV Designer Pro Africa™"
)

st.subheader(
    "Interactive Map + NASA POWER Test"
)


st.write(
    """
    This test verifies the complete location workflow
    before it is integrated into the main Solar PV
    Designer Pro application.
    """
)


# ==========================================================
# SECTION 4 - WORKFLOW
# ==========================================================

st.info(
    """
    ### Test Workflow

    **1. Click a location on the map**

    ↓

    **2. Capture latitude and longitude**

    ↓

    **3. Send coordinates to NASA POWER**

    ↓

    **4. Retrieve solar-resource information**
    """
)


# ==========================================================
# SECTION 5 - INTERACTIVE MAP
# ==========================================================

st.header(
    "🗺️ Step 1 — Select Project Location"
)


selected_location = display_location_map()


# ==========================================================
# SECTION 6 - CHECK MAP RESULT
# ==========================================================

if not selected_location:

    st.warning(
        """
        📍 Please click anywhere on the map to select
        your solar project location.
        """
    )

    st.stop()


# ==========================================================
# SECTION 7 - EXTRACT COORDINATES
# ==========================================================

latitude = selected_location[
    "latitude"
]


longitude = selected_location[
    "longitude"
]


# ==========================================================
# SECTION 8 - DISPLAY COORDINATES
# ==========================================================

st.divider()


st.header(
    "📍 Step 2 — Selected Coordinates"
)


coordinate_col1, coordinate_col2, coordinate_col3 = (
    st.columns(3)
)


coordinate_col1.metric(
    "Latitude",
    f"{latitude:.6f}°"
)


coordinate_col2.metric(
    "Longitude",
    f"{longitude:.6f}°"
)


coordinate_col3.metric(
    "Status",
    "Coordinates Captured"
)


st.code(
    format_coordinates(
        latitude,
        longitude
    )
)


st.success(
    "✅ Interactive map successfully captured "
    "the project coordinates."
)


# ==========================================================
# SECTION 9 - NASA POWER
# ==========================================================

st.divider()


st.header(
    "☀️ Step 3 — NASA POWER Solar Resource"
)


st.write(
    f"""
    The following coordinates will now be sent to
    NASA POWER:

    **Latitude:** {latitude:.6f}°

    **Longitude:** {longitude:.6f}°
    """
)


# ==========================================================
# SECTION 10 - NASA POWER REQUEST
# ==========================================================

if st.button(
    "🚀 Retrieve NASA POWER Solar Data",
    type="primary"
):

    with st.spinner(
        "Connecting to NASA POWER..."
    ):

        try:

            location_result = (
                get_location_solar_resource(

                    latitude=latitude,

                    longitude=longitude,

                    location_name="Map Selected Location",

                    country=""

                )
            )

        except Exception as error:

            location_result = {

                "success": False,

                "message": str(error)

            }


    # ======================================================
    # SECTION 11 - NASA RESPONSE
    # ======================================================

    if not location_result:

        st.error(
            "NASA POWER returned no response."
        )

        st.stop()


    if not location_result.get(
        "success",
        False
    ):

        st.error(
            "NASA POWER request failed."
        )


        st.write(
            location_result.get(
                "message",
                "No additional information."
            )
        )

        st.stop()


    # ======================================================
    # SECTION 12 - SOLAR SUMMARY
    # ======================================================

    st.success(
        "✅ NASA POWER connection successful."
    )


    try:

        summary = (
            get_location_summary(
                location_result
            )
        )

    except Exception as error:

        st.error(
            "NASA POWER data was received, but "
            "the summary could not be generated."
        )

        st.write(
            str(error)
        )

        st.stop()


    if not summary:

        st.warning(
            "NASA POWER responded, but no solar "
            "summary was available."
        )

        st.json(
            location_result
        )

        st.stop()


    # ======================================================
    # SECTION 13 - EXTRACT VALUES
    # ======================================================

    peak_sun_hours = (
        summary.get(
            "peak_sun_hours"
        )
    )


    average_temperature = (
        summary.get(
            "average_temperature"
        )
    )


    location_name = (
        summary.get(
            "location",
            "Map Selected Location"
        )
    )


    climatology_period = (
        summary.get(
            "climatology_period",
            "NASA POWER"
        )
    )


    # ======================================================
    # SECTION 14 - DISPLAY SOLAR RESOURCE
    # ======================================================

    st.header(
        "☀️ Step 4 — Solar Resource Results"
    )


    solar_col1, solar_col2, solar_col3 = (
        st.columns(3)
    )


    if peak_sun_hours is not None:

        try:

            solar_col1.metric(
                "Peak Sun Hours",
                f"{float(peak_sun_hours):.2f} h/day"
            )

        except (
            TypeError,
            ValueError
        ):

            solar_col1.metric(
                "Peak Sun Hours",
                "Unavailable"
            )

    else:

        solar_col1.metric(
            "Peak Sun Hours",
            "Unavailable"
        )


    if average_temperature is not None:

        try:

            solar_col2.metric(
                "Average Temperature",
                f"{float(average_temperature):.1f} °C"
            )

        except (
            TypeError,
            ValueError
        ):

            solar_col2.metric(
                "Average Temperature",
                "Unavailable"
            )

    else:

        solar_col2.metric(
            "Average Temperature",
            "Unavailable"
        )


    solar_col3.metric(
        "Data Source",
        "NASA POWER"
    )


    st.write(
        f"""
        **Location:** {location_name}

        **Climatology:** {climatology_period}

        **Coordinates:** {latitude:.6f}°,
        {longitude:.6f}°
        """
    )


    # ======================================================
    # SECTION 15 - RAW NASA DATA
    # ======================================================

    st.divider()


    with st.expander(
        "🔎 View NASA POWER Response"
    ):

        st.json(
            location_result
        )


    # ======================================================
    # SECTION 16 - SUCCESS
    # ======================================================

    st.success(
        """
        🎉 **Complete workflow successful!**

        Interactive Map

        ↓

        Latitude / Longitude

        ↓

        NASA POWER

        ↓

        Solar Resource
        """
    )


# ==========================================================
# SECTION 17 - FOOTER
# ==========================================================

st.divider()


st.caption(
    """
    Solar PV Designer Pro Africa™
    Map + NASA POWER Integration Test v2.2.2

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
)
