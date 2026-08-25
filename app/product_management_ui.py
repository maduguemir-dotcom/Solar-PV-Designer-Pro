import streamlit as st
from copy import deepcopy

from library_store import (
    load_product_library,
    save_product_library,
    remove_product_from_library,
    get_library_summary,
)

# ============================================================
# CONSTANTS
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

TECHNOLOGIES = {
    "Solar Panel": [
        "Monocrystalline",
        "Polycrystalline",
        "Thin Film",
        "Other",
    ],
    "Battery": [
        "Lithium",
        "LiFePO4",
        "Lead Acid",
        "AGM",
        "Gel",
        "Other",
    ],
    "Inverter": [
        "Hybrid",
        "Off Grid",
        "On Grid",
        "Other",
    ],
    "Charge Controller": [
        "MPPT",
        "PWM",
        "Other",
    ],
}


# ============================================================
# SAFE VALUE HELPERS
# ============================================================

def safe_float(value, default=0.0):
    try:
        if value is None or value == "":
            return float(default)
        return float(value)
    except (ValueError, TypeError):
        return float(default)


def safe_int(value, default=0):
    try:
        if value is None or value == "":
            return int(default)
        return int(value)
    except (ValueError, TypeError):
        return int(default)


def get_product_identifier(product, index):
    """
    Return a stable identifier for editing/deleting.
    """

    product_id = product.get("id")

    if product_id not in (None, ""):
        return str(product_id)

    name = product.get("name", "Unnamed Product")
    category = product.get("category", "Other")

    return f"{index}_{name}_{category}"


# ============================================================
# LOAD PRODUCTS
# ============================================================

def get_products():
    """
    Load products from the persistent product library.
    """

    try:
        products = load_product_library()

        if isinstance(products, list):
            return products

        return []

    except Exception as exc:
        st.error(f"Unable to load product library: {exc}")
        return []


# ============================================================
# SAVE PRODUCTS
# ============================================================

def save_products(products):
    """
    Save the complete product library.
    """

    try:
        save_product_library(products)
        return True

    except Exception as exc:
        st.error(f"Unable to save product library: {exc}")
        return False


# ============================================================
# UPDATE EXISTING PRODUCT
# ============================================================

def update_existing_product(product_identifier, updated_product):
    """
    Update one existing product and save the entire library.
    """

    products = get_products()

    updated = False

    for index, product in enumerate(products):

        current_identifier = get_product_identifier(
            product,
            index,
        )

        if current_identifier == product_identifier:

            products[index] = deepcopy(updated_product)

            updated = True
            break

    if not updated:
        return {
            "success": False,
            "message": "Product was not found.",
        }

    if save_products(products):

        return {
            "success": True,
            "message": "Product updated successfully.",
        }

    return {
        "success": False,
        "message": "Unable to save product changes.",
    }


# ============================================================
# DELETE EXISTING PRODUCT
# ============================================================

def delete_existing_product(product_identifier):
    """
    Delete a product from the persistent library.
    """

    products = get_products()

    remaining_products = []

    deleted_product = None

    for index, product in enumerate(products):

        current_identifier = get_product_identifier(
            product,
            index,
        )

        if current_identifier == product_identifier:

            deleted_product = product

        else:

            remaining_products.append(product)

    if deleted_product is None:

        return {
            "success": False,
            "message": "Product was not found.",
        }

    if save_products(remaining_products):

        return {
            "success": True,
            "message": (
                f"Product '{deleted_product.get('name', '')}' "
                "deleted successfully."
            ),
        }

    return {
        "success": False,
        "message": "Unable to delete product.",
    }


# ============================================================
# PRODUCT DETAILS
# ============================================================

