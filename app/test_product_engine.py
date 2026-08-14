import streamlit as st

from product_engine import (
    PRODUCT_CATEGORIES,
    PRODUCT_TECHNOLOGIES,
    get_default_products,
    create_product,
    search_products,
    rank_products,
    compare_products,
    analyze_products,
)


st.title("🔎 Product Engine Diagnostic")

st.success(
    "product_engine.py imported successfully."
)


st.subheader("Product Categories")

st.write(
    PRODUCT_CATEGORIES
)


st.subheader("Product Technologies")

st.write(
    PRODUCT_TECHNOLOGIES
)


products = get_default_products()


st.subheader("Default Product Database")

st.dataframe(
    products,
    use_container_width=True
)


st.subheader("Search Test")

search_results = search_products(
    products,
    "550"
)

st.dataframe(
    search_results,
    use_container_width=True
)


st.subheader("Engineering Matching Test")

ranked = rank_products(
    products,
    required_power_w=5000,
    required_voltage_v=48,
)

st.dataframe(
    ranked,
    use_container_width=True
)


st.subheader("Comparison")

st.dataframe(
    compare_products(
        products
    ),
    use_container_width=True
)


st.subheader("Complete Analysis")

st.json(
    analyze_products(
        products,
        required_power_w=5000,
        required_voltage_v=48,
    )
)
