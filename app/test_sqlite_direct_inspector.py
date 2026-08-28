import streamlit as st
import sqlite3
from pathlib import Path

# IMPORTANT:
# Import library_store FIRST.
# This automatically initializes the SQLite database.

import library_store


st.set_page_config(
    page_title="Direct SQLite Inspector",
    layout="wide",
)

st.title("🔬 Direct SQLite Database Inspector")


# ==========================================================
# DATABASE PATH FROM THE REAL STORAGE ENGINE
# ==========================================================

DB_PATH = Path(
    library_store.DATABASE_FILE
).resolve()


st.subheader("1. Database Location")

st.code(str(DB_PATH))

st.write(
    "Database exists:",
    DB_PATH.exists()
)

if DB_PATH.exists():

    st.write(
        "Database size:",
        DB_PATH.stat().st_size,
        "bytes"
    )

else:

    st.error(
        "Database file was not created."
    )

    st.stop()


# ==========================================================
# INITIALIZE AGAIN FOR SAFETY
# ==========================================================

st.subheader("2. Initialize Database")

try:

    result = (
        library_store.initialize_database()
    )

    st.success(
        "Database initialized successfully."
    )

    st.write(
        "Initialization result:",
        result
    )

except Exception as e:

    st.error(
        f"Database initialization failed: {e}"
    )

    st.stop()


# ==========================================================
# DIRECT SQLITE CONNECTION
# ==========================================================

st.subheader(
    "3. SQLite Tables"
)

try:

    connection = sqlite3.connect(
        str(DB_PATH)
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
        ORDER BY name
        """
    )

    tables = cursor.fetchall()

    table_names = [
        row[0]
        for row in tables
    ]

    st.success(
        "SQLite database opened successfully."
    )

    st.write(
        "Tables found:",
        table_names
    )

except Exception as e:

    st.error(
        f"SQLite connection error: {e}"
    )

    st.stop()


# ==========================================================
# PRODUCTS TABLE
# ==========================================================

st.subheader(
    "4. Products Table"
)

if "products" not in table_names:

    st.error(
        "Products table does not exist."
    )

else:

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        """
    )

    product_count = (
        cursor.fetchone()[0]
    )

    st.metric(
        "Products Stored",
        product_count
    )

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY name
        """
    )

    rows = cursor.fetchall()

    if rows:

        cursor.execute(
            """
            PRAGMA table_info(products)
            """
        )

        columns = cursor.fetchall()

        column_names = [
            column[1]
            for column in columns
        ]

        products = []

        for row in rows:

            product = dict(
                zip(
                    column_names,
                    row
                )
            )

            products.append(
                product
            )

        st.success(
            f"{len(products)} product(s) found."
        )

        st.json(products)

    else:

        st.info(
            "No products currently stored."
        )


# ==========================================================
# TEST library_store
# ==========================================================

st.subheader(
    "5. Test library_store"
)

try:

    products = (
        library_store.load_product_library()
    )

    st.write(
        "Products returned by "
        "load_product_library():",
        len(products)
    )

    if products:

        st.json(products)

    else:

        st.info(
            "library_store currently returns "
            "an empty product library."
        )

except Exception as e:

    st.error(
        f"library_store error: {e}"
    )


# ==========================================================
# CREATE TEST PRODUCT
# ==========================================================

st.subheader(
    "6. Create Test Product"
)

st.write(
    "Use this only to confirm that SQLite "
    "storage works in the CURRENT deployment."
)

if st.button(
    "➕ Create Test 550W Solar Panel",
    type="primary"
):

    test_product = {

        "id": "test_panel_550w",

        "name":
            "Test 550W Solar Panel",

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

        "current_a":
            13.2,

        "efficiency_percent":
            21.5,

        "warranty_years":
            10,

        "price":
            150,

        "currency":
            "USD",

        "quantity":
            1,

        "notes":
            "SQLite storage test.",

        "capacity_ah":
            0,

        "energy_kwh":
            0,

        "supplier":
            "",

        "country":
            "",

        "specifications":
            {}
    }

    try:

        saved_product = (
            library_store
            .add_product_to_library(
                test_product
            )
        )

        st.success(
            "✅ Test product created successfully."
        )

        st.json(
            saved_product
        )

        st.rerun()

    except Exception as e:

        st.error(
            f"Unable to create test product: {e}"
        )


# ==========================================================
# CLEAN UP
# ==========================================================

connection.close()

st.divider()

st.caption(
    "This diagnostic uses the same "
    "library_store.py storage engine as the application."
)
