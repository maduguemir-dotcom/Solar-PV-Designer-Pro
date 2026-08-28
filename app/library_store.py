# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# PRODUCT LIBRARY STORAGE ENGINE
#
# Central SQLite Storage
#
# Database:
# app/data/solar_pv_library.db
# ==========================================================

import sqlite3
from pathlib import Path
from datetime import datetime
import json
import shutil


# ==========================================================
# PATH CONFIGURATION
# ==========================================================

APP_DIR = Path(__file__).resolve().parent

DATA_DIR = APP_DIR / "data"

DATA_DIR.mkdir(
    parents=True,
    exist_ok=True
)


DATABASE_FILE = (
    DATA_DIR /
    "solar_pv_library.db"
)


BACKUP_DIR = (
    DATA_DIR /
    "backups"
)

BACKUP_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# Backward-compatible constants
DB_PATH = DATABASE_FILE

PRODUCT_LIBRARY_FILE = DATABASE_FILE

SERVICE_LIBRARY_FILE = DATABASE_FILE


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_connection():

    connection = sqlite3.connect(
        str(DATABASE_FILE)
    )

    connection.row_factory = sqlite3.Row

    return connection


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

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

            efficiency_percent REAL DEFAULT 0,

            warranty_years REAL DEFAULT 0,

            price REAL DEFAULT 0,

            currency TEXT DEFAULT 'USD',

            quantity INTEGER DEFAULT 1,

            notes TEXT,

            capacity_ah REAL DEFAULT 0,

            energy_kwh REAL DEFAULT 0,

            supplier TEXT,

            country TEXT,

            specifications TEXT,

            created_at TEXT,

            updated_at TEXT
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS services (

            id TEXT PRIMARY KEY,

            name TEXT NOT NULL,

            category TEXT,

            provider TEXT,

            description TEXT,

            price REAL DEFAULT 0,

            currency TEXT DEFAULT 'USD',

            notes TEXT,

            created_at TEXT,

            updated_at TEXT
        )
        """
    )

    connection.commit()

    connection.close()

    return True


# Initialize database automatically
initialize_database()


# ==========================================================
# UTILITY FUNCTIONS
# ==========================================================

def safe_float(value, default=0.0):

    try:

        if value is None:

            return default

        return float(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def safe_int(value, default=0):

    try:

        if value is None:

            return default

        return int(value)

    except (
        TypeError,
        ValueError
    ):

        return default


def generate_product_id(product):

    existing_id = product.get(
        "id"
    )

    if existing_id:

        return str(existing_id)

    timestamp = datetime.now().strftime(
        "%Y%m%d%H%M%S%f"
    )

    return f"product_{timestamp}"


def normalize_product(product):

    if product is None:

        product = {}

    product = dict(product)

    return {

        "id": generate_product_id(product),

        "name": str(
            product.get(
                "name",
                ""
            )
        ),

        "category": str(
            product.get(
                "category",
                ""
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
                ""
            )
        ),

        "rated_power_w": safe_float(
            product.get(
                "rated_power_w",
                product.get(
                    "power",
                    0
                )
            )
        ),

        "voltage_v": safe_float(
            product.get(
                "voltage_v",
                product.get(
                    "voltage",
                    0
                )
            )
        ),

        "current_a": safe_float(
            product.get(
                "current_a",
                product.get(
                    "current",
                    0
                )
            )
        ),

        "efficiency_percent": safe_float(
            product.get(
                "efficiency_percent",
                product.get(
                    "efficiency",
                    0
                )
            )
        ),

        "warranty_years": safe_float(
            product.get(
                "warranty_years",
                product.get(
                    "warranty",
                    0
                )
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

        "quantity": safe_int(
            product.get(
                "quantity",
                1
            ),
            1
        ),

        "notes": str(
            product.get(
                "notes",
                ""
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

        "specifications": product.get(
            "specifications",
            {}
        )
    }


# ==========================================================
# ADD PRODUCT
# ==========================================================

def add_product_to_library(product):

    product = normalize_product(
        product
    )

    timestamp = datetime.now().isoformat()

    specifications = product.get(
        "specifications",
        {}
    )

    if not isinstance(
        specifications,
        str
    ):

        specifications = json.dumps(
            specifications
        )


    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO products (

            id,
            name,
            category,
            manufacturer,
            model,
            technology,
            rated_power_w,
            voltage_v,
            current_a,
            efficiency_percent,
            warranty_years,
            price,
            currency,
            quantity,
            notes,
            capacity_ah,
            energy_kwh,
            supplier,
            country,
            specifications,
            created_at,
            updated_at

        )

        VALUES (

            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
        )
        """,
        (

            product["id"],
            product["name"],
            product["category"],
            product["manufacturer"],
            product["model"],
            product["technology"],
            product["rated_power_w"],
            product["voltage_v"],
            product["current_a"],
            product["efficiency_percent"],
            product["warranty_years"],
            product["price"],
            product["currency"],
            product["quantity"],
            product["notes"],
            product["capacity_ah"],
            product["energy_kwh"],
            product["supplier"],
            product["country"],
            specifications,
            timestamp,
            timestamp
        )
    )

    connection.commit()

    connection.close()

    return product


