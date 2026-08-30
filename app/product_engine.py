# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT ENGINE
#
# Version: 2.4.1
#
# Purpose:
# - Product creation and normalization
# - Product validation
# - SQLite-backed product storage
# - Product search
# - Product filtering
# - Product ranking
# - Product comparison
# - Product analysis
# - Backward compatibility with product_ui.py
#
# IMPORTANT:
# This module does NOT create a second database.
# All persistent product storage is delegated to
# library_store.py.
# ==========================================================

from copy import deepcopy
from datetime import datetime
import json


# ==========================================================
# LIBRARY STORE
# ==========================================================

try:
    import library_store

except Exception:
    library_store = None


# ==========================================================
# CONSTANTS
# ==========================================================

PRODUCT_CATEGORIES = [
    "Solar Panel",
    "Battery",
    "Inverter",
    "Charge Controller",
    "Solar Cable",
    "Protection",
    "Mounting Structure",
    "Other",
]


PRODUCT_TECHNOLOGIES = [
    "Monocrystalline",
    "Polycrystalline",
    "Thin Film",
    "LiFePO4",
    "Lithium-ion",
    "Lead Acid",
    "AGM",
    "Gel",
    "Hybrid",
    "On-grid",
    "Off-grid",
    "MPPT",
    "PWM",
    "Copper",
    "Aluminium",
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


# ==========================================================
# DATABASE COMPATIBILITY CONSTANTS
# ==========================================================

if library_store is not None:

    DATABASE_FILE = getattr(
        library_store,
        "DATABASE_FILE",
        None,
    )

    DB_PATH = getattr(
        library_store,
        "DB_PATH",
        DATABASE_FILE,
    )

    PRODUCT_LIBRARY_FILE = getattr(
        library_store,
        "PRODUCT_LIBRARY_FILE",
        DATABASE_FILE,
    )

else:

    DATABASE_FILE = None

    DB_PATH = None

    PRODUCT_LIBRARY_FILE = None


# ==========================================================
# SAFE VALUE FUNCTIONS
# ==========================================================

def safe_float(
    value,
    default=0.0,
):
    """
    Safely convert a value to float.
    """

    try:

        if value is None:
            return default

        if isinstance(value, str):

            value = value.strip()

            if not value:
                return default

            value = value.replace(",", "")

        return float(value)

    except (
        TypeError,
        ValueError,
    ):

        return default


def safe_int(
    value,
    default=0,
):
    """
    Safely convert a value to integer.
    """

    try:

        if value is None:
            return default

        if isinstance(value, str):

            value = value.strip()

            if not value:
                return default

            value = value.replace(",", "")

        return int(float(value))

    except (
        TypeError,
        ValueError,
    ):

        return default


def _safe_text(
    value,
    default="",
):
    """
    Safely convert a value to text.
    """

    if value is None:
        return default

    return str(value).strip()


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database():
    """
    Initialize the central SQLite database.

    Delegates completely to library_store.py.
    """

    if library_store is None:
        return False

    function = getattr(
        library_store,
        "initialize_database",
        None,
    )

    if callable(function):

        return function()

    return False


def initialize_product_database():
    """
    Backward-compatible alias.
    """

    return initialize_database()


# ==========================================================
# PRODUCT ID
# ==========================================================

def generate_product_id(
    product=None,
):
    """
    Generate a unique product ID.

    If the product already has an ID,
    preserve it.
    """

    product = product or {}

    existing_id = product.get(
        "id"
    )

    if existing_id:

        return str(existing_id)

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )

    return (
        f"product_{timestamp}"
    )


# ==========================================================
# PRODUCT NORMALIZATION
# ==========================================================

