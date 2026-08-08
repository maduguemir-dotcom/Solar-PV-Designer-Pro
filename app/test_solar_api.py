# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER API Test
# Version 2.1
# ==========================================================

import streamlit as st

from solar_api import (
    get_solar_resource,
    create_solar_summary
)


# ==========================================================
# APPLICATION CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="NASA POWER Test",
    page_icon="🌍",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "🌍 NASA POWER Solar Resource Test"
)

st.write(
    """
    This developer test verifies that Solar PV Designer Pro
    can retrieve solar-resource information from NASA POWER
    using geographical coordinates.
    """
)


# ==========================================================
# TEST LOCATION
# ==========================================================

st.subheader(
    "📍 Test Coordinates"
)


latitude = st.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=0.3476,
    step=0.0001,
    format="%.4f"
)


longitude = st.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=32.5825,
    step=0.0001,
    format="%.4f"
)


# ==========================================================
# TEST BUTTON
# ==========================================================

if st.button(
    "🌍 Test NASA POWER",
    type="primary"
):

    with st.spinner(
        "Requesting solar-resource data..."
    ):

        try:

            solar_data = get_solar_resource(
                latitude,
                longitude
            )


            # ==================================================
            # SUCCESS
            # ==================================================

            st.success(
                "NASA POWER connection successful."
            )


            # ==================================================
            # SUMMARY
            # ==================================================

            summary = create_solar_summary(
                solar_data
            )


            st.subheader(
                "☀️ Solar Resource Summary"
            )


            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Equivalent Peak Sun Hours",
                f'{summary["peak_sun_hours"]:.2f} h/day'
            )


            col2.metric(
                "Average Temperature",
                f'{summary["average_temperature"]:.1f} °C'
            )


            col3.metric(
                "Data Source",
                summary["data_source"]
            )


            # ==================================================
            # MONTHLY SOLAR DATA
            # ==================================================

            st.subheader(
                "📊 Monthly Solar Resource"
            )


            monthly_solar = (
                solar_data["monthly_solar"]
            )


            month_names = [

                "January",
                "February",
                "March",
                "April",
                "May",
                "June",
                "July",
                "August",
                "September",
                "October",
                "November",
                "December"

            ]


            chart_data = {

                "Month": month_names,

                "Solar Resource": [

                    monthly_solar.get(
                        f"{month:02d}",
                        0
                    )

                    for month in range(1, 13)

                ]

            }


            st.dataframe(
                chart_data,
                use_container_width=True
            )


            st.bar_chart(
                chart_data,
                x="Month",
                y="Solar Resource"
            )


            # ==================================================
            # MONTHLY TEMPERATURE
            # ==================================================

            st.subheader(
                "🌡️ Monthly Temperature"
            )


            monthly_temperature = (
                solar_data[
                    "monthly_temperature"
                ]
            )


            temperature_data = {

                "Month": month_names,

                "Temperature": [

                    monthly_temperature.get(
                        f"{month:02d}",
                        0
                    )

                    for month in range(1, 13)

                ]

            }


            st.dataframe(
                temperature_data,
                use_container_width=True
            )


            # ==================================================
            # API INFORMATION
            # ==================================================

            st.subheader(
                "ℹ️ Data Information"
            )


            st.write(
                f"""
                **Latitude:** {latitude:.4f}°

                **Longitude:** {longitude:.4f}°

                **Data Source:** NASA POWER

                **API Endpoint:** NASA POWER
                """
            )


            # ==================================================
            # RAW RESPONSE
            # ==================================================

            with st.expander(
                "View Raw Solar Data"
            ):

                st.json(
                    solar_data
                )


        except Exception as error:

            st.error(
                f"NASA POWER test failed: {error}"
            )
