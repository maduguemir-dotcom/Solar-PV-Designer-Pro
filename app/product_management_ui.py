# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT LIBRARY MANAGEMENT UI
#
# SQLite-based Product Management
#
# Features:
#   - View products
#   - Search products
#   - Filter products
#   - Inspect product details
#   - Edit products
#   - Delete products safely
#   - Create temporary test product
#
# Storage:
#   library_store.py
#   app/data/solar_pv_library.db
# ==========================================================

import streamlit as st
import pandas as pd

from library_store import (
    initialize_database,
    load_product_library,
    get_product_from_library,
    add_product_to_library,
    update_product_in_library,
    remove_product_from_library,
    search_product_library,
    get_product_library_summary,
)


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

initialize_database()


# ==========================================================
# SAFE CONVERSION
# ==========================================================

def safe_float(value, default=0.0):

    try:

        if value is None:
            return default

        return float(value)

    except (TypeError, ValueError):

        return default


def safe_int(value, default=0):

    try:

        if value is None:
            return default

        return int(value)

    except (TypeError, ValueError):

        return default


# ==========================================================
# GET PRODUCTS
# ==========================================================

def get_products():

    try:

        return load_product_library()

    except Exception as error:

        st.error(
            f"Unable to load product library: {error}"
        )

        return []


# ==========================================================
# UPDATE PRODUCT
# ==========================================================

def update_existing_product(
    product_id,
    updated_product
):

    try:

        return update_product_in_library(
            product_id,
            updated_product
        )

    except Exception as error:

        st.error(
            f"Unable to update product: {error}"
        )

        return False


# ==========================================================
# DELETE PRODUCT
# ==========================================================

def delete_existing_product(
    product_id
):

    try:

        return remove_product_from_library(
            product_id
        )

    except Exception as error:

        st.error(
            f"Unable to delete product: {error}"
        )

        return False


# ==========================================================
# TEMPORARY TEST PRODUCT
# ==========================================================

def create_test_product():

    test_product = {

        "id":
            "test_panel_550w",

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
            "Temporary database test product.",

        "capacity_ah":
            0,

        "energy_kwh":
            0,

        "supplier":
            "Test Supplier",

        "country":
            "Uganda",

        "specifications":
            {}

    }

    try:

        result = add_product_to_library(
            test_product
        )

        return result

    except Exception as error:

        st.error(
            f"Unable to create test product: {error}"
        )

        return None


# ==========================================================
# PRODUCT DETAILS
# ==========================================================

def product_details(product):

    st.subheader(
        "📋 Product Details"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            "**Product Name:**",
            product.get("name", "")
        )

        st.write(
            "**Category:**",
            product.get("category", "")
        )

        st.write(
            "**Manufacturer:**",
            product.get("manufacturer", "")
        )

        st.write(
            "**Model:**",
            product.get("model", "")
        )

        st.write(
            "**Technology:**",
            product.get("technology", "")
        )

        st.write(
            "**Supplier:**",
            product.get("supplier", "")
        )

        st.write(
            "**Country:**",
            product.get("country", "")
        )

    with col2:

        st.write(
            "**Rated Power:**",
            f"{safe_float(product.get('rated_power_w'))} W"
        )

        st.write(
            "**Voltage:**",
            f"{safe_float(product.get('voltage_v'))} V"
        )

        st.write(
            "**Current:**",
            f"{safe_float(product.get('current_a'))} A"
        )

        st.write(
            "**Efficiency:**",
            f"{safe_float(product.get('efficiency_percent'))} %"
        )

        st.write(
            "**Warranty:**",
            f"{safe_float(product.get('warranty_years'))} years"
        )

        st.write(
            "**Price:**",
            f"{product.get('currency', 'USD')} "
            f"{safe_float(product.get('price'))}"
        )

        st.write(
            "**Quantity:**",
            safe_int(
                product.get(
                    "quantity",
                    1
                ),
                1
            )
        )

    if product.get("capacity_ah", 0):

        st.write(
            "**Capacity:**",
            f"{safe_float(product.get('capacity_ah'))} Ah"
        )

    if product.get("energy_kwh", 0):

        st.write(
            "**Energy:**",
            f"{safe_float(product.get('energy_kwh'))} kWh"
        )

    if product.get("notes"):

        st.markdown(
            "### Notes"
        )

        st.info(
            product.get("notes")
        )

    with st.expander(
        "🔧 Complete Database Record"
    ):

        st.json(product)


# ==========================================================
# EDIT PRODUCT
# ==========================================================

