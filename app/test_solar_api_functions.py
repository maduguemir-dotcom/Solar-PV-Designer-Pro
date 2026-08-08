# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# ==========================================================
#
# Solar API Function Diagnostic
# Version: 2.3.0
#
# Purpose:
# Display the actual functions available in solar_api.py.
#
# This file does NOT modify solar_api.py.
#
# ==========================================================

import streamlit as st
import inspect
import solar_api


# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="Solar API Diagnostic",
    page_icon="🔎",
    layout="wide"
)


# ==========================================================
# HEADER
# ==========================================================

st.title(
    "🔎 Solar PV Designer Pro Africa™"
)

st.subheader(
    "Solar API Function Diagnostic"
)


st.write(
    """
    This diagnostic page inspects the existing
    `solar_api.py` module so we can identify the
    exact function already being used by the
    working NASA POWER connection.
    """
)


# ==========================================================
# MODULE STATUS
# ==========================================================

st.success(
    "✅ solar_api.py imported successfully."
)


# ==========================================================
# MODULE FILE
# ==========================================================

st.header(
    "📁 Module Information"
)


try:

    st.code(
        solar_api.__file__
    )

except Exception:

    st.write(
        "Module file location unavailable."
    )


# ==========================================================
# FUNCTIONS
# ==========================================================

st.header(
    "⚙️ Functions Found in solar_api.py"
)


functions_found = []


for name in dir(solar_api):

    if name.startswith("_"):

        continue


    try:

        item = getattr(
            solar_api,
            name
        )

    except Exception:

        continue


    if callable(item):

        functions_found.append(
            name
        )


if not functions_found:

    st.error(
        "No callable functions were found."
    )

    st.stop()


st.success(
    f"{len(functions_found)} callable functions found."
)


# ==========================================================
# DISPLAY FUNCTIONS
# ==========================================================

for function_name in functions_found:

    st.subheader(
        f"🔹 {function_name}()"
    )


    try:

        function_object = getattr(
            solar_api,
            function_name
        )


        try:

            signature = inspect.signature(
                function_object
            )

            st.code(
                f"{function_name}{signature}"
            )

        except Exception:

            st.write(
                "Function signature unavailable."
            )


        try:

            source = inspect.getsource(
                function_object
            )

            with st.expander(
                f"View source — {function_name}()"
            ):

                st.code(
                    source,
                    language="python"
                )

        except Exception:

            st.info(
                "Source code unavailable for this function."
            )


    except Exception as error:

        st.warning(
            f"Could not inspect {function_name}: {error}"
        )


# ==========================================================
# NASA-RELATED NAMES
# ==========================================================

st.divider()

st.header(
    "📡 NASA / Solar Related Functions"
)


keywords = [
    "nasa",
    "power",
    "solar",
    "resource",
    "api",
    "monthly",
    "coordinate",
    "location"
]


possible_functions = []


for function_name in functions_found:

    lower_name = (
        function_name.lower()
    )


    if any(
        keyword in lower_name
        for keyword in keywords
    ):

        possible_functions.append(
            function_name
        )


if possible_functions:

    st.success(
        "Possible NASA/solar functions identified:"
    )


    for function_name in possible_functions:

        st.write(
            f"• `{function_name}()`"
        )

else:

    st.warning(
        """
        No function name contains the usual
        NASA/solar/API keywords.
        """
    )


# ==========================================================
# FINAL MESSAGE
# ==========================================================

st.divider()

st.info(
    """
    **Next step**

    Do not modify `solar_api.py`.

    This page is only inspecting the existing module.

    Once we identify the correct function, we will
    modify `test_nasa_graphs.py` to call that exact
    function and connect it to the already-tested
    analytics and graph modules.
    """
)


# ==========================================================
# FOOTER
# ==========================================================

st.caption(
    """
    Solar PV Designer Pro Africa™
    Solar API Diagnostic v2.3.0

    Developed by:
    Engr. Prof. Ibrahim Sani Madugu
    """
)

