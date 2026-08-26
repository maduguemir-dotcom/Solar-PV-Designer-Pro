import streamlit as st
from pathlib import Path
import json

import product_ui
import library_store


st.set_page_config(
    page_title="Product Storage Diagnostic",
    page_icon="🔍",
    layout="wide",
)

st.title("🔍 Product Storage Diagnostic")


# ============================================================
# PRODUCT UI
# ============================================================

st.header("1. product_ui.py")

try:

    products = product_ui.get_products()

    st.success("product_ui.get_products() executed successfully.")

    st.write(
        "Number of products returned:",
        len(products),
    )

    if products:
        st.json(products)
    else:
        st.warning(
            "product_ui.get_products() returned an empty list."
        )

except Exception as exc:

    st.error(
        f"Error from product_ui.get_products(): {exc}"
    )


# ============================================================
# LIBRARY STORE
# ============================================================

st.header("2. library_store.py")

try:

    products = library_store.load_product_library()

    st.success(
        "library_store.load_product_library() executed successfully."
    )

    st.write(
        "Number of products returned:",
        len(products),
    )

    if products:
        st.json(products)
    else:
        st.warning(
            "load_product_library() returned an empty list."
        )

except Exception as exc:

    st.error(
        f"Error loading product library: {exc}"
    )


# ============================================================
# STORAGE PATH
# ============================================================

st.header("3. Product Library Storage Location")

try:

    product_file = library_store.PRODUCT_LIBRARY_FILE

    st.code(
        str(product_file)
    )

    product_path = Path(product_file)

    st.write(
        "File exists:",
        product_path.exists(),
    )

    if product_path.exists():

        st.write(
            "File size:",
            f"{product_path.stat().st_size} bytes",
        )

        raw_data = product_path.read_text(
            encoding="utf-8"
        )

        st.subheader(
            "Raw File Contents"
        )

        st.code(
            raw_data,
            language="json",
        )

        try:

            parsed_data = json.loads(
                raw_data
            )

            st.subheader(
                "Parsed Data"
            )

            st.write(
                "Number of records:",
                len(parsed_data)
                if isinstance(
                    parsed_data,
                    list,
                )
                else "Not a list",
            )

            st.json(
                parsed_data
            )

        except Exception as exc:

            st.error(
                f"JSON parsing error: {exc}"
            )

except Exception as exc:

    st.error(
        f"Storage path diagnostic failed: {exc}"
    )


# ============================================================
# SESSION STATE
# ============================================================

st.header("4. Streamlit Session State")

if st.session_state:

    for key, value in st.session_state.items():

        if "product" in key.lower():

            st.write(
                f"**{key}**"
            )

            try:
                st.write(value)
            except Exception:
                st.write(
                    "Unable to display value."
                )

else:

    st.info(
        "No Streamlit session state variables found."
    )


# ============================================================
# MODULE LOCATIONS
# ============================================================

st.header("5. Module Locations")

st.write(
    "**product_ui.py:**"
)

st.code(
    product_ui.__file__
)

st.write(
    "**library_store.py:**"
)

st.code(
    library_store.__file__
)
