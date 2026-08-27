"""
Solar PV Designer Pro Africa™
Product Library Management UI

This module provides a dedicated management dashboard for
products stored in the Solar PV Product Library.

IMPORTANT:
This module uses the same working product_ui.py interface and,
therefore, the same SQLite-backed Product Library.

Features:
- Product summary
- Category statistics
- Search and filter
- Product inspection
- Edit existing products
- Delete products
- Refresh product library
"""

import streamlit as st

from product_ui import (
    get_products,
    get_product,
    update_product,
    delete_product,
)


# ============================================================
# CONSTANTS
# ============================================================

PRODUCT_CATEGORIES = [
    "All",
    "Solar Panel",
    "Battery",
    "Inverter",
    "Charge Controller",
    "Mounting Structure",
    "Solar Cable",
    "Protection",
    "Other",
]


CURRENCIES = [
    "USD",
    "UGX",
    "NGN",
    "KES",
    "EUR",
    "GBP",
    "Other",
]


TECHNOLOGIES = [
    "Monocrystalline",
    "Polycrystalline",
    "Thin Film",
    "Lithium",
    "LiFePO4",
    "Lead Acid",
    "AGM",
    "Gel",
    "Hybrid",
    "Off Grid",
    "On Grid",
    "MPPT",
    "PWM",
    "Other",
]


# ============================================================
# SAFE HELPERS
# ============================================================

def safe_text(value, default=""):
    """
    Safely convert a value to text.
    """

    if value is None:
        return default

    return str(value)


def safe_float(value, default=0.0):
    """
    Safely convert a value to float.
    """

    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    """
    Safely convert a value to integer.
    """

    try:
        return int(value)
    except (TypeError, ValueError):
        return default


# ============================================================
# LOAD PRODUCTS
# ============================================================

def load_products():
    """
    Load all products from the working Product Library.

    The data source is product_ui.py, which is already connected
    to the SQLite product library.
    """

    try:
        products = get_products()

        if products is None:
            return []

        return list(products)

    except Exception as error:

        st.error(
            f"Unable to load Product Library: {error}"
        )

        return []


# ============================================================
# GET PRODUCTS
# ============================================================

def get_products_for_management():
    """
    Backward-compatible management product loader.
    """

    return load_products()


# ============================================================
# CATEGORY STATISTICS
# ============================================================

def calculate_category_statistics(products):
    """
    Calculate the number of products in each category.
    """

    statistics = {}

    for product in products:

        category = product.get(
            "category",
            "Other",
        )

        if not category:
            category = "Other"

        statistics[category] = (
            statistics.get(
                category,
                0,
            )
            + 1
        )

    return statistics


# ============================================================
# SEARCH PRODUCTS
# ============================================================

def search_and_filter_products(
    products,
    search_query="",
    category="All",
):
    """
    Search and filter products.
    """

    filtered_products = list(products)

    # --------------------------------------------------------
    # CATEGORY FILTER
    # --------------------------------------------------------

    if (
        category
        and category != "All"
    ):

        filtered_products = [

            product

            for product in filtered_products

            if product.get(
                "category"
            ) == category

        ]

    # --------------------------------------------------------
    # SEARCH FILTER
    # --------------------------------------------------------

    if search_query:

        query = search_query.lower().strip()

        filtered_products = [

            product

            for product in filtered_products

            if query
            in " ".join(
                [
                    safe_text(
                        product.get(
                            "id",
                            ""
                        )
                    ),
                    safe_text(
                        product.get(
                            "name",
                            ""
                        )
                    ),
                    safe_text(
                        product.get(
                            "manufacturer",
                            ""
                        )
                    ),
                    safe_text(
                        product.get(
                            "model",
                            ""
                        )
                    ),
                    safe_text(
                        product.get(
                            "technology",
                            ""
                        )
                    ),
                    safe_text(
                        product.get(
                            "supplier",
                            ""
                        )
                    ),
                ]
            ).lower()

        ]

    return filtered_products


# ============================================================
# PRODUCT SUMMARY
# ============================================================

