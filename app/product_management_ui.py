# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT LIBRARY MANAGEMENT UI
#
# Features:
# - View products
# - Search products
# - Filter by category
# - Edit products
# - Update products
# - Delete products
#
# Uses the centralized SQLite product library.
# ==========================================================

import streamlit as st

from library_store import (
    initialize_database,
    load_product_library,
    get_product_from_library,
    update_product_in_library,
    remove_product_from_library,
    search_product_library,
    get_product_library_summary,
    safe_float,
    safe_int,
)


# ==========================================================
# INITIALIZE DATABASE
# ==========================================================

initialize_database()


# ==========================================================
# PRODUCT CATEGORIES
# ==========================================================

PRODUCT_CATEGORIES = [
    "Solar Panel",
    "Battery",
    "Inverter",
    "Charge Controller",
    "Solar Pump",
    "Mounting Structure",
    "Cable",
    "Circuit Breaker",
    "Fuse",
    "Combiner Box",
    "Generator",
    "Other",
]


# ==========================================================
# HELPER FUNCTIONS
# ==========================================================

def get_products():

    return load_product_library()


def normalize_product(product):

    if product is None:
        product = {}

    product = dict(product)

    product.setdefault("id", "")
    product.setdefault("name", "")
    product.setdefault("category", "Other")
    product.setdefault("manufacturer", "")
    product.setdefault("model", "")
    product.setdefault("technology", "")

    product["rated_power_w"] = safe_float(
        product.get("rated_power_w", 0)
    )

    product["voltage_v"] = safe_float(
        product.get("voltage_v", 0)
    )

    product["current_a"] = safe_float(
        product.get("current_a", 0)
    )

    product["efficiency_percent"] = safe_float(
        product.get("efficiency_percent", 0)
    )

    product["warranty_years"] = safe_float(
        product.get("warranty_years", 0)
    )

    product["price"] = safe_float(
        product.get("price", 0)
    )

    product["quantity"] = safe_int(
        product.get("quantity", 1),
        1
    )

    product["capacity_ah"] = safe_float(
        product.get("capacity_ah", 0)
    )

    product["energy_kwh"] = safe_float(
        product.get("energy_kwh", 0)
    )

    product.setdefault("currency", "USD")
    product.setdefault("supplier", "")
    product.setdefault("country", "")
    product.setdefault("notes", "")

    if not isinstance(
        product.get("specifications"),
        dict
    ):
        product["specifications"] = {}

    return product


# ==========================================================
# UPDATE EXISTING PRODUCT
# ==========================================================

def update_existing_product(
    product_id,
    product
):

    product = normalize_product(product)

    return update_product_in_library(
        product_id,
        product
    )


# ==========================================================
# DELETE EXISTING PRODUCT
# ==========================================================

def delete_existing_product(
    product_id
):

    return remove_product_from_library(
        product_id
    )


# ==========================================================
# PRODUCT EDIT FORM
# ==========================================================

