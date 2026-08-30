"""
==========================================================
SOLAR PV DESIGNER PRO AFRICA™
PRODUCT ENGINE
==========================================================

Engineering/service layer between the Product UI and the
central SQLite Product Library.

Storage authority:
    library_store.py
        ↓
    app/data/solar_pv_library.db

This module does NOT maintain a second product database.
==========================================================
"""

from copy import deepcopy


# ==========================================================
# CENTRAL STORAGE
# ==========================================================

try:
    from library_store import (
        initialize_database,
        load_product_library,
        add_product_to_library,
        update_product_in_library,
        remove_product_from_library,
        get_product_from_library,
        search_product_library,
        get_product_library_summary,
        backup_library,
    )
except Exception as exc:
    initialize_database = None
    load_product_library = None
    add_product_to_library = None
    update_product_in_library = None
    remove_product_from_library = None
    get_product_from_library = None
    search_product_library = None
    get_product_library_summary = None
    backup_library = None

    _STORAGE_IMPORT_ERROR = exc
else:
    _STORAGE_IMPORT_ERROR = None


# ==========================================================
# PRODUCT CATEGORIES
# ==========================================================

PRODUCT_CATEGORIES = [
    "Solar Panel",
    "Battery",
    "Inverter",
    "Charge Controller",
    "Mounting Structure",
    "Solar Cable",
    "Protection",
    "Labour & Services",
    "Transport & Logistics",
    "Other",
]


# ==========================================================
# PRODUCT TECHNOLOGIES
# ==========================================================

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


# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

def safe_float(value, default=0.0):
    """Safely convert a value to float."""

    try:
        if value is None or value == "":
            return float(default)

        return float(value)

    except (TypeError, ValueError):
        return float(default)


def safe_int(value, default=0):
    """Safely convert a value to integer."""

    try:
        if value is None or value == "":
            return int(default)

        return int(float(value))

    except (TypeError, ValueError):
        return int(default)


def _storage_ready():
    """Return True when the storage engine is available."""

    return (
        _STORAGE_IMPORT_ERROR is None
        and callable(initialize_database)
    )


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_product_database():
    """
    Initialize the central SQLite database.
    """

    if not _storage_ready():
        return False

    try:
        return bool(
            initialize_database()
        )

    except Exception:
        return False


# ==========================================================
# NORMALIZATION
# ==========================================================

