import streamlit as st

st.set_page_config(
    page_title="Product Management Data Diagnostic",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Product Management Data Diagnostic")

try:
    import product_ui

    st.success("product_ui.py imported successfully.")

    products = product_ui.get_products()

    st.write("### Result from product_ui.get_products()")

    st.write("Number of products:", len(products))

    if products:
        st.success("Products were found.")
        st.json(products)
    else:
        st.warning("product_ui.get_products() returned an empty list.")

except Exception as exc:
    st.error("Error while reading the product library.")
    st.exception(exc)
