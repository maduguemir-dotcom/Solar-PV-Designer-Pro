import streamlit as st

from solar_api import get_solar_resource
from solar_analytics import analyze_solar_resource
from analytics_dashboard import display_analytics_dashboard


st.set_page_config(
    page_title="Solar Analytics Dashboard Test",
    layout="wide"
)

st.title(
    "☀️ Solar Analytics Dashboard Test"
)

latitude = st.number_input(
    "Latitude",
    value=0.3476
)

longitude = st.number_input(
    "Longitude",
    value=32.5825
)

if st.button(
    "Retrieve NASA POWER Data",
    type="primary"
):

    with st.spinner(
        "Retrieving NASA POWER data..."
    ):

        try:

            solar_data = get_solar_resource(
                latitude,
                longitude
            )

            analytics = analyze_solar_resource(
                solar_data
            )

            display_analytics_dashboard(
                analytics
            )

        except Exception as error:

            st.error(
                f"Analytics test failed: {error}"
            )
