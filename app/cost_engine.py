# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Cost & Currency Engine
# Version: 2.4.0
# ==========================================================
#
# Developed by:
# Engr. Prof. Ibrahim Sani Madugu
#
# Purpose:
# Manage user-defined solar-system component costs,
# quantities, currencies and total project cost.
#
# This module is intentionally independent from main.py.
# ==========================================================


# ==========================================================
# SECTION 1 - SUPPORTED CURRENCIES
# ==========================================================

SUPPORTED_CURRENCIES = {
    "NGN": "Nigerian Naira",
    "UGX": "Ugandan Shilling",
    "KES": "Kenyan Shilling",
    "TZS": "Tanzanian Shilling",
    "GHS": "Ghanaian Cedi",
    "ZAR": "South African Rand",
    "USD": "US Dollar",
    "EUR": "Euro",
    "GBP": "British Pound",
}


# ==========================================================
# SECTION 2 - DEFAULT COST ITEMS
# ==========================================================

DEFAULT_COST_ITEMS = [
    {
        "category": "Solar Panels",
        "item": "Solar Panel",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "panel",
    },
    {
        "category": "Battery",
        "item": "Battery",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "unit",
    },
    {
        "category": "Inverter",
        "item": "Inverter",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "unit",
    },
    {
        "category": "Charge Controller",
        "item": "Charge Controller",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "unit",
    },
    {
        "category": "Mounting",
        "item": "Mounting Structure",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "set",
    },
    {
        "category": "Protection",
        "item": "DC/AC Protection",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "set",
    },
    {
        "category": "Cabling",
        "item": "Solar Cable",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "set",
    },
    {
        "category": "Installation",
        "item": "Installation Labour",
        "quantity": 0,
        "unit_price": 0.0,
        "currency": "USD",
        "unit": "service",
    },
]


# ==========================================================
# SECTION 3 - SAFE FLOAT
# ==========================================================

def safe_float(value, default=0.0):
    """
    Safely convert a value to float.

    Returns default when conversion fails.
    """

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
# SECTION 4 - SAFE INTEGER
# ==========================================================

def safe_int(value, default=0):
    """
    Safely convert a value to integer.
    """

    try:

        if value is None:
            return default

        return int(value)

    except (TypeError, ValueError):

        return default


# ==========================================================
# SECTION 5 - GET CURRENCY NAME
# ==========================================================

def get_currency_name(currency_code):
    """
    Return the full name of a currency.
    """

    code = str(
        currency_code
    ).strip().upper()

    return SUPPORTED_CURRENCIES.get(
        code,
        code
    )


# ==========================================================
# SECTION 6 - GET CURRENCY SYMBOL
# ==========================================================

def get_currency_symbol(currency_code):
    """
    Return a display symbol for a currency.
    """

    symbols = {

        "NGN": "₦",
        "UGX": "UGX",
        "KES": "KSh",
        "TZS": "TSh",
        "GHS": "GH₵",
        "ZAR": "R",
        "USD": "$",
        "EUR": "€",
        "GBP": "£",

    }

    code = str(
        currency_code
    ).strip().upper()

    return symbols.get(
        code,
        code
    )


# ==========================================================
# SECTION 7 - VALIDATE CURRENCY
# ==========================================================

def validate_currency(currency_code):
    """
    Validate a currency code.
    """

    code = str(
        currency_code
    ).strip().upper()

    if code not in SUPPORTED_CURRENCIES:

        return {
            "valid": False,
            "message": (
                f"Unsupported currency: {code}"
            ),
        }

    return {
        "valid": True,
        "message": "Currency is valid.",
        "currency": code,
    }


# ==========================================================
# SECTION 8 - CREATE COST ITEM
# ==========================================================

