# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Interactive Map Location Module
# Version: 2.2.2
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Allow users to select a project location directly
# from an interactive world map.
#
# ==========================================================

import streamlit as st
import folium

from streamlit_folium import st_folium


# ==========================================================
# SECTION 1 - DEFAULT MAP LOCATION
# ==========================================================

DEFAULT_LATITUDE = 0.3476

DEFAULT_LONGITUDE = 32.5825


# ==========================================================
# SECTION 2 - CREATE INTERACTIVE MAP
# ==========================================================

def create_location_map(
    latitude=DEFAULT_LATITUDE,
    longitude=DEFAULT_LONGITUDE,
    zoom_start=5
):
    """
    Create an interactive Folium world map.

    Users can click anywhere on the map to select
    a project location.
    """

    project_map = folium.Map(

        location=[
            latitude,
            longitude
        ],

        zoom_start=zoom_start,

        control_scale=True

    )


    # ------------------------------------------------------
    # Instruction marker
    # ------------------------------------------------------

    folium.Marker(

        location=[
            latitude,
            longitude
        ],

        tooltip="Current Location",

        popup=(
            "Click anywhere on the map "
            "to select your solar project location."
        )

    ).add_to(project_map)


    # ------------------------------------------------------
    # Enable map clicking
    # ------------------------------------------------------

    folium.LatLngPopup().add_to(
        project_map
    )


    return project_map


# ==========================================================
# SECTION 3 - DISPLAY MAP
# ==========================================================

def display_location_map():

    """
    Display interactive map and return the
    coordinates selected by the user.

    Returns:

        dict or None
    """

    project_map = create_location_map()


    map_result = st_folium(

        project_map,

        width=None,

        height=500,

        returned_objects=[
            "last_clicked"
        ]

    )


    # ======================================================
    # SECTION 4 - PROCESS CLICK
    # ======================================================

    if not map_result:

        return None


    clicked_location = (
        map_result.get(
            "last_clicked"
        )
    )


    if not clicked_location:

        return None


    latitude = (
        clicked_location.get(
            "lat"
        )
    )


    longitude = (
        clicked_location.get(
            "lng"
        )
    )


    if (
        latitude is None
        or longitude is None
    ):

        return None


    # ======================================================
    # SECTION 5 - RETURN LOCATION
    # ======================================================

    return {

        "latitude": float(
            latitude
        ),

        "longitude": float(
            longitude
        )

    }


# ==========================================================
# SECTION 6 - FORMAT COORDINATES
# ==========================================================

def format_coordinates(
    latitude,
    longitude
):

    """
    Format coordinates for display.
    """

    return (
        f"{latitude:.6f}°, "
        f"{longitude:.6f}°"
    )
