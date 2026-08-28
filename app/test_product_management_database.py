import streamlit as st
import os

from pathlib import Path

st.set_page_config(
    page_title="Product Management Database Diagnostic",
    layout="wide",
)

st.title("🔍 Product Management Database Diagnostic")

# ----------------------------------------------------------
# PATH INFORMATION
# ----------------------------------------------------------

APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
DB_PATH = DATA_DIR / "solar_pv_library.db"

st.subheader("1. Expected Database Location")

st.code(str(DB_PATH))

st.write("Database exists:", DB_PATH.exists())

if DB_PATH.exists():
    st.write(
        "Database size:",
        DB_PATH.stat().st_size,
        "bytes"
    )


# ----------------------------------------------------------
# IMPORT DATABASE MODULE
# ----------------------------------------------------------

st.subheader("2. Import library_store.py")

try:

    import library_store

    st.success(
        "library_store.py imported successfully."
    )

    st.write(
        "Module location:"
    )

    st.code(
        str(
            Path(
                library_store.__file__
            ).resolve()
        )
    )

except Exception as e:

    st.error(
        f"Unable to import library_store.py: {e}"
    )

    st.stop()


# ----------------------------------------------------------
# AVAILABLE FUNCTIONS
# ----------------------------------------------------------

st.subheader("3. Available Product Functions")

functions = [

    name

    for name in dir(library_store)

    if "product" in name.lower()
    or "database" in name.lower()

]

st.write(functions)


# ----------------------------------------------------------
# INITIALIZE DATABASE
# ----------------------------------------------------------

st.subheader("4. Initialize Database")

try:

    if hasattr(
        library_store,
        "initialize_database"
    ):

        library_store.initialize_database()

        st.success(
            "Database initialized successfully."
        )

    else:

        st.warning(
            "initialize_database() was not found."
        )

except Exception as e:

    st.error(
        f"Database initialization error: {e}"
    )


# ----------------------------------------------------------
# LOAD PRODUCTS
# ----------------------------------------------------------

st.subheader("5. Load Products")

try:

    if hasattr(
        library_store,
        "load_product_library"
    ):

        products = (
            library_store.load_product_library()
        )

        st.write(
            "Number of products:",
            len(products)
        )

        if products:

            st.success(
                "Products found."
            )

            st.json(products)

        else:

            st.warning(
                "No products returned."
            )

    else:

        st.error(
            "load_product_library() does not exist."
        )

except Exception as e:

    st.error(
        f"Error loading products: {e}"
    )


# ----------------------------------------------------------
# TEST product_ui.py
# ----------------------------------------------------------

st.subheader(
    "6. Compare With product_ui.py"
)

try:

    import product_ui

    st.success(
        "product_ui.py imported successfully."
    )

    st.code(
        str(
            Path(
                product_ui.__file__
            ).resolve()
        )
    )

    if hasattr(
        product_ui,
        "get_products"
    ):

        ui_products = (
            product_ui.get_products()
        )

        st.write(
            "Products returned by "
            "product_ui.get_products():",
            len(ui_products)
        )

        if ui_products:

            st.json(
                ui_products
            )

        else:

            st.warning(
                "product_ui.get_products() "
                "returned zero products."
            )

    else:

        st.error(
            "get_products() was not found "
            "in product_ui.py"
        )

except Exception as e:

    st.error(
        f"Error importing product_ui.py: {e}"
    )


# ----------------------------------------------------------
# CURRENT WORKING DIRECTORY
# ----------------------------------------------------------

st.subheader(
    "7. Runtime Information"
)

st.write(
    "Current working directory:"
)

st.code(
    os.getcwd()
)

st.write(
    "App directory:"
)

st.code(
    str(APP_DIR)
)

st.write(
    "Data directory:"
)

st.code(
    str(DATA_DIR)
)