# ==========================================================
# LOAD PRODUCTS
# ==========================================================

def load_product_library():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY name ASC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    products = []

    for row in rows:

        product = dict(row)

        specifications = product.get(
            "specifications"
        )

        if specifications:

            try:

                product[
                    "specifications"
                ] = json.loads(
                    specifications
                )

            except Exception:

                pass

        else:

            product[
                "specifications"
            ] = {}

        products.append(
            product
        )

    return products


# ==========================================================
# SAVE PRODUCT LIBRARY
# ==========================================================

def save_product_library(products):

    if products is None:

        products = []


    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        """
    )

    connection.commit()

    connection.close()


    for product in products:

        add_product_to_library(
            product
        )

    return True


# ==========================================================
# GET PRODUCT
# ==========================================================

def get_product_from_library(product_id):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id = ?
        """,
        (
            str(product_id),
        )
    )

    row = cursor.fetchone()

    connection.close()

    if row is None:

        return None


    product = dict(row)

    specifications = product.get(
        "specifications"
    )

    if specifications:

        try:

            product[
                "specifications"
            ] = json.loads(
                specifications
            )

        except Exception:

            pass

    return product


# ==========================================================
# UPDATE PRODUCT
# ==========================================================

def update_product_in_library(
    product_id,
    updated_product
):

    existing_product = (
        get_product_from_library(
            product_id
        )
    )

    if existing_product is None:

        return False


    merged_product = dict(
        existing_product
    )

    merged_product.update(
        dict(updated_product)
    )

    merged_product[
        "id"
    ] = str(product_id)

    normalized = normalize_product(
        merged_product
    )

    specifications = normalized.get(
        "specifications",
        {}
    )

    if not isinstance(
        specifications,
        str
    ):

        specifications = json.dumps(
            specifications
        )


    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE products

        SET

            name = ?,
            category = ?,
            manufacturer = ?,
            model = ?,
            technology = ?,
            rated_power_w = ?,
            voltage_v = ?,
            current_a = ?,
            efficiency_percent = ?,
            warranty_years = ?,
            price = ?,
            currency = ?,
            quantity = ?,
            notes = ?,
            capacity_ah = ?,
            energy_kwh = ?,
            supplier = ?,
            country = ?,
            specifications = ?,
            updated_at = ?

        WHERE id = ?
        """,
        (

            normalized["name"],
            normalized["category"],
            normalized["manufacturer"],
            normalized["model"],
            normalized["technology"],
            normalized["rated_power_w"],
            normalized["voltage_v"],
            normalized["current_a"],
            normalized["efficiency_percent"],
            normalized["warranty_years"],
            normalized["price"],
            normalized["currency"],
            normalized["quantity"],
            normalized["notes"],
            normalized["capacity_ah"],
            normalized["energy_kwh"],
            normalized["supplier"],
            normalized["country"],
            specifications,
            datetime.now().isoformat(),
            str(product_id)
        )
    )

    connection.commit()

    connection.close()

    return True


# ==========================================================
# DELETE PRODUCT
# ==========================================================

def remove_product_from_library(
    product_id
):

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

    deleted = cursor.rowcount > 0

    connection.commit()

    connection.close()

    return deleted


# ==========================================================
# SEARCH PRODUCTS
# ==========================================================

def search_product_library(
    query="",
    category=None
):

    products = load_product_library()

    results = []

    query = str(
        query or ""
    ).lower().strip()


    for product in products:

        if category:

            if product.get(
                "category"
            ) != category:

                continue


        if not query:

            results.append(
                product
            )

            continue


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
                        "category",
                        ""
                    )
                ),

                str(
                    product.get(
                        "technology",
                        ""
                    )
                )

            ]
        ).lower()


        if query in searchable_text:

            results.append(
                product
            )


    return results


# ==========================================================
# CLEAR PRODUCT LIBRARY
# ==========================================================

def clear_product_library():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        """
    )

    connection.commit()

    connection.close()

    return True


# ==========================================================
# PRODUCT LIBRARY SUMMARY
# ==========================================================