def normalize_product(
    product=None,
):
    """
    Normalize a product into the common
    Solar PV Designer Pro structure.

    Additional fields are preserved.
    """

    if product is None:
        product = {}

    if not isinstance(
        product,
        dict,
    ):
        product = dict(product)

    source = dict(product)

    normalized = {

        "id":
            generate_product_id(
                source
            ),

        "name":
            _safe_text(
                source.get(
                    "name",
                    source.get(
                        "product_name",
                        "",
                    ),
                )
            ),

        "category":
            _safe_text(
                source.get(
                    "category",
                    "Other",
                ),
                "Other",
            ),

        "manufacturer":
            _safe_text(
                source.get(
                    "manufacturer",
                    "",
                )
            ),

        "model":
            _safe_text(
                source.get(
                    "model",
                    "",
                )
            ),

        "technology":
            _safe_text(
                source.get(
                    "technology",
                    "",
                )
            ),

        "rated_power_w":
            safe_float(
                source.get(
                    "rated_power_w",
                    source.get(
                        "power",
                        0,
                    ),
                )
            ),

        "voltage_v":
            safe_float(
                source.get(
                    "voltage_v",
                    source.get(
                        "voltage",
                        source.get(
                            "nominal_voltage_v",
                            0,
                        ),
                    ),
                )
            ),

        "current_a":
            safe_float(
                source.get(
                    "current_a",
                    source.get(
                        "current",
                        0,
                    ),
                )
            ),

        "capacity_ah":
            safe_float(
                source.get(
                    "capacity_ah",
                    0,
                )
            ),

        "energy_kwh":
            safe_float(
                source.get(
                    "energy_kwh",
                    0,
                )
            ),

        "efficiency_percent":
            safe_float(
                source.get(
                    "efficiency_percent",
                    source.get(
                        "efficiency",
                        0,
                    ),
                )
            ),

        "warranty_years":
            safe_float(
                source.get(
                    "warranty_years",
                    source.get(
                        "warranty",
                        0,
                    ),
                )
            ),

        "supplier":
            _safe_text(
                source.get(
                    "supplier",
                    "",
                )
            ),

        "country":
            _safe_text(
                source.get(
                    "country",
                    "",
                )
            ),

        "price":
            safe_float(
                source.get(
                    "price",
                    0,
                )
            ),

        "currency":
            _safe_text(
                source.get(
                    "currency",
                    "USD",
                ),
                "USD",
            ),

        "quantity":
            max(
                1,
                safe_int(
                    source.get(
                        "quantity",
                        1,
                    ),
                    1,
                ),
            ),

        "notes":
            _safe_text(
                source.get(
                    "notes",
                    "",
                )
            ),

        "specifications":
            deepcopy(
                source.get(
                    "specifications",
                    {},
                )
            ),
    }

    # ------------------------------------------------------
    # Preserve every additional field.
    # ------------------------------------------------------

    for key, value in source.items():

        if key not in normalized:

            normalized[key] = value

    return normalized


# ==========================================================
# PRODUCT CREATION
# ==========================================================

def create_product(
    **kwargs,
):
    """
    Create and normalize a product.

    This function does not save the product.
    """

    product = normalize_product(
        kwargs
    )

    validation = validate_product(
        product
    )

    if not validation["valid"]:

        return {

            "success":
                False,

            "message":
                validation["message"],

            "product":
                product,

            "errors":
                validation["errors"],
        }

    return product


# ==========================================================
# PRODUCT VALIDATION
# ==========================================================

def validate_product(
    product,
):
    """
    Validate a product before saving.
    """

    if not isinstance(
        product,
        dict,
    ):

        return {

            "valid":
                False,

            "message":
                "Product must be a dictionary.",

            "errors":
                [
                    "Invalid product data."
                ],
        }

    errors = []

    name = _safe_text(
        product.get(
            "name"
        )
    )

    category = _safe_text(
        product.get(
            "category",
            "Other",
        ),
        "Other",
    )

    if not name:

        errors.append(
            "Product name is required."
        )

    if not category:

        errors.append(
            "Product category is required."
        )

    # ------------------------------------------------------
    # Category-specific validation
    # ------------------------------------------------------

    if category == "Solar Panel":

        if safe_float(
            product.get(
                "rated_power_w"
            )
        ) <= 0:

            errors.append(
                "Solar panel rated power must be greater than zero."
            )

    elif category == "Battery":

        if safe_float(
            product.get(
                "capacity_ah"
            )
        ) <= 0:

            errors.append(
                "Battery capacity must be greater than zero."
            )

    elif category == "Inverter":

        if safe_float(
            product.get(
                "rated_power_w"
            )
        ) <= 0:

            errors.append(
                "Inverter rated power must be greater than zero."
            )

    elif category == "Charge Controller":

        specifications = (
            product.get(
                "specifications"
            )
            or {}
        )

        charge_current = safe_float(
            specifications.get(
                "max_charge_current_a",
                product.get(
                    "max_charge_current_a",
                    0,
                ),
            )
        )

        if charge_current <= 0:

            errors.append(
                "Charge-controller current must be greater than zero."
            )

    if errors:

        return {

            "valid":
                False,

            "message":
                errors[0],

            "errors":
                errors,
        }

    return {

        "valid":
            True,

        "message":
            "Product is valid.",

        "errors":
            [],
    }


