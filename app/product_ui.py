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

    from product_schema import (
        get_product_schema,
        get_category_sections,
        get_category_icon,
        get_category_description,
        validate_category_fields,
    )

    st.subheader(
        "➕ Add Product to Library"
    )

    # ======================================================
    # CATEGORY
    # ======================================================

    category = st.selectbox(
        "Product Category",
        PRODUCT_CATEGORIES,
        key="dynamic_product_category"
    )

    icon = get_category_icon(
        category
    )

    description = get_category_description(
        category
    )

    st.info(
        f"{icon} **{category}** — {description}"
    )

    # ======================================================
    # COMMON PRODUCT INFORMATION
    # ======================================================

    st.markdown(
        "### 🏷️ Product Identification"
    )

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name",
            placeholder="e.g. 550W Solar Panel",
            key="dynamic_product_name"
        )

        manufacturer = st.text_input(
            "Manufacturer",
            key="dynamic_product_manufacturer"
        )

        model = st.text_input(
            "Model",
            key="dynamic_product_model"
        )

    with col2:

        technology_options = (
            PRODUCT_TECHNOLOGIES
        )

        technology = st.selectbox(
            "Technology",
            technology_options,
            key="dynamic_product_technology"
        )

        supplier = st.text_input(
            "Supplier",
            key="dynamic_product_supplier"
        )

        country = st.text_input(
            "Country",
            key="dynamic_product_country"
        )

    # ======================================================
    # CATEGORY-SPECIFIC FIELDS
    # ======================================================

    specifications = {}

    sections = get_category_sections(
        category
    )

    for section_name, fields in sections.items():

        st.markdown(
            f"### ⚙️ {section_name}"
        )

        # Two-column layout

        columns = st.columns(2)

        for index, field in enumerate(fields):

            field_name = field["name"]
            label = field["label"]
            field_type = field["type"]

            unit = field.get(
                "unit",
                ""
            )

            default = field.get(
                "default",
                ""
            )

            options = field.get(
                "options",
                []
            )

            column = columns[
                index % 2
            ]

            with column:

                # ------------------------------------------
                # NUMBER
                # ------------------------------------------

                if field_type == "number":

                    min_value = field.get(
                        "min",
                        None
                    )

                    max_value = field.get(
                        "max",
                        None
                    )

                    step = field.get(
                        "step",
                        1.0
                    )

                    # Streamlit number_input requires a
                    # numeric default.

                    try:

                        numeric_default = float(
                            default
                        )

                    except (
                        ValueError,
                        TypeError
                    ):

                        numeric_default = 0.0

                    kwargs = {

                        "label":
                            f"{label}"
                            + (
                                f" ({unit})"
                                if unit
                                else ""
                            ),

                        "value":
                            numeric_default,

                        "step":
                            float(step),

                        "key":
                            f"dynamic_{category}_{field_name}"

                    }

                    if min_value is not None:

                        kwargs[
                            "min_value"
                        ] = float(
                            min_value
                        )

                    if max_value is not None:

                        kwargs[
                            "max_value"
                        ] = float(
                            max_value
                        )

                    value = st.number_input(
                        **kwargs
                    )

                    specifications[
                        field_name
                    ] = value

                # ------------------------------------------
                # SELECT
                # ------------------------------------------

                elif field_type == "select":

                    value = st.selectbox(

                        f"{label}"
                        + (
                            f" ({unit})"
                            if unit
                            else ""
                        ),

                        options,

                        index=(
                            options.index(
                                default
                            )
                            if default in options
                            else 0
                        ),

                        key=(
                            f"dynamic_"
                            f"{category}_"
                            f"{field_name}"
                        )

                    )

                    specifications[
                        field_name
                    ] = value

                # ------------------------------------------
                # TEXT
                # ------------------------------------------

                elif field_type == "text":

                    value = st.text_input(

                        f"{label}"
                        + (
                            f" ({unit})"
                            if unit
                            else ""
                        ),

                        value=str(
                            default
                        ),

                        key=(
                            f"dynamic_"
                            f"{category}_"
                            f"{field_name}"
                        )

                    )

                    specifications[
                        field_name
                    ] = value

    # ======================================================
    # COMMERCIAL INFORMATION
    # ======================================================

    st.markdown(
        "### 💰 Commercial Information"
    )

    col1, col2, col3 = st.columns(3)

    with col1:

        price = st.number_input(
            "Unit Price",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="dynamic_product_price"
        )

    with col2:

        currency = st.selectbox(

            "Currency",

            [
                "USD",
                "UGX",
                "NGN",
                "KES",
                "TZS",
                "RWF",
                "GHS",
                "ZAR",
                "EUR",
                "GBP",
                "Other"
            ],

            key="dynamic_product_currency"

        )

    with col3:

        quantity = st.number_input(
            "Available Quantity",
            min_value=0.0,
            value=0.0,
            step=1.0,
            key="dynamic_product_quantity"
        )

    notes = st.text_area(

        "Notes",

        placeholder=(
            "Technical information, supplier notes, "
            "installation notes, source, etc."
        ),

        key="dynamic_product_notes"

    )

    # ======================================================
    # VALIDATION
    # ======================================================

    validation_errors = (
        validate_category_fields(
            category,
            specifications
        )
    )

    if validation_errors:

        for error in validation_errors:

            st.warning(
                error
            )

    # ======================================================
    # SAVE
    # ======================================================

    submitted = st.button(

        "💾 Save Product to Library",

        use_container_width=True,

        type="primary",

        key="dynamic_save_product"

    )

    if not submitted:

        return

    # ------------------------------------------------------
    # Basic validation
    # ------------------------------------------------------

    if not name.strip():

        st.error(
            "Product name is required."
        )

        return

    if validation_errors:

        st.error(
            "Please correct the specification errors "
            "before saving."
        )

        return

    # ======================================================
    # BUILD PRODUCT
    # ======================================================

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

        "supplier":
            supplier,

        "country":
            country,

        "rated_power_w":
            specifications.get(
                "rated_power_w",
                0
            ),

        "voltage_v":
            specifications.get(
                "nominal_voltage_v",
                specifications.get(
                    "dc_nominal_voltage_v",
                    specifications.get(
                        "vmp_v",
                        specifications.get(
                            "rated_voltage_v",
                            0
                        )
                    )
                )
            ),

        "capacity_ah":
            specifications.get(
                "capacity_ah",
                0
            ),

        "energy_kwh":
            specifications.get(
                "energy_kwh",
                0
            ),

        "efficiency_percent":
            specifications.get(
                "efficiency_percent",
                specifications.get(
                    "round_trip_efficiency_percent",
                    0
                )
            ),

        "warranty_years":
            specifications.get(
                "warranty_years",
                specifications.get(
                    "product_warranty_years",
                    0
                )
            ),

        "price":
            price,

        "currency":
            currency,

        "quantity":
            quantity,

        "notes":
            notes,

        "specifications":
            specifications

    }

    # ======================================================
    # VALIDATE THROUGH PRODUCT ENGINE
    # ======================================================

    try:

        validation = create_product(
            **product
        )

        if not validation["success"]:

            st.error(
                validation.get(
                    "message",
                    "Product validation failed."
                )
            )

            return

    except TypeError:

        # Compatibility with the current
        # product_engine.py if it does not yet
        # accept price/specifications.

        basic_product = {

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
                product[
                    "rated_power_w"
                ],

            "voltage_v":
                product[
                    "voltage_v"
                ],

            "capacity_ah":
                product[
                    "capacity_ah"
                ],

            "energy_kwh":
                product[
                    "energy_kwh"
                ],

            "efficiency_percent":
                product[
                    "efficiency_percent"
                ],

            "warranty_years":
                product[
                    "warranty_years"
                ],

            "supplier":
                supplier,

            "country":
                country,

            "notes":
                notes

        }

        validation = create_product(
            **basic_product
        )

        if not validation["success"]:

            st.error(
                validation.get(
                    "message",
                    "Product validation failed."
                )
            )

            return

    # ======================================================
    # SAVE
    # ======================================================

    try:

        product_id = add_product(
            product
        )

        refresh_product_library()

        st.success(

            f"✅ {icon} {category} saved successfully. "
            f"Database ID: {product_id}"

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

def display_product_library():

    from product_schema import (
        get_category_icon,
    )

    st.subheader("📚 Product Library")

    # ======================================================
    # LOAD PRODUCTS
    # ======================================================

    try:
        products = get_products()
    except Exception as error:
        st.error(f"Unable to load product library: {error}")
        return

    if not products:
        st.info(
            "No products are currently stored in the library."
        )
        return

    # ======================================================
    # CATEGORY SUMMARY
    # ======================================================

    categories = sorted(
        set(
            product.get(
                "category",
                "Other"
            )
            for product in products
        )
    )

    st.markdown("### 📂 Browse by Category")

    # "All Products" + categories
    library_options = ["🌐 All Products"]

    for category in categories:

        icon = get_category_icon(category)

        library_options.append(
            f"{icon} {category}"
        )

    selected_library = st.radio(
        "Library category",
        library_options,
        horizontal=True,
        key="product_library_category"
    )

    # ======================================================
    # FILTER
    # ======================================================

    if selected_library == "🌐 All Products":

        filtered_products = products

        selected_category = None

    else:

        selected_category = selected_library.split(
            " ",
            1
        )[1]

        filtered_products = [

            product

            for product in products

            if product.get(
                "category",
                "Other"
            ) == selected_category

        ]

    # ======================================================
    # CATEGORY HEADER
    # ======================================================

    if selected_category:

        icon = get_category_icon(
            selected_category
        )

        st.markdown(
            f"## {icon} {selected_category}"
        )

    else:

        st.markdown(
            "## 🌐 All Products"
        )

    st.caption(
        f"{len(filtered_products)} "
        f"product(s) in this library."
    )

    # ======================================================
    # EMPTY CATEGORY
    # ======================================================

    if not filtered_products:

        st.info(
            "There are no products in this category yet."
        )

        return

    # ======================================================
    # CATEGORY-SPECIFIC DISPLAY
    # ======================================================

    if selected_category == "Solar Panel":

        _display_solar_panel_library(
            filtered_products
        )

    elif selected_category == "Battery":

        _display_battery_library(
            filtered_products
        )

    elif selected_category == "Inverter":

        _display_inverter_library(
            filtered_products
        )

    elif selected_category == "Charge Controller":

        _display_charge_controller_library(
            filtered_products
        )

    elif selected_category == "Mounting Structure":

        _display_mounting_library(
            filtered_products
        )

    elif selected_category == "Solar Cable":

        _display_cable_library(
            filtered_products
        )

    elif selected_category == "Protection":

        _display_protection_library(
            filtered_products
        )

    else:

        _display_general_product_library(
            filtered_products
        )
def _display_solar_panel_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Technology":
                p.get("technology", ""),

            "Power (W)":
                specs.get(
                    "rated_power_w",
                    p.get("rated_power_w", 0)
                ),

            "Voc (V)":
                specs.get(
                    "voc_v",
                    ""
                ),

            "Vmp (V)":
                specs.get(
                    "vmp_v",
                    ""
                ),

            "Isc (A)":
                specs.get(
                    "isc_a",
                    ""
                ),

            "Imp (A)":
                specs.get(
                    "imp_a",
                    ""
                ),

            "Efficiency (%)":
                specs.get(
                    "efficiency_percent",
                    p.get(
                        "efficiency_percent",
                        ""
                    )
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_battery_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Technology":
                p.get("technology", ""),

            "Voltage (V)":
                specs.get(
                    "nominal_voltage_v",
                    p.get("voltage_v", "")
                ),

            "Capacity (Ah)":
                specs.get(
                    "capacity_ah",
                    p.get("capacity_ah", "")
                ),

            "Energy (kWh)":
                specs.get(
                    "energy_kwh",
                    p.get("energy_kwh", "")
                ),

            "DoD (%)":
                specs.get(
                    "depth_of_discharge_percent",
                    ""
                ),

            "Efficiency (%)":
                specs.get(
                    "round_trip_efficiency_percent",
                    p.get(
                        "efficiency_percent",
                        ""
                    )
                ),

            "Cycle Life":
                specs.get(
                    "cycle_life",
                    ""
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_inverter_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Technology":
                p.get("technology", ""),

            "Power (W)":
                specs.get(
                    "rated_power_w",
                    p.get("rated_power_w", "")
                ),

            "Surge (W)":
                specs.get(
                    "surge_power_w",
                    ""
                ),

            "DC Voltage (V)":
                specs.get(
                    "dc_nominal_voltage_v",
                    p.get("voltage_v", "")
                ),

            "AC Voltage (V)":
                specs.get(
                    "ac_output_voltage_v",
                    ""
                ),

            "MPPT Range":
                (
                    f"{specs.get('mppt_min_voltage_v', '')}"
                    f" – "
                    f"{specs.get('mppt_max_voltage_v', '')}"
                ),

            "Efficiency (%)":
                specs.get(
                    "efficiency_percent",
                    p.get(
                        "efficiency_percent",
                        ""
                    )
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_charge_controller_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Type":
                specs.get(
                    "controller_type",
                    p.get("technology", "")
                ),

            "System Voltage":
                specs.get(
                    "system_voltage_v",
                    ""
                ),

            "Charge Current (A)":
                specs.get(
                    "max_charge_current_a",
                    ""
                ),

            "PV Input (W)":
                specs.get(
                    "max_pv_input_power_w",
                    ""
                ),

            "PV Voltage (V)":
                specs.get(
                    "max_pv_voltage_v",
                    ""
                ),

            "Efficiency (%)":
                specs.get(
                    "efficiency_percent",
                    ""
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_mounting_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Structure":
                specs.get(
                    "structure_type",
                    ""
                ),

            "Material":
                specs.get(
                    "material",
                    ""
                ),

            "Panel Capacity":
                specs.get(
                    "panel_capacity",
                    ""
                ),

            "Roof Type":
                specs.get(
                    "roof_type",
                    ""
                ),

            "Wind Rating":
                specs.get(
                    "wind_rating_kmh",
                    ""
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_cable_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Cross Section (mm²)":
                specs.get(
                    "cross_section_mm2",
                    ""
                ),

            "Material":
                specs.get(
                    "conductor_material",
                    ""
                ),

            "Length (m)":
                specs.get(
                    "cable_length_m",
                    ""
                ),

            "Voltage Rating":
                specs.get(
                    "voltage_rating_v",
                    ""
                ),

            "UV Resistant":
                specs.get(
                    "uv_resistant",
                    ""
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_protection_library(products):

    rows = []

    for p in products:

        specs = p.get(
            "specifications",
            {}
        )

        rows.append({

            "Product":
                p.get("name", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Type":
                specs.get(
                    "protection_type",
                    ""
                ),

            "Voltage (V)":
                specs.get(
                    "rated_voltage_v",
                    ""
                ),

            "Current (A)":
                specs.get(
                    "rated_current_a",
                    ""
                ),

            "Poles":
                specs.get(
                    "poles",
                    ""
                ),

            "Breaking Capacity (kA)":
                specs.get(
                    "breaking_capacity_ka",
                    ""
                ),

            "Application":
                specs.get(
                    "dc_or_ac",
                    ""
                ),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


def _display_general_product_library(products):

    rows = []

    for p in products:

        rows.append({

            "Product":
                p.get("name", ""),

            "Category":
                p.get("category", ""),

            "Manufacturer":
                p.get("manufacturer", ""),

            "Model":
                p.get("model", ""),

            "Technology":
                p.get("technology", ""),

            "Supplier":
                p.get("supplier", ""),

            "Country":
                p.get("country", ""),

            "Price":
                p.get("price", ""),

            "Currency":
                p.get("currency", "")

        })

    st.dataframe(
        rows,
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
