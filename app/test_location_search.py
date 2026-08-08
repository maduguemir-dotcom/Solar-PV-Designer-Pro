# ==========================================================
# TEST GLOBAL LOCATION SEARCH
# ==========================================================

import streamlit as st

from location_search import (
    search_location,
    format_search_result
)


st.set_page_config(
    page_title="Location Search Test",
    page_icon="🌍"
)


st.title(
    "🌍 Global Location Search Test"
)


query = st.text_input(
    "Enter a location",
    value="Kano, Nigeria"
)


if st.button(
    "🔎 Search Location",
    type="primary"
):

    if not query.strip():

        st.warning(
            "Please enter a location."
        )

    else:

        with st.spinner(
            "Searching worldwide locations..."
        ):

            results = search_location(
                query
            )


        if not results:

            st.error(
                "No locations were found."
            )

        else:

            st.success(
                f"Found {len(results)} "
                "location(s)."
            )


            for index, location in enumerate(
                results
            ):

                st.write(
                    f"### {index + 1}. "
                    f"{format_search_result(location)}"
                )


                col1, col2 = st.columns(2)


                with col1:

                    st.metric(
                        "Latitude",
                        f'{location["latitude"]:.4f}°'
                    )


                with col2:

                    st.metric(
                        "Longitude",
                        f'{location["longitude"]:.4f}°'
                    )


                st.caption(
                    location["display_name"]
                )


                st.divider()
