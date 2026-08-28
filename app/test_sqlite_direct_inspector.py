import streamlit as st
import sqlite3
from pathlib import Path

st.set_page_config(
    page_title="Direct SQLite Inspector",
    layout="wide",
)

st.title("🔬 Direct SQLite Database Inspector")

# ==========================================================
# DATABASE PATH
# ==========================================================

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "solar_pv_library.db"

st.subheader("1. Database Location")

st.code(str(DB_PATH))

st.write("Exists:", DB_PATH.exists())

if not DB_PATH.exists():
    st.error("Database file does not exist.")
    st.stop()

st.write(
    "Database size:",
    DB_PATH.stat().st_size,
    "bytes"
)

# ==========================================================
# DIRECT CONNECTION
# ==========================================================

st.subheader("2. SQLite Tables")

try:

    connection = sqlite3.connect(
        str(DB_PATH)
    )

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type='table'
        ORDER BY name
        """
    )

    tables = cursor.fetchall()

    table_names = [
        table[0]
        for table in tables
    ]

    st.success("Database opened successfully.")

    st.write(
        "Tables found:",
        table_names
    )

except Exception as e:

    st.error(
        f"Database connection failed: {e}"
    )

    st.stop()


# ==========================================================
# PRODUCTS TABLE
# ==========================================================

st.subheader("3. Products Table Inspection")

if "products" not in table_names:

    st.error(
        "The 'products' table does not exist."
    )

else:

    # ------------------------------------------------------
    # TABLE STRUCTURE
    # ------------------------------------------------------

    st.markdown("### Products Table Structure")

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

    st.write(column_names)

    # ------------------------------------------------------
    # ROW COUNT
    # ------------------------------------------------------

    st.markdown("### Product Count")

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM products
        """
    )

    product_count = cursor.fetchone()[0]

    st.metric(
        "Products Stored",
        product_count
    )

    # ------------------------------------------------------
    # RAW PRODUCTS
    # ------------------------------------------------------

    st.markdown("### Raw Product Records")

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY name ASC
        """
    )

    rows = cursor.fetchall()

    if rows:

        products = []

        for row in rows:

            product = dict(
                zip(
                    column_names,
                    row
                )
            )

            products.append(product)

        st.success(
            f"{len(products)} product(s) found."
        )

        st.json(products)

    else:

        st.warning(
            "The products table exists but contains zero records."
        )


# ==========================================================
# SERVICES TABLE
# ==========================================================

st.subheader("4. Services Table Inspection")

if "services" not in table_names:

    st.warning(
        "The 'services' table does not exist."
    )

else:

    cursor.execute(
        """
        SELECT COUNT(*)
        FROM services
        """
    )

    service_count = cursor.fetchone()[0]

    st.metric(
        "Services Stored",
        service_count
    )


# ==========================================================
# DATABASE MODULE COMPARISON
# ==========================================================

st.subheader(
    "5. Compare With library_store.py"
)

try:

    import library_store

    st.code(
        str(
            Path(
                library_store.DATABASE_FILE
            ).resolve()
        )
    )

    st.write(
        "Same database path:",
        Path(
            library_store.DATABASE_FILE
        ).resolve() == DB_PATH.resolve()
    )

    products = (
        library_store.load_product_library()
    )

    st.write(
        "Products returned by "
        "library_store:",
        len(products)
    )

    if products:

        st.json(products)

except Exception as e:

    st.error(
        f"library_store comparison failed: {e}"
    )


# ==========================================================
# FINISH
# ==========================================================

connection.close()

st.divider()

st.info(
    "This test reads the SQLite database directly without "
    "depending on product_ui.py or product_management_ui.py."
)
