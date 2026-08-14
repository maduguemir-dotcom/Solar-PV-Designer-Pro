# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Product Engine
# Version: 2.4.0
# ==========================================================
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Maintain, validate, search and compare solar products.
#
# This module does NOT perform PV sizing.
# It connects engineering requirements with products
# that can later be linked to the Cost Diary and AI Advisor.
# ==========================================================


# ==========================================================
# SECTION 1 - PRODUCT CATEGORIES
# ==========================================================

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


# ==========================================================
# SECTION 2 - TECHNOLOGIES
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
# SECTION 3 - SAFE CONVERSION
# ==========================================================

def safe_float(value, default=None):

    try:

        if value is None:
            return default

        number = float(value)

        if number != number:
            return default

        return number

    except (TypeError, ValueError):

        return default


# ==========================================================
# SECTION 4 - PRODUCT VALIDATION
# ==========================================================

def validate_product(product):

    if not isinstance(product, dict):

        return {
            "valid": False,
            "message": "Product must be a dictionary.",
        }

    name = str(
        product.get("name", "")
    ).strip()

    category = str(
        product.get("category", "")
    ).strip()

    if not name:

        return {
            "valid": False,
            "message": "Product name is required.",
        }

    if not category:

        return {
            "valid": False,
            "message": "Product category is required.",
        }

    if category not in PRODUCT_CATEGORIES:

        return {
            "valid": False,
            "message":
                f"Unsupported product category: {category}",
        }

    return {
        "valid": True,
        "message": "Product is valid.",
    }


# ==========================================================
# SECTION 5 - CREATE PRODUCT
# ==========================================================

def create_product(
    name,
    category,
    manufacturer="",
    model="",
    technology="",
    rated_power_w=0,
    voltage_v=0,
    capacity_ah=0,
    energy_kwh=0,
    efficiency_percent=0,
    warranty_years=0,
    supplier="",
    country="",
    notes="",
):
    """
    Create a standardized product record.

    Different product categories use different technical
    fields. Unused fields remain zero.
    """

    product = {

        "name":
            str(name).strip(),

        "category":
            str(category).strip(),

        "manufacturer":
            str(manufacturer).strip(),

        "model":
            str(model).strip(),

        "technology":
            str(technology).strip(),

        "rated_power_w":
            safe_float(
                rated_power_w,
                0.0
            ),

        "voltage_v":
            safe_float(
                voltage_v,
                0.0
            ),

        "capacity_ah":
            safe_float(
                capacity_ah,
                0.0
            ),

        "energy_kwh":
            safe_float(
                energy_kwh,
                0.0
            ),

        "efficiency_percent":
            safe_float(
                efficiency_percent,
                0.0
            ),

        "warranty_years":
            safe_float(
                warranty_years,
                0.0
            ),

        "supplier":
            str(supplier).strip(),

        "country":
            str(country).strip(),

        "notes":
            str(notes).strip(),

    }

    validation = validate_product(
        product
    )

    if not validation["valid"]:

        return {
            "success": False,
            "message":
                validation["message"],
            "product": None,
        }

    return {

        "success": True,

        "message":
            "Product created successfully.",

        "product":
            product,

    }


# ==========================================================
# SECTION 6 - GET PRODUCT NAMES
# ==========================================================

def get_product_names(products):

    if not isinstance(
        products,
        list
    ):

        return []

    return [

        product.get(
            "name"
        )

        for product in products

        if isinstance(
            product,
            dict
        )

        and product.get(
            "name"
        )

    ]


# ==========================================================
# SECTION 7 - FILTER BY CATEGORY
# ==========================================================

def filter_products_by_category(
    products,
    category,
):

    if not isinstance(
        products,
        list
    ):

        return []

    category = str(
        category
    ).strip().lower()

    return [

        product

        for product in products

        if isinstance(
            product,
            dict
        )

        and str(
            product.get(
                "category",
                ""
            )
        ).strip().lower()
        == category

    ]


# ==========================================================
# SECTION 8 - FILTER BY TECHNOLOGY
# ==========================================================

def filter_products_by_technology(
    products,
    technology,
):

    if not isinstance(
        products,
        list
    ):

        return []

    technology = str(
        technology
    ).strip().lower()

    return [

        product

        for product in products

        if isinstance(
            product,
            dict
        )

        and str(
            product.get(
                "technology",
                ""
            )
        ).strip().lower()
        == technology

    ]


# ==========================================================
# SECTION 9 - SEARCH PRODUCTS
# ==========================================================

