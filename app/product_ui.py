"""
Solar PV Designer Pro Africa™
Product Library User Interface

Persistent product library interface.

Storage flow:
    product_ui.py
        ↓
    library_store.py
        ↓
    app/data/product_library.json
"""

from copy import deepcopy
import streamlit as st

from library_store import (
    add_product_to_library,
    load_product_library,
    save_product_library,
    remove_product_from_library,
    update_product_in_library,
    search_product_library,
    backup_library,
    get_library_summary,
    ensure_data_directory,
)


# ============================================================
# PRODUCT OPTIONS
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


# ============================================================
# INITIALIZATION
# ============================================================

def initialize_database():
    """Initialize persistent product storage."""
    ensure_data_directory()
    return True


def initialize_product_database():
    """Backward-compatible product database initializer."""
    return initialize_database()


# ============================================================
# UTILITY FUNCTIONS
# ============================================================

def safe_float(value, default=0.0):
    """Safely convert a value to float."""
    try:
        if value is None or value == "":
            return float(default)
        return float(value)
    except (ValueError, TypeError):
        return float(default)


def safe_int(value, default=0):
    """Safely convert a value to int."""
    try:
        if value is None or value == "":
            return int(default)
        return int(float(value))
    except (ValueError, TypeError):
        return int(default)


def normalize_product(product):
    """
    Normalize a product record so all expected fields exist.

    This keeps compatibility with older records and with
    product_engine.py.
    """

    if not isinstance(product, dict):
        return {}

    item = deepcopy(product)

    defaults = {
        "id": "",
        "name": "",
        "category": "Other",
        "manufacturer": "",
        "model": "",
        "technology": "Other",
        "rated_power_w": 0.0,
        "voltage_v": 0.0,
        "current_a": 0.0,
        "capacity_ah": 0.0,
        "energy_kwh": 0.0,
        "efficiency_percent": 0.0,
        "warranty_years": 0,
        "supplier": "",
        "country": "",
        "price": 0.0,
        "currency": "USD",
        "quantity": 1,
        "notes": "",
    }

    for key, value in defaults.items():
        item.setdefault(key, value)

    return item


def refresh_product_library():
    """
    Reload products from persistent storage.
    """

    initialize_product_database()

    products = load_product_library()

    products = [
        normalize_product(product)
        for product in products
        if isinstance(product, dict)
    ]

    return products


# ============================================================
# CORE PRODUCT FUNCTIONS
# ============================================================

def get_products():
    """Return all products from the persistent library."""
    return refresh_product_library()


def get_product(product_id):
    """Return one product using its ID."""

    for product in get_products():

        if str(product.get("id")) == str(product_id):
            return product

    return None


def create_product(
    name="",
    category="Other",
    manufacturer="",
    model="",
    technology="Other",
    rated_power_w=0,
    voltage_v=0,
    current_a=0,
    capacity_ah=0,
    energy_kwh=0,
    efficiency_percent=0,
    warranty_years=0,
    supplier="",
    country="",
    price=0,
    currency="USD",
    quantity=1,
    notes="",
    **kwargs,
):
    """
    Create a normalized product dictionary.

    Accepts **kwargs for future compatibility and category-
    specific fields.
    """

    product = {
        "name": str(name).strip(),
        "category": str(category).strip() or "Other",
        "manufacturer": str(manufacturer).strip(),
        "model": str(model).strip(),
        "technology": str(technology).strip() or "Other",
        "rated_power_w": safe_float(rated_power_w),
        "voltage_v": safe_float(voltage_v),
        "current_a": safe_float(current_a),
        "capacity_ah": safe_float(capacity_ah),
        "energy_kwh": safe_float(energy_kwh),
        "efficiency_percent": safe_float(efficiency_percent),
        "warranty_years": safe_int(warranty_years),
        "supplier": str(supplier).strip(),
        "country": str(country).strip(),
        "price": safe_float(price),
        "currency": str(currency).strip() or "USD",
        "quantity": max(1, safe_int(quantity, 1)),
        "notes": str(notes).strip(),
    }

    # Include category-specific fields.
    for key, value in kwargs.items():
        product[key] = value

    return normalize_product(product)