def validate_category_fields(
    category,
    specifications,
):
    """
    Validate category-specific specifications.
    """

    specifications = (
        specifications
        if isinstance(
            specifications,
            dict,
        )
        else {}
    )

    errors = []

    if category == "Solar Panel":

        if safe_float(
            specifications.get(
                "rated_power_w",
                0,
            )
        ) <= 0:

            errors.append(
                "Solar panel rated power must be greater than zero."
            )

    elif category == "Battery":

        if safe_float(
            specifications.get(
                "capacity_ah",
                0,
            )
        ) <= 0:

            errors.append(
                "Battery capacity must be greater than zero."
            )

    elif category == "Inverter":

        if safe_float(
            specifications.get(
                "rated_power_w",
                0,
            )
        ) <= 0:

            errors.append(
                "Inverter rated power must be greater than zero."
            )

    elif category == "Charge Controller":

        if safe_float(
            specifications.get(
                "max_charge_current_a",
                0,
            )
        ) <= 0:

            errors.append(
                "Charge-controller charge current must be greater than zero."
            )

    return errors


# ==========================================================
# ADD PRODUCT
# ==========================================================

def add_product(
    product=None,
    **kwargs,
):
    """
    Add a product to the central SQLite library.

    Supports:

        add_product(product)

    and:

        add_product(
            name="550W Panel",
            category="Solar Panel",
        )
    """

    if product is None:

        product = kwargs

    elif isinstance(
        product,
        dict,
    ):

        merged = dict(product)

        merged.update(
            kwargs
        )

        product = merged

    else:

        return {

            "success":
                False,

            "message":
                "Product must be a dictionary.",
        }

    product = normalize_product(
        product
    )

    validation = validate_product(
        product
    )

    if not validation["valid"]:

        return {

            "success":
                False,

            "message":
                validation["message"],

            "errors":
                validation["errors"],

            "product":
                product,
        }

    if library_store is None:

        return {

            "success":
                False,

            "message":
                "library_store.py is unavailable.",
        }

    function = getattr(
        library_store,
        "add_product_to_library",
        None,
    )

    if not callable(function):

        return {

            "success":
                False,

            "message":
                "add_product_to_library() is unavailable.",
        }

    saved = function(
        product
    )

    # Keep the API useful for both old and new callers.
    if isinstance(
        saved,
        dict,
    ):

        return saved

    return product


# ==========================================================
# GET ALL PRODUCTS
# ==========================================================

def get_products():
    """
    Return all products from SQLite.
    """

    if library_store is None:

        return []

    initialize_database()

    function = getattr(
        library_store,
        "load_product_library",
        None,
    )

    if not callable(function):

        return []

    result = function()

    if result is None:

        return []

    if isinstance(
        result,
        dict,
    ):

        result = result.get(
            "products",
            result.get(
                "data",
                [],
            ),
        )

    if not isinstance(
        result,
        list,
    ):

        return []

    return [
        normalize_loaded_product(product)
        for product in result
        if isinstance(
            product,
            dict,
        )
    ]


def load_products():
    """
    Backward-compatible alias.
    """

    return get_products()


def list_products():
    """
    Backward-compatible alias.
    """

    return get_products()


def normalize_loaded_product(
    product,
):
    """
    Normalize a product loaded from SQLite
    without changing its database ID.
    """

    normalized = normalize_product(
        product
    )

    if product.get(
        "id"
    ) is not None:

        normalized["id"] = str(
            product["id"]
        )

    # Preserve timestamps from SQLite.
    if "created_at" in product:

        normalized[
            "created_at"
        ] = product[
            "created_at"
        ]

    if "updated_at" in product:

        normalized[
            "updated_at"
        ] = product[
            "updated_at"
        ]

    return normalized


# ==========================================================
# GET SINGLE PRODUCT
# ==========================================================

