import streamlit as st
from copy import deepcopy

from library_store import (
    load_product_library,
    save_product_library,
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
# HELPER FUNCTIONS
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
    product_id = product.get("id")

    if product_id not in [None, ""]:
        return str(product_id)

    name = product.get("name", "Unnamed Product")
    category = product.get("category", "Other")

    return f"{index}_{name}_{category}"


# ============================================================
# PRODUCT DATA FUNCTIONS
# ============================================================

def get_products():
    try:
        products = load_product_library()

        if products is None:
            return []

        if not isinstance(products, list):
            return []

        return products

    except Exception as exc:
        st.error(f"Unable to load products: {exc}")
        return []


def save_products(products):
    try:
        if not isinstance(products, list):
            return False

        save_product_library(products)

        return True

    except Exception as exc:
        st.error(f"Unable to save products: {exc}")
        return False


# ============================================================
# UPDATE PRODUCT
# ============================================================

def update_existing_product(product_identifier, updated_product):

    products = get_products()

    for index, product in enumerate(products):

        identifier = get_product_identifier(
            product,
            index,
        )

        if identifier == product_identifier:

            products[index] = deepcopy(updated_product)

            if save_products(products):
                return {
                    "success": True,
                    "message": "Product updated successfully.",
                }

            return {
                "success": False,
                "message": "Unable to save product changes.",
            }

    return {
        "success": False,
        "message": "Product not found.",
    }


# ============================================================
# DELETE PRODUCT
# ============================================================

def delete_existing_product(product_identifier):

    products = get_products()

    new_products = []

    deleted = False

    for index, product in enumerate(products):

        identifier = get_product_identifier(
            product,
            index,
        )

        if identifier == product_identifier:
            deleted = True
        else:
            new_products.append(product)

    if not deleted:
        return {
            "success": False,
            "message": "Product not found.",
        }

    if save_products(new_products):
        return {
            "success": True,
            "message": "Product deleted successfully.",
        }

    return {
        "success": False,
        "message": "Unable to delete product.",
    }


# ============================================================
# DISPLAY PRODUCT DETAILS
# ============================================================

def display_product_details(product):

    st.subheader(
        product.get(
            "name",
            "Unnamed Product",
        )
    )

    col1, col2 = st.columns(2)

    with col1:

        st.write(
            f"**Category:** "
            f"{product.get('category', 'Other')}"
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
            f"**Country:** "
            f"{product.get('country', '')}"
        )

        st.write(
            f"**Warranty:** "
            f"{product.get('warranty_years', 0)} years"
        )

        st.write(
            f"**Rated Power:** "
            f"{product.get('rated_power_w', 0)} W"
        )

        st.write(
            f"**Voltage:** "
            f"{product.get('voltage_v', 0)} V"
        )

        st.write(
            f"**Current:** "
            f"{product.get('current_a', 0)} A"
        )

    st.divider()

    st.subheader("Battery / Energy Information")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Capacity",
        f"{product.get('capacity_ah', 0)} Ah",
    )

    col2.metric(
        "Energy",
        f"{product.get('energy_kwh', 0)} kWh",
    )

    col3.metric(
        "Efficiency",
        f"{product.get('efficiency_percent', 0)} %",
    )

    st.divider()

    price = safe_float(
        product.get("price", 0)
    )

    quantity = safe_int(
        product.get("quantity", 1),
        1,
    )

    currency = product.get(
        "currency",
        "USD",
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Unit Price",
        f"{price:,.2f} {currency}",
    )

    col2.metric(
        "Quantity",
        quantity,
    )

    col3.metric(
        "Total Value",
        f"{price * quantity:,.2f} {currency}",
    )

    notes = product.get(
        "notes",
        "",
    )

    if notes:
        st.divider()
        st.subheader("Notes")
        st.write(notes)


# ============================================================
# EDIT PRODUCT FORM
# ============================================================