def normalize_product(product):
    """
    Normalize a product without destroying category-specific
    specifications.
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
        "warranty_years": 0.0,

        "price": 0.0,
        "currency": "USD",
        "quantity": 1,

        "supplier": "",
        "country": "",
        "notes": "",

        "specifications": {},
    }

    for key, default in defaults.items():

        if key not in item:
            item[key] = default

    if not isinstance(
        item.get("specifications"),
        dict
    ):
        item["specifications"] = {}

    item["name"] = str(
        item.get("name", "")
    ).strip()

    item["category"] = str(
        item.get("category", "Other")
    ).strip() or "Other"

    item["manufacturer"] = str(
        item.get("manufacturer", "")
    ).strip()

    item["model"] = str(
        item.get("model", "")
    ).strip()

    item["technology"] = str(
        item.get("technology", "Other")
    ).strip() or "Other"

    item["supplier"] = str(
        item.get("supplier", "")
    ).strip()

    item["country"] = str(
        item.get("country", "")
    ).strip()

    item["notes"] = str(
        item.get("notes", "")
    ).strip()

    item["rated_power_w"] = safe_float(
        item.get("rated_power_w")
    )

    item["voltage_v"] = safe_float(
        item.get("voltage_v")
    )

    item["current_a"] = safe_float(
        item.get("current_a")
    )

    item["capacity_ah"] = safe_float(
        item.get("capacity_ah")
    )

    item["energy_kwh"] = safe_float(
        item.get("energy_kwh")
    )

    item["efficiency_percent"] = safe_float(
        item.get("efficiency_percent")
    )

    item["warranty_years"] = safe_float(
        item.get("warranty_years")
    )

    item["price"] = safe_float(
        item.get("price")
    )

    item["quantity"] = safe_float(
        item.get("quantity"),
        1
    )

    item["currency"] = str(
        item.get("currency", "USD")
    ).strip() or "USD"

    return item


# ==========================================================
# VALIDATION
# ==========================================================

def validate_product(product):
    """
    Validate a product before it enters the library.
    """

    product = normalize_product(product)

    errors = []

    if not product.get("name"):
        errors.append(
            "Product name is required."
        )

    category = product.get(
        "category",
        "Other"
    )

    specs = product.get(
        "specifications",
        {}
    )

    if category == "Solar Panel":

        power = safe_float(
            specs.get(
                "rated_power_w",
                product.get(
                    "rated_power_w",
                    0
                )
            )
        )

        if power <= 0:
            errors.append(
                "Solar panel rated power must be greater than zero."
            )

    elif category == "Battery":

        capacity = safe_float(
            specs.get(
                "capacity_ah",
                product.get(
                    "capacity_ah",
                    0
                )
            )
        )

        if capacity <= 0:
            errors.append(
                "Battery capacity must be greater than zero."
            )

    elif category == "Inverter":

        power = safe_float(
            specs.get(
                "rated_power_w",
                product.get(
                    "rated_power_w",
                    0
                )
            )
        )

        if power <= 0:
            errors.append(
                "Inverter rated power must be greater than zero."
            )

    elif category == "Charge Controller":

        current = safe_float(
            specs.get(
                "max_charge_current_a",
                0
            )
        )

        if current <= 0:
            errors.append(
                "Charge-controller current must be greater than zero."
            )

    return {
        "valid": len(errors) == 0,
        "message": (
            "Product is valid."
            if not errors
            else " ".join(errors)
        ),
        "errors": errors,
        "product": product,
    }


# ==========================================================
# CREATE PRODUCT
# ==========================================================

def create_product(**kwargs):
    """
    Build and validate a product record.

    This function does not automatically write to SQLite.
    Use add_product() to persist it.
    """

    product = normalize_product(
        kwargs
    )

    validation = validate_product(
        product
    )

    if not validation["valid"]:

        return {
            "success": False,
            "message": validation["message"],
            "product": None,
        }

    return {
        "success": True,
        "message": "Product created successfully.",
        "product": product,
    }


# ==========================================================
# GET PRODUCTS
# ==========================================================

def get_products():
    """
    Return all products from the central SQLite library.
    """

    if not _storage_ready():
        return []

    try:

        initialize_product_database()

        products = load_product_library()

        if not isinstance(products, list):
            return []

        return [
            normalize_product(product)
            for product in products
            if isinstance(product, dict)
        ]

    except Exception:
        return []


# ==========================================================
# GET PRODUCT
# ==========================================================

def get_product(product_id):
    """
    Retrieve one product by its database ID.
    """

    if not _storage_ready():
        return None

    try:

        initialize_product_database()

        product = get_product_from_library(
            product_id
        )

        if product is None:
            return None

        return normalize_product(
            product
        )

    except Exception:
        return None


# ==========================================================
# ADD PRODUCT
# ==========================================================

def add_product(product):
    """
    Validate and persist a product in SQLite.
    """

    validation = validate_product(
        product
    )

    if not validation["valid"]:

        return {
            "success": False,
            "message": validation["message"],
            "product": None,
        }

    if not _storage_ready():

        return {
            "success": False,
            "message": "Product storage engine is unavailable.",
            "product": None,
        }

    try:

        initialize_product_database()

        saved = add_product_to_library(
            validation["product"]
        )

        if isinstance(saved, dict):

            return {
                "success": True,
                "message": "Product added successfully.",
                "product": saved,
            }

        return {
            "success": True,
            "message": "Product added successfully.",
            "product": validation["product"],
        }

    except Exception as exc:

        return {
            "success": False,
            "message": str(exc),
            "product": None,
        }


# ==========================================================
# UPDATE PRODUCT
# ==========================================================

def update_product(
    product_id,
    product=None,
    **kwargs,
):
    """
    Update an existing SQLite product.
    """

    if product is None:
        product = {}

    if kwargs:
        merged = dict(product)
        merged.update(kwargs)
        product = merged

    existing = get_product(
        product_id
    )

    if existing is None:

        return {
            "success": False,
            "message": "Product not found.",
        }

    merged = dict(existing)

    merged.update(
        product
    )

    merged["id"] = str(
        product_id
    )

    validation = validate_product(
        merged
    )

    if not validation["valid"]:

        return {
            "success": False,
            "message": validation["message"],
        }

    if not _storage_ready():

        return {
            "success": False,
            "message": "Product storage engine is unavailable.",
        }

    try:

        initialize_product_database()

        result = update_product_in_library(
            product_id,
            validation["product"]
        )

        if isinstance(result, bool):

            success = result

        elif isinstance(result, dict):

            success = result.get(
                "success",
                True
            )

        else:

            success = True

        return {
            "success": bool(success),
            "message": (
                "Product updated successfully."
                if success
                else "Unable to update product."
            ),
            "product": validation["product"],
        }

    except Exception as exc:

        return {
            "success": False,
            "message": str(exc),
        }


# ==========================================================
# DELETE PRODUCT
# ==========================================================

def delete_product(product_id, **kwargs):
    """
    Permanently remove a product from SQLite.
    """

    if not _storage_ready():

        return {
            "success": False,
            "message": "Product storage engine is unavailable.",
        }

    try:

        initialize_product_database()

        deleted = remove_product_from_library(
            product_id
        )

        if isinstance(deleted, dict):
            success = deleted.get(
                "success",
                False
            )
        else:
            success = bool(
                deleted
            )

        return {
            "success": success,
            "message": (
                "Product deleted successfully."
                if success
                else "Product was not found."
            ),
        }

    except Exception as exc:

        return {
            "success": False,
            "message": str(exc),
        }


# ==========================================================
# SEARCH
# ==========================================================

def search_products(
    products=None,
    query="",
):
    """
    Search a supplied product list.

    If products is omitted, search the central library.
    """

    if products is None:

        products = get_products()

    if not isinstance(products, list):
        return []

    query = str(
        query or ""
    ).strip().lower()

    if not query:
        return list(products)

    results = []

    for product in products:

        if not isinstance(
            product,
            dict
        ):
            continue

        searchable = " ".join(
            [
                str(product.get("name", "")),
                str(product.get("category", "")),
                str(product.get("manufacturer", "")),
                str(product.get("model", "")),
                str(product.get("technology", "")),
                str(product.get("supplier", "")),
                str(product.get("country", "")),
                str(product.get("notes", "")),
                str(product.get("specifications", "")),
            ]
        ).lower()

        if query in searchable:
            results.append(product)

    return results


def database_search_products(
    query="",
    category="All",
):
    """
    Search directly against the central product library.
    """

    products = get_products()

    if category and category != "All":

        products = filter_products_by_category(
            products,
            category
        )

    return search_products(
        products,
        query
    )


# ==========================================================
# FILTER BY CATEGORY
# ==========================================================

def filter_products_by_category(
    products,
    category,
):
    """Filter products by category."""

    if not isinstance(products, list):
        return []

    category = str(
        category or ""
    ).strip().lower()

    return [
        product
        for product in products
        if str(
            product.get(
                "category",
                ""
            )
        ).strip().lower()
        == category
    ]


# ==========================================================
# FILTER BY TECHNOLOGY
# ==========================================================

def filter_products_by_technology(
    products,
    technology,
):
    """Filter products by technology."""

    if not isinstance(products, list):
        return []

    technology = str(
        technology or ""
    ).strip().lower()

    return [
        product
        for product in products
        if str(
            product.get(
                "technology",
                ""
            )
        ).strip().lower()
        == technology
    ]


# ==========================================================
# PRODUCT NAMES
# ==========================================================

def get_product_names(
    products=None
):
    """Return product names."""

    if products is None:
        products = get_products()

    if not isinstance(products, list):
        return []

    return [
        str(product.get("name"))
        for product in products
        if isinstance(product, dict)
        and product.get("name")
    ]


# ==========================================================
# CATEGORY PRODUCTS
# ==========================================================

def get_products_by_category(
    category
):
    """Return all products in one category."""

    return filter_products_by_category(
        get_products(),
        category
    )


def get_solar_panels():
    """Return solar panels."""

    return get_products_by_category(
        "Solar Panel"
    )


def get_batteries():
    """Return batteries."""

    return get_products_by_category(
        "Battery"
    )


def get_inverters():
    """Return inverters."""

    return get_products_by_category(
        "Inverter"
    )


def get_charge_controllers():
    """Return charge controllers."""

    return get_products_by_category(
        "Charge Controller"
    )


# ==========================================================
# PRODUCT SELECTION
# ==========================================================

def get_product_options(
    category=None
):
    """
    Return products suitable for a Streamlit selectbox.
    """

    products = (
        get_products()
        if category is None
        else get_products_by_category(category)
    )

    return [
        {
            "id": product.get("id"),
            "name": product.get(
                "name",
                "Unnamed Product"
            ),
            "model": product.get(
                "model",
                ""
            ),
            "manufacturer": product.get(
                "manufacturer",
                ""
            ),
            "category": product.get(
                "category",
                "Other"
            ),
        }
        for product in products
    ]


# ==========================================================
# ENGINEERING HELPERS
# ==========================================================

def get_panel_power_w(
    product
):
    """
    Return usable panel rated power.
    """

    if not isinstance(product, dict):
        return 0.0

    specs = product.get(
        "specifications",
        {}
    )

    return safe_float(
        specs.get(
            "rated_power_w",
            product.get(
                "rated_power_w",
                0
            )
        )
    )


def get_panel_vmp_v(
    product
):
    """Return panel Vmp."""

    if not isinstance(product, dict):
        return 0.0

    specs = product.get(
        "specifications",
        {}
    )

    return safe_float(
        specs.get(
            "vmp_v",
            product.get(
                "voltage_v",
                0
            )
        )
    )


def get_panel_voc_v(
    product
):
    """Return panel Voc."""

    if not isinstance(product, dict):
        return 0.0

    specs = product.get(
        "specifications",
        {}
    )

    return safe_float(
        specs.get(
            "voc_v",
            0
        )
    )


def get_battery_voltage_v(
    product
):
    """Return battery nominal voltage."""

    if not isinstance(product, dict):
        return 0.0

    specs = product.get(
        "specifications",
        {}
    )

    return safe_float(
        specs.get(
            "nominal_voltage_v",
            product.get(
                "voltage_v",
                0
            )
        )
    )


def get_battery_capacity_ah(
    product
):
    """Return battery capacity."""

    if not isinstance(product, dict):
        return 0.0

    specs = product.get(
        "specifications",
        {}
    )

    return safe_float(
        specs.get(
            "capacity_ah",
            product.get(
                "capacity_ah",
                0
            )
        )
    )


def get_inverter_power_w(
    product
):
    """Return inverter rated output power."""

    if not isinstance(product, dict):
        return 0.0

    specs = product.get(
        "specifications",
        {}
    )

    return safe_float(
        specs.get(
            "rated_power_w",
            product.get(
                "rated_power_w",
                0
            )
        )
    )


# ==========================================================
# PRODUCT REQUIREMENT MATCHING
# ==========================================================

def product_matches_requirements(
    product,
    required_power_w=None,
    required_energy_kwh=None,
    required_voltage_v=None,
):
    """
    Determine whether a product meets basic engineering
    requirements.
    """

    if not isinstance(product, dict):
        return False

    if required_power_w is not None:

        power = get_panel_power_w(
            product
        )

        if power < safe_float(
            required_power_w
        ):
            return False

    if required_energy_kwh is not None:

        energy = safe_float(
            product.get(
                "energy_kwh",
                0
            )
        )

        if energy < safe_float(
            required_energy_kwh
        ):
            return False

    if required_voltage_v is not None:

        voltage = (
            get_battery_voltage_v(
                product
            )
        )

        if voltage <= 0:
            voltage = safe_float(
                product.get(
                    "voltage_v",
                    0
                )
            )

        if voltage <= 0:
            return False

        if abs(
            voltage
            - safe_float(required_voltage_v)
        ) > max(
            5.0,
            safe_float(required_voltage_v) * 0.15
        ):
            return False

    return True


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
    Rank products by closeness to engineering requirements.
    """

    if not isinstance(products, list):
        return []

    ranked = []

    for product in products:

        item = dict(
            product
        )

        score = 0.0

        if required_power_w is not None:

            power = get_panel_power_w(
                product
            )

            target = safe_float(
                required_power_w
            )

            if target > 0:
                score += abs(
                    power - target
                ) / target

        if required_energy_kwh is not None:

            energy = safe_float(
                product.get(
                    "energy_kwh",
                    0
                )
            )

            target = safe_float(
                required_energy_kwh
            )

            if target > 0:
                score += abs(
                    energy - target
                ) / target

        if required_voltage_v is not None:

            voltage = safe_float(
                product.get(
                    "voltage_v",
                    0
                )
            )

            target = safe_float(
                required_voltage_v
            )

            if target > 0:
                score += abs(
                    voltage - target
                ) / target

        item["_match_score"] = score

        ranked.append(
            item
        )

    ranked.sort(
        key=lambda item:
        item.get(
            "_match_score",
            999999
        )
    )

    return ranked


