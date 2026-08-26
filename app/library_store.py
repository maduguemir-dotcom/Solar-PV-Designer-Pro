"""
Solar PV Designer Pro Africa™
Persistent Product and Service Library Store

Storage engine:
    SQLite

This module provides persistent storage for:

1. Product Library
2. Service Library
3. Labour Costs
4. Installation Services
5. Transport Services
6. Other Custom Services

Database location:

app/data/solar_pv_library.db
"""

import json
import sqlite3
from datetime import datetime
from pathlib import Path


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR / "data"

DATABASE_FILE = DATA_DIR / "solar_pv_library.db"

# Backward-compatible paths
PRODUCT_LIBRARY_FILE = DATA_DIR / "product_library.json"

SERVICE_LIBRARY_FILE = DATA_DIR / "service_library.json"


# ============================================================
# DATA DIRECTORY
# ============================================================

def ensure_data_directory():
    """
    Ensure that the application data directory exists.
    """

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    return DATA_DIR


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():
    """
    Create and return a SQLite database connection.
    """

    ensure_data_directory()

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection


# ============================================================
# DATABASE INITIALIZATION
# ============================================================

def initialize_database():
    """
    Create the required database tables.
    """

    connection = get_connection()

    cursor = connection.cursor()

    # --------------------------------------------------------
    # PRODUCT LIBRARY
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (

            id TEXT PRIMARY KEY,

            name TEXT NOT NULL,

            category TEXT,

            manufacturer TEXT,

            model TEXT,

            technology TEXT,

            rated_power_w REAL DEFAULT 0,

            voltage_v REAL DEFAULT 0,

            current_a REAL DEFAULT 0,

            capacity_ah REAL DEFAULT 0,

            energy_kwh REAL DEFAULT 0,

            efficiency_percent REAL DEFAULT 0,

            warranty_years INTEGER DEFAULT 0,

            supplier TEXT,

            country TEXT,

            price REAL DEFAULT 0,

            currency TEXT DEFAULT 'USD',

            quantity INTEGER DEFAULT 1,

            notes TEXT,

            product_data TEXT,

            created_at TEXT,

            updated_at TEXT
        )
        """
    )

    # --------------------------------------------------------
    # SERVICE LIBRARY
    # --------------------------------------------------------

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS services (

            id TEXT PRIMARY KEY,

            name TEXT NOT NULL,

            category TEXT,

            description TEXT,

            provider TEXT,

            country TEXT,

            price REAL DEFAULT 0,

            currency TEXT DEFAULT 'USD',

            unit TEXT,

            notes TEXT,

            service_data TEXT,

            created_at TEXT,

            updated_at TEXT
        )
        """
    )

    connection.commit()

    connection.close()


# ============================================================
# SAFE VALUE CONVERSION
# ============================================================

def safe_float(value, default=0.0):

    try:

        if value is None or value == "":
            return float(default)

        return float(value)

    except (
        ValueError,
        TypeError,
    ):

        return float(default)


def safe_int(value, default=0):

    try:

        if value is None or value == "":
            return int(default)

        return int(value)

    except (
        ValueError,
        TypeError,
    ):

        return int(default)


# ============================================================
# PRODUCT NORMALIZATION
# ============================================================

