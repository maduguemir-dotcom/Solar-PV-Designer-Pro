# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Persistent Product Library UI
# Version: 2.4.3
# ==========================================================

import streamlit as st

from product_engine import (
    PRODUCT_CATEGORIES,
    PRODUCT_TECHNOLOGIES,
    create_product,
    search_products,
    filter_products_by_category,
    filter_products_by_technology,
    compare_products,
)

from database import (
    initialize_database,
    add_product,
    get_products,
    get_product,
    delete_product,
    search_products as database_search_products,
    backup_database,
)


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_product_database():

    initialize_database()

    if "product_library" not in st.session_state:

        st.session_state.product_library = (
            get_products()
        )


# ==========================================================
# REFRESH
# ==========================================================

def refresh_product_library():

    st.session_state.product_library = (
        get_products()
    )


# ==========================================================
# ADD PRODUCT
# ==========================================================

def add_product_form():

    st.subheader(
        "➕ Add Product to Library"
    )

    with st.form(
        "sqlite_product_add_form",
        clear_on_submit=True
    ):

        col1, col2 = st.columns(2)

        with col1:

            name = st.text_input(
                "Product Name",
                placeholder="e.g. 550W Solar Panel",
                key="sqlite_product_name"
            )

            category = st.selectbox(
                "Category",
                PRODUCT_CATEGORIES,
                key="sqlite_product_category"
            )

            manufacturer = st.text_input(
                "Manufacturer",
                key="sqlite_product_manufacturer"
            )

            model = st.text_input(
                "Model",
                key="sqlite_product_model"
            )

            technology = st.selectbox(
                "Technology",
                PRODUCT_TECHNOLOGIES,
                key="sqlite_product_technology"
            )

            supplier = st.text_input(
                "Supplier",
                key="sqlite_product_supplier"
            )

            country = st.text_input(
                "Country",
                key="sqlite_product_country"
            )

        with col2:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                key="sqlite_product_power"
            )

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="sqlite_product_voltage"
            )

            capacity_ah = st.number_input(
                "Battery Capacity (Ah)",
                min_value=0.0,
                value=0.0,
                step=10.0,
                key="sqlite_product_capacity"
            )

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=0.0,
                step=0.1,
                key="sqlite_product_energy"
            )

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                step=1.0,
                key="sqlite_product_efficiency"
            )

            warranty_years = st.number_input(
                "Warranty (years)",
                min_value=0.0,
                value=0.0,
                step=1.0,
                key="sqlite_product_warranty"
            )

        notes = st.text_area(
            "Notes",
            placeholder=(
                "Technical information, supplier notes, "
                "installation notes, etc."
            ),
            key="sqlite_product_notes"
        )

        submitted = st.form_submit_button(
            "💾 Save Product",
            use_container_width=True
        )

    if not submitted:

        return

    if not name.strip():

        st.error(
            "Product name is required."
        )

        return

    product = {

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

        "capacity_ah":
            capacity_ah,

        "energy_kwh":
            energy_kwh,

        "efficiency_percent":
            efficiency_percent,

        "warranty_years":
            warranty_years,

        "supplier":
            supplier,

        "country":
            country,

        "notes":
            notes,

    }

    # Validate through product engine first

    validation = create_product(
        **product
    )

    if not validation["success"]:

        st.error(
            validation["message"]
        )

        return

    # Save directly to SQLite

    try:

        product_id = add_product(
            product
        )

        refresh_product_library()

        st.success(
            f"✅ Product saved successfully "
            f"(Database ID: {product_id})."
        )

    except Exception as error:

        st.error(
            f"Unable to save product: {error}"
        )


# ==========================================================
# SEARCH AND FILTER
# ==========================================================

