# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT LIBRARY USER INTERFACE
#
# Compatible with:
# library_store.py
#
# Single product database:
# app/data/solar_pv_library.db
# ==========================================================

import streamlit as st
from copy import deepcopy

from library_store import (
    initialize_database,
    add_product_to_library,
    load_product_library,
    get_product_from_library,
    update_product_in_library,
    remove_product_from_library,
    search_product_library,
    clear_product_library,
    get_product_library_summary,
    get_library_summary,
    backup_library,
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
# COMMON PRODUCT HELPERS
# ==========================================================

def normalize_product(product):

    if product is None:
        product = {}

    product = deepcopy(dict(product))

    product.setdefault("id", "")
    product.setdefault("name", "")
    product.setdefault("category", "")
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
# DATABASE WRAPPER FUNCTIONS
# ==========================================================

def initialize_product_database():

    return initialize_database()


def create_product(product=None, **kwargs):

    if product is None:
        product = {}

    if not isinstance(product, dict):
        product = {}

    product.update(kwargs)

    product = normalize_product(product)

    return add_product_to_library(product)


def add_product(product=None, **kwargs):

    return create_product(
        product,
        **kwargs
    )


def get_products():

    return load_product_library()


def get_product(product_id):

    return get_product_from_library(
        product_id
    )


def update_product(product_id, product=None, **kwargs):

    if product is None:
        product = {}

    if not isinstance(product, dict):
        product = {}

    product.update(kwargs)

    product = normalize_product(product)

    return update_product_in_library(
        product_id,
        product
    )


def delete_product(product_id):

    return remove_product_from_library(
        product_id
    )


def search_products(
    query="",
    category=None
):

    return search_product_library(
        query=query,
        category=category
    )


def filter_products_by_category(category):

    if not category or category == "All":
        return get_products()

    return search_product_library(
        category=category
    )


def filter_products_by_technology(technology):

    technology = str(
        technology or ""
    ).strip().lower()

    products = get_products()

    if not technology:
        return products

    return [
        product
        for product in products
        if technology
        in str(
            product.get(
                "technology",
                ""
            )
        ).lower()
    ]


def refresh_product_library():

    return get_products()


def database_search_products(
    query=""
):

    return search_products(
        query=query
    )


def backup_database():

    return backup_library()


# ==========================================================
# PRODUCT INPUT FORM
# ==========================================================

def add_product_form():

    st.subheader("➕ Add New Product")

    category = st.selectbox(
        "Product Category",
        PRODUCT_CATEGORIES,
        key="add_product_category"
    )

    st.divider()

    st.markdown(
        "### Basic Product Information"
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name *",
            key="add_product_name"
        )

        manufacturer = st.text_input(
            "Manufacturer",
            key="add_product_manufacturer"
        )

        model = st.text_input(
            "Model / Product Code",
            key="add_product_model"
        )

    with col2:

        supplier = st.text_input(
            "Supplier",
            key="add_product_supplier"
        )

        country = st.text_input(
            "Country of Origin",
            key="add_product_country"
        )

        warranty_years = st.number_input(
            "Warranty (Years)",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="add_product_warranty"
        )

    st.divider()

    specifications = {}

    technology = ""
    rated_power_w = 0.0
    voltage_v = 0.0
    current_a = 0.0
    efficiency_percent = 0.0
    capacity_ah = 0.0
    energy_kwh = 0.0

    # ======================================================
    # SOLAR PANEL
    # ======================================================

    if category == "Solar Panel":

        st.markdown(
            "### ☀️ Solar Panel Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            technology = st.selectbox(
                "Technology",
                [
                    "",
                    "Monocrystalline",
                    "Polycrystalline",
                    "TOPCon",
                    "PERC",
                    "Bifacial",
                    "Thin Film",
                ],
                key="panel_technology"
            )

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=0.0,
                key="panel_power"
            )

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                key="panel_efficiency"
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="panel_voltage"
            )

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=0.0,
                key="panel_current"
            )

            cell_count = st.number_input(
                "Number of Cells",
                min_value=0,
                value=0,
                step=1,
                key="panel_cells"
            )

            specifications["cell_count"] = cell_count

        with col3:

            panel_length = st.number_input(
                "Length (mm)",
                min_value=0.0,
                value=0.0,
                key="panel_length"
            )

            panel_width = st.number_input(
                "Width (mm)",
                min_value=0.0,
                value=0.0,
                key="panel_width"
            )

            panel_weight = st.number_input(
                "Weight (kg)",
                min_value=0.0,
                value=0.0,
                key="panel_weight"
            )

            specifications["length_mm"] = panel_length
            specifications["width_mm"] = panel_width
            specifications["weight_kg"] = panel_weight

    # ======================================================
    # BATTERY
    # ======================================================

    elif category == "Battery":

        st.markdown(
            "### 🔋 Battery Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            technology = st.selectbox(
                "Battery Technology",
                [
                    "",
                    "Lithium-ion",
                    "LiFePO4",
                    "Lead Acid",
                    "AGM",
                    "Gel",
                    "Tubular",
                ],
                key="battery_technology"
            )

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=0.0,
                key="battery_capacity"
            )

        with col2:

            voltage_v = st.number_input(
                "Nominal Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="battery_voltage"
            )

            energy_kwh = st.number_input(
                "Energy Capacity (kWh)",
                min_value=0.0,
                value=0.0,
                key="battery_energy"
            )

        with col3:

            cycle_life = st.number_input(
                "Cycle Life",
                min_value=0,
                value=0,
                step=100,
                key="battery_cycles"
            )

            depth_of_discharge = st.number_input(
                "Depth of Discharge (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                key="battery_dod"
            )

            specifications["cycle_life"] = cycle_life
            specifications[
                "depth_of_discharge_percent"
            ] = depth_of_discharge

    # ======================================================
    # INVERTER
    # ======================================================

    elif category == "Inverter":

        st.markdown(
            "### ⚡ Inverter Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            technology = st.selectbox(
                "Inverter Type",
                [
                    "",
                    "Pure Sine Wave",
                    "Modified Sine Wave",
                    "Hybrid",
                    "Grid-Tie",
                    "Off-Grid",
                    "Microinverter",
                ],
                key="inverter_technology"
            )

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=0.0,
                key="inverter_power"
            )

        with col2:

            dc_voltage = st.number_input(
                "DC Input Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="inverter_dc_voltage"
            )

            ac_voltage = st.number_input(
                "AC Output Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="inverter_ac_voltage"
            )

            specifications[
                "dc_input_voltage_v"
            ] = dc_voltage

            specifications[
                "ac_output_voltage_v"
            ] = ac_voltage

        with col3:

            inverter_efficiency = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=0.0,
                key="inverter_efficiency"
            )

            specifications[
                "inverter_efficiency_percent"
            ] = inverter_efficiency

    # ======================================================
    # CHARGE CONTROLLER
    # ======================================================

    elif category == "Charge Controller":

        st.markdown(
            "### 🔌 Charge Controller Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            technology = st.selectbox(
                "Controller Type",
                [
                    "",
                    "MPPT",
                    "PWM",
                ],
                key="controller_type"
            )

            rated_current = st.number_input(
                "Rated Current (A)",
                min_value=0.0,
                value=0.0,
                key="controller_current"
            )

        with col2:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="controller_voltage"
            )

            max_pv_voltage = st.number_input(
                "Maximum PV Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="controller_max_pv_voltage"
            )

            specifications[
                "max_pv_voltage_v"
            ] = max_pv_voltage

        with col3:

            max_pv_power = st.number_input(
                "Maximum PV Power (W)",
                min_value=0.0,
                value=0.0,
                key="controller_pv_power"
            )

            specifications[
                "max_pv_power_w"
            ] = max_pv_power

            current_a = rated_current

    # ======================================================
    # SOLAR PUMP
    # ======================================================

    elif category == "Solar Pump":

        st.markdown(
            "### 💧 Solar Pump Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            pump_type = st.selectbox(
                "Pump Type",
                [
                    "",
                    "Submersible",
                    "Surface",
                    "Borehole",
                ],
                key="pump_type"
            )

            technology = pump_type

            rated_power_w = st.number_input(
                "Pump Power (W)",
                min_value=0.0,
                value=0.0,
                key="pump_power"
            )

        with col2:

            flow_rate = st.number_input(
                "Flow Rate (L/min)",
                min_value=0.0,
                value=0.0,
                key="pump_flow_rate"
            )

            head = st.number_input(
                "Maximum Head (m)",
                min_value=0.0,
                value=0.0,
                key="pump_head"
            )

            specifications["flow_rate_l_min"] = flow_rate
            specifications["maximum_head_m"] = head

        with col3:

            voltage_v = st.number_input(
                "Operating Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="pump_voltage"
            )

    # ======================================================
    # GENERATOR
    # ======================================================

    elif category == "Generator":

        st.markdown(
            "### ⚙️ Generator Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=0.0,
                key="generator_power"
            )

            generator_type = st.selectbox(
                "Fuel Type",
                [
                    "",
                    "Petrol",
                    "Diesel",
                    "Gas",
                    "Hybrid",
                ],
                key="generator_type"
            )

            technology = generator_type

        with col2:

            output_voltage = st.number_input(
                "Output Voltage (V)",
                min_value=0.0,
                value=0.0,
                key="generator_voltage"
            )

            voltage_v = output_voltage

            frequency = st.number_input(
                "Frequency (Hz)",
                min_value=0.0,
                value=50.0,
                key="generator_frequency"
            )

            specifications["frequency_hz"] = frequency

        with col3:

            fuel_consumption = st.number_input(
                "Fuel Consumption (L/hr)",
                min_value=0.0,
                value=0.0,
                key="generator_fuel_consumption"
            )

            specifications[
                "fuel_consumption_l_hr"
            ] = fuel_consumption

    # ======================================================
    # CABLE
    # ======================================================

    elif category == "Cable":

        st.markdown(
            "### 🔧 Cable Specifications"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            cable_type = st.selectbox(
                "Cable Type",
                [
                    "",
                    "DC Solar Cable",
                    "AC Cable",
                    "Battery Cable",
                    "Earth Cable",
                ],
                key="cable_type"
            )

            technology = cable_type

            cross_section = st.number_input(
                "Cross Section (mm²)",
                min_value=0.0,
                value=0.0,
                key="cable_cross_section"
            )

            specifications[
                "cross_section_mm2"
            ] = cross_section

        with col2:

            voltage_rating = st.number_input(
                "Voltage Rating (V)",
                min_value=0.0,
                value=0.0,
                key="cable_voltage"
            )

            current_rating = st.number_input(
                "Current Rating (A)",
                min_value=0.0,
                value=0.0,
                key="cable_current"
            )

            voltage_v = voltage_rating
            current_a = current_rating

        with col3:

            cable_length = st.number_input(
                "Cable Length (m)",
                min_value=0.0,
                value=0.0,
                key="cable_length"
            )

            specifications[
                "length_m"
            ] = cable_length

    # ======================================================
    # OTHER PRODUCTS
    # ======================================================

    else:

        st.markdown(
            f"### {category} Specifications"
        )

        technology = st.text_input(
            "Technology / Type",
            key="generic_technology"
        )

        rated_power_w = st.number_input(
            "Rated Power (W)",
            min_value=0.0,
            value=0.0,
            key="generic_power"
        )

        voltage_v = st.number_input(
            "Voltage (V)",
            min_value=0.0,
            value=0.0,
            key="generic_voltage"
        )

        current_a = st.number_input(
            "Current (A)",
            min_value=0.0,
            value=0.0,
            key="generic_current"
        )

    # ======================================================
    # COMMERCIAL INFORMATION
    # ======================================================

    st.divider()

    st.markdown(
        "### 💰 Commercial Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=0.0,
            key="add_product_price"
        )

    with col2:

        currency = st.selectbox(
            "Currency",
            [
                "USD",
                "UGX",
                "NGN",
                "EUR",
                "GBP",
            ],
            key="add_product_currency"
        )

    with col3:

        quantity = st.number_input(
            "Quantity",
            min_value=1,
            value=1,
            step=1,
            key="add_product_quantity"
        )

    notes = st.text_area(
        "Additional Notes",
        key="add_product_notes"
    )

    st.divider()

    if st.button(
        "💾 Save Product",
        type="primary",
        use_container_width=True,
        key="save_product_button"
    ):

        if not name.strip():

            st.error(
                "Please enter the Product Name."
            )

        else:

            product = {

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

                "supplier":
                    supplier,

                "country":
                    country,

                "specifications":
                    specifications,
            }

            saved_product = create_product(
                product
            )

            if saved_product:

                st.success(
                    f"✅ {name} was successfully "
                    f"added to the Product Library."
                )

                st.rerun()

            else:

                st.error(
                    "Unable to save the product."
                )


# ==========================================================
# DISPLAY PRODUCT DETAILS
# ==========================================================

def product_details(product):

    if not product:

        st.warning(
            "Product not found."
        )

        return

    product = normalize_product(
        product
    )

    st.subheader(
        product.get(
            "name",
            "Product Details"
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Category:** "
            f"{product.get('category', '')}"
        )

        st.write(
            f"**Manufacturer:** "
            f"{product.get('manufacturer', '')}"
        )

        st.write(
            f"**Model:** "
            f"{product.get('model', '')}"
        )

        st.write(
            f"**Technology:** "
            f"{product.get('technology', '')}"
        )

        st.write(
            f"**Supplier:** "
            f"{product.get('supplier', '')}"
        )

    with col2:

        st.write(
            f"**Price:** "
            f"{product.get('price', 0):,.2f} "
            f"{product.get('currency', 'USD')}"
        )

        st.write(
            f"**Quantity:** "
            f"{product.get('quantity', 1)}"
        )

        st.write(
            f"**Country:** "
            f"{product.get('country', '')}"
        )

        st.write(
            f"**Warranty:** "
            f"{product.get('warranty_years', 0)} years"
        )

    st.divider()

    specifications = product.get(
        "specifications",
        {}
    )

    technical_data = {

        "Rated Power (W)":
            product.get(
                "rated_power_w",
                0
            ),

        "Voltage (V)":
            product.get(
                "voltage_v",
                0
            ),

        "Current (A)":
            product.get(
                "current_a",
                0
            ),

        "Efficiency (%)":
            product.get(
                "efficiency_percent",
                0
            ),

        "Battery Capacity (Ah)":
            product.get(
                "capacity_ah",
                0
            ),

        "Energy Capacity (kWh)":
            product.get(
                "energy_kwh",
                0
            ),
    }

    technical_data.update(
        specifications
    )

    st.markdown(
        "### Technical Specifications"
    )

    for key, value in technical_data.items():

        if value not in (
            None,
            "",
            0,
            0.0
        ):

            label = (
                str(key)
                .replace("_", " ")
                .title()
            )

            st.write(
                f"**{label}:** {value}"
            )

    if product.get("notes"):

        st.divider()

        st.markdown(
            "### Notes"
        )

        st.write(
            product.get(
                "notes"
            )
        )


# ==========================================================
# DISPLAY PRODUCT LIBRARY
# ==========================================================

def display_product_library():

    products = get_products()

    if not products:

        st.info(
            "No products found in the library."
        )

        return

    for product in products:

        product_id = product.get(
            "id"
        )

        title = (
            f"{product.get('name', 'Unnamed Product')}"
            f" — "
            f"{product.get('category', '')}"
        )

        with st.expander(title):

            product_details(
                product
            )

            col1, col2 = st.columns(2)

            with col1:

                if st.button(
                    "🗑️ Delete",
                    key=f"delete_library_{product_id}"
                ):

                    delete_product(
                        product_id
                    )

                    st.success(
                        "Product deleted successfully."
                    )

                    st.rerun()

            with col2:

                st.caption(
                    f"Product ID: {product_id}"
                )


# ==========================================================
# SEARCH INTERFACE
# ==========================================================

def product_search_interface():

    st.subheader(
        "🔎 Search Product Library"
    )

    query = st.text_input(
        "Search by product name, manufacturer, "
        "model or technology"
    )

    categories = [
        "All"
    ] + sorted(
        list(
            {
                product.get(
                    "category",
                    "Other"
                )
                for product in get_products()
            }
        )
    )

    selected_category = st.selectbox(
        "Filter by Category",
        categories
    )

    category = None

    if selected_category != "All":

        category = selected_category

    products = search_product_library(
        query=query,
        category=category
    )

    st.caption(
        f"Products found: {len(products)}"
    )

    if not products:

        st.info(
            "No matching products found."
        )

        return

    for product in products:

        with st.expander(
            f"{product.get('name', '')} "
            f"({product.get('category', '')})"
        ):

            product_details(
                product
            )


# ==========================================================
# PRODUCT COMPARISON
# ==========================================================

def compare_products(products):

    if len(products) < 2:

        st.warning(
            "Select at least two products to compare."
        )

        return

    st.subheader(
        "⚖️ Product Comparison"
    )

    comparison_fields = [

        "name",
        "category",
        "manufacturer",
        "model",
        "technology",
        "rated_power_w",
        "voltage_v",
        "current_a",
        "efficiency_percent",
        "capacity_ah",
        "energy_kwh",
        "warranty_years",
        "price",
        "currency",

    ]

    data = {}

    for product in products:

        product_name = (
            product.get(
                "name",
                "Unnamed Product"
            )
        )

        data[
            product_name
        ] = {

            field: product.get(
                field,
                ""
            )

            for field
            in comparison_fields

        }

    st.dataframe(
        data,
        use_container_width=True
    )


def product_comparison():

    products = get_products()

    st.subheader(
        "⚖️ Compare Products"
    )

    if len(products) < 2:

        st.info(
            "At least two products are required "
            "for comparison."
        )

        return

    product_names = [

        f"{product.get('name', '')} "
        f"({product.get('id', '')})"

        for product in products

    ]

    selected = st.multiselect(
        "Select Products",
        product_names
    )

    selected_products = []

    for item in selected:

        product_id = item.split("(")[-1]
        product_id = product_id.rstrip(")")

        product = get_product(
            product_id
        )

        if product:

            selected_products.append(
                product
            )

    if st.button(
        "Compare Selected Products",
        type="primary"
    ):

        compare_products(
            selected_products
        )


# ==========================================================
# DELETE PRODUCT INTERFACE
# ==========================================================

def delete_product_interface():

    products = get_products()

    st.subheader(
        "🗑️ Delete Product"
    )

    if not products:

        st.info(
            "No products available."
        )

        return

    product_map = {

        f"{product.get('name', '')} "
        f"— {product.get('manufacturer', '')}":
            product.get("id")

        for product in products

    }

    selected_name = st.selectbox(
        "Select Product",
        list(product_map.keys())
    )

    if st.button(
        "Delete Selected Product",
        type="secondary"
    ):

        product_id = product_map[
            selected_name
        ]

        if delete_product(product_id):

            st.success(
                "Product deleted successfully."
            )

            st.rerun()

        else:

            st.error(
                "Unable to delete product."
            )


# ==========================================================
# DATABASE MANAGEMENT
# ==========================================================

def database_management():

    st.subheader(
        "🗄️ Product Library Database"
    )

    summary = get_product_library_summary()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Products",
        summary.get(
            "total_products",
            0
        )
    )

    col2.metric(
        "Total Quantity",
        summary.get(
            "total_quantity",
            0
        )
    )

    col3.metric(
        "Categories",
        len(
            summary.get(
                "product_categories",
                {}
            )
        )
    )

    st.divider()

    if st.button(
        "💾 Create Database Backup"
    ):

        backup_file = backup_library()

        st.success(
            f"Backup created successfully: "
            f"{backup_file}"
        )

    st.divider()

    with st.expander(
        "⚠️ Dangerous Zone"
    ):

        st.warning(
            "This action permanently deletes "
            "all products."
        )

        confirm = st.checkbox(
            "I understand that all products "
            "will be deleted."
        )

        if st.button(
            "Delete All Products",
            disabled=not confirm
        ):

            clear_product_library()

            st.success(
                "All products deleted."
            )

            st.rerun()


# ==========================================================
# MAIN PRODUCT LIBRARY UI
# ==========================================================

def display_product_library_ui():

    st.title(
        "📦 Solar PV Product Library"
    )

    st.caption(
        "Add, search, inspect, compare and "
        "manage Solar PV system components."
    )

    summary = get_product_library_summary()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Products",
        summary.get(
            "total_products",
            0
        )
    )

    col2.metric(
        "Categories",
        len(
            summary.get(
                "product_categories",
                {}
            )
        )
    )

    col3.metric(
        "Total Quantity",
        summary.get(
            "total_quantity",
            0
        )
    )

    st.divider()

    tab1, tab2, tab3, tab4, tab5 = st.tabs(

        [

            "➕ Add Product",
            "📚 Product Library",
            "🔎 Search",
            "⚖️ Compare",
            "🗄️ Database",

        ]

    )

    with tab1:

        add_product_form()

    with tab2:

        display_product_library()

    with tab3:

        product_search_interface()

    with tab4:

        product_comparison()

    with tab5:

        database_management()


# ==========================================================
# ALTERNATIVE FUNCTION NAMES
# ==========================================================

def display_product_library_ui():

    return product_library_interface()


def product_library_interface():

    st.title(
        "📦 Solar PV Product Library"
    )

    summary = get_product_library_summary()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Products",
        summary.get(
            "total_products",
            0
        )
    )

    col2.metric(
        "Categories",
        len(
            summary.get(
                "product_categories",
                {}
            )
        )
    )

    col3.metric(
        "Total Quantity",
        summary.get(
            "total_quantity",
            0
        )
    )

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
        [
            "➕ Add Product",
            "📚 Library",
            "🔎 Search",
            "⚖️ Compare",
            "🗄️ Database",
        ]
    )

    with tab1:
        add_product_form()

    with tab2:
        display_product_library()

    with tab3:
        product_search_interface()

    with tab4:
        product_comparison()

    with tab5:
        database_management()


# ==========================================================
# RUN DIRECTLY
# ==========================================================

if __name__ == "__main__":

    display_product_library_ui()
