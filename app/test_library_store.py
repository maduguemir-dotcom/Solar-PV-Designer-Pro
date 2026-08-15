import streamlit as st

from library_store import (
    ensure_data_directory,
    load_product_library,
    save_product_library,
    load_service_library,
    save_service_library,
    create_service_record,
    add_product_to_library,
    add_service_to_library,
    search_product_library,
    search_service_library,
    get_library_summary,
    backup_library,
)


st.title(
    "💾 Library Storage Diagnostic"
)

st.success(
    "library_store.py imported successfully."
)


# ==========================================================
# DIRECTORY
# ==========================================================

st.subheader(
    "Storage Directory"
)

data_dir = ensure_data_directory()

st.write(
    str(data_dir)
)


# ==========================================================
# CURRENT LIBRARIES
# ==========================================================

st.subheader(
    "Current Product Library"
)

products = load_product_library()

st.write(
    f"Products stored: {len(products)}"
)

if products:

    st.json(
        products
    )


st.subheader(
    "Current Service Library"
)

services = load_service_library()

st.write(
    f"Services stored: {len(services)}"
)

if services:

    st.json(
        services
    )


# ==========================================================
# PRODUCT TEST
# ==========================================================

st.subheader(
    "Product Storage Test"
)

test_product = {

    "name":
        "TEST 550W Solar Panel",

    "category":
        "Solar Panel",

    "manufacturer":
        "Test Manufacturer",

    "model":
        "TEST-550",

    "technology":
        "Monocrystalline",

    "rated_power_w":
        550,

    "voltage_v":
        41.5,

    "capacity_ah":
        0,

    "energy_kwh":
        0,

    "efficiency_percent":
        21,

    "warranty_years":
        10,

    "supplier":
        "Test Supplier",

    "country":
        "Uganda",

    "notes":
        "Diagnostic test product.",

}


if st.button(
    "💾 Save Test Product"
):

    result = add_product_to_library(
        test_product
    )

    if result["success"]:

        st.success(
            result["message"]
        )

    else:

        st.error(
            result["message"]
        )


# ==========================================================
# SERVICE TEST
# ==========================================================

st.subheader(
    "Service Storage Test"
)

test_service = create_service_record(

    name="TEST Solar Installation Labour",

    category="Installation Labour",

    unit="job",

    unit_price=100000,

    currency="UGX",

    supplier="Test Contractor",

    location="Kampala",

    notes="Diagnostic test service.",

)


if st.button(
    "💾 Save Test Service"
):

    result = add_service_to_library(
        test_service
    )

    if result["success"]:

        st.success(
            result["message"]
        )

    else:

        st.error(
            result["message"]
        )


# ==========================================================
# SEARCH TEST
# ==========================================================

st.subheader(
    "Product Search Test"
)

product_search = search_product_library(
    "TEST"
)

st.write(
    f"Products found: {len(product_search)}"
)

if product_search:

    st.json(
        product_search
    )


st.subheader(
    "Service Search Test"
)

service_search = search_service_library(
    "TEST"
)

st.write(
    f"Services found: {len(service_search)}"
)

if service_search:

    st.json(
        service_search
    )


# ==========================================================
# SUMMARY
# ==========================================================

st.subheader(
    "Library Summary"
)

st.json(
    get_library_summary()
)


# ==========================================================
# BACKUP TEST
# ==========================================================

st.subheader(
    "Backup Test"
)

if st.button(
    "📦 Create Library Backup"
):

    result = backup_library()

    if result["success"]:

        st.success(
            "Library backup created successfully."
        )

        st.json(
            result
        )

    else:

        st.error(
            "Backup failed."
        )