def normalize_product(product):
    """
    Normalize a product record so that all
    standard fields exist.
    """

    product = dict(product or {})

    return {

        "id": str(
            product.get(
                "id",
                ""
            )
        ),

        "name": str(
            product.get(
                "name",
                ""
            )
        ),

        "category": str(
            product.get(
                "category",
                "Other"
            )
        ),

        "manufacturer": str(
            product.get(
                "manufacturer",
                ""
            )
        ),

        "model": str(
            product.get(
                "model",
                ""
            )
        ),

        "technology": str(
            product.get(
                "technology",
                "Other"
            )
        ),

        "rated_power_w": safe_float(
            product.get(
                "rated_power_w",
                0
            )
        ),

        "voltage_v": safe_float(
            product.get(
                "voltage_v",
                0
            )
        ),

        "current_a": safe_float(
            product.get(
                "current_a",
                0
            )
        ),

        "capacity_ah": safe_float(
            product.get(
                "capacity_ah",
                0
            )
        ),

        "energy_kwh": safe_float(
            product.get(
                "energy_kwh",
                0
            )
        ),

        "efficiency_percent": safe_float(
            product.get(
                "efficiency_percent",
                0
            )
        ),

        "warranty_years": safe_int(
            product.get(
                "warranty_years",
                0
            )
        ),

        "supplier": str(
            product.get(
                "supplier",
                ""
            )
        ),

        "country": str(
            product.get(
                "country",
                ""
            )
        ),

        "price": safe_float(
            product.get(
                "price",
                0
            )
        ),

        "currency": str(
            product.get(
                "currency",
                "USD"
            )
        ),

        "quantity": max(
            1,
            safe_int(
                product.get(
                    "quantity",
                    1
                ),
                1
            )
        ),

        "notes": str(
            product.get(
                "notes",
                ""
            )
        ),
    }


# ============================================================
# ADD PRODUCT
# ============================================================

def add_product_to_library(product):
    """
    Add a new product to the SQLite library.

    If the product ID already exists,
    the product will be updated.
    """

    initialize_database()

    product = dict(product or {})

    normalized = normalize_product(
        product
    )

    product_id = normalized.get(
        "id",
        ""
    )

    if not product_id:

        product_id = (
            f"product_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        )

        normalized["id"] = product_id

    now = datetime.now().isoformat()

    product_data = deepcopy_product_data(
        product,
        normalized,
    )

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (

            id,
            name,
            category,
            manufacturer,
            model,
            technology,
            rated_power_w,
            voltage_v,
            current_a,
            capacity_ah,
            energy_kwh,
            efficiency_percent,
            warranty_years,
            supplier,
            country,
            price,
            currency,
            quantity,
            notes,
            product_data,
            created_at,
            updated_at

        )

        VALUES (

            :id,
            :name,
            :category,
            :manufacturer,
            :model,
            :technology,
            :rated_power_w,
            :voltage_v,
            :current_a,
            :capacity_ah,
            :energy_kwh,
            :efficiency_percent,
            :warranty_years,
            :supplier,
            :country,
            :price,
            :currency,
            :quantity,
            :notes,
            :product_data,
            :created_at,
            :updated_at

        )

        ON CONFLICT(id)

        DO UPDATE SET

            name = excluded.name,
            category = excluded.category,
            manufacturer = excluded.manufacturer,
            model = excluded.model,
            technology = excluded.technology,
            rated_power_w = excluded.rated_power_w,
            voltage_v = excluded.voltage_v,
            current_a = excluded.current_a,
            capacity_ah = excluded.capacity_ah,
            energy_kwh = excluded.energy_kwh,
            efficiency_percent = excluded.efficiency_percent,
            warranty_years = excluded.warranty_years,
            supplier = excluded.supplier,
            country = excluded.country,
            price = excluded.price,
            currency = excluded.currency,
            quantity = excluded.quantity,
            notes = excluded.notes,
            product_data = excluded.product_data,
            updated_at = excluded.updated_at
        """,

        {
            **normalized,

            "product_data": json.dumps(
                product_data
            ),

            "created_at": now,

            "updated_at": now,
        }
    )

    connection.commit()

    connection.close()

    return normalized


# ============================================================
# PRESERVE CUSTOM PRODUCT FIELDS
# ============================================================

def deepcopy_product_data(
    original_product,
    normalized_product,
):
    """
    Preserve all custom category-specific fields.
    """

    data = dict(
        original_product
    )

    data.update(
        normalized_product
    )

    return data


# ============================================================
# LOAD PRODUCT LIBRARY
# ============================================================

def load_product_library():
    """
    Load all products from SQLite.
    """

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM products

        ORDER BY updated_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    products = []

    for row in rows:

        product = dict(row)

        raw_data = product.get(
            "product_data"
        )

        if raw_data:

            try:

                stored_data = json.loads(
                    raw_data
                )

                if isinstance(
                    stored_data,
                    dict
                ):

                    stored_data.update(
                        {
                            key: value

                            for key, value
                            in product.items()

                            if key
                            not in [
                                "product_data",
                                "created_at",
                                "updated_at",
                            ]
                        }
                    )

                    product = stored_data

            except Exception:

                pass

        product.pop(
            "product_data",
            None
        )

        product.pop(
            "created_at",
            None
        )

        product.pop(
            "updated_at",
            None
        )

        products.append(
            product
        )

    return products


# ============================================================
# SAVE PRODUCT LIBRARY
# ============================================================

def save_product_library(products):
    """
    Replace the current product library
    with the supplied list.
    """

    if not isinstance(
        products,
        list
    ):

        raise ValueError(
            "Products must be provided as a list."
        )

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM products"
    )

    connection.commit()

    connection.close()

    for product in products:

        add_product_to_library(
            product
        )

    return True


# ============================================================
# UPDATE PRODUCT
# ============================================================

def update_product_in_library(
    product_id,
    updated_product,
):
    """
    Update an existing product.
    """

    if not product_id:

        return False

    existing_products = (
        load_product_library()
    )

    existing = None

    for product in existing_products:

        if str(
            product.get(
                "id"
            )
        ) == str(product_id):

            existing = product

            break

    if existing is None:

        return False

    merged_product = dict(
        existing
    )

    merged_product.update(
        dict(updated_product or {})
    )

    merged_product["id"] = str(
        product_id
    )

    add_product_to_library(
        merged_product
    )

    return True


# ============================================================
# REMOVE PRODUCT
# ============================================================

def remove_product_from_library(
    product_id,
):
    """
    Remove a product permanently.
    """

    if not product_id:

        return False

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products

        WHERE id = ?
        """,
        (
            str(product_id),
        )
    )

    deleted = (
        cursor.rowcount > 0
    )

    connection.commit()

    connection.close()

    return deleted