def display_product_details(product):
    """
    Display complete product information.
    """

    st.subheader(
        product.get(
            "name",
            "Unnamed Product",
        )
    )

    st.caption(
        f"Category: {product.get('category', 'Other')}"
    )

    basic_data = {
        "Manufacturer": product.get("manufacturer", ""),
        "Model": product.get("model", ""),
        "Technology": product.get("technology", ""),
        "Supplier": product.get("supplier", ""),
        "Country": product.get("country", ""),
        "Warranty (Years)": product.get("warranty_years", 0),
    }

    specification_data = {
        "Rated Power (W)": product.get("rated_power_w", 0),
        "Voltage (V)": product.get("voltage_v", 0),
        "Current (A)": product.get("current_a", 0),
        "Capacity (Ah)": product.get("capacity_ah", 0),
        "Energy (kWh)": product.get("energy_kwh", 0),
        "Efficiency (%)": product.get("efficiency_percent", 0),
    }

    commercial_data = {
        "Unit Price": product.get("price", 0),
        "Currency": product.get("currency", "USD"),
        "Quantity": product.get("quantity", 1),
    }

    st.markdown("### Basic Information")

    col1, col2 = st.columns(2)

    basic_items = list(basic_data.items())

    midpoint = (len(basic_items) + 1) // 2

    with col1:

        for label, value in basic_items[:midpoint]:

            st.write(f"**{label}:** {value}")

    with col2:

        for label, value in basic_items[midpoint:]:

            st.write(f"**{label}:** {value}")

    st.markdown("### Technical Specifications")

    spec_col1, spec_col2 = st.columns(2)

    specification_items = list(
        specification_data.items()
    )

    midpoint = (
        len(specification_items) + 1
    ) // 2

    with spec_col1:

        for label, value in specification_items[:midpoint]:

            if safe_float(value) != 0:

                st.write(
                    f"**{label}:** {value}"
                )

    with spec_col2:

        for label, value in specification_items[midpoint:]:

            if safe_float(value) != 0:

                st.write(
                    f"**{label}:** {value}"
                )

    st.markdown("### Commercial Information")

    price = safe_float(
        commercial_data["Unit Price"]
    )

    currency = commercial_data["Currency"]

    quantity = safe_int(
        commercial_data["Quantity"],
        1,
    )

    total_cost = price * quantity

    metric1, metric2, metric3 = st.columns(3)

    metric1.metric(
        "Unit Price",
        f"{price:,.2f} {currency}",
    )

    metric2.metric(
        "Quantity",
        quantity,
    )

    metric3.metric(
        "Total Value",
        f"{total_cost:,.2f} {currency}",
    )

    notes = product.get("notes", "")

    if notes:

        st.markdown("### Notes")

        st.write(notes)


# ============================================================
# EDIT PRODUCT FORM
# ============================================================

