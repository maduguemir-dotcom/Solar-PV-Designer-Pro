import streamlit as st
from copy import deepcopy

from library_store import (
    load_product_library,
    save_product_library,
)


# ============================================================
# CONFIGURATION
# ============================================================

PRODUCT_CATEGORIES = [
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
    "EUR",
    "GBP",
    "Other",
]


# ============================================================
# SAFE CONVERSION FUNCTIONS
# ============================================================

def safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        if value is None or value == "":
            return default
        return float(value)
    except (TypeError, ValueError):
        return default


def safe_int(value, default=0):
    """Safely convert a value to integer."""
    try:
        if value is None or value == "":
            return default
        return int(float(value))
    except (TypeError, ValueError):
        return default


# ============================================================
# PRODUCT ACCESS FUNCTIONS
# ============================================================

def get_products():
    """Load all products from the persistent product library."""
    products = load_product_library()

    if not isinstance(products, list):
        return []

    return products


def get_product_index(products, selected_product):
    """
    Find the index of a selected product.

    Uses ID when available, otherwise falls back to
    matching name/category/model.
    """

    selected_id = selected_product.get("id")

    if selected_id:

        for index, product in enumerate(products):

            if product.get("id") == selected_id:
                return index

    for index, product in enumerate(products):

        if (
            product.get("name") == selected_product.get("name")
            and product.get("category") == selected_product.get("category")
            and product.get("model") == selected_product.get("model")
        ):
            return index

    return None


# ============================================================
# DELETE PRODUCT
# ============================================================

def delete_existing_product(selected_product):
    """
    Delete a product from the persistent library.
    """

    products = get_products()

    product_index = get_product_index(
        products,
        selected_product,
    )

    if product_index is None:

        return {
            "success": False,
            "message": "Product could not be found.",
        }

    deleted_product = products.pop(product_index)

    save_product_library(products)

    return {
        "success": True,
        "message": (
            f"Product '{deleted_product.get('name')}' "
            "was deleted successfully."
        ),
    }


# ============================================================
# UPDATE PRODUCT
# ============================================================

def update_existing_product(
    selected_product,
    updated_data,
):
    """
    Update an existing product and save the changes permanently.
    """

    products = get_products()

    product_index = get_product_index(
        products,
        selected_product,
    )

    if product_index is None:

        return {
            "success": False,
            "message": "Product could not be found.",
        }

    updated_product = deepcopy(products[product_index])

    updated_product.update(updated_data)

    products[product_index] = updated_product

    save_product_library(products)

    return {
        "success": True,
        "message": (
            f"Product '{updated_product.get('name')}' "
            "was updated successfully."
        ),
        "product": updated_product,
    }


# ============================================================
# PRODUCT INSPECTION
# ============================================================

def display_product_information(product):
    """Display complete information about a product."""

    st.markdown("### 📋 Product Information")

    basic_data = {
        "Name": product.get("name", ""),
        "Category": product.get("category", ""),
        "Manufacturer": product.get("manufacturer", ""),
        "Model": product.get("model", ""),
        "Technology": product.get("technology", ""),
    }

    st.json(basic_data)

    st.markdown("### ⚙️ Technical Specifications")

    technical_data = {
        key: value
        for key, value in product.items()
        if key not in [
            "id",
            "name",
            "category",
            "manufacturer",
            "model",
            "technology",
            "supplier",
            "country",
            "price",
            "currency",
            "quantity",
            "notes",
        ]
    }

    st.json(technical_data)

    st.markdown("### 💰 Commercial Information")

    commercial_data = {
        "Supplier": product.get("supplier", ""),
        "Country": product.get("country", ""),
        "Price": product.get("price", 0),
        "Currency": product.get("currency", "USD"),
        "Quantity": product.get("quantity", 1),
        "Notes": product.get("notes", ""),
    }

    st.json(commercial_data)


# ============================================================
# EDIT FORM
# ============================================================

