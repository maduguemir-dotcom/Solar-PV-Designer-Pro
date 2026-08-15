# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Library Storage Engine
# Version: 2.4.0
# ==========================================================
#
# Purpose:
# Persistent local storage for:
#   1. Product Library
#   2. Service / Cost Library
#
# Storage format:
# JSON
#
# This module is deliberately independent from Streamlit UI.
# ==========================================================

import json
from pathlib import Path
from datetime import datetime


# ==========================================================
# SECTION 1 - STORAGE LOCATION
# ==========================================================

APP_DIR = Path(__file__).resolve().parent

DATA_DIR = APP_DIR / "data"

PRODUCT_LIBRARY_FILE = (
    DATA_DIR / "product_library.json"
)

SERVICE_LIBRARY_FILE = (
    DATA_DIR / "service_library.json"
)


# ==========================================================
# SECTION 2 - DIRECTORY MANAGEMENT
# ==========================================================

def ensure_data_directory():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return DATA_DIR


# ==========================================================
# SECTION 3 - GENERIC JSON LOAD
# ==========================================================

def load_json_file(
    file_path,
    default=None
):

    if default is None:
        default = []

    try:

        ensure_data_directory()

        if not file_path.exists():

            return default

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        return data

    except (
        OSError,
        json.JSONDecodeError,
        TypeError
    ):

        return default


# ==========================================================
# SECTION 4 - GENERIC JSON SAVE
# ==========================================================

