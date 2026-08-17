import streamlit as st

st.set_page_config(
    page_title="Product Management UI Diagnostic",
    page_icon="🧰",
    layout="wide",
)

st.title("🧰 Product Management UI Diagnostic")

try:
    import product_management_ui

    st.success("product_management_ui.py imported successfully.")

    st.subheader("Available Functions")

    functions = [
        name
        for name in dir(product_management_ui)
        if not name.startswith("_")
        and callable(getattr(product_management_ui, name))
    ]

    st.write(functions)

except Exception as e:
    st.error("product_management_ui.py failed to import.")

    st.exception(e)