def edit_product_form(product):

    product = normalize_product(product)

    product_id = product.get("id")

    st.subheader(
        f"✏️ Edit Product: {product.get('name', '')}"
    )

    st.caption(
        f"Product ID: {product_id}"
    )

    # ------------------------------------------------------
    # BASIC INFORMATION
    # ------------------------------------------------------

    st.markdown(
        "### Basic Product Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name *",
            value=product.get("name", ""),
            key=f"edit_name_{product_id}"
        )

        manufacturer = st.text_input(
            "Manufacturer",
            value=product.get(
                "manufacturer",
                ""
            ),
            key=f"edit_manufacturer_{product_id}"
        )

        model = st.text_input(
            "Model / Product Code",
            value=product.get(
                "model",
                ""
            ),
            key=f"edit_model_{product_id}"
        )

    with col2:

        current_category = product.get(
            "category",
            "Other"
        )

        if current_category not in PRODUCT_CATEGORIES:
            current_category = "Other"

        category_index = PRODUCT_CATEGORIES.index(
            current_category
        )

        category = st.selectbox(
            "Product Category",
            PRODUCT_CATEGORIES,
            index=category_index,
            key=f"edit_category_{product_id}"
        )

        supplier = st.text_input(
            "Supplier",
            value=product.get(
                "supplier",
                ""
            ),
            key=f"edit_supplier_{product_id}"
        )

        country = st.text_input(
            "Country of Origin",
            value=product.get(
                "country",
                ""
            ),
            key=f"edit_country_{product_id}"
        )

    warranty_years = st.number_input(
        "Warranty (Years)",
        min_value=0.0,
        value=float(
            product.get(
                "warranty_years",
                0
            )
        ),
        step=1.0,
        key=f"edit_warranty_{product_id}"
    )

    st.divider()

    # ------------------------------------------------------
    # TECHNICAL INFORMATION
    # ------------------------------------------------------

    st.markdown(
        "### Technical Specifications"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        technology = st.text_input(
            "Technology / Type",
            value=product.get(
                "technology",
                ""
            ),
            key=f"edit_technology_{product_id}"
        )

        rated_power_w = st.number_input(
            "Rated Power (W)",
            min_value=0.0,
            value=float(
                product.get(
                    "rated_power_w",
                    0
                )
            ),
            key=f"edit_power_{product_id}"
        )

        capacity_ah = st.number_input(
            "Capacity (Ah)",
            min_value=0.0,
            value=float(
                product.get(
                    "capacity_ah",
                    0
                )
            ),
            key=f"edit_capacity_{product_id}"
        )

    with col2:

        voltage_v = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            value=float(
                product.get(
                    "voltage_v",
                    0
                )
            ),
            key=f"edit_voltage_{product_id}"
        )

        current_a = st.number_input(
            "Current (A)",
            min_value=0.0,
            value=float(
                product.get(
                    "current_a",
                    0
                )
            ),
            key=f"edit_current_{product_id}"
        )

        energy_kwh = st.number_input(
            "Energy Capacity (kWh)",
            min_value=0.0,
            value=float(
                product.get(
                    "energy_kwh",
                    0
                )
            ),
            key=f"edit_energy_{product_id}"
        )

    with col3:

        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            value=float(
                product.get(
                    "efficiency_percent",
                    0
                )
            ),
            key=f"edit_efficiency_{product_id}"
        )

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=max(
                1,
                int(
                    product.get(
                        "quantity",
                        1
                    )
                )
            ),
            step=1,
            key=f"edit_quantity_{product_id}"
        )

    # ------------------------------------------------------
    # COMMERCIAL INFORMATION
    # ------------------------------------------------------

    st.divider()

    st.markdown(
        "### 💰 Commercial Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=float(
                product.get(
                    "price",
                    0
                )
            ),
            key=f"edit_price_{product_id}"
        )

    with col2:

        currencies = [
            "USD",
            "UGX",
            "NGN",
            "EUR",
            "GBP",
        ]

        current_currency = product.get(
            "currency",
            "USD"
        )

        if current_currency not in currencies:
            current_currency = "USD"

        currency_index = currencies.index(
            current_currency
        )

        currency = st.selectbox(
            "Currency",
            currencies,
            index=currency_index,
            key=f"edit_currency_{product_id}"
        )

    # ------------------------------------------------------
    # NOTES
    # ------------------------------------------------------

    notes = st.text_area(
        "Additional Notes",
        value=product.get(
            "notes",
            ""
        ),
        key=f"edit_notes_{product_id}"
    )

    # ------------------------------------------------------
    # SPECIFICATIONS
    # ------------------------------------------------------

    specifications = product.get(
        "specifications",
        {}
    )

    st.divider()

    with st.expander(
        "Advanced Specifications"
    ):

        st.caption(
            "Additional product-specific "
            "technical information."
        )

        specification_text = st.text_area(
            "Specifications",
            value="\n".join(
                [
                    f"{key}: {value}"
                    for key, value
                    in specifications.items()
                ]
            ),
            key=f"edit_specifications_{product_id}"
        )

    # ------------------------------------------------------
    # SAVE BUTTON
    # ------------------------------------------------------

    st.divider()

    col1, col2 = st.columns(2)

    with col1:

        save_changes = st.button(
            "💾 Save Changes",
            type="primary",
            use_container_width=True,
            key=f"save_changes_{product_id}"
        )

    with col2:

        delete_button = st.button(
            "🗑️ Delete Product",
            type="secondary",
            use_container_width=True,
            key=f"delete_product_{product_id}"
        )

    # ------------------------------------------------------
    # SAVE PRODUCT
    # ------------------------------------------------------

    if save_changes:

        if not name.strip():

            st.error(
                "Product name cannot be empty."
            )

        else:

            new_specifications = {}

            for line in specification_text.splitlines():

                if ":" in line:

                    key, value = line.split(
                        ":",
                        1
                    )

                    key = key.strip()
                    value = value.strip()

                    if key:

                        new_specifications[
                            key
                        ] = value

            updated_product = {

                "id": product_id,

                "name": name,

                "category": category,

                "manufacturer":
                    manufacturer,

                "model": model,

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

                "specifications":
                    new_specifications,
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
                    "Unable to update the product."
                )

    # ------------------------------------------------------
    # DELETE PRODUCT
    # ------------------------------------------------------

    if delete_button:

        st.session_state[
            f"confirm_delete_{product_id}"
        ] = True

    if st.session_state.get(
        f"confirm_delete_{product_id}",
        False
    ):

        st.warning(
            "⚠️ Are you sure you want to permanently "
            "delete this product?"
        )

        col1, col2 = st.columns(2)

        with col1:

            if st.button(
                "Yes, Delete",
                key=f"confirm_yes_{product_id}"
            ):

                success = delete_existing_product(
                    product_id
                )

                if success:

                    st.success(
                        "Product deleted successfully."
                    )

                    st.session_state[
                        f"confirm_delete_{product_id}"
                    ] = False

                    st.rerun()

                else:

                    st.error(
                        "Unable to delete product."
                    )

        with col2:

            if st.button(
                "Cancel",
                key=f"confirm_cancel_{product_id}"
            ):

                st.session_state[
                    f"confirm_delete_{product_id}"
                ] = False

                st.rerun()