def get_product_library_summary():

    products = load_product_library()

    categories = {}

    total_quantity = 0


    for product in products:

        category = (
            product.get(
                "category"
            )
            or "Uncategorized"
        )


        categories[
            category
        ] = (
            categories.get(
                category,
                0
            )
            + 1
        )


        total_quantity += safe_int(
            product.get(
                "quantity",
                1
            ),
            1
        )


    return {

        "total_products":
            len(products),

        "total_quantity":
            total_quantity,

        "product_categories":
            categories,

        "database_file":
            str(DATABASE_FILE)

    }


# ==========================================================
# SERVICE FUNCTIONS
# ==========================================================

def create_service_record(
    service
):

    if service is None:

        service = {}

    service = dict(service)

    service_id = service.get(
        "id"
    )

    if not service_id:

        timestamp = (
            datetime.now().strftime(
                "%Y%m%d%H%M%S%f"
            )
        )

        service_id = (
            f"service_{timestamp}"
        )


    timestamp = datetime.now().isoformat()


    return {

        "id":
            str(service_id),

        "name":
            str(
                service.get(
                    "name",
                    ""
                )
            ),

        "category":
            str(
                service.get(
                    "category",
                    ""
                )
            ),

        "provider":
            str(
                service.get(
                    "provider",
                    ""
                )
            ),

        "description":
            str(
                service.get(
                    "description",
                    ""
                )
            ),

        "price":
            safe_float(
                service.get(
                    "price",
                    0
                )
            ),

        "currency":
            str(
                service.get(
                    "currency",
                    "USD"
                )
            ),

        "notes":
            str(
                service.get(
                    "notes",
                    ""
                )
            ),

        "created_at":
            timestamp,

        "updated_at":
            timestamp
    }


def add_service_to_library(
    service
):

    service = create_service_record(
        service
    )


    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT OR REPLACE INTO services (

            id,
            name,
            category,
            provider,
            description,
            price,
            currency,
            notes,
            created_at,
            updated_at

        )

        VALUES (
            ?, ?, ?, ?, ?, ?,
            ?, ?, ?, ?
        )
        """,
        (

            service["id"],
            service["name"],
            service["category"],
            service["provider"],
            service["description"],
            service["price"],
            service["currency"],
            service["notes"],
            service["created_at"],
            service["updated_at"]

        )
    )

    connection.commit()

    connection.close()

    return service


def load_service_library():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM services
        ORDER BY name ASC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return [

        dict(row)

        for row in rows

    ]


def save_service_library(
    services
):

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM services
        """
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

    deleted = cursor.rowcount > 0

    connection.commit()

    connection.close()

    return deleted


def search_service_library(
    query=""
):

    services = load_service_library()

    query = str(
        query or ""
    ).lower().strip()


    if not query:

        return services


    results = []


    for service in services:

        searchable_text = " ".join(

            [

                str(
                    service.get(
                        "name",
                        ""
                    )
                ),

                str(
                    service.get(
                        "provider",
                        ""
                    )
                ),

                str(
                    service.get(
                        "category",
                        ""
                    )
                )

            ]

        ).lower()


        if query in searchable_text:

            results.append(
                service
            )


    return results


def clear_service_library():

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM services
        """
    )

    connection.commit()

    connection.close()

    return True


# ==========================================================
# BACKUP LIBRARY
# ==========================================================

def backup_library():

    initialize_database()

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )


    backup_file = (

        BACKUP_DIR /

        f"solar_pv_library_backup_"
        f"{timestamp}.db"

    )


    shutil.copy2(
        DATABASE_FILE,
        backup_file
    )


    return str(
        backup_file
    )


# ==========================================================
# BACKWARD COMPATIBILITY FUNCTIONS
# ==========================================================

def ensure_data_directory():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return DATA_DIR


def get_library_summary():

    product_summary = (
        get_product_library_summary()
    )

    services = load_service_library()


    return {

        "total_products":
            product_summary[
                "total_products"
            ],

        "total_services":
            len(services),

        "product_categories":
            product_summary[
                "product_categories"
            ],

        "database_file":
            str(DATABASE_FILE)

    }


def clear_all_libraries():

    clear_product_library()

    clear_service_library()

    return True


# ==========================================================
# LEGACY JSON COMPATIBILITY
# ==========================================================

def load_json_file(file_path):

    file_path = Path(
        file_path
    )

    if not file_path.exists():

        return []


    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return json.load(
                file
            )

    except Exception:

        return []


def save_json_file(
    file_path,
    data
):

    file_path = Path(
        file_path
    )

    file_path.parent.mkdir(
        parents=True,
        exist_ok=True
    )


    with open(
        file_path,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


    return True
