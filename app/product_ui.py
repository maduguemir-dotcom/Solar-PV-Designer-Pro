"""
Solar PV Designer Pro Africa™
Product Library User Interface

SQLite-connected Product Library UI.

This module provides:

- Add Product
- View Product Library
- Search Products
- Product Details
- Product Comparison
- Edit Product
- Delete Product
- Database Management
- Backup

All products are stored through library_store.py
using the SQLite database:

app/data/solar_pv_library.db
"""

import streamlit as st
from copy import deepcopy


# ============================================================
# LIBRARY STORE IMPORTS
# ============================================================

from library_store import (
    initialize_database,
    add_product_to_library,
    load_product_library,
    save_product_library,
    search_product_library,
    update_product_in_library,
    remove_product_from_library,
    backup_library,
    get_library_summary,
    clear_product_library,
    safe_float,
    safe_int,
)


# ============================================================
# PRODUCT CATEGORIES
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


PRODUCT_TECHNOLOGIES = [
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


CURRENCIES = [
    "USD",
    "UGX",
    "NGN",
    "KES",
    "EUR",
    "GBP",
    "Other",
]


# ============================================================
# INITIALIZE
# ============================================================

def initialize_product_database():
    """
    Initialize the SQLite Product Library.
    """

    initialize_database()

    return True


# Backward compatibility

initialize_product_database()


def initialize_database_compatibility():
    """
    Backward-compatible database initializer.
    """

    initialize_database()

    return True


# ============================================================
# SAFE HELPERS
# ============================================================

def _safe_text(value, default=""):

    if value is None:
        return default

    return str(value)


def _generate_product_id(category):

    import datetime

    clean_category = (
        str(category)
        .lower()
        .replace(" ", "_")
    )

    timestamp = (
        datetime.datetime.now()
        .strftime("%Y%m%d%H%M%S%f")
    )

    return f"{clean_category}_{timestamp}"


# ============================================================
# PRODUCT NORMALIZATION
# ============================================================

def normalize_product(product):
    """
    Normalize a product record while preserving
    category-specific information.
    """

    product = deepcopy(product or {})

    category = product.get(
        "category",
        "Other",
    )

    if not product.get("id"):

        product["id"] = (
            _generate_product_id(category)
        )

    normalized = {

        "id": _safe_text(
            product.get("id")
        ),

        "name": _safe_text(
            product.get("name")
        ),

        "category": _safe_text(
            category,
            "Other",
        ),

        "manufacturer": _safe_text(
            product.get("manufacturer")
        ),

        "model": _safe_text(
            product.get("model")
        ),

        "technology": _safe_text(
            product.get(
                "technology",
                "Other",
            )
        ),

        "rated_power_w": safe_float(
            product.get(
                "rated_power_w",
                0,
            )
        ),

        "voltage_v": safe_float(
            product.get(
                "voltage_v",
                0,
            )
        ),

        "current_a": safe_float(
            product.get(
                "current_a",
                0,
            )
        ),

        "capacity_ah": safe_float(
            product.get(
                "capacity_ah",
                0,
            )
        ),

        "energy_kwh": safe_float(
            product.get(
                "energy_kwh",
                0,
            )
        ),

        "efficiency_percent": safe_float(
            product.get(
                "efficiency_percent",
                0,
            )
        ),

        "warranty_years": safe_int(
            product.get(
                "warranty_years",
                0,
            )
        ),

        "supplier": _safe_text(
            product.get("supplier")
        ),

        "country": _safe_text(
            product.get("country")
        ),

        "price": safe_float(
            product.get(
                "price",
                0,
            )
        ),

        "currency": _safe_text(
            product.get(
                "currency",
                "USD",
            ),
            "USD",
        ),

        "quantity": max(
            1,
            safe_int(
                product.get(
                    "quantity",
                    1,
                ),
                1,
            ),
        ),

        "notes": _safe_text(
            product.get("notes")
        ),
    }

    # Preserve all additional fields.

    for key, value in product.items():

        if key not in normalized:

            normalized[key] = value

    return normalized


# ============================================================
# CORE PRODUCT FUNCTIONS
# ============================================================

def create_product(**kwargs):
    """
    Create a normalized product record.

    Accepts category-specific fields.
    """

    return normalize_product(kwargs)


def add_product(product=None, **kwargs):
    """
    Add a product to the SQLite library.
    """

    if product is None:

        product = kwargs

    else:

        merged = dict(product)

        merged.update(kwargs)

        product = merged

    product = normalize_product(product)

    return add_product_to_library(product)


def get_products():
    """
    Get all products from SQLite.
    """

    initialize_product_database()

    return load_product_library()


def get_product(product_id):
    """
    Get one product by ID.
    """

    products = get_products()

    for product in products:

        if str(
            product.get("id")
        ) == str(product_id):

            return product

    return None


def update_product(product_id, updated_product):
    """
    Update a product in SQLite.
    """

    if not product_id:

        return False

    existing = get_product(product_id)

    if existing is None:

        return False

    merged = dict(existing)

    merged.update(
        updated_product or {}
    )

    merged["id"] = str(product_id)

    merged = normalize_product(merged)

    return update_product_in_library(
        product_id,
        merged,
    )


def delete_product(product_id):
    """
    Delete a product from SQLite.
    """

    return remove_product_from_library(
        product_id
    )


# ============================================================
# SEARCH AND FILTER
# ============================================================

def search_products(query=""):
    """
    Search products.
    """

    return search_product_library(
        query=query
    )


def database_search_products(query=""):

    return search_products(query)


def filter_products_by_category(category):

    products = get_products()

    if (
        not category
        or category == "All"
    ):

        return products

    return [

        product

        for product in products

        if product.get("category")
        == category

    ]


def filter_products_by_technology(technology):

    products = get_products()

    if (
        not technology
        or technology == "All"
    ):

        return products

    return [

        product

        for product in products

        if product.get("technology")
        == technology

    ]


def refresh_product_library():

    initialize_product_database()

    return get_products()


# ============================================================
# PRODUCT CATEGORY FIELDS
# ============================================================

def product_category_fields(
    category,
    product=None,
    prefix="add",
):
    """
    Display category-specific input fields.
    """

    product = product or {}

    extra_data = {}

    # --------------------------------------------------------
    # SOLAR PANEL
    # --------------------------------------------------------

    if category == "Solar Panel":

        st.subheader(
            "☀️ Solar Panel Specifications"
        )

        col1, col2 = st.columns(2)

        with col1:

            extra_data[
                "rated_power_w"
            ] = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "rated_power_w",
                        0,
                    )
                ),
                key=f"{prefix}_panel_power",
            )

            extra_data[
                "voltage_v"
            ] = st.number_input(
                "Maximum Power Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"{prefix}_panel_voltage",
            )

            extra_data[
                "current_a"
            ] = st.number_input(
                "Maximum Power Current (A)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "current_a",
                        0,
                    )
                ),
                key=f"{prefix}_panel_current",
            )

        with col2:

            extra_data[
                "efficiency_percent"
            ] = st.number_input(
                "Module Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    product.get(
                        "efficiency_percent",
                        0,
                    )
                ),
                key=f"{prefix}_panel_efficiency",
            )

            extra_data[
                "cell_type"
            ] = st.text_input(
                "Cell Type",
                value=_safe_text(
                    product.get(
                        "cell_type",
                        ""
                    )
                ),
                key=f"{prefix}_panel_cell_type",
            )

            extra_data[
                "dimensions"
            ] = st.text_input(
                "Dimensions",
                value=_safe_text(
                    product.get(
                        "dimensions",
                        ""
                    )
                ),
                key=f"{prefix}_panel_dimensions",
            )

    # --------------------------------------------------------
    # BATTERY
    # --------------------------------------------------------

    elif category == "Battery":

        st.subheader(
            "🔋 Battery Specifications"
        )

        col1, col2 = st.columns(2)

        with col1:

            extra_data[
                "voltage_v"
            ] = st.number_input(
                "Nominal Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"{prefix}_battery_voltage",
            )

            extra_data[
                "capacity_ah"
            ] = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "capacity_ah",
                        0,
                    )
                ),
                key=f"{prefix}_battery_capacity",
            )

            extra_data[
                "energy_kwh"
            ] = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "energy_kwh",
                        0,
                    )
                ),
                key=f"{prefix}_battery_energy",
            )

        with col2:

            extra_data[
                "cycle_life"
            ] = st.number_input(
                "Cycle Life",
                min_value=0,
                value=safe_int(
                    product.get(
                        "cycle_life",
                        0,
                    )
                ),
                key=f"{prefix}_battery_cycle_life",
            )

            extra_data[
                "depth_of_discharge_percent"
            ] = st.number_input(
                "Depth of Discharge (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    product.get(
                        "depth_of_discharge_percent",
                        0,
                    )
                ),
                key=f"{prefix}_battery_dod",
            )

            extra_data[
                "efficiency_percent"
            ] = st.number_input(
                "Round Trip Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    product.get(
                        "efficiency_percent",
                        0,
                    )
                ),
                key=f"{prefix}_battery_efficiency",
            )

    # --------------------------------------------------------
    # INVERTER
    # --------------------------------------------------------

    elif category == "Inverter":

        st.subheader(
            "⚡ Inverter Specifications"
        )

        col1, col2 = st.columns(2)

        with col1:

            extra_data[
                "rated_power_w"
            ] = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "rated_power_w",
                        0,
                    )
                ),
                key=f"{prefix}_inverter_power",
            )

            extra_data[
                "surge_power_w"
            ] = st.number_input(
                "Surge Power (W)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "surge_power_w",
                        0,
                    )
                ),
                key=f"{prefix}_inverter_surge",
            )

            extra_data[
                "voltage_v"
            ] = st.number_input(
                "DC Input Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"{prefix}_inverter_voltage",
            )

        with col2:

            extra_data[
                "ac_output_voltage"
            ] = st.number_input(
                "AC Output Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "ac_output_voltage",
                        0,
                    )
                ),
                key=f"{prefix}_inverter_ac_voltage",
            )

            extra_data[
                "efficiency_percent"
            ] = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    product.get(
                        "efficiency_percent",
                        0,
                    )
                ),
                key=f"{prefix}_inverter_efficiency",
            )

    # --------------------------------------------------------
    # CHARGE CONTROLLER
    # --------------------------------------------------------

    elif category == "Charge Controller":

        st.subheader(
            "🎛️ Charge Controller Specifications"
        )

        col1, col2 = st.columns(2)

        with col1:

            extra_data[
                "voltage_v"
            ] = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"{prefix}_controller_voltage",
            )

            extra_data[
                "max_current_a"
            ] = st.number_input(
                "Maximum Charging Current (A)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "max_current_a",
                        0,
                    )
                ),
                key=f"{prefix}_controller_current",
            )

        with col2:

            extra_data[
                "max_pv_power_w"
            ] = st.number_input(
                "Maximum PV Power (W)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "max_pv_power_w",
                        0,
                    )
                ),
                key=f"{prefix}_controller_pv_power",
            )

            extra_data[
                "max_pv_voltage"
            ] = st.number_input(
                "Maximum PV Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "max_pv_voltage",
                        0,
                    )
                ),
                key=f"{prefix}_controller_pv_voltage",
            )

    # --------------------------------------------------------
    # SOLAR CABLE
    # --------------------------------------------------------

    elif category == "Solar Cable":

        st.subheader(
            "🔌 Solar Cable Specifications"
        )

        col1, col2 = st.columns(2)

        with col1:

            extra_data[
                "cross_section_mm2"
            ] = st.number_input(
                "Cross-sectional Area (mm²)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "cross_section_mm2",
                        0,
                    )
                ),
                key=f"{prefix}_cable_cross_section",
            )

            extra_data[
                "current_a"
            ] = st.number_input(
                "Current Rating (A)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "current_a",
                        0,
                    )
                ),
                key=f"{prefix}_cable_current",
            )

        with col2:

            extra_data[
                "voltage_v"
            ] = st.number_input(
                "Voltage Rating (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"{prefix}_cable_voltage",
            )

            extra_data[
                "length_m"
            ] = st.number_input(
                "Cable Length (m)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "length_m",
                        0,
                    )
                ),
                key=f"{prefix}_cable_length",
            )

    # --------------------------------------------------------
    # PROTECTION
    # --------------------------------------------------------

    elif category == "Protection":

        st.subheader(
            "🛡️ Protection Device Specifications"
        )

        col1, col2 = st.columns(2)

        with col1:

            extra_data[
                "device_type"
            ] = st.text_input(
                "Device Type",
                value=_safe_text(
                    product.get(
                        "device_type",
                        ""
                    )
                ),
                key=f"{prefix}_protection_type",
            )

            extra_data[
                "current_a"
            ] = st.number_input(
                "Current Rating (A)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "current_a",
                        0,
                    )
                ),
                key=f"{prefix}_protection_current",
            )

        with col2:

            extra_data[
                "voltage_v"
            ] = st.number_input(
                "Voltage Rating (V)",
                min_value=0.0,
                value=safe_float(
                    product.get(
                        "voltage_v",
                        0,
                    )
                ),
                key=f"{prefix}_protection_voltage",
            )

            extra_data[
                "poles"
            ] = st.number_input(
                "Number of Poles",
                min_value=1,
                value=max(
                    1,
                    safe_int(
                        product.get(
                            "poles",
                            1,
                        ),
                        1,
                    ),
                ),
                key=f"{prefix}_protection_poles",
            )

    # --------------------------------------------------------
    # MOUNTING STRUCTURE
    # --------------------------------------------------------

    elif category == "Mounting Structure":

        st.subheader(
            "🏗️ Mounting Structure Specifications"
        )

        extra_data[
            "mounting_type"
        ] = st.text_input(
            "Mounting Type",
            value=_safe_text(
                product.get(
                    "mounting_type",
                    ""
                )
            ),
            key=f"{prefix}_mounting_type",
        )

        extra_data[
            "material"
        ] = st.text_input(
            "Material",
            value=_safe_text(
                product.get(
                    "material",
                    ""
                )
            ),
            key=f"{prefix}_mounting_material",
        )

    # --------------------------------------------------------
    # OTHER
    # --------------------------------------------------------

    else:

        st.subheader(
            "📦 Additional Specifications"
        )

        extra_data[
            "specification"
        ] = st.text_area(
            "Product Specification",
            value=_safe_text(
                product.get(
                    "specification",
                    ""
                )
            ),
            key=f"{prefix}_other_specification",
        )

    return extra_data


