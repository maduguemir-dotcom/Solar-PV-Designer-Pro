import streamlit as st

from product_management_ui import (
    display_product_management_ui,
)

st.set_page_config(
    page_title="Product Management Test",
    page_icon="🛠️",
    layout="wide",
)

display_product_management_ui()