def edit_product_form(selected_product):
    """
    Display a product editing form and return updated data.
    """

    product_id = selected_product.get(
        "id",
        selected_product.get("name", "product"),
    )

    st.markdown("## ✏️ Edit Product")

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    st.markdown("### Basic Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name *",
            value=str(
                selected_product.get("name", "")
            ),
            key=f"pm_name_{product_id}",
        )

        manufacturer = st.text_input(
            "Manufacturer",
            value=str(
                selected_product.get(
                    "manufacturer",
                    "",
                )
            ),
            key=f"pm_manufacturer_{product_id}",
        )

        model = st.text_input(
            "Model",
            value=str(
                selected_product.get("model", "")
            ),
            key=f"pm_model_{product_id}",
        )

    with col2:

        supplier = st.text_input(
            "Supplier",
            value=str(
                selected_product.get(
                    "supplier",
                    "",
                )
            ),
            key=f"pm_supplier_{product_id}",
        )

        country = st.text_input(
            "Country",
            value=str(
                selected_product.get(
                    "country",
                    "",
                )
            ),
            key=f"pm_country_{product_id}",
        )

        warranty_years = st.number_input(
            "Warranty (Years)",
            min_value=0,
            value=safe_int(
                selected_product.get(
                    "warranty_years",
                    0,
                )
            ),
            step=1,
            key=f"pm_warranty_{product_id}",
        )

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    current_category = selected_product.get(
        "category",
        "Other",
    )

    if current_category not in PRODUCT_CATEGORIES:
        current_category = "Other"

    category = st.selectbox(
        "Product Category",
        PRODUCT_CATEGORIES,
        index=PRODUCT_CATEGORIES.index(
            current_category
        ),
        key=f"pm_category_{product_id}",
    )

    st.divider()

    updated_data = {}

    # ========================================================
    # SOLAR PANEL
    # ========================================================

    if category == "Solar Panel":

        technologies = [
            "Monocrystalline",
            "Polycrystalline",
            "Thin Film",
            "Other",
        ]

        current_technology = selected_product.get(
            "technology",
            "Other",
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Panel Technology",
            technologies,
            index=technologies.index(
                current_technology
            ),
            key=f"pm_panel_technology_{product_id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "rated_power_w",
                        0,
                    )
                ),
                step=10.0,
                key=f"pm_panel_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0,
                    )
                ),
                step=0.1,
                key=f"pm_panel_voltage_{product_id}",
            )

        with col3:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "current_a",
                        0,
                    )
                ),
                step=0.1,
                key=f"pm_panel_current_{product_id}",
            )

        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            value=safe_float(
                selected_product.get(
                    "efficiency_percent",
                    0,
                )
            ),
            step=0.1,
            key=f"pm_panel_efficiency_{product_id}",
        )

        updated_data.update({
            "technology": technology,
            "rated_power_w": rated_power_w,
            "voltage_v": voltage_v,
            "current_a": current_a,
            "efficiency_percent": efficiency_percent,
        })

    # ========================================================
    # BATTERY
    # ========================================================

    elif category == "Battery":

        technologies = [
            "Lithium",
            "LiFePO4",
            "Lead Acid",
            "AGM",
            "Gel",
            "Other",
        ]

        current_technology = selected_product.get(
            "technology",
            "Other",
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Battery Technology",
            technologies,
            index=technologies.index(
                current_technology
            ),
            key=f"pm_battery_technology_{product_id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            voltage_v = st.number_input(
                "Nominal Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0,
                    )
                ),
                step=0.1,
                key=f"pm_battery_voltage_{product_id}",
            )

        with col2:

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "capacity_ah",
                        0,
                    )
                ),
                step=1.0,
                key=f"pm_battery_capacity_{product_id}",
            )

        with col3:

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "energy_kwh",
                        0,
                    )
                ),
                step=0.1,
                key=f"pm_battery_energy_{product_id}",
            )

        updated_data.update({
            "technology": technology,
            "voltage_v": voltage_v,
            "capacity_ah": capacity_ah,
            "energy_kwh": energy_kwh,
        })

    # ========================================================
    # INVERTER
    # ========================================================

    elif category == "Inverter":

        technologies = [
            "Hybrid",
            "Off Grid",
            "On Grid",
            "Other",
        ]

        current_technology = selected_product.get(
            "technology",
            "Other",
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Inverter Type",
            technologies,
            index=technologies.index(
                current_technology
            ),
            key=f"pm_inverter_technology_{product_id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "rated_power_w",
                        0,
                    )
                ),
                step=100.0,
                key=f"pm_inverter_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0,
                    )
                ),
                step=1.0,
                key=f"pm_inverter_voltage_{product_id}",
            )

        with col3:

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    selected_product.get(
                        "efficiency_percent",
                        0,
                    )
                ),
                step=0.1,
                key=f"pm_inverter_efficiency_{product_id}",
            )

        updated_data.update({
            "technology": technology,
            "rated_power_w": rated_power_w,
            "voltage_v": voltage_v,
            "efficiency_percent": efficiency_percent,
        })

    # ========================================================
    # CHARGE CONTROLLER
    # ========================================================

    elif category == "Charge Controller":

        technologies = [
            "MPPT",
            "PWM",
            "Other",
        ]

        current_technology = selected_product.get(
            "technology",
            "Other",
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Controller Type",
            technologies,
            index=technologies.index(
                current_technology
            ),
            key=f"pm_controller_technology_{product_id}",
        )

        col1, col2 = st.columns(2)

        with col1:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0,
                    )
                ),
                step=1.0,
                key=f"pm_controller_voltage_{product_id}",
            )

        with col2:

            current_a = st.number_input(
                "Rated Current (A)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "current_a",
                        0,
                    )
                ),
                step=1.0,
                key=f"pm_controller_current_{product_id}",
            )

        updated_data.update({
            "technology": technology,
            "voltage_v": voltage_v,
            "current_a": current_a,
        })

    # ========================================================
    # OTHER COMPONENTS
    # ========================================================

    else:

        technology = st.text_input(
            "Technology / Type",
            value=str(
                selected_product.get(
                    "technology",
                    "",
                )
            ),
            key=f"pm_technology_{product_id}",
        )

        updated_data["technology"] = technology

    # --------------------------------------------------------
    # COMMERCIAL INFORMATION
    # --------------------------------------------------------

    st.divider()

    st.markdown("### 💰 Commercial Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=safe_float(
                selected_product.get(
                    "price",
                    0,
                )
            ),
            step=1.0,
            key=f"pm_price_{product_id}",
        )

    with col2:

        current_currency = selected_product.get(
            "currency",
            "USD",
        )

        if current_currency not in CURRENCIES:
            current_currency = "USD"

        currency = st.selectbox(
            "Currency",
            CURRENCIES,
            index=CURRENCIES.index(
                current_currency
            ),
            key=f"pm_currency_{product_id}",
        )

    with col3:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=max(
                1,
                safe_int(
                    selected_product.get(
                        "quantity",
                        1,
                    )
                )
            ),
            step=1,
            key=f"pm_quantity_{product_id}",
        )

    notes = st.text_area(
        "Notes",
        value=str(
            selected_product.get(
                "notes",
                "",
            )
        ),
        key=f"pm_notes_{product_id}",
    )

    # --------------------------------------------------------
    # BUILD COMPLETE UPDATED DATA
    # --------------------------------------------------------

    updated_data.update({
        "name": name.strip(),
        "category": category,
        "manufacturer": manufacturer.strip(),
        "model": model.strip(),
        "supplier": supplier.strip(),
        "country": country.strip(),
        "warranty_years": warranty_years,
        "price": price,
        "currency": currency,
        "quantity": quantity,
        "notes": notes.strip(),
    })

    return updated_data