def search_products(
    products,
    query,
):

    if not isinstance(
        products,
        list
    ):

        return []

    query = str(
        query
    ).strip().lower()

    if not query:

        return products

    results = []

    for product in products:

        if not isinstance(
            product,
            dict
        ):

            continue

        searchable_text = " ".join([

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
                    "category",
                    ""
                )
            ),

            str(
                product.get(
                    "technology",
                    ""
                )
            ),

            str(
                product.get(
                    "supplier",
                    ""
                )
            ),

            str(
                product.get(
                    "country",
                    ""
                )
            ),

        ]).lower()

        if query in searchable_text:

            results.append(
                product
            )

    return results


# ==========================================================
# SECTION 10 - PRODUCT REQUIREMENT MATCH
# ==========================================================

def match_product_requirement(
    product,
    required_power_w=None,
    required_energy_kwh=None,
    required_voltage_v=None,
):
    """
    Determine whether a product satisfies basic
    engineering requirements.

    This is deliberately a simple matching engine.
    The advanced recommendation logic will be developed
    later in the AI Product Advisor.
    """

    if not isinstance(
        product,
        dict
    ):

        return {

            "match": False,

            "score": 0,

            "reasons": [
                "Invalid product."
            ],

        }

    score = 0

    reasons = []

    # ------------------------------------------------------
    # Power requirement
    # ------------------------------------------------------

    if required_power_w is not None:

        required = safe_float(
            required_power_w,
            0
        )

        available = safe_float(
            product.get(
                "rated_power_w",
                0
            ),
            0
        )

        if available >= required:

            score += 40

            reasons.append(
                "Rated power meets requirement."
            )

        else:

            reasons.append(
                "Rated power is below requirement."
            )

    # ------------------------------------------------------
    # Energy requirement
    # ------------------------------------------------------

    if required_energy_kwh is not None:

        required = safe_float(
            required_energy_kwh,
            0
        )

        available = safe_float(
            product.get(
                "energy_kwh",
                0
            ),
            0
        )

        if available >= required:

            score += 40

            reasons.append(
                "Energy capacity meets requirement."
            )

        else:

            reasons.append(
                "Energy capacity is below requirement."
            )

    # ------------------------------------------------------
    # Voltage requirement
    # ------------------------------------------------------

    if required_voltage_v is not None:

        required = safe_float(
            required_voltage_v,
            0
        )

        available = safe_float(
            product.get(
                "voltage_v",
                0
            ),
            0
        )

        if available == required:

            score += 20

            reasons.append(
                "Voltage matches requirement."
            )

        elif available > 0:

            reasons.append(
                "Voltage does not exactly match requirement."
            )

    return {

        "match":
            score >= 60,

        "score":
            score,

        "reasons":
            reasons,

    }


# ==========================================================
# SECTION 11 - RANK PRODUCTS
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
        list
    ):

        return []

    ranked = []

    for product in products:

        if not isinstance(
            product,
            dict
        ):

            continue

        evaluation = match_product_requirement(

            product,

            required_power_w=
                required_power_w,

            required_energy_kwh=
                required_energy_kwh,

            required_voltage_v=
                required_voltage_v,

        )

        record = dict(
            product
        )

        record["match_score"] = (
            evaluation["score"]
        )

        record["matches_requirement"] = (
            evaluation["match"]
        )

        record["match_reasons"] = (
            evaluation["reasons"]
        )

        ranked.append(
            record
        )

    ranked.sort(

        key=lambda product:
            product.get(
                "match_score",
                0
            ),

        reverse=True

    )

    return ranked


# ==========================================================
# SECTION 12 - PRODUCT COMPARISON
# ==========================================================