def display_product_summary(products):
    """
    Display management dashboard summary.
    """

    total_products = len(products)

    category_statistics = (
        calculate_category_statistics(
            products
        )
    )

    total_categories = len(
        category_statistics
    )

    total_quantity = sum(

        safe_int(
            product.get(
                "quantity",
                1,
            ),
            1,
        )

        for product in products

    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Products",
            total_products,
        )

    with col2:

        st.metric(
            "Categories Used",
            total_categories,
        )

    with col3:

        st.metric(
            "Total Quantity",
            total_quantity,
        )


# ============================================================
# CATEGORY OVERVIEW
# ============================================================

def display_category_overview(products):
    """
    Display products grouped by category.
    """

    statistics = (
        calculate_category_statistics(
            products
        )
    )

    if not statistics:
        return

    st.subheader(
        "📂 Products by Category"
    )

    category_data = []

    for category, count in statistics.items():

        category_data.append(
            {
                "Category": category,
                "Products": count,
            }
        )

    st.dataframe(
        category_data,
        use_container_width=True,
        hide_index=True,
    )


# ============================================================
# PRODUCT DETAILS
# ============================================================

def display_product_details(product):
    """
    Display detailed information about one product.
    """

    st.subheader(
        "📋 Product Details"
    )

    basic_fields = [

        ("ID", "id"),
        ("Name", "name"),
        ("Category", "category"),
        ("Manufacturer", "manufacturer"),
        ("Model", "model"),
        ("Technology", "technology"),
        ("Supplier", "supplier"),
        ("Country", "country"),

    ]

    st.markdown(
        "### Basic Information"
    )

    col1, col2 = st.columns(2)

    for index, (
        label,
        field,
    ) in enumerate(basic_fields):

        value = product.get(
            field,
            "",
        )

        if value in (
            "",
            None,
        ):
            value = "-"

        if index % 2 == 0:

            with col1:

                st.write(
                    f"**{label}:** {value}"
                )

        else:

            with col2:

                st.write(
                    f"**{label}:** {value}"
                )

    st.divider()

    st.markdown(
        "### Technical Specifications"
    )

    excluded_fields = [

        "id",
        "name",
        "category",
        "manufacturer",
        "model",
        "technology",
        "supplier",
        "country",
        "notes",

    ]

    technical_data = []

    for key, value in product.items():

        if key in excluded_fields:
            continue

        if value in (
            "",
            None,
        ):
            continue

        label = (
            key
            .replace("_", " ")
            .title()
        )

        technical_data.append(
            {
                "Specification": label,
                "Value": value,
            }
        )

    if technical_data:

        st.dataframe(
            technical_data,
            use_container_width=True,
            hide_index=True,
        )

    notes = product.get(
        "notes",
        "",
    )

    if notes:

        st.divider()

        st.markdown(
            "### Notes"
        )

        st.write(notes)


# ============================================================
# EDIT EXISTING PRODUCT
# ============================================================