# ============================================================
# MAIN MANAGEMENT INTERFACE
# ============================================================

def display_product_management_ui():
    """
    Main Product Management interface.
    """

    st.title("📦 Product Library Management")

    st.write(
        "Inspect, edit, update and safely delete "
        "products from the persistent product library."
    )

    products = get_products()

    if not products:

        st.info(
            "No products found in the library. "
            "Add products using the Product Library first."
        )

        return

    # --------------------------------------------------------
    # PRODUCT SELECTOR
    # --------------------------------------------------------

    product_options = {}

    for index, product in enumerate(products):

        label = (
            f"{product.get('name', 'Unnamed Product')} "
            f"| {product.get('category', 'Other')} "
            f"| {product.get('manufacturer', '')}"
        )

        # Prevent duplicate labels
        if label in product_options:
            label = f"{label} [{index + 1}]"

        product_options[label] = product

    selected_label = st.selectbox(
        "Select a Product",
        options=list(product_options.keys()),
        key="product_management_selector",
    )

    selected_product = product_options[selected_label]

    st.divider()

    # --------------------------------------------------------
    # MANAGEMENT TABS
    # --------------------------------------------------------

    tab1, tab2, tab3 = st.tabs([
        "👀 Inspect Product",
        "✏️ Edit Product",
        "🗑️ Delete Product",
    ])

    # ========================================================
    # INSPECT
    # ========================================================

    with tab1:

        display_product_information(
            selected_product
        )

    # ========================================================
    # EDIT
    # ========================================================

    with tab2:

        updated_data = edit_product_form(
            selected_product
        )

        st.divider()

        if st.button(
            "💾 Save Changes",
            type="primary",
            use_container_width=True,
            key=(
                f"save_product_"
                f"{selected_product.get('id', selected_label)}"
            ),
        ):

            if not updated_data.get("name"):

                st.error(
                    "Product name cannot be empty."
                )

            else:

                result = update_existing_product(
                    selected_product,
                    updated_data,
                )

                if result.get("success"):

                    st.success(
                        result.get("message")
                    )

                    st.rerun()

                else:

                    st.error(
                        result.get("message")
                    )

    # ========================================================
    # DELETE
    # ========================================================

    with tab3:

        st.warning(
            "⚠️ Deleting a product permanently removes "
            "it from the product library."
        )

        confirm_delete = st.checkbox(
            (
                "I understand that this product "
                "will be permanently deleted."
            ),
            key=(
                f"confirm_delete_"
                f"{selected_product.get('id', selected_label)}"
            ),
        )

        if st.button(
            "🗑️ Delete Product",
            type="primary",
            use_container_width=True,
            disabled=not confirm_delete,
            key=(
                f"delete_product_"
                f"{selected_product.get('id', selected_label)}"
            ),
        ):

            result = delete_existing_product(
                selected_product
            )

            if result.get("success"):

                st.success(
                    result.get("message")
                )

                st.rerun()

            else:

                st.error(
                    result.get("message")
                )


# ============================================================
# COMPATIBILITY ALIASES
# ============================================================

def display_management_ui():
    """Compatibility alias."""
    display_product_management_ui()


def product_management_interface():
    """Compatibility alias."""
    display_product_management_ui()