# ==========================================================
# PRODUCT MANAGEMENT INTERFACE
# ==========================================================

def display_product_management_ui():

    st.title(
        "🛠️ Product Library Management"
    )

    st.caption(
        "Inspect, search, edit and safely delete "
        "products from your Solar PV Product Library."
    )

    # ------------------------------------------------------
    # LOAD PRODUCTS
    # ------------------------------------------------------

    products = get_products()

    summary = get_product_library_summary()

    # ------------------------------------------------------
    # SUMMARY METRICS
    # ------------------------------------------------------

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Products",
            summary.get(
                "total_products",
                len(products)
            )
        )

    with col2:

        categories = summary.get(
            "product_categories",
            {}
        )

        st.metric(
            "Categories Used",
            len(categories)
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
    # NO PRODUCTS
    # ------------------------------------------------------

    if not products:

        st.info(
            "No products found in the library."
        )

        st.caption(
            "Please add products through the "
            "Product Library interface first."
        )

        return

    # ------------------------------------------------------
    # SEARCH AND FILTER
    # ------------------------------------------------------

    st.subheader(
        "🔎 Find a Product"
    )

    col1, col2 = st.columns(2)

    with col1:

        search_query = st.text_input(
            "Search Product",
            placeholder=(
                "Search name, manufacturer, "
                "model or technology"
            )
        )

    with col2:

        available_categories = sorted(
            list(
                {
                    product.get(
                        "category",
                        "Other"
                    )
                    for product in products
                }
            )
        )

        category_options = [
            "All Categories"
        ] + available_categories

        selected_category = st.selectbox(
            "Filter by Category",
            category_options
        )

    # ------------------------------------------------------
    # APPLY FILTERS
    # ------------------------------------------------------

    filtered_products = products

    if search_query.strip():

        filtered_products = search_product_library(
            query=search_query.strip()
        )

    if selected_category != "All Categories":

        filtered_products = [

            product

            for product in filtered_products

            if product.get(
                "category"
            ) == selected_category

        ]

    st.caption(
        f"Products displayed: "
        f"{len(filtered_products)}"
    )

    # ------------------------------------------------------
    # NO SEARCH RESULTS
    # ------------------------------------------------------

    if not filtered_products:

        st.warning(
            "No matching products found."
        )

        return

    # ------------------------------------------------------
    # PRODUCT SELECTOR
    # ------------------------------------------------------

    product_options = {

        (
            f"{product.get('name', 'Unnamed Product')}"
            f" | "
            f"{product.get('category', 'Other')}"
            f" | "
            f"{product.get('manufacturer', '')}"
        ):
        product.get("id")

        for product
        in filtered_products

    }

    selected_label = st.selectbox(
        "Select Product to Manage",
        list(product_options.keys())
    )

    selected_product_id = product_options[
        selected_label
    ]

    selected_product = get_product_from_library(
        selected_product_id
    )

    if selected_product:

        st.divider()

        edit_product_form(
            selected_product
        )

    else:

        st.error(
            "The selected product could not be loaded."
        )


# ==========================================================
# ALTERNATIVE FUNCTION NAMES
# ==========================================================

def display_management_ui():

    return display_product_management_ui()


def product_management_interface():

    return display_product_management_ui()


# ==========================================================
# RUN DIRECTLY
# ==========================================================

if __name__ == "__main__":

    display_product_management_ui()