def get_product(
    product_id,
):
    """
    Retrieve one product by ID.
    """

    if not product_id:

        return None

    if library_store is None:

        return None

    function = getattr(
        library_store,
        "get_product_from_library",
        None,
    )

    if callable(function):

        result = function(
            product_id
        )

        if isinstance(
            result,
            dict,
        ):

            return normalize_loaded_product(
                result
            )

        if result is not None:

            return result

    # Fallback through loaded library.
    for product in get_products():

        if str(
            product.get(
                "id"
            )
        ) == str(
            product_id
        ):

            return product

    return None


# ==========================================================
# UPDATE PRODUCT
# ==========================================================

def update_product(
    product_id,
    updated_product=None,
    **kwargs,
):
    """
    Update an existing product.

    Supports both:

        update_product(id, product)

    and:

        update_product(
            id,
            name="New Name",
            price=200,
        )
    """

    if not product_id:

        return {

            "success":
                False,

            "message":
                "Product ID is required.",
        }

    existing = get_product(
        product_id
    )

    if existing is None:

        return {

            "success":
                False,

            "message":
                "Product not found.",
        }

    if updated_product is None:

        updated_product = {}

    if not isinstance(
        updated_product,
        dict,
    ):

        return {

            "success":
                False,

            "message":
                "Updated product must be a dictionary.",
        }

    merged = dict(
        existing
    )

    merged.update(
        updated_product
    )

    merged.update(
        kwargs
    )

    merged["id"] = str(
        product_id
    )

    normalized = normalize_product(
        merged
    )

    validation = validate_product(
        normalized
    )

    if not validation["valid"]:

        return {

            "success":
                False,

            "message":
                validation["message"],

            "errors":
                validation["errors"],
        }

    if library_store is None:

        return {

            "success":
                False,

            "message":
                "library_store.py is unavailable.",
        }

    function = getattr(
        library_store,
        "update_product_in_library",
        None,
    )

    if not callable(function):

        return {

            "success":
                False,

            "message":
                "update_product_in_library() is unavailable.",
        }

    result = function(
        product_id,
        normalized,
    )

    if result is True:

        return {

            "success":
                True,

            "message":
                "Product updated successfully.",

            "product":
                normalized,
        }

    if isinstance(
        result,
        dict,
    ):

        return result

    return {

        "success":
            bool(result),

        "message":
            (
                "Product updated successfully."
                if result
                else "Unable to update product."
            ),

        "product":
            normalized,
    }


def edit_product(
    product_id,
    updated_product=None,
    **kwargs,
):
    """
    Alias for update_product().
    """

    return update_product(
        product_id,
        updated_product,
        **kwargs,
    )


def update_product_in_library(
    product_id,
    updated_product,
):
    """
    Backward-compatible wrapper.
    """

    return update_product(
        product_id,
        updated_product,
    )


# ==========================================================
# DELETE PRODUCT
# ==========================================================

def delete_product(
    product_id,
):
    """
    Delete a product from SQLite.
    """

    if not product_id:

        return {

            "success":
                False,

            "message":
                "Product ID is required.",
        }

    if library_store is None:

        return {

            "success":
                False,

            "message":
                "library_store.py is unavailable.",
        }

    function = getattr(
        library_store,
        "remove_product_from_library",
        None,
    )

    if not callable(function):

        return {

            "success":
                False,

            "message":
                "remove_product_from_library() is unavailable.",
        }

    result = function(
        product_id
    )

    if isinstance(
        result,
        dict,
    ):

        return result

    return {

        "success":
            bool(result),

        "message":
            (
                "Product deleted successfully."
                if result
                else "Product was not found."
            ),
    }


def remove_product_from_library(
    product_id,
):
    """
    Backward-compatible alias.
    """

    return delete_product(
        product_id
    )


# ==========================================================
# SEARCH PRODUCTS
# ==========================================================

def search_products(
    products_or_query=None,
    query=None,
):
    """
    Flexible search function.

    Supported forms:

        search_products("550W")

        search_products(products, "550W")

    """

    if isinstance(
        products_or_query,
        list,
    ):

        products = products_or_query

        search_query = query

    else:

        products = get_products()

        search_query = (
            products_or_query
            if query is None
            else query
        )

    q = _safe_text(
        search_query
    ).lower()

    if not q:

        return list(
            products
        )

    results = []

    for product in products:

        if not isinstance(
            product,
            dict,
        ):

            continue

        searchable_fields = [

            product.get(
                "name",
                "",
            ),

            product.get(
                "category",
                "",
            ),

            product.get(
                "manufacturer",
                "",
            ),

            product.get(
                "model",
                "",
            ),

            product.get(
                "technology",
                "",
            ),

            product.get(
                "supplier",
                "",
            ),

            product.get(
                "country",
                "",
            ),

            product.get(
                "notes",
                "",
            ),
        ]

        searchable_text = " ".join(
            str(value)
            for value in searchable_fields
        )

        specifications = product.get(
            "specifications",
            {},
        )

        try:

            searchable_text += " "

            searchable_text += json.dumps(
                specifications,
                ensure_ascii=False,
            )

        except Exception:

            searchable_text += " "

            searchable_text += str(
                specifications
            )

        if q in searchable_text.lower():

            results.append(
                product
            )

    return results


