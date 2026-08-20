import streamlit as st

from library_store import (
    add_product_to_library,
    load_product_library,
    get_library_summary,
)

st.set_page_config(
    page_title="Product Library Write Test",
    page_icon="🧪",
    layout="wide",
)

st.title("🧪 Product Library Write Diagnostic")

st.write(
    "This test checks whether a product can be "
    "saved and reloaded from product_library.json."
)

st.divider()

# -------------------------------------------------
# CURRENT RECORDS
# -------------------------------------------------

products_before = load_product_library()

st.subheader("Current Product Library")

st.write(
    f"Number of products before test: "
    f"**{len(products_before)}**"
)

if products_before:
    st.json(products_before)

else:
    st.info("The product library is currently empty.")


# -------------------------------------------------
# ADD TEST PRODUCT
# -------------------------------------------------

st.divider()

st.subheader("Add Test Product")

if st.button(
    "➕ Add Test Solar Panel",
    type="primary",
    use_container_width=True,
):

    test_product = {
        "name": "Test 550W Solar Panel",
        "category": "Solar Panel",
        "manufacturer": "Test Manufacturer",
        "model": "TEST-550",
        "technology": "Monocrystalline",
        "rated_power_w": 550,
        "voltage_v": 41.5,
        "efficiency_percent": 21.0,
        "warranty_years": 10,
        "supplier": "Test Supplier",
        "country": "Uganda",
        "price": 150,
        "currency": "USD",
        "quantity": 1,
        "notes": "Temporary diagnostic product.",
    }

    saved_product = add_product_to_library(
        test_product
    )

    st.success(
        "Test product saved successfully."
    )

    st.json(saved_product)

    st.rerun()


# -------------------------------------------------
# RELOAD LIBRARY
# -------------------------------------------------

st.divider()

st.subheader("Reloaded Product Library")

products_after = load_product_library()

st.write(
    f"Number of products after reload: "
    f"**{len(products_after)}**"
)

if products_after:

    st.success(
        "Product records are being loaded "
        "successfully."
    )

    st.json(products_after)

else:

    st.warning(
        "No product records were found."
    )


# -------------------------------------------------
# LIBRARY SUMMARY
# -------------------------------------------------

st.divider()

st.subheader("Library Summary")

summary = get_library_summary()

st.json(summary)