def save_json_file(
    file_path,
    data
):

    try:

        ensure_data_directory()

        with open(
            file_path,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

        return {
            "success": True,
            "message":
                "Library saved successfully."
        }

    except (
        OSError,
        TypeError
    ) as error:

        return {
            "success": False,
            "message":
                f"Unable to save library: {error}"
        }


# ==========================================================
# SECTION 5 - PRODUCT LIBRARY
# ==========================================================

def load_product_library():

    return load_json_file(
        PRODUCT_LIBRARY_FILE,
        []
    )


def save_product_library(
    products
):

    if not isinstance(
        products,
        list
    ):

        return {
            "success": False,
            "message":
                "Product library must be a list."
        }

    return save_json_file(
        PRODUCT_LIBRARY_FILE,
        products
    )


def add_product_to_library(
    product
):

    products = load_product_library()

    if not isinstance(
        product,
        dict
    ):

        return {
            "success": False,
            "message":
                "Product must be a dictionary."
        }

    product = dict(product)

    product.setdefault(
        "created_at",
        datetime.now().isoformat()
    )

    products.append(
        product
    )

    result = save_product_library(
        products
    )

    if result["success"]:

        result["product"] = product

    return result


def remove_product_from_library(
    index
):

    products = load_product_library()

    try:

        index = int(index)

    except (
        TypeError,
        ValueError
    ):

        return {
            "success": False,
            "message":
                "Invalid product index."
        }

    if index < 0 or index >= len(
        products
    ):

        return {
            "success": False,
            "message":
                "Product index is out of range."
        }

    removed = products.pop(
        index
    )

    result = save_product_library(
        products
    )

    if result["success"]:

        result["removed"] = removed

    return result


# ==========================================================
# SECTION 6 - SERVICE LIBRARY
# ==========================================================

def load_service_library():

    return load_json_file(
        SERVICE_LIBRARY_FILE,
        []
    )


def save_service_library(
    services
):

    if not isinstance(
        services,
        list
    ):

        return {
            "success": False,
            "message":
                "Service library must be a list."
        }

    return save_json_file(
        SERVICE_LIBRARY_FILE,
        services
    )


# ==========================================================
# SECTION 7 - SERVICE RECORD
# ==========================================================

def create_service_record(
    name,
    category="Service",
    unit="job",
    unit_price=0.0,
    currency="UGX",
    supplier="",
    location="",
    notes="",
):

    try:

        unit_price = float(
            unit_price
        )

    except (
        TypeError,
        ValueError
    ):

        unit_price = 0.0

    return {

        "name":
            str(name).strip(),

        "category":
            str(category).strip(),

        "unit":
            str(unit).strip(),

        "unit_price":
            unit_price,

        "currency":
            str(currency).strip(),

        "supplier":
            str(supplier).strip(),

        "location":
            str(location).strip(),

        "notes":
            str(notes).strip(),

        "created_at":
            datetime.now().isoformat(),

    }


def add_service_to_library(
    service
):

    services = load_service_library()

    if not isinstance(
        service,
        dict
    ):

        return {
            "success": False,
            "message":
                "Service must be a dictionary."
        }

    services.append(
        dict(service)
    )

    return save_service_library(
        services
    )


def remove_service_from_library(
    index
):

    services = load_service_library()

    try:

        index = int(index)

    except (
        TypeError,
        ValueError
    ):

        return {
            "success": False,
            "message":
                "Invalid service index."
        }

    if index < 0 or index >= len(
        services
    ):

        return {
            "success": False,
            "message":
                "Service index is out of range."
        }

    removed = services.pop(
        index
    )

    result = save_service_library(
        services
    )

    if result["success"]:

        result["removed"] = removed

    return result


# ==========================================================
# SECTION 8 - SEARCH PRODUCTS
# ==========================================================

def search_product_library(
    query
):

    products = load_product_library()

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

        searchable = " ".join([

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

        if query in searchable:

            results.append(
                product
            )

    return results


# ==========================================================
# SECTION 9 - SEARCH SERVICES
# ==========================================================

def search_service_library(
    query
):

    services = load_service_library()

    query = str(
        query
    ).strip().lower()

    if not query:

        return services

    results = []

    for service in services:

        if not isinstance(
            service,
            dict
        ):

            continue

        searchable = " ".join([

            str(
                service.get(
                    "name",
                    ""
                )
            ),

            str(
                service.get(
                    "category",
                    ""
                )
            ),

            str(
                service.get(
                    "supplier",
                    ""
                )
            ),

            str(
                service.get(
                    "location",
                    ""
                )
            ),

            str(
                service.get(
                    "notes",
                    ""
                )
            ),

        ]).lower()

        if query in searchable:

            results.append(
                service
            )

    return results


# ==========================================================
# SECTION 10 - LIBRARY SUMMARY
# ==========================================================

def get_library_summary():

    products = load_product_library()

    services = load_service_library()

    product_categories = {}

    for product in products:

        category = product.get(
            "category",
            "Other"
        )

        product_categories[category] = (
            product_categories.get(
                category,
                0
            ) + 1
        )

    service_categories = {}

    for service in services:

        category = service.get(
            "category",
            "Service"
        )

        service_categories[category] = (
            service_categories.get(
                category,
                0
            ) + 1
        )

    return {

        "product_count":
            len(products),

        "service_count":
            len(services),

        "total_library_items":
            len(products) + len(services),

        "product_categories":
            product_categories,

        "service_categories":
            service_categories,

    }


# ==========================================================
# SECTION 11 - BACKUP
# ==========================================================

def backup_library():

    ensure_data_directory()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_dir = (
        DATA_DIR / "backups"
    )

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    product_backup = (
        backup_dir /
        f"product_library_{timestamp}.json"
    )

    service_backup = (
        backup_dir /
        f"service_library_{timestamp}.json"
    )

    products = load_product_library()

    services = load_service_library()

    product_result = save_json_file(
        product_backup,
        products
    )

    service_result = save_json_file(
        service_backup,
        services
    )

    return {

        "success":
            (
                product_result["success"]
                and
                service_result["success"]
            ),

        "product_backup":
            str(product_backup),

        "service_backup":
            str(service_backup),

    }


# ==========================================================
# SECTION 12 - CLEAR LIBRARIES
# ==========================================================

def clear_product_library():

    return save_product_library([])


def clear_service_library():

    return save_service_library([])


# ==========================================================
# SECTION 13 - COMPLETE LIBRARY RESET
# ==========================================================

def clear_all_libraries():

    product_result = (
        clear_product_library()
    )

    service_result = (
        clear_service_library()
    )

    return {

        "success":
            (
                product_result["success"]
                and
                service_result["success"]
            ),

        "product":
            product_result,

        "service":
            service_result,

    }


# ==========================================================
# END OF LIBRARY STORAGE ENGINE
# ==========================================================