def database_search_products(
    query="",
    category="All",
):
    """
    Database-backed product search.
    """

    products = get_products()

    if (
        category
        and category != "All"
    ):

        products = filter_products_by_category(
            products,
            category,
        )

    return search_products(
        products,
        query,
    )


def search_product_library(
    query="",
):
    """
    Compatibility wrapper.
    """

    return search_products(
        query
    )


# ==========================================================
# FILTER BY CATEGORY
# ==========================================================

def filter_products_by_category(
    products_or_category,
    category=None,
):
    """
    Flexible category filter.

    Supported forms:

        filter_products_by_category(
            products,
            "Solar Panel",
        )

        filter_products_by_category(
            "Solar Panel",
        )
    """

    if isinstance(
        products_or_category,
        list,
    ):

        products = products_or_category

        selected_category = category

    else:

        products = get_products()

        selected_category = (
            products_or_category
            if category is None
            else category
        )

    if (
        not selected_category
        or selected_category == "All"
    ):

        return list(
            products
        )

    return [

        product

        for product in products

        if str(
            product.get(
                "category",
                "Other",
            )
        ).strip().lower()
        ==
        str(
            selected_category
        ).strip().lower()
    ]


# ==========================================================
# FILTER BY TECHNOLOGY
# ==========================================================

def filter_products_by_technology(
    products_or_technology,
    technology=None,
):
    """
    Flexible technology filter.

    Supported forms:

        filter_products_by_technology(
            products,
            "Monocrystalline",
        )

        filter_products_by_technology(
            "Monocrystalline",
        )
    """

    if isinstance(
        products_or_technology,
        list,
    ):

        products = products_or_technology

        selected_technology = technology

    else:

        products = get_products()

        selected_technology = (
            products_or_technology
            if technology is None
            else technology
        )

    if (
        not selected_technology
        or selected_technology == "All"
    ):

        return list(
            products
        )

    return [

        product

        for product in products

        if str(
            product.get(
                "technology",
                "",
            )
        ).strip().lower()
        ==
        str(
            selected_technology
        ).strip().lower()
    ]


# ==========================================================
# REFRESH PRODUCT LIBRARY
# ==========================================================

def refresh_product_library():

    initialize_database()

    return get_products()


# ==========================================================
# DEFAULT PRODUCTS
# ==========================================================

DEFAULT_PRODUCTS = []


def get_default_products():
    """
    Return default products.

    Intentionally empty.

    The production application must not insert
    illustrative products into the user's real
    product library automatically.
    """

    return []


# ==========================================================
# LEGACY LIST-BASED ADD
# ==========================================================

def add_product_to_list(
    products,
    product,
):
    """
    Legacy helper that adds a product to
    an in-memory list without saving it.

    This is kept for older tests.
    """

    if not isinstance(
        products,
        list,
    ):

        products = []

    validation = validate_product(
        product
    )

    if not validation["valid"]:

        return {

            "success":
                False,

            "message":
                validation["message"],

            "products":
                products,
        }

    products.append(
        dict(product)
    )

    return {

        "success":
            True,

        "message":
            "Product added successfully.",

        "products":
            products,
    }


# ==========================================================
# LEGACY REMOVE PRODUCT
# ==========================================================

def remove_product(
    products,
    index,
):
    """
    Legacy in-memory list removal.

    NOTE:
    This function is deliberately different from
    delete_product(), which deletes a database record.
    """

    if not isinstance(
        products,
        list,
    ):

        return {

            "success":
                False,

            "message":
                "Product list is invalid.",

            "products":
                [],
        }

    try:

        index = int(
            index
        )

    except (
        TypeError,
        ValueError,
    ):

        return {

            "success":
                False,

            "message":
                "Invalid product index.",

            "products":
                products,
        }

    if (
        index < 0
        or index >= len(products)
    ):

        return {

            "success":
                False,

            "message":
                "Invalid product index.",

            "products":
                products,
        }

    removed = products.pop(
        index
    )

    return {

        "success":
            True,

        "message":
            "Product removed successfully.",

        "removed":
            removed,

        "products":
            products,
    }


