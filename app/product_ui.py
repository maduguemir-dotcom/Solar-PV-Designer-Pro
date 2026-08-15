# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Product Library User Interface
# Version: 2.4.0
# ==========================================================
#
# Purpose:
# Standalone Streamlit interface for creating and managing
# a user's solar product library.
#
# This module does NOT modify main.py.
# ==========================================================

import streamlit as st

from product_engine import (
    PRODUCT_CATEGORIES,
    PRODUCT_TECHNOLOGIES,
    get_default_products,
    create_product,
    search_products,
    filter_products_by_category,
    filter_products_by_technology,
    compare_products,
)


# ==========================================================
# SECTION 1 - SESSION STATE
# ==========================================================

def initialize_product_library():
    """
    Initialize the product library in Streamlit session state.
    """

    if "product_library" not in st.session_state:

        st.session_state.product_library = (
            get_default_products()
        )


# ==========================================================
# SECTION 2 - ADD PRODUCT
# ==========================================================

def add_product_form():

    st.subheader("➕ Add Product to Library")

    with st.form(
        "add_product_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Product Name",
                placeholder="e.g. 550W Solar Panel"
            )

            category = st.selectbox(
                "Category",
                PRODUCT_CATEGORIES
            )

            manufacturer = st.text_input(
                "Manufacturer"
            )

            model = st.text_input(
                "Model"
            )

            technology = st.selectbox(
                "Technology",
                PRODUCT_TECHNOLOGIES
            )

            supplier = st.text_input(
                "Supplier"
            )

            country = st.text_input(
                "Country"
            )

        with col2:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=0.0,
                step=10.0
            )

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

            capacity_ah = st.number_input(
                "Battery Capacity (Ah)",
                min_value=0.0,
                value=0.0,
                step=10.0
            )

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=0.0,
                step=0.1
            )

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0
            )

            warranty_years = st.number_input(
                "Warranty (years)",
                min_value=0.0,
                value=0.0,
                step=1.0
            )

        notes = st.text_area(
            "Notes",
            placeholder=(
                "Additional technical information, "
                "supplier notes, installation notes, etc."
            )
        )

        submitted = st.form_submit_button(
            "💾 Save Product",
            use_container_width=True
        )

    if submitted:

        result = create_product(

            name=name,

            category=category,

            manufacturer=manufacturer,

            model=model,

            technology=technology,

            rated_power_w=rated_power_w,

            voltage_v=voltage_v,

            capacity_ah=capacity_ah,

            energy_kwh=energy_kwh,

            efficiency_percent=efficiency_percent,

            warranty_years=warranty_years,

            supplier=supplier,

            country=country,

            notes=notes,

        )

        if result["success"]:

            st.session_state.product_library.append(
                result["product"]
            )

            st.success(
                f"✅ {name} added to the product library."
            )

        else:

            st.error(
                result["message"]
            )


# ==========================================================
# SECTION 3 - SEARCH AND FILTER
# ==========================================================

def product_search_interface():

    st.subheader("🔎 Search & Filter Product Library")

    col1, col2, col3 = st.columns(3)

    with col1:

        search_query = st.text_input(
            "Search",
            placeholder=(
                "Name, manufacturer, model, supplier..."
            )
        )

    with col2:

        category_filter = st.selectbox(
            "Category Filter",
            ["All"] + PRODUCT_CATEGORIES
        )

    with col3:

        technology_filter = st.selectbox(
            "Technology Filter",
            ["All"] + PRODUCT_TECHNOLOGIES
        )

    products = (
        st.session_state.product_library
    )

    if search_query:

        products = search_products(
            products,
            search_query
        )

    if category_filter != "All":

        products = filter_products_by_category(
            products,
            category_filter
        )

    if technology_filter != "All":

        products = filter_products_by_technology(
            products,
            technology_filter
        )

    return products


# ==========================================================
# SECTION 4 - DISPLAY PRODUCTS
# ==========================================================

