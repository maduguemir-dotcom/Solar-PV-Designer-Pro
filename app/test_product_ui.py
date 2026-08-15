import streamlit as st

from product_ui import (
    display_product_library_ui,
    initialize_product_library,
)


st.set_page_config(
    page_title="Product Library Test",
    page_icon="📚",
    layout="wide",
)


st.title(
    "📚 Product Library UI Diagnostic"
)

st.success(
    "product_ui.py imported successfully."
)


initialize_product_library()

st.write(
    f"Products currently in library: "
    f"{len(st.session_state.product_library)}"
)


display_product_library_ui()