# ==========================================================
# PRODUCT REQUIREMENT MATCHING
# ==========================================================

def match_product_requirement(
    product,
    required_power_w=None,
    required_energy_kwh=None,
    required_voltage_v=None,
):
    """
    Evaluate how well a product matches
    engineering requirements.

    Maximum score = 100.
    """

    if not isinstance(
        product,
        dict,
    ):

        return {

            "match":
                False,

            "score":
                0,

            "reasons":
                [
                    "Invalid product."
                ],
        }

    score = 0

    reasons = []

    # ------------------------------------------------------
    # POWER
    # ------------------------------------------------------

    if required_power_w is not None:

        required = safe_float(
            required_power_w
        )

        available = safe_float(
            product.get(
                "rated_power_w",
                0,
            )
        )

        if required > 0:

            if available >= required:

                score += 40

                reasons.append(
                    "Rated power meets or exceeds requirement."
                )

            elif available > 0:

                score += min(
                    40,
                    (
                        available
                        / required
                    )
                    * 40,
                )

                reasons.append(
                    "Rated power is below the required value."
                )

            else:

                reasons.append(
                    "Rated power is not specified."
                )

    # ------------------------------------------------------
    # ENERGY
    # ------------------------------------------------------

    if required_energy_kwh is not None:

        required = safe_float(
            required_energy_kwh
        )

        available = safe_float(
            product.get(
                "energy_kwh",
                0,
            )
        )

        if required > 0:

            if available >= required:

                score += 30

                reasons.append(
                    "Energy capacity meets or exceeds requirement."
                )

            elif available > 0:

                score += min(
                    30,
                    (
                        available
                        / required
                    )
                    * 30,
                )

                reasons.append(
                    "Energy capacity is below requirement."
                )

            else:

                reasons.append(
                    "Energy capacity is not specified."
                )

    # ------------------------------------------------------
    # VOLTAGE
    # ------------------------------------------------------

    if required_voltage_v is not None:

        required = safe_float(
            required_voltage_v
        )

        available = safe_float(
            product.get(
                "voltage_v",
                0,
            )
        )

        if required > 0:

            if available == required:

                score += 30

                reasons.append(
                    "Voltage matches requirement."
                )

            elif available > 0:

                difference = abs(
                    available
                    - required
                )

                tolerance = (
                    required
                    * 0.10
                )

                if difference <= tolerance:

                    score += 20

                    reasons.append(
                        "Voltage is within 10% of requirement."
                    )

                else:

                    reasons.append(
                        "Voltage does not match requirement."
                    )

            else:

                reasons.append(
                    "Voltage is not specified."
                )

    # ------------------------------------------------------
    # No engineering requirements supplied
    # ------------------------------------------------------

    if (
        required_power_w is None
        and required_energy_kwh is None
        and required_voltage_v is None
    ):

        score = 0

        reasons.append(
            "No engineering requirements were supplied."
        )

    return {

        "match":
            score >= 60,

        "score":
            round(
                score,
                2,
            ),

        "reasons":
            reasons,
    }


# ==========================================================
# RANK PRODUCTS
# ==========================================================

def rank_products(
    products,
    required_power_w=None,
    required_energy_kwh=None,
    required_voltage_v=None,
):
    """
    Rank products according to engineering requirements.
    """

    if not isinstance(
        products,
        list,
    ):

        return []

    ranked = []

    for product in products:

        if not isinstance(
            product,
            dict,
        ):

            continue

        evaluation = (
            match_product_requirement(
                product,
                required_power_w=
                    required_power_w,
                required_energy_kwh=
                    required_energy_kwh,
                required_voltage_v=
                    required_voltage_v,
            )
        )

        record = dict(
            product
        )

        record[
            "match_score"
        ] = evaluation[
            "score"
        ]

        record[
            "matches_requirement"
        ] = evaluation[
            "match"
        ]

        record[
            "match_reasons"
        ] = evaluation[
            "reasons"
        ]

        ranked.append(
            record
        )

    ranked.sort(
        key=lambda product:
            product.get(
                "match_score",
                0,
            ),
        reverse=True,
    )

    return ranked