def update_existing_product(product):
    """
    Display an editing interface for an existing product.
    """

    product_id = product.get("id")

    if not product_id:

        st.error(
            "This product does not have a valid ID."
        )

        return

    st.subheader(
        "✏️ Edit Product"
    )

    with st.form(
        f"management_edit_form_{product_id}"
    ):

        col1, col2 = st.columns(2)

        # ----------------------------------------------------
        # COLUMN 1
        # ----------------------------------------------------

        with col1:

            name = st.text_input(
                "Product Name",
                value=safe_text(
                    product.get(
                        "name",
                        ""
                    )
                ),
                key=f"mgmt_name_{product_id}",
            )

            category_value = (
                product.get(
                    "category",
                    "Other",
                )
            )

            categories_without_all = [
                item
                for item in PRODUCT_CATEGORIES
                if item != "All"
            ]

            if (
                category_value
                not in categories_without_all
            ):

                category_value = "Other"

            category = st.selectbox(
                "Category",
                categories_without_all,
                index=categories_without_all.index(
                    category_value
                ),
                key=f"mgmt_category_{product_id}",
            )

            manufacturer = st.text_input(
                "Manufacturer",
                value=safe_text(
                    product.get(
                        "manufacturer",
                        ""
                    )
                ),
                key=f"mgmt_manufacturer_{product_id}",
            )

            model = st.text_input(
                "Model",
                value=safe_text(
                    product.get(
                        "model",
                        ""
                    )
                ),
                key=f"mgmt_model_{product_id}",
            )

            technology_value = (
                product.get(
                    "technology",
                    "Other",
                )
            )

            if (
                technology_value
                not in TECHNOLOGIES
            ):

                technology_value = "Other"

            technology = st.selectbox(
                "Technology",
                TECHNOLOGIES,
                index=TECHNOLOGIES.index(
                    technology_value
                ),
                key=f"mgmt_technology_{product_id}",
            )

        # ----------------------------------------------------
        # COLUMN 2
        # ----------------------------------------------------

        with col2:

            supplier = st.text_input(
                "Supplier",
                value=safe_text(
                    product.get(
                        "supplier",
                        ""
                    )
                ),
                key=f"mgmt_supplier_{product_id}",
            )

            country = st.text_input(
                "Country",
                value=safe_text(
                    product.get(
                        "country",
                        ""
                    )
                ),
                key=f"mgmt_country_{product_id}",
            )

            warranty_years = st.number_input(
                "Warranty Years",
                min_value=0,
                value=safe_int(
                    product.get(
                        "warranty_years",
                        0,
                    )
                ),
                key=f"mgmt_warranty_{product_id}",
            )

            price = st.number_input(
                "Unit Price",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "price",
                        0,
                    )
                ),
                key=f"mgmt_price_{product_id}",
            )

            currency_value = (
                product.get(
                    "currency",
                    "USD",
                )
            )

            if (
                currency_value
                not in CURRENCIES
            ):

                currency_value = "USD"

            currency = st.selectbox(
                "Currency",
                CURRENCIES,
                index=CURRENCIES.index(
                    currency_value
                ),
                key=f"mgmt_currency_{product_id}",
            )

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=max(
                    1,
                    safe_int(
                        product.get(
                            "quantity",
                            1,
                        ),
                        1,
                    ),
                ),
                key=f"mgmt_quantity_{product_id}",
            )

        st.divider()

        st.markdown(
            "### Main Technical Values"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "rated_power_w",
                        0,
                    )
                ),
                key=f"mgmt_power_{product_id}",
            )

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"mgmt_voltage_{product_id}",
            )

        with col2:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "current_a",
                        0,
                    )
                ),
                key=f"mgmt_current_{product_id}",
            )

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "capacity_ah",
                        0,
                    )
                ),
                key=f"mgmt_capacity_{product_id}",
            )

        with col3:

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "energy_kwh",
                        0,
                    )
                ),
                key=f"mgmt_energy_{product_id}",
            )

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    product.get(
                        "efficiency_percent",
                        0,
                    )
                ),
                key=f"mgmt_efficiency_{product_id}",
            )

        notes = st.text_area(
            "Notes",
            value=safe_text(
                product.get(
                    "notes",
                    ""
                )
            ),
            key=f"mgmt_notes_{product_id}",
        )

        submitted = st.form_submit_button(
            "💾 Save Changes"
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Product Name cannot be empty."
                )

                return

            updated_data = dict(product)

            updated_data.update({

                "id": product_id,

                "name": name,

                "category": category,

                "manufacturer": manufacturer,

                "model": model,

                "technology": technology,

                "supplier": supplier,

                "country": country,

                "warranty_years": warranty_years,

                "price": price,

                "currency": currency,

                "quantity": quantity,

                "rated_power_w": rated_power_w,

                "voltage_v": voltage_v,

                "current_a": current_a,

                "capacity_ah": capacity_ah,

                "energy_kwh": energy_kwh,

                "efficiency_percent": efficiency_percent,

                "notes": notes,

            })

            try:

                success = update_product(
                    product_id,
                    updated_data,
                )

                if success:

                    st.success(
                        "Product updated successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        "Unable to update product."
                    )

            except Exception as error:

                st.error(
                    f"Update failed: {error}"
                )


# ============================================================
# DELETE PRODUCT
# ============================================================

