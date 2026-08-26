import streamlit as st

from library_store import (
    DATABASE_FILE,
    initialize_database,
    add_product_to_library,
    load_product_library,
    get_library_summary,
)

st.set_page_config(
    page_title="SQLite Library Test",
    page_icon="🗄️",
)

st.title("🗄️ SQLite Product Library Diagnostic")

initialize_database()

st.success(
    "SQLite database initialized successfully."
)

st.write(
    "Database location:"
)

st.code(
    str(DATABASE_FILE)
)

products = load_product_library()

st.write(
    "Current products:",
    len(products)
)

if st.button(
    "Add Test Product"
):

    test_product = {

        "id": "test_panel_550w",

        "name": "Test 550W Solar Panel",

        "category": "Solar Panel",

        "manufacturer": "Test Manufacturer",

        "model": "TEST-550",

        "technology": "Monocrystalline",

        "rated_power_w": 550,

        "voltage_v": 41.5,

        "current_a": 13.2,

        "efficiency_percent": 21.5,

        "warranty_years": 10,

        "price": 150,

        "currency": "USD",

        "quantity": 1,

        "notes": (
            "SQLite storage test."
        ),
    }

    result = add_product_to_library(
        test_product
    )

    st.success(
        "Test product added successfully."
    )

    st.json(
        result
    )

    st.rerun()


st.divider()

st.subheader(
    "Products in Database"
)

products = load_product_library()

if products:

    st.json(products)

else:

    st.info(
        "No products stored yet."
    )


st.divider()

st.subheader(
    "Library Summary"
)

st.json(
    get_library_summary()
)