# ==========================================================
# PRODUCT COMPARISON
# ==========================================================

def compare_products(
    products,
):
    """
    Prepare products for side-by-side comparison.

    This is a backend function and does not import
    Streamlit.
    """

    if not isinstance(
        products,
        list,
    ):

        return []

    comparison = []

    for product in products:

        if not isinstance(
            product,
            dict,
        ):

            continue

        row = {

            "id":
                product.get(
                    "id",
                    "",
                ),

            "name":
                product.get(
                    "name",
                    "N/A",
                ),

            "manufacturer":
                product.get(
                    "manufacturer",
                    "N/A",
                ),

            "model":
                product.get(
                    "model",
                    "N/A",
                ),

            "category":
                product.get(
                    "category",
                    "N/A",
                ),

            "technology":
                product.get(
                    "technology",
                    "N/A",
                ),

            "power_w":
                product.get(
                    "rated_power_w",
                    0,
                ),

            "voltage_v":
                product.get(
                    "voltage_v",
                    0,
                ),

            "current_a":
                product.get(
                    "current_a",
                    0,
                ),

            "capacity_ah":
                product.get(
                    "capacity_ah",
                    0,
                ),

            "energy_kwh":
                product.get(
                    "energy_kwh",
                    0,
                ),

            "efficiency_percent":
                product.get(
                    "efficiency_percent",
                    0,
                ),

            "warranty_years":
                product.get(
                    "warranty_years",
                    0,
                ),

            "price":
                product.get(
                    "price",
                    0,
                ),

            "currency":
                product.get(
                    "currency",
                    "USD",
                ),

            "quantity":
                product.get(
                    "quantity",
                    0,
                ),
        }

        specifications = product.get(
            "specifications",
            {},
        )

        if isinstance(
            specifications,
            dict,
        ):

            for key, value in specifications.items():

                if key not in row:

                    row[key] = value

        comparison.append(
            row
        )

    return comparison


# ==========================================================
# PRODUCT COMPARISON BY IDs
# ==========================================================

def compare_product_ids(
    product_ids,
):
    """
    Retrieve products using IDs and compare them.
    """

    if not product_ids:

        return []

    products = get_products()

    selected = []

    wanted = {

        str(product_id)

        for product_id in product_ids
    }

    for product in products:

        if str(
            product.get(
                "id"
            )
        ) in wanted:

            selected.append(
                product
            )

    return compare_products(
        selected
    )


# ==========================================================
# PRODUCT SUMMARY
# ==========================================================

def create_product_summary(
    products,
):
    """
    Create a summary of a product collection.
    """

    if not isinstance(
        products,
        list,
    ):

        products = []

    categories = {}

    technologies = {}

    total_quantity = 0

    total_value = 0.0

    for product in products:

        if not isinstance(
            product,
            dict,
        ):

            continue

        category = (
            _safe_text(
                product.get(
                    "category",
                    "Other",
                ),
                "Other",
            )
            or "Other"
        )

        technology = (
            _safe_text(
                product.get(
                    "technology",
                    "",
                )
            )
            or "Unspecified"
        )

        categories[
            category
        ] = (
            categories.get(
                category,
                0,
            )
            + 1
        )

        technologies[
            technology
        ] = (
            technologies.get(
                technology,
                0,
            )
            + 1
        )

        quantity = safe_int(
            product.get(
                "quantity",
                1,
            ),
            1,
        )

        price = safe_float(
            product.get(
                "price",
                0,
            )
        )

        total_quantity += quantity

        total_value += (
            price
            * quantity
        )

    return {

        "total_products":
            len(
                products
            ),

        "total_quantity":
            total_quantity,

        "total_inventory_value":
            round(
                total_value,
                2,
            ),

        "categories":
            categories,

        "technologies":
            technologies,

        "product_categories":
            categories,
    }


# ==========================================================
# PRODUCT ANALYSIS
# ==========================================================

