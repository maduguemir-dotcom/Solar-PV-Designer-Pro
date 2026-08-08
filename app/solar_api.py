# ==========================================================
# Solar PV Designer Pro Africa™
# NASA POWER API Test
# Version 2.1.5
# ==========================================================

import streamlit as st
import pandas as pd

from solar_api import (
    get_solar_resource,
    create_solar_summary
)


# ==========================================================
# CONFIGURATION
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
# COORDINATES
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


            # --------------------------------------------------
            # PEAK SUN HOURS
            # --------------------------------------------------

            peak_sun_hours = summary.get(
                "peak_sun_hours"
            )

            if peak_sun_hours is not None:

                peak_display = (
                    f"{peak_sun_hours:.2f} h/day"
                )

            else:

                peak_display = "Unavailable"


            col1.metric(
                "Equivalent Peak Sun Hours",
                peak_display
            )


            # --------------------------------------------------
            # TEMPERATURE
            # --------------------------------------------------

            temperature = summary.get(
                "average_temperature"
            )

            if temperature is not None:

                temperature_display = (
                    f"{temperature:.1f} °C"
                )

            else:

                temperature_display = "Unavailable"


            col2.metric(
                "Average Temperature",
                temperature_display
            )


            # --------------------------------------------------
            # DATA SOURCE
            # --------------------------------------------------

            col3.metric(
                "Data Source",
                summary.get(
                    "data_source",
                    "NASA POWER"
                )
            )


            # ==================================================
            # CLIMATOLOGY PERIOD
            # ==================================================

            st.info(
                "NASA POWER climatology period: "
                + str(
                    summary.get(
                        "climatology_period",
                        "2001-2020"
                    )
                )
            )


            # ==================================================
            # PREPARE MONTHLY DATAFRAME
            # ==================================================

            monthly_display = solar_data.get(
                "monthly_display",
                []
            )


            if not monthly_display:

                st.warning(
                    "No monthly data was returned."
                )

            else:

                df = pd.DataFrame(
                    monthly_display
                )


                # ==================================================
                # MONTHLY SOLAR RESOURCE
                # ==================================================

                st.subheader(
                    "☀️ Monthly Solar Resource"
                )


                solar_chart_df = df[
                    [
                        "month",
                        "solar_resource"
                    ]
                ].copy()


                solar_chart_df = (
                    solar_chart_df
                    .dropna(
                        subset=[
                            "solar_resource"
                        ]
                    )
                )


                if not solar_chart_df.empty:

                    solar_chart_df = (
                        solar_chart_df
                        .set_index("month")
                    )


                    st.bar_chart(
                        solar_chart_df[
                            "solar_resource"
                        ]
                    )


                    st.dataframe(
                        solar_chart_df,
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "Solar values are available "
                        "in the API response but could "
                        "not be prepared for plotting."
                    )


                # ==================================================
                # MONTHLY TEMPERATURE
                # ==================================================

                st.subheader(
                    "🌡️ Monthly Temperature"
                )


                temperature_chart_df = df[
                    [
                        "month",
                        "temperature"
                    ]
                ].copy()


                temperature_chart_df = (
                    temperature_chart_df
                    .dropna(
                        subset=[
                            "temperature"
                        ]
                    )
                )


                if not temperature_chart_df.empty:

                    temperature_chart_df = (
                        temperature_chart_df
                        .set_index("month")
                    )


                    st.line_chart(
                        temperature_chart_df[
                            "temperature"
                        ]
                    )


                    st.dataframe(
                        temperature_chart_df,
                        use_container_width=True
                    )

                else:

                    st.warning(
                        "Temperature values are "
                        "not available for plotting."
                    )


                # ==================================================
                # BEST / WORST MONTH
                # ==================================================

                st.subheader(
                    "📊 Solar Resource Extremes"
                )


                best_col, worst_col = st.columns(2)


                best_col.metric(
                    "☀️ Best Solar Month",
                    summary.get(
                        "best_month",
                        "Unavailable"
                    ),
                    (
                        f'{summary.get("best_month_value", 0):.2f} '
                        "kWh/m²/day"
                        if summary.get(
                            "best_month_value"
                        ) is not None
                        else None
                    )
                )


                worst_col.metric(
                    "🌧️ Lowest Solar Month",
                    summary.get(
                        "worst_month",
                        "Unavailable"
                    ),
                    (
                        f'{summary.get("worst_month_value", 0):.2f} '
                        "kWh/m²/day"
                        if summary.get(
                            "worst_month_value"
                        ) is not None
                        else None
                    )
                )


            # ==================================================
            # LOCATION INFORMATION
            # ==================================================

            st.subheader(
                "📍 Location Information"
            )


            st.write(
                f"""
                **Latitude:** {latitude:.4f}°

                **Longitude:** {longitude:.4f}°

                **Data Source:** NASA POWER

                **API:** NASA POWER Climatology Point API
                """
            )


            # ==================================================
            # RAW DATA
            # ==================================================

            with st.expander(
                "🔎 View Raw NASA POWER Data"
            ):

                st.json(
                    solar_data
                )


        except Exception as error:

            st.error(
                f"NASA POWER test failed: {error}"
            )
