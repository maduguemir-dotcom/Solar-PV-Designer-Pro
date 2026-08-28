import streamlit as st

st.set_page_config(
    page_title="Product Management Test",
    layout="wide"
)

st.title("🧪 Product Management UI Test")

st.success("Streamlit is running correctly.")

st.write("Attempting to import product_management_ui.py ...")

try:

    from product_management_ui import (
        display_product_management_ui
    )

    st.success(
        "✅ product_management_ui.py imported successfully."
    )

    st.write(
        "Calling display_product_management_ui() ..."
    )

    display_product_management_ui()

except Exception as error:

    st.error(
        "❌ An error occurred while loading "
        "Product Management UI."
    )

    st.exception(error)