def analyze_products(
    products,
    search_query="",
    category="",
    technology="",
    required_power_w=None,
    required_energy_kwh=None,
    required_voltage_v=None,
):
    """
    Complete product analysis pipeline.
    """

    if not isinstance(
        products,
        list,
    ):

        products = []

    working_products = list(
        products
    )

    if search_query:

        working_products = (
            search_products(
                working_products,
                search_query,
            )
        )

    if category:

        working_products = (
            filter_products_by_category(
                working_products,
                category,
            )
        )

    if technology:

        working_products = (
            filter_products_by_technology(
                working_products,
                technology,
            )
        )

    ranked = rank_products(

        working_products,

        required_power_w=
            required_power_w,

        required_energy_kwh=
            required_energy_kwh,

        required_voltage_v=
            required_voltage_v,
    )

    return {

        "success":
            True,

        "products_found":
            len(
                ranked
            ),

        "products":
            ranked,

        "comparison":
            compare_products(
                ranked
            ),

        "summary":
            create_product_summary(
                working_products
            ),
    }


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

def get_library_summary():
    """
    Return central library summary.
    """

    if library_store is not None:

        function = getattr(
            library_store,
            "get_library_summary",
            None,
        )

        if callable(function):

            try:

                return function()

            except Exception:

                pass

    products = get_products()

    summary = create_product_summary(
        products
    )

    summary[
        "total_services"
    ] = 0

    summary[
        "database_file"
    ] = (
        str(DB_PATH)
        if DB_PATH is not None
        else ""
    )

    return summary


def get_product_library_summary():
    """
    Product-only summary.
    """

    if library_store is not None:

        function = getattr(
            library_store,
            "get_product_library_summary",
            None,
        )

        if callable(function):

            try:

                return function()

            except Exception:

                pass

    products = get_products()

    return create_product_summary(
        products
    )


# ==========================================================
# DATABASE BACKUP
# ==========================================================

def backup_library():
    """
    Create a database backup.
    """

    if library_store is None:

        return None

    function = getattr(
        library_store,
        "backup_library",
        None,
    )

    if callable(function):

        return function()

    return None


def backup_database():
    """
    Backward-compatible alias.
    """

    return backup_library()


# ==========================================================
# CLEAR PRODUCT LIBRARY
# ==========================================================

def clear_product_library():
    """
    Delete all products from the central library.
    """

    if library_store is None:

        return False

    function = getattr(
        library_store,
        "clear_product_library",
        None,
    )

    if callable(function):

        return function()

    return False


# ==========================================================
# SAVE PRODUCT LIBRARY
# ==========================================================

def save_product_library(
    products,
):
    """
    Replace the central product library.
    """

    if library_store is None:

        return False

    function = getattr(
        library_store,
        "save_product_library",
        None,
    )

    if not callable(function):

        return False

    return function(
        products or []
    )


# ==========================================================
# PRODUCT DETAILS DATA
# ==========================================================

def product_details_data(
    product_id,
):
    """
    Return a single complete product record.
    """

    return get_product(
        product_id
    )


# ==========================================================
# PRODUCT COST
# ==========================================================

def calculate_product_inventory_value(
    product,
):
    """
    Calculate inventory value:

        price × quantity
    """

    if not isinstance(
        product,
        dict,
    ):

        return 0.0

    price = safe_float(
        product.get(
            "price",
            0,
        )
    )

    quantity = safe_int(
        product.get(
            "quantity",
            1,
        ),
        1,
    )

    return round(
        price * quantity,
        2,
    )


# ==========================================================
# PRODUCT NAME LIST
# ==========================================================

def get_product_names():
    """
    Return product names from the central library.
    """

    return [

        product.get(
            "name",
            "",
        )

        for product in get_products()

        if product.get(
            "name"
        )
    ]


# ==========================================================
# PRODUCT CATEGORIES
# ==========================================================

def get_product_categories():
    """
    Return categories actually present in the library.
    """

    categories = []

    for product in get_products():

        category = product.get(
            "category"
        )

        if category and category not in categories:

            categories.append(
                category
            )

    return sorted(
        categories
    )


# ==========================================================
# PRODUCT TECHNOLOGIES
# ==========================================================

def get_product_technologies():
    """
    Return technologies actually present in the library.
    """

    technologies = []

    for product in get_products():

        technology = product.get(
            "technology"
        )

        if (
            technology
            and technology not in technologies
        ):

            technologies.append(
                technology
            )

    return sorted(
        technologies
    )


# ==========================================================
# MODULE INITIALIZATION
# ==========================================================

# Initialize the central database when this module is
# imported. No product records are inserted.
initialize_database()