def update_product_form(product, product_identifier):
    """
    Display category-specific editing form.
    """

    product = deepcopy(product)

    product_id = (
        product.get("id")
        or product_identifier
    )

    st.subheader("✏️ Edit Product")

    st.info(
        f"Editing: {product.get('name', 'Unnamed Product')}"
    )

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    st.markdown("### Basic Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name *",
            value=str(
                product.get("name", "")
            ),
            key=f"edit_name_{product_id}",
        )

        manufacturer = st.text_input(
            "Manufacturer",
            value=str(
                product.get("manufacturer", "")
            ),
            key=f"edit_manufacturer_{product_id}",
        )

        model = st.text_input(
            "Model",
            value=str(
                product.get("model", "")
            ),
            key=f"edit_model_{product_id}",
        )

    with col2:

        supplier = st.text_input(
            "Supplier",
            value=str(
                product.get("supplier", "")
            ),
            key=f"edit_supplier_{product_id}",
        )

        country = st.text_input(
            "Country",
            value=str(
                product.get("country", "")
            ),
            key=f"edit_country_{product_id}",
        )

        warranty_years = st.number_input(
            "Warranty (Years)",
            min_value=0,
            value=safe_int(
                product.get(
                    "warranty_years",
                    0,
                )
            ),
            step=1,
            key=f"edit_warranty_{product_id}",
        )

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    current_category = product.get(
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
        key=f"edit_category_{product_id}",
    )

    # --------------------------------------------------------
    # TECHNOLOGY
    # --------------------------------------------------------

    technology_options = TECHNOLOGIES.get(
        category,
        None,
    )

    current_technology = product.get(
        "technology",
        "Other",
    )

    if technology_options:

        if current_technology not in technology_options:

            current_technology = "Other"

        technology = st.selectbox(
            "Technology",
            technology_options,
            index=technology_options.index(
                current_technology
            ),
            key=f"edit_technology_{product_id}",
        )

    else:

        technology = st.text_input(
            "Technology / Type",
            value=str(
                product.get(
                    "technology",
                    "",
                )
            ),
            key=f"edit_technology_{product_id}",
        )

    st.divider()

    # ========================================================
    # SOLAR PANEL
    # ========================================================

    rated_power_w = safe_float(
        product.get(
            "rated_power_w",
            0,
        )
    )

    voltage_v = safe_float(
        product.get(
            "voltage_v",
            0,
        )
    )

    current_a = safe_float(
        product.get(
            "current_a",
            0,
        )
    )

    capacity_ah = safe_float(
        product.get(
            "capacity_ah",
            0,
        )
    )

    energy_kwh = safe_float(
        product.get(
            "energy_kwh",
            0,
        )
    )

    efficiency_percent = safe_float(
        product.get(
            "efficiency_percent",
            0,
        )
    )

    st.markdown(
        f"### {category} Specifications"
    )

    if category == "Solar Panel":

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=rated_power_w,
                step=10.0,
                key=f"edit_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                step=0.1,
                key=f"edit_voltage_{product_id}",
            )

        with col3:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=current_a,
                step=0.1,
                key=f"edit_current_{product_id}",
            )

        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            value=efficiency_percent,
            step=0.1,
            key=f"edit_efficiency_{product_id}",
        )

    # ========================================================
    # BATTERY
    # ========================================================

    elif category == "Battery":

        col1, col2, col3 = st.columns(3)

        with col1:

            voltage_v = st.number_input(
                "Nominal Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                step=0.1,
                key=f"edit_voltage_{product_id}",
            )

        with col2:

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=capacity_ah,
                step=1.0,
                key=f"edit_capacity_{product_id}",
            )

        with col3:

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=energy_kwh,
                step=0.1,
                key=f"edit_energy_{product_id}",
            )

    # ========================================================
    # INVERTER
    # ========================================================

    elif category == "Inverter":

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=rated_power_w,
                step=100.0,
                key=f"edit_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                step=1.0,
                key=f"edit_voltage_{product_id}",
            )

        with col3:

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=efficiency_percent,
                step=0.1,
                key=f"edit_efficiency_{product_id}",
            )

    # ========================================================
    # CHARGE CONTROLLER
    # ========================================================

    elif category == "Charge Controller":

        col1, col2 = st.columns(2)

        with col1:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                step=1.0,
                key=f"edit_voltage_{product_id}",
            )

        with col2:

            current_a = st.number_input(
                "Rated Current (A)",
                min_value=0.0,
                value=current_a,
                step=1.0,
                key=f"edit_current_{product_id}",
            )

    # ========================================================
    # COMMERCIAL INFORMATION
    # ========================================================

    st.divider()

    st.markdown(
        "### Commercial Information"
    )

    current_currency = product.get(
        "currency",
        "USD",
    )

    if current_currency not in CURRENCIES:

        current_currency = "USD"

    col1, col2, col3 = st.columns(3)

    with col1:

        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=safe_float(
                product.get(
                    "price",
                    0,
                )
            ),
            step=1.0,
            key=f"edit_price_{product_id}",
        )

    with col2:

        currency = st.selectbox(
            "Currency",
            CURRENCIES,
            index=CURRENCIES.index(
                current_currency
            ),
            key=f"edit_currency_{product_id}",
        )

    with col3:

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
                )
            ),
            step=1,
            key=f"edit_quantity_{product_id}",
        )

    notes = st.text_area(
        "Notes",
        value=str(
            product.get(
                "notes",
                "",
            )
        ),
        key=f"edit_notes_{product_id}",
    )

    st.divider()

    if st.button(
        "💾 Save Product Changes",
        type="primary",
        use_container_width=True,
        key=f"save_product_{product_id}",
    ):

        if not name.strip():

            st.error(
                "Product name is required."
            )

            return

        updated_product = deepcopy(product)

        updated_product.update({

            "name": name.strip(),

            "category": category,

            "manufacturer": manufacturer.strip(),

            "model": model.strip(),

            "technology": technology,

            "supplier": supplier.strip(),

            "country": country.strip(),

            "warranty_years": warranty_years,

            "rated_power_w": rated_power_w,

            "voltage_v": voltage_v,

            "current_a": current_a,

            "capacity_ah": capacity_ah,

            "energy_kwh": energy_kwh,

            "efficiency_percent": efficiency_percent,

            "price": price,

            "currency": currency,

            "quantity": quantity,

            "notes": notes.strip(),
        })

        result = update_existing_product(
            product_identifier,
            updated_product,
        )

        if result.get("success"):

            st.success(
                result.get(
                    "message",
                    "Product updated successfully.",
                )
            )

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Unable to update product.",
                )
            )


