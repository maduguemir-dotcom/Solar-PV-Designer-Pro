# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT LIBRARY MANAGEMENT UI
#
# Search | Inspect | Edit | Delete
#
# Uses:
# library_store.py
# app/data/solar_pv_library.db
# ==========================================================

import streamlit as st
import pandas as pd

from library_store import (
    initialize_database,
    load_product_library,
    get_product_from_library,
    update_product_in_library,
    remove_product_from_library,
    search_product_library,
    get_product_library_summary,
)


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

initialize_database()


# ==========================================================
# SAFE CONVERSION FUNCTIONS
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
            f"Unable to load products: {error}"
        )

        return []


# ==========================================================
# UPDATE EXISTING PRODUCT
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
# DELETE EXISTING PRODUCT
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
# PRODUCT EDIT FORM
# ==========================================================

def display_edit_product_form(product):

    product_id = str(
        product.get("id", "")
    )

    st.subheader(
        f"✏️ Edit Product: "
        f"{product.get('name', '')}"
    )

    with st.form(
        key=f"edit_product_form_{product_id}"
    ):

        # ----------------------------------------------
        # BASIC INFORMATION
        # ----------------------------------------------

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

        # ----------------------------------------------
        # TECHNICAL SPECIFICATIONS
        # ----------------------------------------------

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

        # ----------------------------------------------
        # COMMERCIAL INFORMATION
        # ----------------------------------------------

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

        # ----------------------------------------------
        # WARRANTY / LOCATION
        # ----------------------------------------------

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

        # ----------------------------------------------
        # SAVE BUTTON
        # ----------------------------------------------

        submitted = st.form_submit_button(
            "💾 Save Product Changes",
            type="primary"
        )

        if submitted:

            updated_product = {

                "name": name,

                "category": category,

                "manufacturer": manufacturer,

                "model": model,

                "technology": technology,

                "rated_power_w": rated_power_w,

                "voltage_v": voltage_v,

                "current_a": current_a,

                "efficiency_percent":
                    efficiency_percent,

                "warranty_years":
                    warranty_years,

                "price": price,

                "currency": currency,

                "quantity": quantity,

                "notes": notes,

                "capacity_ah":
                    capacity_ah,

                "energy_kwh":
                    energy_kwh,

                "supplier": supplier,

                "country": country,
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
# DELETE PRODUCT SECTION
# ==========================================================

def display_delete_product(product):

    product_id = str(
        product.get("id", "")
    )

    product_name = product.get(
        "name",
        "Unnamed Product"
    )

    st.markdown("---")

    st.subheader(
        "🗑️ Delete Product"
    )

    st.warning(
        f"You are about to delete: "
        f"**{product_name}**"
    )

    confirmation = st.checkbox(
        "I understand that this action "
        "cannot be undone.",
        key=f"delete_confirm_{product_id}"
    )

    if st.button(
        "🗑️ Permanently Delete Product",
        key=f"delete_product_{product_id}",
        type="secondary"
    ):

        if not confirmation:

            st.warning(
                "Please confirm deletion first."
            )

        else:

            success = delete_existing_product(
                product_id
            )

            if success:

                st.success(
                    "Product deleted successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to delete product."
                )


# ==========================================================
# PRODUCT DETAILS
# ==========================================================

def display_product_details(product):

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
            product.get(
                "manufacturer",
                ""
            )
        )

        st.write(
            "**Model:**",
            product.get("model", "")
        )

        st.write(
            "**Technology:**",
            product.get(
                "technology",
                ""
            )
        )

        st.write(
            "**Supplier:**",
            product.get(
                "supplier",
                ""
            )
        )

    with col2:

        st.write(
            "**Rated Power:**",
            f"{product.get('rated_power_w', 0)} W"
        )

        st.write(
            "**Voltage:**",
            f"{product.get('voltage_v', 0)} V"
        )

        st.write(
            "**Current:**",
            f"{product.get('current_a', 0)} A"
        )

        st.write(
            "**Efficiency:**",
            f"{product.get('efficiency_percent', 0)} %"
        )

        st.write(
            "**Price:**",
            f"{product.get('currency', 'USD')} "
            f"{product.get('price', 0)}"
        )

        st.write(
            "**Quantity:**",
            product.get(
                "quantity",
                0
            )
        )

    if product.get("notes"):

        st.markdown(
            "### Notes"
        )

        st.info(
            product.get("notes")
        )

    with st.expander(
        "🔧 View Complete Record"
    ):

        st.json(product)


# ==========================================================
# MAIN PRODUCT MANAGEMENT INTERFACE
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

    # ----------------------------------------------
    # SUMMARY
    # ----------------------------------------------

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

    # ----------------------------------------------
    # LOAD PRODUCTS
    # ----------------------------------------------

    products = get_products()

    if not products:

        st.info(
            "No products found in the library."
        )

        st.caption(
            "Please add products through the "
            "Product Library interface first."
        )

        return

    # ----------------------------------------------
    # SEARCH / FILTER
    # ----------------------------------------------

    st.subheader(
        "🔎 Search Products"
    )

    col1, col2 = st.columns(2)

    with col1:

        search_query = st.text_input(
            "Search by name, manufacturer, "
            "model or technology",
            key="product_management_search"
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

            "Filter by Category",

            options=[
                "All Categories"
            ] + categories

        )

    # ----------------------------------------------
    # FILTER RESULTS
    # ----------------------------------------------

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

    # ----------------------------------------------
    # PRODUCT TABLE
    # ----------------------------------------------

    st.subheader(
        f"📦 Products Found: "
        f"{len(filtered_products)}"
    )

    table_data = []

    for product in filtered_products:

        table_data.append({

            "Name":
                product.get("name", ""),

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
                product.get(
                    "rated_power_w",
                    0
                ),

            "Price":
                product.get(
                    "price",
                    0
                ),

            "Currency":
                product.get(
                    "currency",
                    "USD"
                ),

            "Quantity":
                product.get(
                    "quantity",
                    0
                )

        })

    st.dataframe(
        pd.DataFrame(table_data),
        use_container_width=True,
        hide_index=True
    )

    # ----------------------------------------------
    # SELECT PRODUCT
    # ----------------------------------------------

    product_options = {

        f"{product.get('name', 'Unnamed')} "
        f"| {product.get('manufacturer', '')} "
        f"| {product.get('model', '')}":
        product.get("id")

        for product in filtered_products

    }

    selected_label = st.selectbox(

        "Select a product to inspect or manage",

        options=list(
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
            "Unable to retrieve selected product."
        )

        return

    st.divider()

    # ----------------------------------------------
    # PRODUCT ACTION TABS
    # ----------------------------------------------

    details_tab, edit_tab, delete_tab = st.tabs(

        [

            "📋 Product Details",

            "✏️ Edit Product",

            "🗑️ Delete Product"

        ]

    )

    with details_tab:

        display_product_details(
            selected_product
        )

    with edit_tab:

        display_edit_product_form(
            selected_product
        )

    with delete_tab:

        display_delete_product(
            selected_product
        )


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def display_management_ui():

    return display_product_management_ui()


def product_management_interface():

    return display_product_management_ui()