def edit_product(product):

    product_id = str(
        product.get("id", "")
    )

    st.subheader(
        "✏️ Edit Product"
    )

    with st.form(
        key=f"edit_product_{product_id}"
    ):

        # --------------------------------------------------
        # BASIC INFORMATION
        # --------------------------------------------------

        st.markdown(
            "### Basic Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Product Name",
                value=str(
                    product.get(
                        "name",
                        ""
                    )
                )
            )

            category = st.text_input(
                "Category",
                value=str(
                    product.get(
                        "category",
                        ""
                    )
                )
            )

            manufacturer = st.text_input(
                "Manufacturer",
                value=str(
                    product.get(
                        "manufacturer",
                        ""
                    )
                )
            )

        with col2:

            model = st.text_input(
                "Model",
                value=str(
                    product.get(
                        "model",
                        ""
                    )
                )
            )

            technology = st.text_input(
                "Technology",
                value=str(
                    product.get(
                        "technology",
                        ""
                    )
                )
            )

            supplier = st.text_input(
                "Supplier",
                value=str(
                    product.get(
                        "supplier",
                        ""
                    )
                )
            )

        # --------------------------------------------------
        # TECHNICAL INFORMATION
        # --------------------------------------------------

        st.markdown(
            "### Technical Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "rated_power_w",
                        0
                    )
                )
            )

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0
                    )
                )
            )

        with col2:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "current_a",
                        0
                    )
                )
            )

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "efficiency_percent",
                        0
                    )
                )
            )

        with col3:

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "capacity_ah",
                        0
                    )
                )
            )

            energy_kwh = st.number_input(
                "Energy (kWh)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "energy_kwh",
                        0
                    )
                )
            )

        # --------------------------------------------------
        # COMMERCIAL INFORMATION
        # --------------------------------------------------

        st.markdown(
            "### Commercial Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            price = st.number_input(
                "Price",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "price",
                        0
                    )
                )
            )

        with col2:

            currency = st.text_input(
                "Currency",
                value=str(
                    product.get(
                        "currency",
                        "USD"
                    )
                )
            )

        with col3:

            quantity = st.number_input(
                "Quantity",
                min_value=0,
                value=safe_int(
                    product.get(
                        "quantity",
                        1
                    ),
                    1
                )
            )

        # --------------------------------------------------
        # ADDITIONAL INFORMATION
        # --------------------------------------------------

        st.markdown(
            "### Additional Information"
        )

        col1, col2 = st.columns(2)

        with col1:

            warranty_years = st.number_input(
                "Warranty (Years)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "warranty_years",
                        0
                    )
                )
            )

        with col2:

            country = st.text_input(
                "Country",
                value=str(
                    product.get(
                        "country",
                        ""
                    )
                )
            )

        notes = st.text_area(
            "Notes",
            value=str(
                product.get(
                    "notes",
                    ""
                )
            ),
            height=120
        )

        # --------------------------------------------------
        # SAVE
        # --------------------------------------------------

        save = st.form_submit_button(
            "💾 Save Product Changes",
            type="primary"
        )

        if save:

            updated_product = {

                "name":
                    name,

                "category":
                    category,

                "manufacturer":
                    manufacturer,

                "model":
                    model,

                "technology":
                    technology,

                "rated_power_w":
                    rated_power_w,

                "voltage_v":
                    voltage_v,

                "current_a":
                    current_a,

                "efficiency_percent":
                    efficiency_percent,

                "warranty_years":
                    warranty_years,

                "price":
                    price,

                "currency":
                    currency,

                "quantity":
                    quantity,

                "notes":
                    notes,

                "capacity_ah":
                    capacity_ah,

                "energy_kwh":
                    energy_kwh,

                "supplier":
                    supplier,

                "country":
                    country,

            }

            success = update_existing_product(
                product_id,
                updated_product
            )

            if success:

                st.success(
                    "✅ Product updated successfully."
                )

                st.rerun()

            else:

                st.error(
                    "❌ Product update failed."
                )


# ==========================================================
# DELETE PRODUCT
# ==========================================================

def delete_product_interface(product):

    product_id = str(
        product.get("id", "")
    )

    product_name = product.get(
        "name",
        "Unnamed Product"
    )

    st.subheader(
        "🗑️ Delete Product"
    )

    st.warning(
        f"Product selected for deletion: "
        f"**{product_name}**"
    )

    confirm = st.checkbox(
        "I understand that deleting this product "
        "cannot be undone.",
        key=f"confirm_delete_{product_id}"
    )

    if st.button(
        "🗑️ Permanently Delete Product",
        key=f"delete_{product_id}"
    ):

        if not confirm:

            st.warning(
                "Please confirm the deletion first."
            )

        else:

            deleted = delete_existing_product(
                product_id
            )

            if deleted:

                st.success(
                    "✅ Product deleted successfully."
                )

                st.rerun()

            else:

                st.error(
                    "❌ Product could not be deleted."
                )


# ==========================================================
# MAIN MANAGEMENT UI
# ==========================================================