def create_cost_item(
    category,
    item,
    quantity=0,
    unit_price=0.0,
    currency="USD",
    unit="unit",
):
    """
    Create a standardized cost item.
    """

    currency_code = str(
        currency
    ).strip().upper()

    validation = validate_currency(
        currency_code
    )

    if not validation["valid"]:

        return {
            "success": False,
            "message": validation["message"],
            "item": None,
        }

    quantity = safe_int(
        quantity
    )

    unit_price = safe_float(
        unit_price
    )

    if quantity < 0:

        return {
            "success": False,
            "message": "Quantity cannot be negative.",
            "item": None,
        }

    if unit_price < 0:

        return {
            "success": False,
            "message": "Unit price cannot be negative.",
            "item": None,
        }

    record = {

        "category":
            str(category).strip(),

        "item":
            str(item).strip(),

        "quantity":
            quantity,

        "unit_price":
            unit_price,

        "currency":
            currency_code,

        "unit":
            str(unit).strip(),

    }

    record["total_cost"] = (
        quantity * unit_price
    )

    return {

        "success": True,

        "message":
            "Cost item created successfully.",

        "item":
            record,

    }


# ==========================================================
# SECTION 9 - CALCULATE ITEM COST
# ==========================================================

def calculate_item_cost(
    quantity,
    unit_price,
):
    """
    Calculate total cost for one item.
    """

    quantity = safe_float(
        quantity
    )

    unit_price = safe_float(
        unit_price
    )

    if quantity < 0:
        quantity = 0

    if unit_price < 0:
        unit_price = 0

    return (
        quantity * unit_price
    )


# ==========================================================
# SECTION 10 - UPDATE COST ITEM
# ==========================================================

def update_cost_item(
    item,
    quantity=None,
    unit_price=None,
    currency=None,
):
    """
    Update an existing cost item.
    """

    if not isinstance(
        item,
        dict
    ):

        return None

    updated = dict(
        item
    )

    if quantity is not None:

        updated["quantity"] = max(
            0,
            safe_int(quantity)
        )

    if unit_price is not None:

        updated["unit_price"] = max(
            0.0,
            safe_float(unit_price)
        )

    if currency is not None:

        currency_code = str(
            currency
        ).strip().upper()

        if currency_code in SUPPORTED_CURRENCIES:

            updated["currency"] = (
                currency_code
            )

    updated["total_cost"] = calculate_item_cost(
        updated.get("quantity", 0),
        updated.get("unit_price", 0),
    )

    return updated


# ==========================================================
# SECTION 11 - CALCULATE TOTAL PROJECT COST
# ==========================================================

def calculate_total_cost(
    cost_items
):
    """
    Calculate total cost grouped by currency.

    Important:
    Different currencies are NOT added together.

    Example:

        USD total = 2,000
        UGX total = 7,500,000
        NGN total = 3,000,000

    Each remains separate until a currency conversion
    rate is supplied.
    """

    totals = {}

    if not isinstance(
        cost_items,
        list
    ):

        return totals

    for item in cost_items:

        if not isinstance(
            item,
            dict
        ):

            continue

        currency = str(
            item.get(
                "currency",
                "USD"
            )
        ).strip().upper()

        total = calculate_item_cost(

            item.get(
                "quantity",
                0
            ),

            item.get(
                "unit_price",
                0
            ),

        )

        if currency not in totals:

            totals[currency] = 0.0

        totals[currency] += total

    return totals


# ==========================================================
# SECTION 12 - CALCULATE CATEGORY TOTALS
# ==========================================================

def calculate_category_totals(
    cost_items
):
    """
    Calculate costs by category and currency.
    """

    result = {}

    if not isinstance(
        cost_items,
        list
    ):

        return result

    for item in cost_items:

        if not isinstance(
            item,
            dict
        ):

            continue

        category = str(
            item.get(
                "category",
                "Other"
            )
        ).strip()

        currency = str(
            item.get(
                "currency",
                "USD"
            )
        ).strip().upper()

        total = calculate_item_cost(

            item.get(
                "quantity",
                0
            ),

            item.get(
                "unit_price",
                0
            ),

        )

        if category not in result:

            result[category] = {}

        if currency not in result[category]:

            result[category][currency] = 0.0

        result[category][currency] += total

    return result


# ==========================================================
# SECTION 13 - COUNT COST ITEMS
# ==========================================================

def count_cost_items(
    cost_items
):
    """
    Return number of valid cost items.
    """

    if not isinstance(
        cost_items,
        list
    ):

        return 0

    return len([
        item
        for item in cost_items
        if isinstance(item, dict)
    ])


# ==========================================================
# SECTION 14 - SORT COST ITEMS
# ==========================================================

