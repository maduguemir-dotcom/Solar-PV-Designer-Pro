"""
Solar PV Designer Pro Africa™
Product Library Management Interface

This module uses the SAME persistent product storage
as product_ui.py.

Storage flow:

product_management_ui.py
        ↓
product_ui.py
        ↓
library_store.py
        ↓
app/data/product_library.json
"""

from copy import deepcopy
import streamlit as st

from product_ui import (
    get_products,
    get_product,
    update_product,
    delete_product,
    normalize_product,
    safe_float,
    safe_int,
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


# ============================================================
# TECHNOLOGY OPTIONS
# ============================================================

def get_technology_options(category):

    technologies = {

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

        "Mounting Structure": [
            "Roof Mount",
            "Ground Mount",
            "Pole Mount",
            "Carport",
            "Other",
        ],

        "Solar Cable": [
            "Solar Cable",
            "DC Cable",
            "AC Cable",
            "Other",
        ],

        "Protection": [
            "Circuit Breaker",
            "Fuse",
            "Surge Protection Device",
            "Isolator",
            "Other",
        ],

        "Other": [
            "Other",
        ],
    }

    return technologies.get(
        category,
        ["Other"],
    )


# ============================================================
# PRODUCT LABEL
# ============================================================

def product_label(product, index):

    product = normalize_product(product)

    name = product.get(
        "name",
        "Unnamed Product",
    )

    category = product.get(
        "category",
        "Other",
    )

    manufacturer = product.get(
        "manufacturer",
        "",
    )

    product_id = product.get(
        "id",
        "",
    )

    return (
        f"{index + 1}. "
        f"{name} | "
        f"{category} | "
        f"{manufacturer} | "
        f"ID: {product_id}"
    )


# ============================================================
# PRODUCT DETAILS
# ============================================================

def display_product_details(product):

    if not product:

        st.warning(
            "No product selected."
        )

        return

    product = normalize_product(product)

    st.subheader(
        product.get(
            "name",
            "Unnamed Product",
        )
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        st.write(
            "**Category**"
        )

        st.write(
            product.get(
                "category",
                "Other",
            )
        )

        st.write(
            "**Manufacturer**"
        )

        st.write(
            product.get(
                "manufacturer",
                "—",
            )
            or "—"
        )

        st.write(
            "**Model**"
        )

        st.write(
            product.get(
                "model",
                "—",
            )
            or "—"
        )

    with col2:

        st.write(
            "**Technology**"
        )

        st.write(
            product.get(
                "technology",
                "—",
            )
            or "—"
        )

        st.write(
            "**Supplier**"
        )

        st.write(
            product.get(
                "supplier",
                "—",
            )
            or "—"
        )

        st.write(
            "**Country**"
        )

        st.write(
            product.get(
                "country",
                "—",
            )
            or "—"
        )

    with col3:

        st.write(
            "**Price**"
        )

        price = safe_float(
            product.get(
                "price",
                0,
            )
        )

        currency = product.get(
            "currency",
            "USD",
        )

        st.write(
            f"{currency} {price:,.2f}"
        )

        st.write(
            "**Quantity**"
        )

        st.write(
            product.get(
                "quantity",
                1,
            )
        )

        st.write(
            "**Warranty**"
        )

        st.write(
            f"{product.get('warranty_years', 0)} years"
        )

    st.divider()

    st.subheader(
        "Technical Specifications"
    )

    specifications = {}

    for key, value in product.items():

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
            "warranty_years",
            "notes",
        ]:

            specifications[key] = value

    if specifications:

        st.json(
            specifications
        )

    notes = product.get(
        "notes",
        "",
    )

    if notes:

        st.divider()

        st.subheader(
            "Notes"
        )

        st.write(notes)


# ============================================================
# EDIT PRODUCT FORM
# ============================================================

def update_existing_product(
    product_id,
    updated_data,
):

    try:

        result = update_product(
            product_id,
            updated_data,
        )

        return result

    except Exception as exc:

        return {
            "success": False,
            "message": str(exc),
        }


def edit_product_form(product):

    product = normalize_product(
        deepcopy(product)
    )

    product_id = str(
        product.get(
            "id",
            "",
        )
    )

    st.subheader(
        "✏️ Edit Product"
    )

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name *",
            value=str(
                product.get(
                    "name",
                    "",
                )
            ),
            key=f"edit_name_{product_id}",
        )

        manufacturer = st.text_input(
            "Manufacturer",
            value=str(
                product.get(
                    "manufacturer",
                    "",
                )
            ),
            key=f"edit_manufacturer_{product_id}",
        )

        model = st.text_input(
            "Model",
            value=str(
                product.get(
                    "model",
                    "",
                )
            ),
            key=f"edit_model_{product_id}",
        )

    with col2:

        supplier = st.text_input(
            "Supplier",
            value=str(
                product.get(
                    "supplier",
                    "",
                )
            ),
            key=f"edit_supplier_{product_id}",
        )

        country = st.text_input(
            "Country",
            value=str(
                product.get(
                    "country",
                    "",
                )
            ),
            key=f"edit_country_{product_id}",
        )

        warranty_years = st.number_input(
            "Warranty Years",
            min_value=0,
            step=1,
            value=safe_int(
                product.get(
                    "warranty_years",
                    0,
                )
            ),
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

    technology_options = (
        get_technology_options(
            category
        )
    )

    current_technology = product.get(
        "technology",
        "Other",
    )

    if current_technology not in technology_options:

        current_technology = (
            technology_options[0]
        )

    technology = st.selectbox(
        "Technology",
        technology_options,
        index=technology_options.index(
            current_technology
        ),
        key=f"edit_technology_{product_id}",
    )

    st.divider()

    # ========================================================
    # CATEGORY-SPECIFIC EDITING
    # ========================================================

    st.subheader(
        f"{category} Specifications"
    )

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

    extra_fields = {}

    # --------------------------------------------------------
    # SOLAR PANEL
    # --------------------------------------------------------

    if category == "Solar Panel":

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=rated_power_w,
                key=f"edit_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"edit_voltage_{product_id}",
            )

        with col3:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=current_a,
                key=f"edit_current_{product_id}",
            )

        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            value=efficiency_percent,
            key=f"edit_efficiency_{product_id}",
        )

    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    elif category == "Battery":

        col1, col2, col3 = st.columns(3)

        with col1:

            voltage_v = st.number_input(
                "Nominal Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"edit_battery_voltage_{product_id}",
            )

        with col2:

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=capacity_ah,
                key=f"edit_capacity_{product_id}",
            )

        with col3:

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=energy_kwh,
                key=f"edit_energy_{product_id}",
            )

    # --------------------------------------------------------
    # INVERTER
    # --------------------------------------------------------

    elif category == "Inverter":

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=rated_power_w,
                key=f"edit_inverter_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"edit_inverter_voltage_{product_id}",
            )

        with col3:

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=efficiency_percent,
                key=f"edit_inverter_efficiency_{product_id}",
            )

    # --------------------------------------------------------
    # CHARGE CONTROLLER
    # --------------------------------------------------------

    elif category == "Charge Controller":

        col1, col2 = st.columns(2)

        with col1:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"edit_controller_voltage_{product_id}",
            )

        with col2:

            current_a = st.number_input(
                "Rated Current (A)",
                min_value=0.0,
                value=current_a,
                key=f"edit_controller_current_{product_id}",
            )

    # --------------------------------------------------------
    # SOLAR CABLE
    # --------------------------------------------------------

    elif category == "Solar Cable":

        conductor_area_mm2 = st.number_input(
            "Conductor Area (mm²)",
            min_value=0.0,
            value=safe_float(
                product.get(
                    "conductor_area_mm2",
                    0,
                )
            ),
            key=f"edit_cable_area_{product_id}",
        )

        voltage_v = st.number_input(
            "Voltage Rating (V)",
            min_value=0.0,
            value=voltage_v,
            key=f"edit_cable_voltage_{product_id}",
        )

        current_a = st.number_input(
            "Current Rating (A)",
            min_value=0.0,
            value=current_a,
            key=f"edit_cable_current_{product_id}",
        )

        extra_fields[
            "conductor_area_mm2"
        ] = conductor_area_mm2

    # --------------------------------------------------------
    # MOUNTING STRUCTURE
    # --------------------------------------------------------

    elif category == "Mounting Structure":

        material = st.text_input(
            "Material",
            value=str(
                product.get(
                    "material",
                    "",
                )
            ),
            key=f"edit_material_{product_id}",
        )

        extra_fields[
            "material"
        ] = material

    # --------------------------------------------------------
    # COMMERCIAL INFORMATION
    # --------------------------------------------------------

    st.divider()

    st.subheader(
        "Commercial Information"
    )

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
            key=f"edit_price_{product_id}",
        )

    with col2:

        current_currency = product.get(
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
            key=f"edit_currency_{product_id}",
        )

    with col3:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1,
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

    # --------------------------------------------------------
    # SAVE CHANGES
    # --------------------------------------------------------

    if st.button(
        "💾 Save Changes",
        type="primary",
        use_container_width=True,
        key=f"save_product_{product_id}",
    ):

        if not name.strip():

            st.error(
                "Product name is required."
            )

            return

        updated_data = deepcopy(
            product
        )

        updated_data.update({

            "name": name.strip(),

            "category": category,

            "manufacturer": (
                manufacturer.strip()
            ),

            "model": model.strip(),

            "technology": technology,

            "supplier": supplier.strip(),

            "country": country.strip(),

            "warranty_years": (
                warranty_years
            ),

            "rated_power_w": (
                rated_power_w
            ),

            "voltage_v": voltage_v,

            "current_a": current_a,

            "capacity_ah": capacity_ah,

            "energy_kwh": energy_kwh,

            "efficiency_percent": (
                efficiency_percent
            ),

            "price": price,

            "currency": currency,

            "quantity": quantity,

            "notes": notes.strip(),
        })

        updated_data.update(
            extra_fields
        )

        result = update_existing_product(
            product_id,
            updated_data,
        )

        if isinstance(result, dict):

            if result.get("success"):

                st.success(
                    "Product updated successfully."
                )

                st.rerun()

            else:

                st.error(
                    result.get(
                        "message",
                        "Unable to update product.",
                    )
                )

        else:

            st.success(
                "Product updated successfully."
            )

            st.rerun()