# ============================================================
# ADD PRODUCT FORM
# ============================================================

def add_product_form():
    """
    Display the Add Product form.
    """

    st.subheader(
        "➕ Add New Product"
    )

    with st.form(
        "add_product_form_sqlite",
        clear_on_submit=True,
    ):

        col1, col2 = st.columns(2)

        with col1:

            category = st.selectbox(
                "Product Category",
                PRODUCT_CATEGORIES,
                key="add_product_category",
            )

            name = st.text_input(
                "Product Name *",
                key="add_product_name",
            )

            manufacturer = st.text_input(
                "Manufacturer",
                key="add_product_manufacturer",
            )

            model = st.text_input(
                "Model",
                key="add_product_model",
            )

        with col2:

            technology = st.selectbox(
                "Technology",
                PRODUCT_TECHNOLOGIES,
                key="add_product_technology",
            )

            supplier = st.text_input(
                "Supplier",
                key="add_product_supplier",
            )

            country = st.text_input(
                "Country",
                key="add_product_country",
            )

            warranty_years = st.number_input(
                "Warranty (Years)",
                min_value=0,
                value=0,
                key="add_product_warranty",
            )

        st.divider()

        extra_data = product_category_fields(
            category=category,
            product={},
            prefix="add",
        )

        st.divider()

        st.subheader(
            "💰 Commercial Information"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            price = st.number_input(
                "Unit Price",
                min_value=0.0,
                value=0.0,
                key="add_product_price",
            )

        with col2:

            currency = st.selectbox(
                "Currency",
                CURRENCIES,
                key="add_product_currency",
            )

        with col3:

            quantity = st.number_input(
                "Quantity",
                min_value=1,
                value=1,
                key="add_product_quantity",
            )

        notes = st.text_area(
            "Notes",
            key="add_product_notes",
        )

        submitted = st.form_submit_button(
            "💾 Save Product"
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter a Product Name."
                )

                return

            product = {

                "id": _generate_product_id(
                    category
                ),

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

                "notes": notes,

                **extra_data,
            }

            result = add_product(product)

            st.success(
                f"Product '{result['name']}' "
                "saved successfully."
            )


# ============================================================
# EDIT PRODUCT FORM
# ============================================================

def edit_product_form(product):
    """
    Display an edit form for an existing product.
    """

    product_id = product.get("id")

    if not product_id:

        st.error(
            "Invalid product ID."
        )

        return

    with st.form(
        f"edit_product_form_{product_id}"
    ):

        st.subheader(
            f"✏️ Edit: {product.get('name', '')}"
        )

        col1, col2 = st.columns(2)

        with col1:

            category_index = 0

            if (
                product.get("category")
                in PRODUCT_CATEGORIES
            ):

                category_index = (
                    PRODUCT_CATEGORIES.index(
                        product.get("category")
                    )
                )

            category = st.selectbox(
                "Product Category",
                PRODUCT_CATEGORIES,
                index=category_index,
                key=f"edit_category_{product_id}",
            )

            name = st.text_input(
                "Product Name *",
                value=_safe_text(
                    product.get("name")
                ),
                key=f"edit_name_{product_id}",
            )

            manufacturer = st.text_input(
                "Manufacturer",
                value=_safe_text(
                    product.get("manufacturer")
                ),
                key=f"edit_manufacturer_{product_id}",
            )

            model = st.text_input(
                "Model",
                value=_safe_text(
                    product.get("model")
                ),
                key=f"edit_model_{product_id}",
            )

        with col2:

            technology_value = (
                product.get(
                    "technology",
                    "Other",
                )
            )

            if (
                technology_value
                not in PRODUCT_TECHNOLOGIES
            ):

                technology_value = "Other"

            technology_index = (
                PRODUCT_TECHNOLOGIES.index(
                    technology_value
                )
            )

            technology = st.selectbox(
                "Technology",
                PRODUCT_TECHNOLOGIES,
                index=technology_index,
                key=f"edit_technology_{product_id}",
            )

            supplier = st.text_input(
                "Supplier",
                value=_safe_text(
                    product.get("supplier")
                ),
                key=f"edit_supplier_{product_id}",
            )

            country = st.text_input(
                "Country",
                value=_safe_text(
                    product.get("country")
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
                key=f"edit_warranty_{product_id}",
            )

        st.divider()

        extra_data = product_category_fields(
            category=category,
            product=product,
            prefix=f"edit_{product_id}",
        )

        st.divider()

        st.subheader(
            "💰 Commercial Information"
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

            current_currency = (
                product.get(
                    "currency",
                    "USD",
                )
            )

            if (
                current_currency
                not in CURRENCIES
            ):

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
                key=f"edit_quantity_{product_id}",
            )

        notes = st.text_area(
            "Notes",
            value=_safe_text(
                product.get("notes")
            ),
            key=f"edit_notes_{product_id}",
        )

        submitted = st.form_submit_button(
            "💾 Update Product"
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Product Name cannot be empty."
                )

                return

            updated_product = {

                **product,

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

                "notes": notes,

                **extra_data,
            }

            success = update_product(
                product_id,
                updated_product,
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


# ============================================================
# PRODUCT DETAILS
# ============================================================

def product_details(product=None):
    """
    Display product details.
    """

    if product is None:

        st.info(
            "Select a product to view details."
        )

        return

    st.subheader(
        product.get(
            "name",
            "Product Details",
        )
    )

    excluded = [
        "id",
        "name",
        "category",
    ]

    for key, value in product.items():

        if key in excluded:

            continue

        if (
            value is None
            or value == ""
            or value == 0
            or value == 0.0
        ):

            continue

        label = (
            key
            .replace("_", " ")
            .title()
        )

        st.write(
            f"**{label}:** {value}"
        )


# ============================================================
# PRODUCT LIBRARY DISPLAY
# ============================================================

def display_product_library():
    """
    Display products with View, Edit and Delete options.
    """

    products = get_products()

    if not products:

        st.info(
            "No products found in the library."
        )

        return

    for product in products:

        product_id = product.get("id")

        title = (
            f"{product.get('name', 'Unnamed Product')} "
            f"— {product.get('category', '')}"
        )

        with st.expander(
            title
        ):

            col1, col2, col3 = st.columns(
                3
            )

            with col1:

                st.write(
                    f"**Manufacturer:** "
                    f"{product.get('manufacturer', '')}"
                )

                st.write(
                    f"**Model:** "
                    f"{product.get('model', '')}"
                )

            with col2:

                st.write(
                    f"**Technology:** "
                    f"{product.get('technology', '')}"
                )

                st.write(
                    f"**Price:** "
                    f"{product.get('price', 0)} "
                    f"{product.get('currency', '')}"
                )

            with col3:

                st.write(
                    f"**Warranty:** "
                    f"{product.get('warranty_years', 0)} years"
                )

                st.write(
                    f"**Quantity:** "
                    f"{product.get('quantity', 1)}"
                )

            st.divider()

            tab1, tab2, tab3 = st.tabs(
                [
                    "📋 Details",
                    "✏️ Edit",
                    "🗑️ Delete",
                ]
            )

            with tab1:

                product_details(product)

            with tab2:

                edit_product_form(product)

            with tab3:

                st.warning(
                    "This action permanently deletes "
                    "the selected product."
                )

                if st.button(
                    "Delete This Product",
                    key=f"delete_button_{product_id}",
                ):

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


# ============================================================
# PRODUCT SEARCH INTERFACE
# ============================================================

def product_search_interface():
    """
    Search and filter products.
    """

    st.subheader(
        "🔍 Search Product Library"
    )

    col1, col2 = st.columns(
        [2, 1]
    )

    with col1:

        search_query = st.text_input(
            "Search",
            placeholder=(
                "Search by name, manufacturer, model..."
            ),
            key="product_library_search_query",
        )

    with col2:

        category = st.selectbox(
            "Category",
            ["All"] + PRODUCT_CATEGORIES,
            key="product_library_search_category",
        )

    products = get_products()

    if search_query:

        products = [

            product

            for product in products

            if search_query.lower()
            in " ".join(
                [

                    str(
                        product.get(
                            "name",
                            ""
                        )
                    ),

                    str(
                        product.get(
                            "manufacturer",
                            ""
                        )
                    ),

                    str(
                        product.get(
                            "model",
                            ""
                        )
                    ),

                    str(
                        product.get(
                            "technology",
                            ""
                        )
                    ),
                ]
            ).lower()

        ]

    if category != "All":

        products = [

            product

            for product in products

            if product.get("category")
            == category

        ]

    st.write(
        f"Products found: **{len(products)}**"
    )

    if products:

        for product in products:

            st.write(
                f"**{product.get('name')}** — "
                f"{product.get('manufacturer', '')} "
                f"{product.get('model', '')}"
            )

    else:

        st.info(
            "No matching products found."
        )


# ============================================================
# PRODUCT COMPARISON
# ============================================================

def compare_products(product_ids):
    """
    Return selected products for comparison.
    """

    if not product_ids:

        return []

    products = get_products()

    selected = [

        product

        for product in products

        if str(
            product.get("id")
        )
        in [
            str(item)
            for item in product_ids
        ]

    ]

    return selected


def product_comparison():
    """
    Product comparison interface.
    """

    st.subheader(
        "⚖️ Product Comparison"
    )

    products = get_products()

    if len(products) < 2:

        st.info(
            "At least two products are required "
            "for comparison."
        )

        return

    product_map = {

        f"{product.get('name')} "
        f"({product.get('manufacturer', '')})":
        product.get("id")

        for product in products

    }

    selected_names = st.multiselect(
        "Select Products",
        list(product_map.keys()),
        key="product_comparison_selection",
    )

    selected_ids = [

        product_map[name]

        for name in selected_names

    ]

    comparison = compare_products(
        selected_ids
    )

    if comparison:

        st.dataframe(
            comparison,
            use_container_width=True,
        )


# ============================================================
# DELETE INTERFACE
# ============================================================

def delete_product_interface():
    """
    Standalone delete interface.
    """

    products = get_products()

    if not products:

        st.info(
            "No products available."
        )

        return

    product_map = {

        f"{product.get('name')} "
        f"({product.get('category')})":
        product.get("id")

        for product in products

    }

    selected = st.selectbox(
        "Select Product",
        list(product_map.keys()),
        key="standalone_delete_product",
    )

    if st.button(
        "🗑️ Delete Selected Product",
        key="standalone_delete_button",
    ):

        product_id = product_map[selected]

        if delete_product(product_id):

            st.success(
                "Product deleted successfully."
            )

            st.rerun()


# ============================================================
# DATABASE MANAGEMENT
# ============================================================

def backup_database():
    """
    Create a backup.
    """

    return backup_library()


def database_management():
    """
    Database management interface.
    """

    st.subheader(
        "🗄️ Product Library Management"
    )

    summary = get_library_summary()

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "Total Products",
            summary.get(
                "total_products",
                0,
            ),
        )

    with col2:

        st.write(
            "**Database Location:**"
        )

        st.code(
            summary.get(
                "database_file",
                ""
            )
        )

    st.divider()

    if st.button(
        "💾 Create Library Backup",
        key="create_library_backup",
    ):

        try:

            backup_file = backup_database()

            st.success(
                "Backup created successfully."
            )

            st.code(
                str(backup_file)
            )

        except Exception as error:

            st.error(
                f"Backup failed: {error}"
            )

    st.divider()

    st.warning(
        "Danger Zone"
    )

    if st.checkbox(
        "I understand that this will delete "
        "all products.",
        key="confirm_clear_product_library",
    ):

        if st.button(
            "⚠️ Clear Entire Product Library",
            key="clear_entire_product_library",
        ):

            clear_product_library()

            st.success(
                "Product Library cleared."
            )

            st.rerun()


# ============================================================
# MAIN PRODUCT LIBRARY UI
# ============================================================

def display_product_library_ui():
    """
    Main Product Library interface.
    """

    initialize_product_database()

    st.title(
        "📦 Solar PV Product Library"
    )

    st.caption(
        "Create, store, search, edit and manage "
        "your Solar PV components."
    )

    summary = get_library_summary()

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric(
            "Total Products",
            summary.get(
                "total_products",
                0,
            ),
        )

    with col2:

        category_count = len(
            summary.get(
                "product_categories",
                {}
            )
        )

        st.metric(
            "Categories Used",
            category_count,
        )

    with col3:

        st.metric(
            "Database",
            "SQLite",
        )

    st.divider()

    tabs = st.tabs(
        [
            "➕ Add Product",
            "📚 Product Library",
            "🔍 Search",
            "⚖️ Compare",
            "🗄️ Database",
        ]
    )

    with tabs[0]:

        add_product_form()

    with tabs[1]:

        st.subheader(
            "📚 Your Product Library"
        )

        display_product_library()

    with tabs[2]:

        product_search_interface()

    with tabs[3]:

        product_comparison()

    with tabs[4]:

        database_management()


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def display_management_ui():

    database_management()


# Legacy aliases

database_search_products = search_products


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    display_product_library_ui()