def compare_products(
    products
):
    """
    Prepare products for side-by-side comparison.
    """

    if not isinstance(
        products,
        list
    ):

        return []

    comparison = []

    for product in products:

        if not isinstance(
            product,
            dict
        ):

            continue

        comparison.append({

            "name":
                product.get(
                    "name",
                    "N/A"
                ),

            "manufacturer":
                product.get(
                    "manufacturer",
                    "N/A"
                ),

            "model":
                product.get(
                    "model",
                    "N/A"
                ),

            "category":
                product.get(
                    "category",
                    "N/A"
                ),

            "technology":
                product.get(
                    "technology",
                    "N/A"
                ),

            "power_w":
                product.get(
                    "rated_power_w",
                    0
                ),

            "voltage_v":
                product.get(
                    "voltage_v",
                    0
                ),

            "capacity_ah":
                product.get(
                    "capacity_ah",
                    0
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

            "warranty_years":
                product.get(
                    "warranty_years",
                    0
                ),

        })

    return comparison


# ==========================================================
# SECTION 13 - PRODUCT SUMMARY
# ==========================================================

def create_product_summary(
    products
):

    if not isinstance(
        products,
        list
    ):

        products = []

    categories = {}

    for product in products:

        if not isinstance(
            product,
            dict
        ):

            continue

        category = product.get(
            "category",
            "Other"
        )

        categories[category] = (
            categories.get(
                category,
                0
            ) + 1
        )

    return {

        "product_count":
            len(products),

        "category_count":
            len(categories),

        "categories":
            categories,

        "products":
            products,

    }


# ==========================================================
# SECTION 14 - ANALYZE PRODUCT DATABASE
# ==========================================================

def analyze_product_database(
    products
):
    """
    Main product-engine analysis function.
    """

    summary = create_product_summary(
        products
    )

    return {

        "success":
            True,

        "summary":
            summary,

        "products":
            products
            if isinstance(
                products,
                list
            )
            else [],

    }


# ==========================================================
# SECTION 15 - SAMPLE PRODUCT DATABASE
# ==========================================================
#
# These are illustrative database records only.
# They are NOT recommendations, prices or claims about
# currently available commercial products.
#
# Real products should later be entered by the user,
# supplier or administrator.
# ==========================================================

DEFAULT_PRODUCTS = [

    {
        "name":
            "Example 550W Solar Panel",

        "category":
            "Solar Panel",

        "manufacturer":
            "Example Manufacturer",

        "model":
            "EX-550",

        "technology":
            "Monocrystalline",

        "rated_power_w":
            550,

        "voltage_v":
            41.5,

        "capacity_ah":
            0,

        "energy_kwh":
            0,

        "efficiency_percent":
            21.0,

        "warranty_years":
            10,

        "supplier":
            "",

        "country":
            "",

        "notes":
            "Illustrative database record only.",

    },

    {
        "name":
            "Example 5kWh LiFePO4 Battery",

        "category":
            "Battery",

        "manufacturer":
            "Example Manufacturer",

        "model":
            "EX-LFP-5",

        "technology":
            "LiFePO4",

        "rated_power_w":
            0,

        "voltage_v":
            51.2,

        "capacity_ah":
            100,

        "energy_kwh":
            5.12,

        "efficiency_percent":
            95,

        "warranty_years":
            5,

        "supplier":
            "",

        "country":
            "",

        "notes":
            "Illustrative database record only.",

    },

    {
        "name":
            "Example 5kW Hybrid Inverter",

        "category":
            "Inverter",

        "manufacturer":
            "Example Manufacturer",

        "model":
            "EX-HY-5000",

        "technology":
            "Hybrid",

        "rated_power_w":
            5000,

        "voltage_v":
            48,

        "capacity_ah":
            0,

        "energy_kwh":
            0,

        "efficiency_percent":
            95,

        "warranty_years":
            5,

        "supplier":
            "",

        "country":
            "",

        "notes":
            "Illustrative database record only.",

    },

]


# ==========================================================
# SECTION 16 - GET DEFAULT PRODUCTS
# ==========================================================

def get_default_products():

    return [

        dict(product)

        for product in DEFAULT_PRODUCTS

    ]


# ==========================================================
# SECTION 17 - ADD PRODUCT
# ==========================================================

def add_product(
    products,
    product,
):

    if not isinstance(
        products,
        list
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
# SECTION 18 - REMOVE PRODUCT
# ==========================================================

def remove_product(
    products,
    index,
):

    if not isinstance(
        products,
        list
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

        index = int(index)

        if index < 0 or index >= len(
            products
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

    except (
        TypeError,
        ValueError
    ):

        return {

            "success":
                False,

            "message":
                "Invalid product index.",

            "products":
                products,

        }


# ==========================================================
# SECTION 19 - COMPLETE PRODUCT ANALYSIS
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

    working_products = products

    if search_query:

        working_products = search_products(
            working_products,
            search_query
        )

    if category:

        working_products = filter_products_by_category(
            working_products,
            category
        )

    if technology:

        working_products = filter_products_by_technology(
            working_products,
            technology
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
            len(ranked),

        "products":
            ranked,

        "comparison":
            compare_products(ranked),

    }


# ==========================================================
# END OF PRODUCT ENGINE
# ==========================================================