def display_product_library(
    products
):

    st.subheader("📚 Product Library")

    if not products:

        st.info(
            "No products found."
        )

        return

    display_data = []

    for index, product in enumerate(
        products
    ):

        display_data.append({

            "ID":
                index,

            "Product":
                product.get(
                    "name",
                    "N/A"
                ),

            "Category":
                product.get(
                    "category",
                    "N/A"
                ),

            "Manufacturer":
                product.get(
                    "manufacturer",
                    "N/A"
                ),

            "Model":
                product.get(
                    "model",
                    "N/A"
                ),

            "Technology":
                product.get(
                    "technology",
                    "N/A"
                ),

            "Power (W)":
                product.get(
                    "rated_power_w",
                    0
                ),

            "Voltage (V)":
                product.get(
                    "voltage_v",
                    0
                ),

            "Capacity (Ah)":
                product.get(
                    "capacity_ah",
                    0
                ),

            "Energy (kWh)":
                product.get(
                    "energy_kwh",
                    0
                ),

            "Efficiency (%)":
                product.get(
                    "efficiency_percent",
                    0
                ),

            "Warranty (years)":
                product.get(
                    "warranty_years",
                    0
                ),

        })

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# SECTION 5 - PRODUCT DETAILS
# ==========================================================

def product_details(products):

    st.subheader("🔍 Product Details")

    if not products:

        st.info(
            "No products available."
        )

        return

    names = [
        product.get(
            "name",
            "Unnamed Product"
        )
        for product in products
    ]

    selected_name = st.selectbox(
        "Select Product",
        names
    )

    selected_product = next(

        (
            product
            for product in products

            if product.get(
                "name"
            )
            == selected_name
        ),

        None

    )

    if selected_product:

        st.json(
            selected_product
        )


# ==========================================================
# SECTION 6 - PRODUCT COMPARISON
# ==========================================================

def product_comparison(products):

    st.subheader("⚖️ Compare Products")

    if len(products) < 2:

        st.info(
            "At least two products are required "
            "for comparison."
        )

        return

    names = [

        product.get(
            "name",
            "Unnamed Product"
        )

        for product in products

    ]

    selected_names = st.multiselect(

        "Select products to compare",

        names,

        default=names[:2]

    )

    if len(selected_names) < 2:

        st.info(
            "Select at least two products."
        )

        return

    selected_products = [

        product

        for product in products

        if product.get(
            "name"
        )
        in selected_names

    ]

    comparison = compare_products(
        selected_products
    )

    st.dataframe(
        comparison,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# SECTION 7 - DELETE PRODUCT
# ==========================================================

def delete_product_interface():

    st.subheader("🗑️ Remove Product")

    products = (
        st.session_state.product_library
    )

    if not products:

        st.info(
            "The product library is empty."
        )

        return

    product_names = [

        product.get(
            "name",
            "Unnamed Product"
        )

        for product in products

    ]

    selected_name = st.selectbox(

        "Select product to remove",

        product_names,

        key="delete_product_selector"

    )

    if st.button(
        "🗑️ Remove Selected Product",
        use_container_width=True
    ):

        for index, product in enumerate(
            products
        ):

            if product.get(
                "name"
            ) == selected_name:

                products.pop(
                    index
                )

                st.success(
                    f"Removed: {selected_name}"
                )

                st.rerun()


# ==========================================================
# SECTION 8 - RESET LIBRARY
# ==========================================================

def reset_product_library():

    st.subheader("♻️ Library Management")

    if st.button(
        "Reset to Example Products",
        use_container_width=True
    ):

        st.session_state.product_library = (
            get_default_products()
        )

        st.success(
            "Product library reset successfully."
        )

        st.rerun()


# ==========================================================
# SECTION 9 - MAIN PRODUCT UI
# ==========================================================

def display_product_library_ui():

    initialize_product_library()

    st.header(
        "📚 Solar Product Library"
    )

    st.caption(
        "Create, manage, search and compare "
        "your own solar equipment database."
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([

        "➕ Add Product",

        "📚 Library",

        "🔍 Details",

        "⚖️ Compare",

        "⚙️ Manage",

    ])

    with tab1:

        add_product_form()

    with tab2:

        filtered_products = (
            product_search_interface()
        )

        display_product_library(
            filtered_products
        )

    with tab3:

        filtered_products = (
            product_search_interface()
        )

        product_details(
            filtered_products
        )

    with tab4:

        filtered_products = (
            product_search_interface()
        )

        product_comparison(
            filtered_products
        )

    with tab5:

        delete_product_interface()

        st.divider()

        reset_product_library()


# ==========================================================
# STANDALONE EXECUTION
# ==========================================================

if __name__ == "__main__":

    display_product_library_ui()