# ==========================================================
# ANALYZE PRODUCTS
# ==========================================================

def analyze_products(
    products=None,
    search_query="",
    category="",
    technology="",
    required_power_w=None,
    required_energy_kwh=None,
    required_voltage_v=None,
):
    """
    Complete product search, filtering and ranking operation.
    """

    if products is None:
        products = get_products()

    working = list(
        products
        if isinstance(products, list)
        else []
    )

    if search_query:

        working = search_products(
            working,
            search_query
        )

    if category:

        working = filter_products_by_category(
            working,
            category
        )

    if technology:

        working = filter_products_by_technology(
            working,
            technology
        )

    ranked = rank_products(
        working,
        required_power_w=
            required_power_w,
        required_energy_kwh=
            required_energy_kwh,
        required_voltage_v=
            required_voltage_v,
    )

    return {
        "success": True,
        "products_found": len(ranked),
        "products": ranked,
        "comparison": compare_products(
            ranked
        ),
    }


# ==========================================================
# PRODUCT COMPARISON
# ==========================================================

def compare_products(
    products=None
):
    """
    Produce a normalized comparison dataset.
    """

    if products is None:
        products = get_products()

    if not isinstance(products, list):
        products = []

    rows = []

    for product in products:

        if not isinstance(product, dict):
            continue

        specs = product.get(
            "specifications",
            {}
        )

        if not isinstance(specs, dict):
            specs = {}

        row = {
            "id":
                product.get("id"),

            "name":
                product.get("name"),

            "category":
                product.get("category"),

            "manufacturer":
                product.get("manufacturer"),

            "model":
                product.get("model"),

            "technology":
                product.get("technology"),

            "rated_power_w":
                get_panel_power_w(
                    product
                ),

            "voltage_v":
                product.get(
                    "voltage_v",
                    0
                ),

            "capacity_ah":
                get_battery_capacity_ah(
                    product
                ),

            "energy_kwh":
                product.get(
                    "energy_kwh",
                    0
                ),

            "efficiency_percent":
                product.get(
                    "efficiency_percent",
                    0
                ),

            "price":
                product.get(
                    "price",
                    0
                ),

            "currency":
                product.get(
                    "currency",
                    "USD"
                ),
        }

        row.update(
            specs
        )

        rows.append(
            row
        )

    return rows


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