def add_product(product):
    """
    Add a product to persistent storage.

    The function accepts either:
        - a product dictionary, or
        - keyword-compatible product data.
    """

    if not isinstance(product, dict):
        raise ValueError("Product must be a dictionary.")

    product = normalize_product(product)

    if not product.get("name"):
        raise ValueError("Product name is required.")

    saved_product = add_product_to_library(product)

    return normalize_product(saved_product)


def update_product(product_id, updated_data):
    """
    Update an existing product.
    """

    if not isinstance(updated_data, dict):
        raise ValueError("updated_data must be a dictionary.")

    result = update_product_in_library(
        product_id,
        updated_data
    )

    return result


def delete_product(product_id):
    """
    Delete a product from persistent storage.
    """

    return remove_product_from_library(product_id)


# ============================================================
# FILTERING AND SEARCHING
# ============================================================

def search_products(query=""):
    """
    Search products using the persistent product library.
    """

    return [
        normalize_product(product)
        for product in search_product_library(query=query)
    ]


def database_search_products(query=""):
    """Backward-compatible search function."""
    return search_products(query)


def filter_products_by_category(category):
    """Return products belonging to one category."""

    if not category or category == "All":
        return get_products()

    return [
        product
        for product in get_products()
        if product.get("category") == category
    ]


def filter_products_by_technology(technology):
    """Return products belonging to one technology."""

    if not technology or technology == "All":
        return get_products()

    return [
        product
        for product in get_products()
        if product.get("technology") == technology
    ]


# ============================================================
# PRODUCT DETAILS
# ============================================================

def product_details(product):
    """Display one product's details."""

    if not product:
        st.warning("No product selected.")
        return

    product = normalize_product(product)

    st.subheader(product.get("name", "Product Details"))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.write("**Category**")
        st.write(product.get("category"))

        st.write("**Manufacturer**")
        st.write(product.get("manufacturer") or "—")

        st.write("**Model**")
        st.write(product.get("model") or "—")

    with col2:
        st.write("**Technology**")
        st.write(product.get("technology") or "—")

        st.write("**Supplier**")
        st.write(product.get("supplier") or "—")

        st.write("**Country**")
        st.write(product.get("country") or "—")

    with col3:
        st.write("**Price**")
        st.write(
            f"{product.get('currency', 'USD')} "
            f"{safe_float(product.get('price')):,.2f}"
        )

        st.write("**Quantity**")
        st.write(product.get("quantity", 1))

        st.write("**Warranty**")
        st.write(
            f"{product.get('warranty_years', 0)} years"
        )

    st.divider()

    st.json(product)


# ============================================================
# PRODUCT COMPARISON
# ============================================================

def compare_products(products):
    """
    Return comparison-ready product records.
    """

    comparison = []

    for product in products:

        item = normalize_product(product)

        comparison.append({
            "name": item.get("name"),
            "manufacturer": item.get("manufacturer"),
            "model": item.get("model"),
            "category": item.get("category"),
            "technology": item.get("technology"),
            "power_w": item.get("rated_power_w"),
            "voltage_v": item.get("voltage_v"),
            "current_a": item.get("current_a"),
            "capacity_ah": item.get("capacity_ah"),
            "energy_kwh": item.get("energy_kwh"),
            "efficiency_percent": item.get(
                "efficiency_percent"
            ),
            "warranty_years": item.get(
                "warranty_years"
            ),
            "price": item.get("price"),
            "currency": item.get("currency"),
        })

    return comparison