# ============================================================
# SEARCH PRODUCT LIBRARY
# ============================================================

def search_product_library(
    query="",
    category=None,
):
    """
    Search products by name,
    manufacturer, model or category.
    """

    products = (
        load_product_library()
    )

    query = str(
        query or ""
    ).lower().strip()

    results = []

    for product in products:

        if category:

            if product.get(
                "category"
            ) != category:

                continue

        if query:

            searchable_text = " ".join(
                [
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
                            "technology",
                            ""
                        )
                    ),

                    str(
                        product.get(
                            "category",
                            ""
                        )
                    ),
                ]
            ).lower()

            if query not in searchable_text:

                continue

        results.append(
            product
        )

    return results


# ============================================================
# SERVICE LIBRARY
# ============================================================

def create_service_record(
    service
):
    """
    Normalize a service record.
    """

    service = dict(
        service or {}
    )

    if not service.get("id"):

        service["id"] = (
            f"service_"
            f"{datetime.now().strftime('%Y%m%d%H%M%S%f')}"
        )

    return {

        **service,

        "name": str(
            service.get(
                "name",
                ""
            )
        ),

        "category": str(
            service.get(
                "category",
                "Other"
            )
        ),

        "description": str(
            service.get(
                "description",
                ""
            )
        ),

        "provider": str(
            service.get(
                "provider",
                ""
            )
        ),

        "country": str(
            service.get(
                "country",
                ""
            )
        ),

        "price": safe_float(
            service.get(
                "price",
                0
            )
        ),

        "currency": str(
            service.get(
                "currency",
                "USD"
            )
        ),

        "unit": str(
            service.get(
                "unit",
                "Unit"
            )
        ),

        "notes": str(
            service.get(
                "notes",
                ""
            )
        ),
    }


