import streamlit as st

from database import (
    DATABASE_FILE,
    initialize_database,
    add_product,
    get_products,
    get_product,
    delete_product,
    add_service,
    get_services,
    add_cost_item,
    get_cost_items,
    search_products,
    search_services,
    get_database_summary,
    backup_database,
)


st.title(
    "🗄️ Solar PV Designer Pro Database Diagnostic"
)

st.success(
    "database.py imported successfully."
)


# ==========================================================
# INITIALIZATION
# ==========================================================

st.subheader(
    "Database Initialization"
)

initialize_database()

st.success(
    "SQLite database initialized successfully."
)

st.write(
    f"Database location: `{DATABASE_FILE}`"
)


# ==========================================================
# PRODUCT TEST
# ==========================================================

st.subheader(
    "☀️ Product Database Test"
)

test_product = {

    "name":
        "DATABASE TEST 550W Panel",

    "category":
        "Solar Panel",

    "manufacturer":
        "Database Test",

    "model":
        "DB-550",

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
        "Database diagnostic record."

}


if st.button(
    "💾 Insert Test Product",
    key="database_insert_product"
):

    product_id = add_product(
        test_product
    )

    st.success(
        f"Product inserted with ID: {product_id}"
    )


products = get_products()

st.write(
    f"Products in database: {len(products)}"
)

if products:

    st.dataframe(
        products,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# PRODUCT SEARCH
# ==========================================================

st.subheader(
    "🔎 Product Search"
)

search_query = st.text_input(
    "Search products",
    key="database_product_search"
)

if search_query:

    results = search_products(
        search_query
    )

    st.write(
        f"Search results: {len(results)}"
    )

    st.json(
        results
    )


# ==========================================================
# SERVICE TEST
# ==========================================================

st.subheader(
    "🔧 Service Database Test"
)

test_service = {

    "name":
        "Database Test Installation Labour",

    "category":
        "Installation Labour",

    "unit":
        "job",

    "unit_price":
        150000,

    "currency":
        "UGX",

    "supplier":
        "Test Contractor",

    "location":
        "Kampala",

    "notes":
        "Database diagnostic service."

}


if st.button(
    "💾 Insert Test Service",
    key="database_insert_service"
):

    service_id = add_service(
        test_service
    )

    st.success(
        f"Service inserted with ID: {service_id}"
    )


services = get_services()

st.write(
    f"Services in database: {len(services)}"
)

if services:

    st.dataframe(
        services,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# COST TEST
# ==========================================================

st.subheader(
    "💰 Cost Item Database Test"
)

test_cost = {

    "name":
        "Database Test Transport",

    "category":
        "Transportation",

    "unit":
        "trip",

    "unit_price":
        50000,

    "quantity":
        2,

    "currency":
        "UGX",

    "supplier":
        "Test Transporter",

    "location":
        "Kampala",

    "notes":
        "Database diagnostic cost."

}


if st.button(
    "💾 Insert Test Cost",
    key="database_insert_cost"
):

    cost_id = add_cost_item(
        test_cost
    )

    st.success(
        f"Cost item inserted with ID: {cost_id}"
    )


cost_items = get_cost_items()

st.write(
    f"Cost items in database: {len(cost_items)}"
)

if cost_items:

    st.dataframe(
        cost_items,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

st.subheader(
    "📊 Database Summary"
)

st.json(
    get_database_summary()
)


# ==========================================================
# BACKUP
# ==========================================================

st.subheader(
    "📦 Database Backup"
)

if st.button(
    "Create SQLite Backup",
    key="database_backup"
):

    result = backup_database()

    if result["success"]:

        st.success(
            "Database backup created successfully."
        )

        st.write(
            result["file"]
        )

    else:

        st.error(
            result["message"]
        )