def product_comparison():
    """Interactive product comparison interface."""

    st.subheader("⚖️ Product Comparison")

    products = get_products()

    if not products:
        st.info("No products available for comparison.")
        return

    product_names = {
        f"{p.get('name', 'Unnamed')} | "
        f"{p.get('manufacturer', '')} | "
        f"{p.get('model', '')}": p
        for p in products
    }

    selected_names = st.multiselect(
        "Select products to compare",
        options=list(product_names.keys()),
        max_selections=5,
        key="product_comparison_selector",
    )

    if selected_names:

        selected_products = [
            product_names[name]
            for name in selected_names
        ]

        comparison = compare_products(
            selected_products
        )

        st.dataframe(
            comparison,
            use_container_width=True,
            hide_index=True,
        )


# ============================================================
# CATEGORY-SPECIFIC INPUT FORMS
# ============================================================

def _basic_product_fields(category, prefix):
    """
    Common fields shared by all product categories.
    """

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input(
            "Product Name *",
            key=f"{prefix}_name",
        )

        manufacturer = st.text_input(
            "Manufacturer",
            key=f"{prefix}_manufacturer",
        )

        model = st.text_input(
            "Model",
            key=f"{prefix}_model",
        )

    with col2:
        supplier = st.text_input(
            "Supplier",
            key=f"{prefix}_supplier",
        )

        country = st.text_input(
            "Country",
            key=f"{prefix}_country",
        )

        warranty_years = st.number_input(
            "Warranty (Years)",
            min_value=0,
            step=1,
            key=f"{prefix}_warranty",
        )

    col3, col4, col5 = st.columns(3)

    with col3:
        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_price",
        )

    with col4:
        currency = st.selectbox(
            "Currency",
            ["USD", "UGX", "NGN", "EUR", "GBP", "Other"],
            key=f"{prefix}_currency",
        )

    with col5:
        quantity = st.number_input(
            "Quantity",
            min_value=1,
            step=1,
            value=1,
            key=f"{prefix}_quantity",
        )

    return {
        "name": name,
        "category": category,
        "manufacturer": manufacturer,
        "model": model,
        "supplier": supplier,
        "country": country,
        "warranty_years": warranty_years,
        "price": price,
        "currency": currency,
        "quantity": quantity,
    }


def _solar_panel_fields(prefix):
    """Solar-panel-specific fields."""

    technology = st.selectbox(
        "Panel Technology",
        [
            "Monocrystalline",
            "Polycrystalline",
            "Thin Film",
            "Other",
        ],
        key=f"{prefix}_panel_technology",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        rated_power_w = st.number_input(
            "Rated Power (W)",
            min_value=0.0,
            step=10.0,
            key=f"{prefix}_panel_power",
        )

    with col2:
        voltage_v = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            step=0.1,
            key=f"{prefix}_panel_voltage",
        )

    with col3:
        current_a = st.number_input(
            "Current (A)",
            min_value=0.0,
            step=0.1,
            key=f"{prefix}_panel_current",
        )

    efficiency_percent = st.number_input(
        "Efficiency (%)",
        min_value=0.0,
        max_value=100.0,
        step=0.1,
        key=f"{prefix}_panel_efficiency",
    )

    return {
        "technology": technology,
        "rated_power_w": rated_power_w,
        "voltage_v": voltage_v,
        "current_a": current_a,
        "efficiency_percent": efficiency_percent,
    }