def display_product_management_ui():

    initialize_database()

    st.title(
        "🛠️ Product Library Management"
    )

    st.write(
        "Inspect, search, edit and safely "
        "delete products from your "
        "Solar PV Product Library."
    )

    # ------------------------------------------------------
    # DATABASE TEST
    # ------------------------------------------------------

    with st.expander(
        "🧪 Database Test / Development Tools"
    ):

        st.write(
            "This section is for testing the "
            "SQLite database connection."
        )

        if st.button(
            "➕ Create Test 550W Solar Panel",
            key="create_management_test_product"
        ):

            result = create_test_product()

            if result:

                st.success(
                    "✅ Test product created successfully."
                )

                st.rerun()

    # ------------------------------------------------------
    # SUMMARY
    # ------------------------------------------------------

    summary = (
        get_product_library_summary()
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Products",
            summary.get(
                "total_products",
                0
            )
        )

    with col2:

        st.metric(
            "Categories Used",
            len(
                summary.get(
                    "product_categories",
                    {}
                )
            )
        )

    with col3:

        st.metric(
            "Total Quantity",
            summary.get(
                "total_quantity",
                0
            )
        )

    st.divider()

    # ------------------------------------------------------
    # LOAD PRODUCTS
    # ------------------------------------------------------

    products = get_products()

    if not products:

        st.info(
            "No products found in the library."
        )

        st.caption(
            "Please add products through the "
            "Product Library interface or use "
            "the database test above."
        )

        return

    # ------------------------------------------------------
    # SEARCH
    # ------------------------------------------------------

    st.subheader(
        "🔎 Search and Filter"
    )

    col1, col2 = st.columns(2)

    with col1:

        search_query = st.text_input(
            "Search products",
            placeholder=(
                "Name, manufacturer, model "
                "or technology..."
            ),
            key="management_search"
        )

    categories = sorted(
        list(
            {
                product.get(
                    "category",
                    "Uncategorized"
                )
                for product in products
            }
        )
    )

    with col2:

        selected_category = st.selectbox(
            "Category",
            [
                "All Categories"
            ] + categories
        )

    # ------------------------------------------------------
    # FILTER
    # ------------------------------------------------------

    filtered_products = products

    if search_query:

        filtered_products = (
            search_product_library(
                query=search_query
            )
        )

    if selected_category != "All Categories":

        filtered_products = [

            product

            for product in filtered_products

            if product.get(
                "category",
                "Uncategorized"
            )
            == selected_category

        ]

    if not filtered_products:

        st.warning(
            "No products match your search."
        )

        return

    # ------------------------------------------------------
    # PRODUCT TABLE
    # ------------------------------------------------------

    st.subheader(
        f"📦 Products Found: "
        f"{len(filtered_products)}"
    )

    table_rows = []

    for product in filtered_products:

        table_rows.append({

            "Name":
                product.get(
                    "name",
                    ""
                ),

            "Category":
                product.get(
                    "category",
                    ""
                ),

            "Manufacturer":
                product.get(
                    "manufacturer",
                    ""
                ),

            "Model":
                product.get(
                    "model",
                    ""
                ),

            "Power (W)":
                safe_float(
                    product.get(
                        "rated_power_w",
                        0
                    )
                ),

            "Price":
                safe_float(
                    product.get(
                        "price",
                        0
                    )
                ),

            "Currency":
                product.get(
                    "currency",
                    "USD"
                ),

            "Quantity":
                safe_int(
                    product.get(
                        "quantity",
                        0
                    )
                )

        })

    st.dataframe(
        pd.DataFrame(table_rows),
        use_container_width=True,
        hide_index=True
    )

    # ------------------------------------------------------
    # PRODUCT SELECTION
    # ------------------------------------------------------

    product_options = {}

    for product in filtered_products:

        label = (
            f"{product.get('name', 'Unnamed')} "
            f"| {product.get('manufacturer', '')} "
            f"| {product.get('model', '')}"
        )

        product_options[label] = (
            product.get("id")
        )

    selected_label = st.selectbox(
        "Select a product to manage",
        list(
            product_options.keys()
        )
    )

    selected_product_id = (
        product_options[
            selected_label
        ]
    )

    selected_product = (
        get_product_from_library(
            selected_product_id
        )
    )

    if selected_product is None:

        st.error(
            "Unable to retrieve the selected product."
        )

        return

    st.divider()

    # ------------------------------------------------------
    # MANAGEMENT TABS
    # ------------------------------------------------------

    details_tab, edit_tab, delete_tab = st.tabs(

        [

            "📋 Product Details",

            "✏️ Edit Product",

            "🗑️ Delete Product"

        ]

    )

    with details_tab:

        product_details(
            selected_product
        )

    with edit_tab:

        edit_product(
            selected_product
        )

    with delete_tab:

        delete_product_interface(
            selected_product
        )


# ==========================================================
# ALTERNATIVE INTERFACE NAME
# ==========================================================

def display_management_ui():

    return display_product_management_ui()


def product_management_interface():

    return display_product_management_ui()


# ==========================================================
# COMPATIBILITY ALIASES
# ==========================================================

def update_product(
    product_id,
    updated_product
):

    return update_existing_product(
        product_id,
        updated_product
    )


def delete_product(
    product_id
):

    return delete_existing_product(
        product_id
    )