def sort_cost_items(
    cost_items,
    descending=True
):
    """
    Sort cost items by total cost.
    """

    if not isinstance(
        cost_items,
        list
    ):

        return []

    return sorted(

        cost_items,

        key=lambda item:
            calculate_item_cost(

                item.get(
                    "quantity",
                    0
                ),

                item.get(
                    "unit_price",
                    0
                ),

            ),

        reverse=descending

    )


# ==========================================================
# SECTION 15 - CREATE COST SUMMARY
# ==========================================================

def create_cost_summary(
    cost_items
):
    """
    Produce a complete cost-analysis summary.
    """

    totals = calculate_total_cost(
        cost_items
    )

    category_totals = calculate_category_totals(
        cost_items
    )

    sorted_items = sort_cost_items(
        cost_items
    )

    highest_cost_item = None

    if sorted_items:

        highest_cost_item = (
            sorted_items[0]
        )

    return {

        "item_count":
            count_cost_items(
                cost_items
            ),

        "totals_by_currency":
            totals,

        "category_totals":
            category_totals,

        "highest_cost_item":
            highest_cost_item,

        "items":
            cost_items
            if isinstance(
                cost_items,
                list
            )
            else [],

    }


# ==========================================================
# SECTION 16 - FORMAT MONEY
# ==========================================================

def format_money(
    amount,
    currency="USD",
    decimals=2,
):
    """
    Format a monetary value for dashboard display.
    """

    amount = safe_float(
        amount
    )

    code = str(
        currency
    ).strip().upper()

    symbol = get_currency_symbol(
        code
    )

    try:

        formatted = (
            f"{amount:,.{decimals}f}"
        )

    except (ValueError, TypeError):

        formatted = "0.00"

    return (
        f"{symbol} {formatted}"
    )


# ==========================================================
# SECTION 17 - ANALYZE COST DATA
# ==========================================================

def analyze_cost_data(
    cost_items
):
    """
    Main cost-engine analysis function.

    Returns a single dictionary suitable for
    Streamlit dashboards and reports.
    """

    summary = create_cost_summary(
        cost_items
    )

    return {

        "success":
            True,

        "summary":
            summary,

        "supported_currencies":
            SUPPORTED_CURRENCIES,

    }


# ==========================================================
# SECTION 18 - DEFAULT COST ITEMS
# ==========================================================

def get_default_cost_items():
    """
    Return a fresh copy of the default cost-item list.

    A fresh list prevents accidental modification of
    DEFAULT_COST_ITEMS.
    """

    return [

        dict(item)

        for item in DEFAULT_COST_ITEMS

    ]


# ==========================================================
# SECTION 19 - ADD COST ITEM
# ==========================================================

def add_cost_item(
    cost_items,
    category,
    item,
    quantity=0,
    unit_price=0.0,
    currency="USD",
    unit="unit",
):
    """
    Add a new cost item to an existing list.
    """

    if not isinstance(
        cost_items,
        list
    ):

        cost_items = []

    result = create_cost_item(

        category=category,

        item=item,

        quantity=quantity,

        unit_price=unit_price,

        currency=currency,

        unit=unit,

    )

    if not result["success"]:

        return {

            "success": False,

            "message":
                result["message"],

            "items":
                cost_items,

        }

    cost_items.append(
        result["item"]
    )

    return {

        "success": True,

        "message":
            "Cost item added successfully.",

        "items":
            cost_items,

    }


# ==========================================================
# SECTION 20 - REMOVE COST ITEM
# ==========================================================

def remove_cost_item(
    cost_items,
    index,
):
    """
    Remove a cost item by list index.
    """

    if not isinstance(
        cost_items,
        list
    ):

        return {

            "success": False,

            "message":
                "Cost-item list is invalid.",

            "items": [],

        }

    try:

        index = int(index)

        if index < 0 or index >= len(
            cost_items
        ):

            return {

                "success": False,

                "message":
                    "Invalid cost-item index.",

                "items":
                    cost_items,

            }

        removed = cost_items.pop(
            index
        )

        return {

            "success": True,

            "message":
                "Cost item removed successfully.",

            "removed":
                removed,

            "items":
                cost_items,

        }

    except (
        TypeError,
        ValueError
    ):

        return {

            "success": False,

            "message":
                "Invalid cost-item index.",

            "items":
                cost_items,

        }


# ==========================================================
# END OF COST ENGINE
# ==========================================================