def _battery_fields(prefix):
    """Battery-specific fields."""

    technology = st.selectbox(
        "Battery Technology",
        [
            "Lithium",
            "LiFePO4",
            "Lead Acid",
            "AGM",
            "Gel",
            "Other",
        ],
        key=f"{prefix}_battery_technology",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        voltage_v = st.number_input(
            "Nominal Voltage (V)",
            min_value=0.0,
            step=0.1,
            key=f"{prefix}_battery_voltage",
        )

    with col2:
        capacity_ah = st.number_input(
            "Capacity (Ah)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_battery_capacity",
        )

    with col3:
        energy_kwh = st.number_input(
            "Energy Capacity (kWh)",
            min_value=0.0,
            step=0.1,
            key=f"{prefix}_battery_energy",
        )

    return {
        "technology": technology,
        "voltage_v": voltage_v,
        "capacity_ah": capacity_ah,
        "energy_kwh": energy_kwh,
    }


def _inverter_fields(prefix):
    """Inverter-specific fields."""

    technology = st.selectbox(
        "Inverter Type",
        [
            "Hybrid",
            "Off Grid",
            "On Grid",
            "Other",
        ],
        key=f"{prefix}_inverter_technology",
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        rated_power_w = st.number_input(
            "Rated Power (W)",
            min_value=0.0,
            step=100.0,
            key=f"{prefix}_inverter_power",
        )

    with col2:
        voltage_v = st.number_input(
            "System/DC Voltage (V)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_inverter_voltage",
        )

    with col3:
        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            step=0.1,
            key=f"{prefix}_inverter_efficiency",
        )

    return {
        "technology": technology,
        "rated_power_w": rated_power_w,
        "voltage_v": voltage_v,
        "efficiency_percent": efficiency_percent,
    }


def _charge_controller_fields(prefix):
    """Charge-controller-specific fields."""

    technology = st.selectbox(
        "Controller Type",
        ["MPPT", "PWM", "Other"],
        key=f"{prefix}_controller_technology",
    )

    col1, col2 = st.columns(2)

    with col1:
        voltage_v = st.number_input(
            "System Voltage (V)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_controller_voltage",
        )

    with col2:
        current_a = st.number_input(
            "Rated Current (A)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_controller_current",
        )

    return {
        "technology": technology,
        "voltage_v": voltage_v,
        "current_a": current_a,
    }


def _cable_fields(prefix):
    """Solar-cable-specific fields."""

    col1, col2, col3 = st.columns(3)

    with col1:
        conductor_area_mm2 = st.number_input(
            "Conductor Area (mm²)",
            min_value=0.0,
            step=0.5,
            key=f"{prefix}_cable_area",
        )

    with col2:
        voltage_v = st.number_input(
            "Voltage Rating (V)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_cable_voltage",
        )

    with col3:
        current_a = st.number_input(
            "Current Rating (A)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_cable_current",
        )

    return {
        "technology": "Other",
        "conductor_area_mm2": conductor_area_mm2,
        "voltage_v": voltage_v,
        "current_a": current_a,
    }


def _protection_fields(prefix):
    """Protection-device-specific fields."""

    protection_type = st.selectbox(
        "Protection Type",
        [
            "Circuit Breaker",
            "Fuse",
            "Surge Protection Device",
            "Isolator",
            "Other",
        ],
        key=f"{prefix}_protection_type",
    )

    col1, col2 = st.columns(2)

    with col1:
        voltage_v = st.number_input(
            "Voltage Rating (V)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_protection_voltage",
        )

    with col2:
        current_a = st.number_input(
            "Current Rating (A)",
            min_value=0.0,
            step=1.0,
            key=f"{prefix}_protection_current",
        )

    return {
        "technology": protection_type,
        "voltage_v": voltage_v,
        "current_a": current_a,
    }


def _mounting_fields(prefix):
    """Mounting-structure-specific fields."""

    mounting_type = st.selectbox(
        "Mounting Type",
        [
            "Roof Mount",
            "Ground Mount",
            "Pole Mount",
            "Carport",
            "Other",
        ],
        key=f"{prefix}_mounting_type",
    )

    material = st.text_input(
        "Material",
        key=f"{prefix}_mounting_material",
    )

    return {
        "technology": mounting_type,
        "material": material,
    }


def _other_product_fields(prefix):
    """Generic fields for other components."""

    technology = st.selectbox(
        "Technology",
        PRODUCT_TECHNOLOGIES,
        key=f"{prefix}_other_technology",
    )

    return {
        "technology": technology,
    }


# ============================================================
# ADD PRODUCT FORM
# ============================================================

def add_product_form():
    """Display the category-specific add-product form."""

    st.subheader("➕ Add Product to Library")

    category = st.selectbox(
        "Product Category",
        PRODUCT_CATEGORIES,
        key="add_product_category",
    )

    prefix = "add_product"

    common_data = _basic_product_fields(
        category,
        prefix,
    )

    st.divider()
    st.markdown(
        f"### {category} Specifications"
    )

    specific_data = {}

    if category == "Solar Panel":
        specific_data = _solar_panel_fields(prefix)

    elif category == "Battery":
        specific_data = _battery_fields(prefix)

    elif category == "Inverter":
        specific_data = _inverter_fields(prefix)

    elif category == "Charge Controller":
        specific_data = _charge_controller_fields(prefix)

    elif category == "Solar Cable":
        specific_data = _cable_fields(prefix)

    elif category == "Protection":
        specific_data = _protection_fields(prefix)

    elif category == "Mounting Structure":
        specific_data = _mounting_fields(prefix)

    else:
        specific_data = _other_product_fields(prefix)

    notes = st.text_area(
        "Notes",
        key="add_product_notes",
    )

    st.divider()

    if st.button(
        "💾 Save Product",
        type="primary",
        use_container_width=True,
        key="save_product_button",
    ):

        product_data = {}

        product_data.update(common_data)
        product_data.update(specific_data)

        product_data["notes"] = notes

        if not product_data.get("name", "").strip():
            st.error(
                "Please enter a product name."
            )
            return

        try:

            product = create_product(
                **product_data
            )

            saved_product = add_product(product)

            st.success(
                f"Product saved successfully: "
                f"{saved_product.get('name')}"
            )

            st.json(saved_product)

        except Exception as exc:

            st.error(
                f"Unable to save product: {exc}"
            )


# ============================================================
# SEARCH INTERFACE
# ============================================================

def product_search_interface():
    """Interactive product search interface."""

    st.subheader("🔎 Search Product Library")

    search_query = st.text_input(
        "Search",
        placeholder=(
            "Search by product, manufacturer, "
            "model or technology..."
        ),
        key="product_library_search_query",
    )

    col1, col2 = st.columns(2)

    with col1:
        category_filter = st.selectbox(
            "Filter by Category",
            ["All"] + PRODUCT_CATEGORIES,
            key="product_library_category_filter",
        )

    with col2:

        technologies = sorted(
            {
                product.get("technology", "Other")
                for product in get_products()
                if product.get("technology")
            }
        )

        technology_filter = st.selectbox(
            "Filter by Technology",
            ["All"] + technologies,
            key="product_library_technology_filter",
        )

    products = get_products()

    if search_query.strip():
        products = search_products(search_query)

    if category_filter != "All":
        products = [
            product
            for product in products
            if product.get("category") == category_filter
        ]

    if technology_filter != "All":
        products = [
            product
            for product in products
            if product.get("technology")
            == technology_filter
        ]

    st.write(
        f"### Products Found: {len(products)}"
    )

    if products:

        display_data = []

        for product in products:

            display_data.append({
                "Name": product.get("name"),
                "Category": product.get("category"),
                "Manufacturer": product.get(
                    "manufacturer"
                ),
                "Model": product.get("model"),
                "Technology": product.get(
                    "technology"
                ),
                "Power (W)": product.get(
                    "rated_power_w"
                ),
                "Voltage (V)": product.get(
                    "voltage_v"
                ),
                "Capacity (Ah)": product.get(
                    "capacity_ah"
                ),
                "Energy (kWh)": product.get(
                    "energy_kwh"
                ),
                "Price": product.get("price"),
                "Currency": product.get(
                    "currency"
                ),
            })

        st.dataframe(
            display_data,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info("No matching products found.")


# ============================================================
# DELETE INTERFACE
# ============================================================

def delete_product_interface():
    """Simple product deletion interface."""

    st.subheader("🗑️ Delete Product")

    products = get_products()

    if not products:
        st.info("No products available.")
        return

    options = {
        (
            f"{product.get('name', 'Unnamed')} "
            f"| {product.get('category', '')} "
            f"| {product.get('id', '')}"
        ): product
        for product in products
    }

    selected_label = st.selectbox(
        "Select Product",
        list(options.keys()),
        key="delete_product_selector",
    )

    selected_product = options[selected_label]

    st.warning(
        "You are about to permanently remove this "
        "product from the library."
    )

    product_details(selected_product)

    if st.button(
        "🗑️ Delete Selected Product",
        type="secondary",
        key="delete_selected_product_button",
    ):

        result = delete_product(
            selected_product.get("id")
        )

        if result.get("success"):

            st.success(
                "Product deleted successfully."
            )

            st.rerun()

        else:

            st.error(
                result.get(
                    "message",
                    "Unable to delete product."
                )
            )

# ============================================================
# EDIT PRODUCT INTERFACE
# ============================================================

def edit_product_interface():
    """
    Edit an existing product in the persistent library.
    """

    st.subheader("✏️ Edit Product")

    products = get_products()

    if not products:
        st.info("No products are available to edit.")
        return

    product_options = {
        (
            f"{product.get('name', 'Unnamed Product')} "
            f"| {product.get('category', 'Other')} "
            f"| ID: {product.get('id', '')}"
        ): product
        for product in products
    }

    selected_label = st.selectbox(
        "Select Product to Edit",
        options=list(product_options.keys()),
        key="edit_product_selector",
    )

    selected_product = product_options[selected_label]

    if not selected_product:
        st.warning("Please select a product.")
        return

    st.info(
        f"Editing: **{selected_product.get('name')}**"
    )

    product_id = selected_product.get("id")

    # --------------------------------------------------------
    # BASIC PRODUCT INFORMATION
    # --------------------------------------------------------

    st.markdown("### Basic Product Information")

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name *",
            value=selected_product.get("name", ""),
            key=f"edit_name_{product_id}",
        )

        manufacturer = st.text_input(
            "Manufacturer",
            value=selected_product.get("manufacturer", ""),
            key=f"edit_manufacturer_{product_id}",
        )

        model = st.text_input(
            "Model",
            value=selected_product.get("model", ""),
            key=f"edit_model_{product_id}",
        )

    with col2:

        supplier = st.text_input(
            "Supplier",
            value=selected_product.get("supplier", ""),
            key=f"edit_supplier_{product_id}",
        )

        country = st.text_input(
            "Country",
            value=selected_product.get("country", ""),
            key=f"edit_country_{product_id}",
        )

        warranty_years = st.number_input(
            "Warranty (Years)",
            min_value=0,
            value=safe_int(
                selected_product.get("warranty_years", 0)
            ),
            step=1,
            key=f"edit_warranty_{product_id}",
        )

    # --------------------------------------------------------
    # CATEGORY
    # --------------------------------------------------------

    current_category = selected_product.get(
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
        key=f"edit_category_{product_id}",
    )

    st.divider()

    # --------------------------------------------------------
    # CATEGORY-SPECIFIC SPECIFICATIONS
    # --------------------------------------------------------

    st.markdown(
        f"### {category} Specifications"
    )

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
            "Other"
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Panel Technology",
            technologies,
            index=technologies.index(current_technology),
            key=f"edit_panel_technology_{product_id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "rated_power_w",
                        0
                    )
                ),
                step=10.0,
                key=f"edit_panel_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0
                    )
                ),
                step=0.1,
                key=f"edit_panel_voltage_{product_id}",
            )

        with col3:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "current_a",
                        0
                    )
                ),
                step=0.1,
                key=f"edit_panel_current_{product_id}",
            )

        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            value=safe_float(
                selected_product.get(
                    "efficiency_percent",
                    0
                )
            ),
            step=0.1,
            key=f"edit_panel_efficiency_{product_id}",
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
            "Other"
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Battery Technology",
            technologies,
            index=technologies.index(current_technology),
            key=f"edit_battery_technology_{product_id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            voltage_v = st.number_input(
                "Nominal Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0
                    )
                ),
                step=0.1,
                key=f"edit_battery_voltage_{product_id}",
            )

        with col2:

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "capacity_ah",
                        0
                    )
                ),
                step=1.0,
                key=f"edit_battery_capacity_{product_id}",
            )

        with col3:

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "energy_kwh",
                        0
                    )
                ),
                step=0.1,
                key=f"edit_battery_energy_{product_id}",
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
            "Other"
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Inverter Type",
            technologies,
            index=technologies.index(current_technology),
            key=f"edit_inverter_technology_{product_id}",
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "rated_power_w",
                        0
                    )
                ),
                step=100.0,
                key=f"edit_inverter_power_{product_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "System/DC Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0
                    )
                ),
                step=1.0,
                key=f"edit_inverter_voltage_{product_id}",
            )

        with col3:

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=safe_float(
                    selected_product.get(
                        "efficiency_percent",
                        0
                    )
                ),
                step=0.1,
                key=f"edit_inverter_efficiency_{product_id}",
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
            "Other"
        )

        if current_technology not in technologies:
            current_technology = "Other"

        technology = st.selectbox(
            "Controller Type",
            technologies,
            index=technologies.index(current_technology),
            key=f"edit_controller_technology_{product_id}",
        )

        col1, col2 = st.columns(2)

        with col1:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "voltage_v",
                        0
                    )
                ),
                step=1.0,
                key=f"edit_controller_voltage_{product_id}",
            )

        with col2:

            current_a = st.number_input(
                "Rated Current (A)",
                min_value=0.0,
                value=safe_float(
                    selected_product.get(
                        "current_a",
                        0
                    )
                ),
                step=1.0,
                key=f"edit_controller_current_{product_id}",
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
            value=selected_product.get(
                "technology",
                ""
            ),
            key=f"edit_technology_{product_id}",
        )

        updated_data["technology"] = technology

    # --------------------------------------------------------
    # PRICE INFORMATION
    # --------------------------------------------------------

    st.divider()

    st.markdown("### Commercial Information")

    col1, col2, col3 = st.columns(3)

    with col1:

        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=safe_float(
                selected_product.get("price", 0)
            ),
            step=1.0,
            key=f"edit_price_{product_id}",
        )

    with col2:

        currencies = [
            "USD",
            "UGX",
            "NGN",
            "EUR",
            "GBP",
            "Other",
        ]

        current_currency = selected_product.get(
            "currency",
            "USD"
        )

        if current_currency not in currencies:
            current_currency = "USD"

        currency = st.selectbox(
            "Currency",
            currencies,
            index=currencies.index(current_currency),
            key=f"edit_currency_{product_id}",
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
                        1
                    )
                )
            ),
            step=1,
            key=f"edit_quantity_{product_id}",
        )

    notes = st.text_area(
        "Notes",
        value=selected_product.get("notes", ""),
        key=f"edit_notes_{product_id}",
    )

    # --------------------------------------------------------
    # SAVE CHANGES
    # --------------------------------------------------------

    st.divider()

    if st.button(
        "💾 Save Changes",
        type="primary",
        use_container_width=True,
        key=f"save_changes_{product_id}",
    ):

        if not name.strip():

            st.error(
                "Product name cannot be empty."
            )

            return

        # Common updated fields
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

        try:

            result = update_product(
                product_id,
                updated_data
            )

            if isinstance(result, dict):

                if result.get("success") is False:

                    st.error(
                        result.get(
                            "message",
                            "Unable to update product."
                        )
                    )

                else:

                    st.success(
                        "Product updated successfully."
                    )

                    st.rerun()

            else:

                st.success(
                    "Product updated successfully."
                )

                st.rerun()

        except Exception as exc:

            st.error(
                f"Unable to update product: {exc}"
            )