def product_search_interface(
    key_prefix="default"
):

    st.subheader(
        "🔎 Search & Filter Product Library"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        search_query = st.text_input(
            "Search",
            placeholder=(
                "Name, manufacturer, model, supplier..."
            ),
            key=f"{key_prefix}_sqlite_search"
        )

    with col2:

        category_filter = st.selectbox(
            "Category Filter",
            ["All"] + PRODUCT_CATEGORIES,
            key=f"{key_prefix}_sqlite_category"
        )

    with col3:

        technology_filter = st.selectbox(
            "Technology Filter",
            ["All"] + PRODUCT_TECHNOLOGIES,
            key=f"{key_prefix}_sqlite_technology"
        )

    products = list(
        st.session_state.product_library
    )

    # Database search

    if search_query:

        products = database_search_products(
            search_query
        )

    # Engine filters

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
# DISPLAY LIBRARY
# ==========================================================

def display_product_library(
    products
):

    st.subheader(
        "📚 Product Library"
    )

    if not products:

        st.info(
            "No products found."
        )

        return

    display_data = []

    for product in products:

        display_data.append({

            "ID":
                product.get(
                    "id",
                    ""
                ),

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

            "Supplier":
                product.get(
                    "supplier",
                    ""
                ),

            "Country":
                product.get(
                    "country",
                    ""
                ),

        })

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# PRODUCT DETAILS
# ==========================================================

def product_details(
    products,
    key_prefix="details"
):

    st.subheader(
        "🔍 Product Details"
    )

    if not products:

        st.info(
            "No products available."
        )

        return

    labels = []

    product_map = {}

    for product in products:

        product_id = product.get(
            "id"
        )

        name = product.get(
            "name",
            "Unnamed Product"
        )

        label = (
            f"{name} "
            f"(ID: {product_id})"
        )

        labels.append(
            label
        )

        product_map[label] = product

    selected_label = st.selectbox(
        "Select Product",
        labels,
        key=f"{key_prefix}_sqlite_product"
    )

    selected_product = product_map.get(
        selected_label
    )

    if selected_product:

        st.json(
            selected_product
        )


# ==========================================================
# PRODUCT COMPARISON
# ==========================================================

def product_comparison(
    products,
    key_prefix="comparison"
):

    st.subheader(
        "⚖️ Compare Products"
    )

    if len(products) < 2:

        st.info(
            "At least two products are required "
            "for comparison."
        )

        return

    labels = []

    product_map = {}

    for product in products:

        product_id = product.get(
            "id"
        )

        name = product.get(
            "name",
            "Unnamed Product"
        )

        label = (
            f"{name} "
            f"(ID: {product_id})"
        )

        labels.append(
            label
        )

        product_map[label] = product

    selected_labels = st.multiselect(

        "Select products to compare",

        labels,

        default=labels[:2],

        key=f"{key_prefix}_sqlite_products"

    )

    if len(selected_labels) < 2:

        st.info(
            "Select at least two products."
        )

        return

    selected_products = [

        product_map[label]

        for label in selected_labels

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
# DELETE PRODUCT
# ==========================================================

def delete_product_interface():

    st.subheader(
        "🗑️ Remove Product"
    )

    products = (
        st.session_state.product_library
    )

    if not products:

        st.info(
            "The product library is empty."
        )

        return

    labels = []

    product_map = {}

    for product in products:

        product_id = product.get(
            "id"
        )

        name = product.get(
            "name",
            "Unnamed Product"
        )

        label = (
            f"{name} "
            f"(ID: {product_id})"
        )

        labels.append(
            label
        )

        product_map[label] = product

    selected_label = st.selectbox(

        "Select product to remove",

        labels,

        key="sqlite_delete_product_selector"

    )

    selected_product = product_map.get(
        selected_label
    )

    if not selected_product:

        return

    product_id = selected_product.get(
        "id"
    )

    if st.button(

        "🗑️ Remove Selected Product",

        use_container_width=True,

        key="sqlite_delete_product_button"

    ):

        try:

            deleted = delete_product(
                product_id
            )

            if deleted:

                refresh_product_library()

                st.success(
                    "Product removed successfully."
                )

                st.rerun()

            else:

                st.error(
                    "Product could not be removed."
                )

        except Exception as error:

            st.error(
                f"Delete operation failed: {error}"
            )


# ==========================================================
# DATABASE MANAGEMENT
# ==========================================================

def database_management():

    st.subheader(
        "⚙️ Database Management"
    )

    col1, col2 = st.columns(2)

    with col1:

        if st.button(

            "🔄 Refresh Database",

            use_container_width=True,

            key="sqlite_refresh_button"

        ):

            refresh_product_library()

            st.success(
                "Product database refreshed."
            )

            st.rerun()

    with col2:

        if st.button(

            "📦 Backup Database",

            use_container_width=True,

            key="sqlite_backup_button"

        ):

            result = backup_database()

            if result["success"]:

                st.success(
                    "SQLite database backed up successfully."
                )

                st.code(
                    result["file"]
                )

            else:

                st.error(
                    result.get(
                        "message",
                        "Backup failed."
                    )
                )


# ==========================================================
# MAIN PRODUCT UI
# ==========================================================

def display_product_library_ui():

    initialize_product_database()

    st.header(
        "📚 Solar Product Library"
    )

    st.caption(
        "Persistent solar equipment database "
        "for Solar PV Designer Pro Africa™"
    )

    st.success(
        "Products are stored in the SQLite database "
        "and persist between application sessions."
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs([

        "➕ Add Product",

        "📚 Library",

        "🔍 Details",

        "⚖️ Compare",

        "⚙️ Manage",

    ])

    # ------------------------------------------------------
    # ADD
    # ------------------------------------------------------

    with tab1:

        add_product_form()

    # ------------------------------------------------------
    # LIBRARY
    # ------------------------------------------------------

    with tab2:

        products = product_search_interface(
            key_prefix="library"
        )

        display_product_library(
            products
        )

    # ------------------------------------------------------
    # DETAILS
    # ------------------------------------------------------

    with tab3:

        products = product_search_interface(
            key_prefix="details"
        )

        product_details(
            products,
            key_prefix="details"
        )

    # ------------------------------------------------------
    # COMPARE
    # ------------------------------------------------------

    with tab4:

        products = product_search_interface(
            key_prefix="comparison"
        )

        product_comparison(
            products,
            key_prefix="comparison"
        )

    # ------------------------------------------------------
    # MANAGE
    # ------------------------------------------------------

    with tab5:

        delete_product_interface()

        st.divider()

        database_management()


# ==========================================================
# STANDALONE EXECUTION
# ==========================================================

if __name__ == "__main__":

    st.set_page_config(

        page_title=
            "Solar Product Library",

        page_icon=
            "📚",

        layout=
            "wide"

    )

    display_product_library_ui()