def delete_existing_product(product):
    """
    Display a safe delete interface.
    """

    product_id = product.get("id")

    if not product_id:

        st.error(
            "This product does not have a valid ID."
        )

        return

    st.subheader(
        "🗑️ Delete Product"
    )

    st.warning(
        "This action will permanently remove "
        "the selected product from the Product Library."
    )

    st.write(
        f"**Product:** "
        f"{product.get('name', '')}"
    )

    st.write(
        f"**Category:** "
        f"{product.get('category', '')}"
    )

    confirmation = st.checkbox(
        "I understand that this product "
        "will be permanently deleted.",
        key=f"mgmt_delete_confirm_{product_id}",
    )

    if confirmation:

        if st.button(
            "🗑️ Permanently Delete Product",
            key=f"mgmt_delete_button_{product_id}",
        ):

            try:

                success = delete_product(
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

            except Exception as error:

                st.error(
                    f"Delete failed: {error}"
                )


# ============================================================
# PRODUCT MANAGEMENT INTERFACE
# ============================================================

def product_management_interface():
    """
    Main Product Management interface.
    """

    st.title(
        "🛠️ Product Library Management"
    )

    st.caption(
        "Inspect, search, edit and safely delete "
        "products from your Solar PV Product Library."
    )

    products = load_products()

    # --------------------------------------------------------
    # SUMMARY
    # --------------------------------------------------------

    display_product_summary(products)

    st.divider()

    # --------------------------------------------------------
    # NO PRODUCTS
    # --------------------------------------------------------

    if not products:

        st.info(
            "No products found in the library."
        )

        st.write(
            "Please add products through the "
            "Product Library interface first."
        )

        return

    # --------------------------------------------------------
    # CATEGORY OVERVIEW
    # --------------------------------------------------------

    display_category_overview(
        products
    )

    st.divider()

    # --------------------------------------------------------
    # SEARCH AND FILTER
    # --------------------------------------------------------

    st.subheader(
        "🔍 Search and Filter Products"
    )

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        search_query = st.text_input(
            "Search Product",
            placeholder=(
                "Search by product name, "
                "manufacturer or model..."
            ),
            key="management_search_product",
        )

    with col2:

        category_filter = st.selectbox(
            "Filter by Category",
            PRODUCT_CATEGORIES,
            key="management_category_filter",
        )

    filtered_products = (
        search_and_filter_products(
            products,
            search_query,
            category_filter,
        )
    )

    st.write(
        f"Products found: **{len(filtered_products)}**"
    )

    if not filtered_products:

        st.info(
            "No products match your search criteria."
        )

        return

    st.divider()

    # --------------------------------------------------------
    # SELECT PRODUCT
    # --------------------------------------------------------

    product_options = {}

    for product in filtered_products:

        label = (

            f"{product.get('name', 'Unnamed Product')} "

            f"| {product.get('category', 'Other')} "

            f"| {product.get('manufacturer', '')}"

        )

        product_options[label] = (
            product.get("id")
        )

    selected_label = st.selectbox(
        "Select Product to Manage",
        list(product_options.keys()),
        key="management_selected_product",
    )

    selected_product_id = (
        product_options[selected_label]
    )

    selected_product = get_product(
        selected_product_id
    )

    if selected_product is None:

        st.error(
            "The selected product could not be loaded."
        )

        return

    st.divider()

    # --------------------------------------------------------
    # MANAGEMENT TABS
    # --------------------------------------------------------

    tab1, tab2, tab3 = st.tabs(
        [
            "📋 Inspect",
            "✏️ Edit",
            "🗑️ Delete",
        ]
    )

    with tab1:

        display_product_details(
            selected_product
        )

    with tab2:

        update_existing_product(
            selected_product
        )

    with tab3:

        delete_existing_product(
            selected_product
        )


# ============================================================
# MAIN DISPLAY FUNCTION
# ============================================================

def display_product_management_ui():
    """
    Main public function used by Streamlit tests
    and the main application.
    """

    product_management_interface()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def display_management_ui():
    """
    Backward-compatible alias.
    """

    product_management_interface()


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    display_product_management_ui()
