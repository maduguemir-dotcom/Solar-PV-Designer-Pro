# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Interactive Map Test
# Version: 2.2.2
#
# Purpose:
# Test the interactive world map on Streamlit Cloud
#
# ==========================================================

import streamlit as st

from map_location import (
    display_location_map,
    format_coordinates
)


# ==========================================================
# SECTION 1 - PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar PV Map Test",
    page_icon="🌍",
    layout="wide"
)


# ==========================================================
# SECTION 2 - HEADER
# ==========================================================

st.title(
    "🌍 Solar PV Designer Pro Africa™"
)

st.subheader(
    "Interactive World Map Test"
)

st.write(
    """
    This test page verifies that the interactive map
    works correctly on Streamlit Cloud and that the
    application can capture latitude and longitude
    when the user clicks on the map.
    """
)


# ==========================================================
# SECTION 3 - INSTRUCTIONS
# ==========================================================

st.info(
    """
    ### How to test

    1. Use the map controls to zoom and move around.
    2. Click anywhere on the map.
    3. The selected latitude and longitude should
       appear below the map.
    """
)


# ==========================================================
# SECTION 4 - DISPLAY MAP
# ==========================================================

st.header(
    "🗺️ Interactive World Map"
)


selected_location = display_location_map()


# ==========================================================
# SECTION 5 - DISPLAY SELECTED LOCATION
# ==========================================================

st.divider()

st.header(
    "📍 Selected Project Location"
)


if selected_location:

    latitude = selected_location[
        "latitude"
    ]

    longitude = selected_location[
        "longitude"
    ]


    # ------------------------------------------------------
    # Display coordinates
    # ------------------------------------------------------

    col1, col2, col3 = st.columns(3)


    col1.metric(
        "Latitude",
        f"{latitude:.6f}°"
    )


    col2.metric(
        "Longitude",
        f"{longitude:.6f}°"
    )


    col3.metric(
        "Status",
        "Location Selected"
    )


    st.success(
        "✅ Map is working correctly! "
        "The application successfully captured "
        "the selected coordinates."
    )


    # ------------------------------------------------------
    # Coordinate format
    # ------------------------------------------------------

    st.write(
        "**Selected Coordinates:**"
    )


    st.code(
        format_coordinates(
            latitude,
            longitude
        )
    )


    # ------------------------------------------------------
    # Future NASA POWER integration
    # ------------------------------------------------------

    st.info(
        """
        🚀 **Next Stage**

        These coordinates will later be passed
        automatically to the NASA POWER engine to
        retrieve solar-resource information.
        """
    )


else:

    st.warning(
        """
        📍 No location selected yet.

        Click anywhere on the map above to select
        your project location.
        """
    )


# ==========================================================
# SECTION 6 - FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    Interactive Map Test v2.2.2

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
)