# ============================================================
# PRODUCT MANAGEMENT INTERFACE
# ============================================================

def product_management_interface():
    """
    Main Product Management interface.
    """

    st.title("🛠️ Product Library Management")

    st.write(
        "Edit, inspect and safely delete records "
        "from the persistent product library."
    )

    try:

        summary = get_library_summary()

        if isinstance(summary, dict):

            total_products = summary.get(
                "products",
                summary.get(
                    "total_products",
                    0,
                )
            )

        else:

            total_products = 0

    except Exception:

        total_products = 0

    products = get_products()

    if not products:

        st.info(
            "No products found in the library."
        )

        st.caption(
            "Add products first through "
            "the Product Library interface."
        )

        return

    metric1, metric2 = st.columns(2)

    metric1.metric(
        "Products Loaded",
        len(products),
    )

    metric2.metric(
        "Library Summary",
        total_products,
    )

    st.divider()

    product_map = {}

    for index, product in enumerate(products):

        identifier = get_product_identifier(
            product,
            index,
        )

        label = (
            f"{index + 1}. "
            f"{product.get('name', 'Unnamed Product')} "
            f"— {product.get('category', 'Other')}"
        )

        product_map[label] = {
            "product": product,
            "identifier": identifier,
        }

    selected_label = st.selectbox(
        "Select a Product",
        options=list(product_map.keys()),
        key="management_product_selector",
    )

    selected_data = product_map[selected_label]

    selected_product = selected_data["product"]

    product_identifier = selected_data["identifier"]

    tab1, tab2, tab3 = st.tabs([

        "🔎 Inspect",

        "✏️ Edit",

        "🗑️ Delete",
    ])

    # --------------------------------------------------------
    # INSPECT
    # --------------------------------------------------------

    with tab1:

        display_product_details(
            selected_product
        )

    # --------------------------------------------------------
    # EDIT
    # --------------------------------------------------------

    with tab2:

        update_product_form(
            selected_product,
            product_identifier,
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    with tab3:

        st.warning(
            "Deleting a product permanently removes "
            "it from the product library."
        )

        st.write(
            f"Selected product: "
            f"**{selected_product.get('name', '')}**"
        )

        confirm_delete = st.checkbox(
            "I understand that this product "
            "will be permanently deleted.",
            key=(
                f"confirm_delete_"
                f"{product_identifier}"
            ),
        )

        if st.button(
            "🗑️ Delete Product",
            type="secondary",
            use_container_width=True,
            key=(
                f"delete_product_"
                f"{product_identifier}"
            ),
            disabled=not confirm_delete,
        ):

            result = delete_existing_product(
                product_identifier
            )

            if result.get("success"):

                st.success(
                    result.get(
                        "message",
                        "Product deleted successfully.",
                    )
                )

                st.rerun()

            else:

                st.error(
                    result.get(
                        "message",
                        "Unable to delete product.",
                    )
                )


# ============================================================
# PUBLIC DISPLAY FUNCTIONS
# ============================================================

def display_product_management_ui():
    """
    Public function for displaying the Product
    Management interface.
    """

    product_management_interface()


def display_management_ui():
    """
    Backward-compatible alias.
    """

    product_management_interface()


# ============================================================
# DIRECT TEST
# ============================================================

if __name__ == "__main__":

    st.set_page_config(
        page_title="Product Management",
        page_icon="🛠️",
        layout="wide",
    )

    product_management_interface()