def get_product_summary():
    """
    Return summary information from the central database.
    """

    if not _storage_ready():
        return {
            "total_products": 0,
            "total_quantity": 0,
            "product_categories": {},
        }

    try:

        initialize_product_database()

        summary = get_product_library_summary()

        if isinstance(summary, dict):
            return summary

    except Exception:
        pass

    products = get_products()

    categories = {}

    quantity = 0

    for product in products:

        category = product.get(
            "category",
            "Other"
        )

        categories[category] = (
            categories.get(
                category,
                0
            )
            + 1
        )

        quantity += safe_float(
            product.get(
                "quantity",
                1
            ),
            1
        )

    return {
        "total_products": len(products),
        "total_quantity": quantity,
        "product_categories": categories,
    }


# ==========================================================
# BACKUP
# ==========================================================

def backup_product_database():
    """
    Create a backup using library_store.py.
    """

    if not callable(
        backup_library
    ):
        return {
            "success": False,
            "message": "Backup function unavailable.",
        }

    try:

        result = backup_library()

        if isinstance(result, dict):
            return result

        return {
            "success": True,
            "backup": result,
        }

    except Exception as exc:

        return {
            "success": False,
            "message": str(exc),
        }


# ==========================================================
# MODULE STATUS
# ==========================================================

def get_engine_status():
    """
    Diagnostic information for testing.
    """

    return {
        "storage_available":
            _storage_import_error_is_none(),

        "database_initialized":
            initialize_product_database(),

        "products":
            len(get_products()),

        "categories":
            PRODUCT_CATEGORIES,
    }


def _storage_import_error_is_none():
    return (
        _STORAGE_IMPORT_ERROR is None
    )


# ==========================================================
# BACKWARD COMPATIBILITY
# ==========================================================

def remove_product(
    products,
    index,
):
    """
    Legacy in-memory helper retained so older tests do not
    immediately fail.

    This does NOT delete from SQLite.
    Use delete_product(product_id) for database deletion.
    """

    if not isinstance(
        products,
        list
    ):

        return {
            "success": False,
            "message": "Product list is invalid.",
            "products": [],
        }

    try:
        index = int(index)

    except (
        TypeError,
        ValueError
    ):

        return {
            "success": False,
            "message": "Invalid product index.",
            "products": products,
        }

    if index < 0 or index >= len(products):

        return {
            "success": False,
            "message": "Invalid product index.",
            "products": products,
        }

    removed = products.pop(
        index
    )

    return {
        "success": True,
        "message": "Product removed successfully.",
        "removed": removed,
        "products": products,
    }


# ==========================================================
# INITIALIZE ON IMPORT
# ==========================================================

initialize_product_database()