def add_service_to_library(
    service
):

    initialize_database()

    service = create_service_record(
        service
    )

    now = datetime.now().isoformat()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO services (

            id,
            name,
            category,
            description,
            provider,
            country,
            price,
            currency,
            unit,
            notes,
            service_data,
            created_at,
            updated_at

        )

        VALUES (

            :id,
            :name,
            :category,
            :description,
            :provider,
            :country,
            :price,
            :currency,
            :unit,
            :notes,
            :service_data,
            :created_at,
            :updated_at

        )

        ON CONFLICT(id)

        DO UPDATE SET

            name = excluded.name,
            category = excluded.category,
            description = excluded.description,
            provider = excluded.provider,
            country = excluded.country,
            price = excluded.price,
            currency = excluded.currency,
            unit = excluded.unit,
            notes = excluded.notes,
            service_data = excluded.service_data,
            updated_at = excluded.updated_at
        """,

        {
            **service,

            "service_data": json.dumps(
                service
            ),

            "created_at": now,

            "updated_at": now,
        }
    )

    connection.commit()

    connection.close()

    return service


def load_service_library():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *

        FROM services

        ORDER BY updated_at DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    services = []

    for row in rows:

        service = dict(row)

        raw_data = service.get(
            "service_data"
        )

        if raw_data:

            try:

                stored = json.loads(
                    raw_data
                )

                if isinstance(
                    stored,
                    dict
                ):

                    service = stored

            except Exception:

                pass

        service.pop(
            "service_data",
            None
        )

        service.pop(
            "created_at",
            None
        )

        service.pop(
            "updated_at",
            None
        )

        services.append(
            service
        )

    return services


def save_service_library(
    services
):

    if not isinstance(
        services,
        list
    ):

        raise ValueError(
            "Services must be a list."
        )

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM services"
    )

    connection.commit()

    connection.close()

    for service in services:

        add_service_to_library(
            service
        )

    return True


def remove_service_from_library(
    service_id
):

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM services

        WHERE id = ?
        """,
        (
            str(service_id),
        )
    )

    deleted = (
        cursor.rowcount > 0
    )

    connection.commit()

    connection.close()

    return deleted


def clear_product_library():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM products"
    )

    connection.commit()

    connection.close()

    return True


def clear_service_library():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM services"
    )

    connection.commit()

    connection.close()

    return True


def clear_all_libraries():

    clear_product_library()

    clear_service_library()

    return True


# ============================================================
# BACKUP DATABASE
# ============================================================

def backup_library():
    """
    Create a JSON backup of all libraries.
    """

    ensure_data_directory()

    backup_dir = (
        DATA_DIR / "backups"
    )

    backup_dir.mkdir(
        parents=True,
        exist_ok=True,
    )

    timestamp = (
        datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )
    )

    backup_file = (
        backup_dir
        / f"library_backup_{timestamp}.json"
    )

    backup_data = {

        "created_at": (
            datetime.now().isoformat()
        ),

        "products": (
            load_product_library()
        ),

        "services": (
            load_service_library()
        ),
    }

    with open(
        backup_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            backup_data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return backup_file


# ============================================================
# LIBRARY SUMMARY
# ============================================================

def get_library_summary():

    products = (
        load_product_library()
    )

    services = (
        load_service_library()
    )

    categories = {}

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

    return {

        "total_products": len(
            products
        ),

        "total_services": len(
            services
        ),

        "product_categories": categories,

        "database_file": str(
            DATABASE_FILE
        ),
    }


# ============================================================
# BACKWARD COMPATIBILITY
# ============================================================

def load_json_file(file_path):
    """
    Compatibility function.
    """

    path = Path(file_path)

    if not path.exists():

        return []

    try:

        with open(
            path,
            "r",
            encoding="utf-8",
        ) as file:

            return json.load(file)

    except Exception:

        return []


def save_json_file(
    file_path,
    data,
):
    """
    Compatibility function.
    """

    path = Path(file_path)

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        path,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            data,
            file,
            indent=4,
            ensure_ascii=False,
        )

    return True


# ============================================================
# INITIALIZE DATABASE
# ============================================================

initialize_database()