def update_product_form(product, product_identifier):

    product = deepcopy(product)

    unique_id = (
        product.get("id")
        or product_identifier
    )

    st.subheader("✏️ Edit Product")

    # --------------------------------------------------------
    # BASIC INFORMATION
    # --------------------------------------------------------

    col1, col2 = st.columns(2)

    with col1:

        name = st.text_input(
            "Product Name",
            value=str(
                product.get("name", "")
            ),
            key=f"name_{unique_id}",
        )

        manufacturer = st.text_input(
            "Manufacturer",
            value=str(
                product.get(
                    "manufacturer",
                    "",
                )
            ),
            key=f"manufacturer_{unique_id}",
        )

        model = st.text_input(
            "Model",
            value=str(
                product.get(
                    "model",
                    "",
                )
            ),
            key=f"model_{unique_id}",
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
            key=f"supplier_{unique_id}",
        )

        country = st.text_input(
            "Country",
            value=str(
                product.get(
                    "country",
                    "",
                )
            ),
            key=f"country_{unique_id}",
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
            key=f"warranty_{unique_id}",
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
        key=f"category_{unique_id}",
    )

    technology_options = TECHNOLOGIES.get(
        category,
        ["Other"],
    )

    current_technology = product.get(
        "technology",
        "Other",
    )

    if current_technology not in technology_options:
        current_technology = technology_options[0]

    technology = st.selectbox(
        "Technology",
        technology_options,
        index=technology_options.index(
            current_technology
        ),
        key=f"technology_{unique_id}",
    )

    st.divider()

    # --------------------------------------------------------
    # TECHNICAL VALUES
    # --------------------------------------------------------

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

    st.subheader(
        f"{category} Specifications"
    )

    if category == "Solar Panel":

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=rated_power_w,
                key=f"power_{unique_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"voltage_{unique_id}",
            )

        with col3:

            current_a = st.number_input(
                "Current (A)",
                min_value=0.0,
                value=current_a,
                key=f"current_{unique_id}",
            )

        efficiency_percent = st.number_input(
            "Efficiency (%)",
            min_value=0.0,
            max_value=100.0,
            value=efficiency_percent,
            key=f"efficiency_{unique_id}",
        )

    elif category == "Battery":

        col1, col2, col3 = st.columns(3)

        with col1:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"voltage_{unique_id}",
            )

        with col2:

            capacity_ah = st.number_input(
                "Capacity (Ah)",
                min_value=0.0,
                value=capacity_ah,
                key=f"capacity_{unique_id}",
            )

        with col3:

            energy_kwh = st.number_input(
                "Energy (kWh)",
                min_value=0.0,
                value=energy_kwh,
                key=f"energy_{unique_id}",
            )

    elif category == "Inverter":

        col1, col2, col3 = st.columns(3)

        with col1:

            rated_power_w = st.number_input(
                "Rated Power (W)",
                min_value=0.0,
                value=rated_power_w,
                key=f"power_{unique_id}",
            )

        with col2:

            voltage_v = st.number_input(
                "Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"voltage_{unique_id}",
            )

        with col3:

            efficiency_percent = st.number_input(
                "Efficiency (%)",
                min_value=0.0,
                max_value=100.0,
                value=efficiency_percent,
                key=f"efficiency_{unique_id}",
            )

    elif category == "Charge Controller":

        col1, col2 = st.columns(2)

        with col1:

            voltage_v = st.number_input(
                "System Voltage (V)",
                min_value=0.0,
                value=voltage_v,
                key=f"voltage_{unique_id}",
            )

        with col2:

            current_a = st.number_input(
                "Rated Current (A)",
                min_value=0.0,
                value=current_a,
                key=f"current_{unique_id}",
            )

    # --------------------------------------------------------
    # COMMERCIAL INFORMATION
    # --------------------------------------------------------

    st.divider()

    st.subheader("Commercial Information")

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
            key=f"price_{unique_id}",
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
            key=f"currency_{unique_id}",
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
            key=f"quantity_{unique_id}",
        )

    notes = st.text_area(
        "Notes",
        value=str(
            product.get(
                "notes",
                "",
            )
        ),
        key=f"notes_{unique_id}",
    )

    # --------------------------------------------------------
    # SAVE BUTTON
    # --------------------------------------------------------

    if st.button(
        "💾 Save Changes",
        type="primary",
        use_container_width=True,
        key=f"save_{unique_id}",
    ):

        if not name.strip():

            st.error(
                "Product name cannot be empty."
            )

            return

        updated_product = deepcopy(product)

        updated_product.update({
            "name": name.strip(),
            "manufacturer": manufacturer.strip(),
            "model": model.strip(),
            "category": category,
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

        if result["success"]:

            st.success(
                result["message"]
            )

            st.rerun()

        else:

            st.error(
                result["message"]
            )


# ============================================================
# MAIN MANAGEMENT INTERFACE
# ============================================================

def product_management_interface():

    st.title("🛠️ Product Library Management")

    st.write(
        "Inspect, edit and delete products "
        "from your persistent product library."
    )

    products = get_products()

    st.caption(
        f"Products loaded: {len(products)}"
    )

    if not products:

        st.info(
            "No products found in the library."
        )

        return

    st.divider()

    product_options = {}

    for index, product in enumerate(products):

        identifier = get_product_identifier(
            product,
            index,
        )

        label = (
            f"{index + 1}. "
            f"{product.get('name', 'Unnamed Product')} "
            f"({product.get('category', 'Other')})"
        )

        product_options[label] = {
            "product": product,
            "identifier": identifier,
        }

    selected_label = st.selectbox(
        "Select Product",
        list(product_options.keys()),
        key="product_management_selector",
    )

    selected_data = product_options[
        selected_label
    ]

    selected_product = selected_data[
        "product"
    ]

    product_identifier = selected_data[
        "identifier"
    ]

    tab1, tab2, tab3 = st.tabs([
        "🔎 Inspect",
        "✏️ Edit",
        "🗑️ Delete",
    ])

    with tab1:

        display_product_details(
            selected_product
        )

    with tab2:

        update_product_form(
            selected_product,
            product_identifier,
        )

    with tab3:

        st.warning(
            "This action permanently deletes "
            "the selected product."
        )

        confirm = st.checkbox(
            "I confirm that I want to delete this product.",
            key=f"confirm_{product_identifier}",
        )

        if st.button(
            "🗑️ Delete Product",
            use_container_width=True,
            disabled=not confirm,
            key=f"delete_{product_identifier}",
        ):

            result = delete_existing_product(
                product_identifier
            )

            if result["success"]:

                st.success(
                    result["message"]
                )

                st.rerun()

            else:

                st.error(
                    result["message"]
                )


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
        page_title="Product Management",
        page_icon="🛠️",
        layout="wide",
    )

    product_management_interface()
