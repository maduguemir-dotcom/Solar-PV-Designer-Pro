"""
Solar PV Designer Pro Africa™
Persistent Product and Service Library Storage

Files:
    app/data/product_library.json
    app/data/service_library.json
"""

import json
import shutil
from pathlib import Path
from datetime import datetime


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

PRODUCT_LIBRARY_FILE = DATA_DIR / "product_library.json"

SERVICE_LIBRARY_FILE = DATA_DIR / "service_library.json"

BACKUP_DIR = DATA_DIR / "backups"


# ============================================================
# DIRECTORY INITIALIZATION
# ============================================================

def ensure_data_directory():
    """Create data and backup directories if they do not exist."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)

    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    # Create empty product library if missing
    if not PRODUCT_LIBRARY_FILE.exists():
        save_json_file(PRODUCT_LIBRARY_FILE, [])

    # Create empty service library if missing
    if not SERVICE_LIBRARY_FILE.exists():
        save_json_file(SERVICE_LIBRARY_FILE, [])

    return DATA_DIR


# ============================================================
# JSON HELPERS
# ============================================================

def load_json_file(file_path, default=None):
    """
    Safely load a JSON file.

    Returns the supplied default value if the file does not
    exist or cannot be read.
    """

    ensure_data_directory()

    file_path = Path(file_path)

    if default is None:
        default = []

    if not file_path.exists():
        save_json_file(file_path, default)
        return default

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)

        return data

    except json.JSONDecodeError:
        return default

    except Exception:
        return default


def save_json_file(file_path, data):
    """
    Safely save Python data to JSON.
    """

    file_path = Path(file_path)

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )

    with open(file_path, "w", encoding="utf-8") as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
            default=str
        )

    return True


# ============================================================
# PRODUCT LIBRARY
# ============================================================

def load_product_library():
    """Load all products from the product library."""

    ensure_data_directory()

    data = load_json_file(
        PRODUCT_LIBRARY_FILE,
        default=[]
    )

    if isinstance(data, list):
        return data

    return []


def save_product_library(products):
    """Save the complete product library."""

    ensure_data_directory()

    if products is None:
        products = []

    return save_json_file(
        PRODUCT_LIBRARY_FILE,
        products
    )


def add_product_to_library(product):
    """
    Add a product to the persistent product library.
    """

    products = load_product_library()

    if not isinstance(product, dict):
        raise ValueError(
            "Product must be a dictionary."
        )

    product = product.copy()

    # Generate ID if one does not already exist
    if not product.get("id"):

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        product["id"] = f"PROD-{timestamp}"

    # Add timestamps
    now = datetime.now().isoformat()

    if not product.get("created_at"):
        product["created_at"] = now

    product["updated_at"] = now

    products.append(product)

    save_product_library(products)

    return product


def get_product_from_library(product_id):
    """Retrieve a single product by ID."""

    products = load_product_library()

    for product in products:

        if str(product.get("id")) == str(product_id):
            return product

    return None


def update_product_in_library(product_id, updated_data):
    """
    Update an existing product.
    """

    products = load_product_library()

    for index, product in enumerate(products):

        if str(product.get("id")) == str(product_id):

            original_created_at = product.get(
                "created_at"
            )

            product.update(updated_data)

            product["id"] = product_id

            product["created_at"] = original_created_at

            product["updated_at"] = (
                datetime.now().isoformat()
            )

            products[index] = product

            save_product_library(products)

            return {
                "success": True,
                "product": product,
                "message": "Product updated successfully."
            }

    return {
        "success": False,
        "message": "Product not found."
    }


def remove_product_from_library(product_id):
    """
    Remove a product from the library.
    """

    products = load_product_library()

    original_count = len(products)

    products = [

        product
        for product in products

        if str(product.get("id"))
        != str(product_id)
    ]

    if len(products) == original_count:

        return {
            "success": False,
            "message": "Product not found."
        }

    save_product_library(products)

    return {
        "success": True,
        "message": "Product removed successfully."
    }


def search_product_library(
    query="",
    category=None,
    technology=None
):
    """
    Search the product library.
    """

    products = load_product_library()

    results = []

    query = str(query or "").lower().strip()

    for product in products:

        # Category filter
        if category:

            if str(
                product.get("category", "")
            ) != str(category):

                continue

        # Technology filter
        if technology:

            if str(
                product.get("technology", "")
            ) != str(technology):

                continue

        # Search query
        if query:

            searchable_text = " ".join(

                str(value)

                for value in product.values()

                if value is not None

            ).lower()

            if query not in searchable_text:

                continue

        results.append(product)

    return results


def clear_product_library():
    """
    Clear all products.

    A backup is created first.
    """

    backup_library()

    save_product_library([])

    return {
        "success": True,
        "message": "Product library cleared."
    }


# ============================================================
# SERVICE LIBRARY
# ============================================================

def create_service_record(
    name,
    category="Other Service",
    price=0,
    currency="USD",
    **kwargs
):
    """
    Create a standard service record.
    """

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )

    service = {

        "id": f"SERV-{timestamp}",

        "name": name,

        "category": category,

        "price": price,

        "currency": currency,

        "created_at":
            datetime.now().isoformat(),

        "updated_at":
            datetime.now().isoformat()
    }

    service.update(kwargs)

    return service


def load_service_library():
    """Load all services."""

    ensure_data_directory()

    data = load_json_file(
        SERVICE_LIBRARY_FILE,
        default=[]
    )

    if isinstance(data, list):
        return data

    return []


def save_service_library(services):
    """Save the complete service library."""

    ensure_data_directory()

    if services is None:
        services = []

    return save_json_file(
        SERVICE_LIBRARY_FILE,
        services
    )


def add_service_to_library(service):
    """Add a service."""

    services = load_service_library()

    if not isinstance(service, dict):

        raise ValueError(
            "Service must be a dictionary."
        )

    service = service.copy()

    if not service.get("id"):

        timestamp = datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )

        service["id"] = f"SERV-{timestamp}"

    now = datetime.now().isoformat()

    if not service.get("created_at"):

        service["created_at"] = now

    service["updated_at"] = now

    services.append(service)

    save_service_library(services)

    return service


def remove_service_from_library(service_id):

    services = load_service_library()

    original_count = len(services)

    services = [

        service
        for service in services

        if str(service.get("id"))
        != str(service_id)

    ]

    if len(services) == original_count:

        return {
            "success": False,
            "message": "Service not found."
        }

    save_service_library(services)

    return {
        "success": True,
        "message": "Service removed successfully."
    }


def search_service_library(
    query="",
    category=None
):

    services = load_service_library()

    results = []

    query = str(query or "").lower().strip()

    for service in services:

        if category:

            if str(
                service.get("category", "")
            ) != str(category):

                continue

        if query:

            searchable_text = " ".join(

                str(value)

                for value in service.values()

                if value is not None

            ).lower()

            if query not in searchable_text:

                continue

        results.append(service)

    return results


def clear_service_library():

    backup_library()

    save_service_library([])

    return {
        "success": True,
        "message": "Service library cleared."
    }


# ============================================================
# BACKUP SYSTEM
# ============================================================

def backup_library():
    """
    Create timestamped backups of product and service libraries.
    """

    ensure_data_directory()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_files = []

    files_to_backup = [

        PRODUCT_LIBRARY_FILE,
        SERVICE_LIBRARY_FILE
    ]

    for source_file in files_to_backup:

        if source_file.exists():

            destination = (

                BACKUP_DIR

                / f"{source_file.stem}_{timestamp}.json"

            )

            shutil.copy2(
                source_file,
                destination
            )

            backup_files.append(
                str(destination)
            )

    return {

        "success": True,

        "timestamp": timestamp,

        "files": backup_files
    }


# ============================================================
# COMPLETE LIBRARY MANAGEMENT
# ============================================================

def clear_all_libraries():
    """
    Back up and clear both product and service libraries.
    """

    backup_result = backup_library()

    save_product_library([])

    save_service_library([])

    return {

        "success": True,

        "message":
            "All libraries cleared successfully.",

        "backup": backup_result
    }


def get_library_summary():
    """
    Return a summary of stored records.
    """

    products = load_product_library()

    services = load_service_library()

    categories = {}

    for product in products:

        category = product.get(
            "category",
            "Other"
        )

        categories[category] = (
            categories.get(category, 0) + 1
        )

    service_categories = {}

    for service in services:

        category = service.get(
            "category",
            "Other"
        )

        service_categories[category] = (

            service_categories.get(
                category,
                0
            )

            + 1
        )

    return {

        "total_products": len(products),

        "total_services": len(services),

        "product_categories": categories,

        "service_categories":
            service_categories,

        "data_directory": str(DATA_DIR),

        "product_library_file":
            str(PRODUCT_LIBRARY_FILE),

        "service_library_file":
            str(SERVICE_LIBRARY_FILE),

        "backup_directory":
            str(BACKUP_DIR)
    }


# ============================================================
# INITIALIZE STORAGE ON IMPORT
# ============================================================

ensure_data_directory()
