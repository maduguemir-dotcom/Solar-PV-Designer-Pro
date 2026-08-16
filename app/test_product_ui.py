import streamlit as st

from product_ui import (
    display_product_library_ui,
)


st.set_page_config(
    page_title="Product Library Diagnostic",
    page_icon="📚",
    layout="wide",
)


st.title(
    "📚 Product Library UI Diagnostic"
)

st.success(
    "product_ui.py imported successfully."
)


st.write(
    "Launching the complete Product Library interface..."
)


display_product_library_ui()
