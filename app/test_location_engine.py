import streamlit as st

from location_engine import (
    get_location_solar_resource,
    get_location_summary
)


st.set_page_config(
    page_title="Location Engine Test",
    page_icon="🌍"
)


st.title(
    "🌍 Global Location Engine Test"
)


latitude = st.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=0.3476,
    step=0.0001
)


longitude = st.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=32.5825,
    step=0.0001
)


location_name = st.text_input(
    "Location Name",
    value="Kampala"
)


country = st.text_input(
    "Country",
    value="Uganda"
)


if st.button(
    "🌍 Test Location Engine",
    type="primary"
):

    with st.spinner(
        "Connecting location to NASA POWER..."
    ):

        result = get_location_solar_resource(

            latitude=latitude,

            longitude=longitude,

            location_name=location_name,

            country=country

        )


    if result["success"]:

        st.success(
            result["message"]
        )


        summary = get_location_summary(
            result
        )


        st.subheader(
            "📍 Location"
        )

        st.write(
            summary["location"]
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Latitude",
            f'{summary["latitude"]:.4f}°'
        )


        col2.metric(
            "Longitude",
            f'{summary["longitude"]:.4f}°'
        )


        col3.metric(
            "Peak Sun Hours",
            (
                f'{summary["peak_sun_hours"]:.2f} h/day'
                if summary["peak_sun_hours"] is not None
                else "Unavailable"
            )
        )


        st.subheader(
            "☀️ Solar Resource"
        )


        st.write(
            f'Average Temperature: '
            f'{summary["average_temperature"]:.1f} °C'
            if summary["average_temperature"] is not None
            else "Average Temperature: Unavailable"
        )


        st.write(
            f'Best Solar Month: '
            f'{summary["best_month"]}'
        )


        st.write(
            f'Lowest Solar Month: '
            f'{summary["worst_month"]}'
        )


        st.info(
            f'Source: {summary["data_source"]} | '
            f'Climatology: '
            f'{summary["climatology_period"]}'
        )


        with st.expander(
            "🔎 View Complete Data"
        ):

            st.json(
                result
            )


    else:

        st.error(
            f'Location test failed: '
            f'{result["message"]}'
        )
