# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# NASA POWER / SOLAR RESOURCE TEST
# Version: 2.3.0
#
# This test uses the confirmed function:
#
#     get_solar_resource()
#
# ==========================================================

import streamlit as st
import inspect

from solar_api import get_solar_resource


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar Resource Test",
    page_icon="☀️",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "☀️ Solar PV Designer Pro Africa™"
)

st.subheader(
    "Solar Resource API Test"
)


st.success(
    "✅ solar_api.py loaded successfully."
)


# ==========================================================
# SHOW FUNCTION SIGNATURE
# ==========================================================

st.header(
    "🔎 Existing Solar Resource Function"
)


try:

    signature = inspect.signature(
        get_solar_resource
    )

    st.success(
        "✅ get_solar_resource() found."
    )

    st.code(
        f"get_solar_resource{signature}"
    )

except Exception as error:

    st.error(
        f"Could not inspect function: {error}"
    )


# ==========================================================
# LOCATION
# ==========================================================

st.sidebar.header(
    "📍 Test Coordinates"
)


latitude = st.sidebar.number_input(
    "Latitude",
    min_value=-90.0,
    max_value=90.0,
    value=0.3476,
    step=0.0001,
    format="%.4f"
)


longitude = st.sidebar.number_input(
    "Longitude",
    min_value=-180.0,
    max_value=180.0,
    value=32.5825,
    step=0.0001,
    format="%.4f"
)


# ==========================================================
# BUTTON
# ==========================================================

test_button = st.button(
    "🚀 Test Solar Resource",
    type="primary"
)


if test_button:

    st.header(
        "📡 Solar Resource Response"
    )


    solar_resource = None


    # ------------------------------------------------------
    # Attempt 1
    # ------------------------------------------------------

    try:

        solar_resource = get_solar_resource(
            latitude,
            longitude
        )

        st.success(
            "✅ Function accepted positional coordinates."
        )

    except Exception as error1:

        # --------------------------------------------------
        # Attempt 2
        # --------------------------------------------------

        try:

            solar_resource = get_solar_resource(
                latitude=latitude,
                longitude=longitude
            )

            st.success(
                "✅ Function accepted latitude/longitude keywords."
            )

        except Exception as error2:

            # ----------------------------------------------
            # Attempt 3
            # ----------------------------------------------

            try:

                solar_resource = get_solar_resource(
                    lat=latitude,
                    lon=longitude
                )

                st.success(
                    "✅ Function accepted lat/lon keywords."
                )

            except Exception as error3:

                st.error(
                    "❌ get_solar_resource() could not be called."
                )


                st.write(
                    "Attempt 1:"
                )

                st.code(
                    str(error1)
                )


                st.write(
                    "Attempt 2:"
                )

                st.code(
                    str(error2)
                )


                st.write(
                    "Attempt 3:"
                )

                st.code(
                    str(error3)
                )


                st.stop()


    # ======================================================
    # RESULT
    # ======================================================

    if solar_resource is None:

        st.error(
            "❌ get_solar_resource() returned no data."
        )

        st.stop()


    st.success(
        "🎉 Solar resource data received!"
    )


    # ======================================================
    # DISPLAY RESPONSE
    # ======================================================

    st.header(
        "📋 Returned Data"
    )


    if isinstance(
        solar_resource,
        dict
    ):

        st.json(
            solar_resource
        )

    else:

        st.write(
            solar_resource
        )


    # ======================================================
    # DATA TYPE
    # ======================================================

    st.header(
        "🔬 Response Information"
    )


    st.write(
        "Response type:"
    )

    st.code(
        type(solar_resource).__name__
    )


    if isinstance(
        solar_resource,
        dict
    ):

        st.write(
            "Dictionary keys:"
        )

        st.write(
            list(
                solar_resource.keys()
            )
        )


# ==========================================================
# FOOTER
# ==========================================================

st.divider()

st.caption(
    """
    Solar PV Designer Pro Africa™
    Solar Resource API Test v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
)