# ============================================================
# DATABASE MANAGEMENT
# ============================================================

def backup_database():
    """Create a backup of persistent libraries."""
    return backup_library()


def database_management():
    """Display persistent library management tools."""

    st.subheader("🗄️ Product Library Storage")

    summary = get_library_summary()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Total Products",
            summary.get("total_products", 0),
        )

    with col2:
        st.metric(
            "Total Services",
            summary.get("total_services", 0),
        )

    with st.expander("Storage Information"):

        st.json(summary)

    if st.button(
        "💾 Create Library Backup",
        key="create_library_backup_button",
    ):

        result = backup_database()

        if result.get("success"):

            st.success(
                "Backup created successfully."
            )

            if result.get("files"):
                st.write("Backup files:")
                st.write(result["files"])


# ============================================================
# MAIN PRODUCT LIBRARY UI
# ============================================================

def display_product_library():
    """Backward-compatible library display function."""
    display_product_library_ui()


def display_product_library_ui():
    """
    Main persistent Product Library interface.
    """

    initialize_product_database()

    st.title("📦 Solar PV Product Library")

    st.caption(
        "Create, store, search and manage solar PV "
        "components in your persistent product library."
    )

 tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "➕ Add Product",
    "📚 Product Library",
    "✏️ Edit Product",
    "🔎 Search & Filter",
    "⚖️ Compare",
    "🗄️ Storage",
])

    with tab1:
        add_product_form()

    with tab2:

        st.subheader("📚 Saved Products")

        products = get_products()

        if not products:

            st.info(
                "No products found in the library."
            )

        else:

            categories = sorted(
                {
                    product.get(
                        "category",
                        "Other"
                    )
                    for product in products
                }
            )

            selected_category = st.selectbox(
                "Display Category",
                ["All"] + categories,
                key="product_library_display_category",
            )

            if selected_category != "All":

                products = [
                    product
                    for product in products
                    if product.get("category")
                    == selected_category
                ]

            st.write(
                f"### {len(products)} Product(s)"
            )

            display_rows = []

            for product in products:

                display_rows.append({
                    "Name": product.get("name"),
                    "Category": product.get(
                        "category"
                    ),
                    "Manufacturer": product.get(
                        "manufacturer"
                    ),
                    "Model": product.get("model"),
                    "Technology": product.get(
                        "technology"
                    ),
                    "Power (W)": product.get(
                        "rated_power_w"
                    ),
                    "Voltage (V)": product.get(
                        "voltage_v"
                    ),
                    "Capacity (Ah)": product.get(
                        "capacity_ah"
                    ),
                    "Energy (kWh)": product.get(
                        "energy_kwh"
                    ),
                    "Price": product.get(
                        "price"
                    ),
                    "Currency": product.get(
                        "currency"
                    ),
                })

            st.dataframe(
                display_rows,
                use_container_width=True,
                hide_index=True,
            )

            st.divider()

            selected_product_name = st.selectbox(
                "Inspect Product",
                [
                    (
                        f"{product.get('name')} "
                        f"| {product.get('id')}"
                    )
                    for product in products
                ],
                key="product_details_selector",
            )

            selected_id = selected_product_name.split(
                "|"
            )[-1].strip()

            selected_product = get_product(
                selected_id
            )

            if selected_product:
                product_details(selected_product)
    with tab3:
    edit_product_interface()
    with tab4:
    product_search_interface()

    with tab5:
    product_comparison()

    with tab6:
    database_management()


# ============================================================
# RUN INITIALIZATION
# ============================================================

initialize_product_database()