# ============================================================
# DELETE PRODUCT
# ============================================================

def delete_existing_product(product_id):

    try:

        result = delete_product(
            product_id
        )

        return result

    except Exception as exc:

        return {
            "success": False,
            "message": str(exc),
        }


# ============================================================
# MAIN MANAGEMENT UI
# ============================================================

def product_management_interface():

    st.title(
        "🛠️ Product Library Management"
    )

    st.write(
        "Inspect, edit and safely delete products "
        "from your Solar PV Product Library."
    )

    products = get_products()

    st.caption(
        f"Products available: {len(products)}"
    )

    if not products:

        st.info(
            "No products found in the library."
        )

        st.warning(
            "Please add products through the "
            "Product Library interface first."
        )

        return

    st.divider()

    # --------------------------------------------------------
    # BUILD PRODUCT SELECTION
    # --------------------------------------------------------

    product_options = {}

    for index, product in enumerate(products):

        product = normalize_product(
            product
        )

        label = product_label(
            product,
            index,
        )

        product_options[label] = (
            product
        )

    selected_label = st.selectbox(
        "Select Product to Manage",
        options=list(
            product_options.keys()
        ),
        key="management_product_selector",
    )

    selected_product = product_options[
        selected_label
    ]

    product_id = selected_product.get(
        "id"
    )

    # --------------------------------------------------------
    # TABS
    # --------------------------------------------------------

    tab1, tab2, tab3 = st.tabs([

        "🔎 Inspect Product",

        "✏️ Edit Product",

        "🗑️ Delete Product",

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

        edit_product_form(
            selected_product
        )

    # --------------------------------------------------------
    # DELETE
    # --------------------------------------------------------

    with tab3:

        st.warning(
            "⚠️ Deleting a product cannot be undone."
        )

        st.write(
            f"Selected product: "
            f"**{selected_product.get('name')}**"
        )

        confirm_delete = st.checkbox(
            "I understand and want to delete this product.",
            key=f"confirm_delete_{product_id}",
        )

        if st.button(
            "🗑️ Delete Product",
            type="secondary",
            use_container_width=True,
            disabled=not confirm_delete,
            key=f"delete_product_{product_id}",
        ):

            result = delete_existing_product(
                product_id
            )

            if isinstance(result, dict):

                if result.get("success"):

                    st.success(
                        "Product deleted successfully."
                    )

                    st.rerun()

                else:

                    st.error(
                        result.get(
                            "message",
                            "Unable to delete product.",
                        )
                    )

            else:

                st.success(
                    "Product deleted successfully."
                )

                st.rerun()


# ============================================================
# PUBLIC FUNCTIONS
# ============================================================

def display_product_management_ui():

    product_management_interface()


def display_management_ui():

    product_management_interface()


# ============================================================
# DIRECT EXECUTION
# ============================================================

if __name__ == "__main__":

    st.set_page_config(
        page_title=(
            "Product Library Management"
        ),
        page_icon="🛠️",
        layout="wide",
    )

    product_management_interface()
