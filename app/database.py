# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Persistent Database Layer
# Version: 2.4.0
# ==========================================================

import sqlite3
from pathlib import Path
from datetime import datetime


# ==========================================================
# DATABASE LOCATION
# ==========================================================

APP_DIR = Path(__file__).resolve().parent

DATA_DIR = APP_DIR / "data"

DATABASE_FILE = DATA_DIR / "solar_pv_designer.db"


# ==========================================================
# DATABASE INITIALIZATION
# ==========================================================

def ensure_database_directory():

    DATA_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    return DATA_DIR


def get_connection():

    ensure_database_directory()

    connection = sqlite3.connect(
        DATABASE_FILE,
        check_same_thread=False
    )

    connection.row_factory = sqlite3.Row

    return connection


def initialize_database():

    connection = get_connection()

    cursor = connection.cursor()

    # ------------------------------------------------------
    # PRODUCTS
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            category TEXT DEFAULT '',

            manufacturer TEXT DEFAULT '',

            model TEXT DEFAULT '',

            technology TEXT DEFAULT '',

            rated_power_w REAL DEFAULT 0,

            voltage_v REAL DEFAULT 0,

            capacity_ah REAL DEFAULT 0,

            energy_kwh REAL DEFAULT 0,

            efficiency_percent REAL DEFAULT 0,

            warranty_years REAL DEFAULT 0,

            supplier TEXT DEFAULT '',

            country TEXT DEFAULT '',

            notes TEXT DEFAULT '',

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )
    """)

    # ------------------------------------------------------
    # SERVICES
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS services (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            category TEXT DEFAULT '',

            unit TEXT DEFAULT 'job',

            unit_price REAL DEFAULT 0,

            currency TEXT DEFAULT 'UGX',

            supplier TEXT DEFAULT '',

            location TEXT DEFAULT '',

            notes TEXT DEFAULT '',

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )
    """)

    # ------------------------------------------------------
    # COST ITEMS
    # ------------------------------------------------------

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cost_items (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            name TEXT NOT NULL,

            category TEXT DEFAULT '',

            unit TEXT DEFAULT 'item',

            unit_price REAL DEFAULT 0,

            quantity REAL DEFAULT 1,

            currency TEXT DEFAULT 'UGX',

            supplier TEXT DEFAULT '',

            location TEXT DEFAULT '',

            notes TEXT DEFAULT '',

            created_at TEXT NOT NULL,

            updated_at TEXT NOT NULL

        )
    """)

    # ------------------------------------------------------
    # SAVE
    # ------------------------------------------------------

    connection.commit()

    connection.close()

    return True


# ==========================================================
# GENERIC HELPERS
# ==========================================================

def _now():

    return datetime.now().isoformat()


def _row_to_dict(row):

    if row is None:

        return None

    return dict(row)


def _rows_to_dicts(rows):

    return [
        dict(row)
        for row in rows
    ]


# ==========================================================
# PRODUCT FUNCTIONS
# ==========================================================

def add_product(product):

    initialize_database()

    now = _now()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO products (

            name,
            category,
            manufacturer,
            model,
            technology,
            rated_power_w,
            voltage_v,
            capacity_ah,
            energy_kwh,
            efficiency_percent,
            warranty_years,
            supplier,
            country,
            notes,
            created_at,
            updated_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (

            product.get("name", ""),

            product.get(
                "category",
                ""
            ),

            product.get(
                "manufacturer",
                ""
            ),

            product.get(
                "model",
                ""
            ),

            product.get(
                "technology",
                ""
            ),

            float(
                product.get(
                    "rated_power_w",
                    0
                ) or 0
            ),

            float(
                product.get(
                    "voltage_v",
                    0
                ) or 0
            ),

            float(
                product.get(
                    "capacity_ah",
                    0
                ) or 0
            ),

            float(
                product.get(
                    "energy_kwh",
                    0
                ) or 0
            ),

            float(
                product.get(
                    "efficiency_percent",
                    0
                ) or 0
            ),

            float(
                product.get(
                    "warranty_years",
                    0
                ) or 0
            ),

            product.get(
                "supplier",
                ""
            ),

            product.get(
                "country",
                ""
            ),

            product.get(
                "notes",
                ""
            ),

            now,

            now

        )
    )

    product_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return product_id


def get_products():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return _rows_to_dicts(rows)


def get_product(
    product_id
):

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products
        WHERE id = ?
        """,

        (product_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return _row_to_dict(row)


def delete_product(
    product_id
):

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM products
        WHERE id = ?
        """,

        (product_id,)
    )

    deleted = cursor.rowcount

    connection.commit()

    connection.close()

    return deleted > 0


# ==========================================================
# SERVICE FUNCTIONS
# ==========================================================

def add_service(service):

    initialize_database()

    now = _now()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO services (

            name,
            category,
            unit,
            unit_price,
            currency,
            supplier,
            location,
            notes,
            created_at,
            updated_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (

            service.get(
                "name",
                ""
            ),

            service.get(
                "category",
                ""
            ),

            service.get(
                "unit",
                "job"
            ),

            float(
                service.get(
                    "unit_price",
                    0
                ) or 0
            ),

            service.get(
                "currency",
                "UGX"
            ),

            service.get(
                "supplier",
                ""
            ),

            service.get(
                "location",
                ""
            ),

            service.get(
                "notes",
                ""
            ),

            now,

            now

        )
    )

    service_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return service_id


def get_services():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM services
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return _rows_to_dicts(rows)


def get_service(
    service_id
):

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM services
        WHERE id = ?
        """,

        (service_id,)
    )

    row = cursor.fetchone()

    connection.close()

    return _row_to_dict(row)


def delete_service(
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

        (service_id,)
    )

    deleted = cursor.rowcount

    connection.commit()

    connection.close()

    return deleted > 0


# ==========================================================
# COST ITEM FUNCTIONS
# ==========================================================

def add_cost_item(
    item
):

    initialize_database()

    now = _now()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO cost_items (

            name,
            category,
            unit,
            unit_price,
            quantity,
            currency,
            supplier,
            location,
            notes,
            created_at,
            updated_at

        )

        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,

        (

            item.get(
                "name",
                ""
            ),

            item.get(
                "category",
                ""
            ),

            item.get(
                "unit",
                "item"
            ),

            float(
                item.get(
                    "unit_price",
                    0
                ) or 0
            ),

            float(
                item.get(
                    "quantity",
                    1
                ) or 1
            ),

            item.get(
                "currency",
                "UGX"
            ),

            item.get(
                "supplier",
                ""
            ),

            item.get(
                "location",
                ""
            ),

            item.get(
                "notes",
                ""
            ),

            now,

            now

        )
    )

    item_id = cursor.lastrowid

    connection.commit()

    connection.close()

    return item_id


def get_cost_items():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM cost_items
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    return _rows_to_dicts(rows)


def delete_cost_item(
    item_id
):

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        DELETE FROM cost_items
        WHERE id = ?
        """,

        (item_id,)
    )

    deleted = cursor.rowcount

    connection.commit()

    connection.close()

    return deleted > 0


# ==========================================================
# SEARCH
# ==========================================================

def search_products(
    query
):

    initialize_database()

    query = str(
        query
    ).strip()

    if not query:

        return get_products()

    pattern = f"%{query}%"

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM products

        WHERE
            name LIKE ?
            OR category LIKE ?
            OR manufacturer LIKE ?
            OR model LIKE ?
            OR technology LIKE ?
            OR supplier LIKE ?
            OR country LIKE ?

        ORDER BY name
        """,

        (
            pattern,
            pattern,
            pattern,
            pattern,
            pattern,
            pattern,
            pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return _rows_to_dicts(rows)


def search_services(
    query
):

    initialize_database()

    query = str(
        query
    ).strip()

    if not query:

        return get_services()

    pattern = f"%{query}%"

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT *
        FROM services

        WHERE
            name LIKE ?
            OR category LIKE ?
            OR supplier LIKE ?
            OR location LIKE ?

        ORDER BY name
        """,

        (
            pattern,
            pattern,
            pattern,
            pattern
        )
    )

    rows = cursor.fetchall()

    connection.close()

    return _rows_to_dicts(rows)


# ==========================================================
# DATABASE SUMMARY
# ==========================================================

def get_database_summary():

    initialize_database()

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        "SELECT COUNT(*) FROM products"
    )

    product_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM services"
    )

    service_count = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM cost_items"
    )

    cost_count = cursor.fetchone()[0]

    connection.close()

    return {

        "database":
            str(DATABASE_FILE),

        "products":
            product_count,

        "services":
            service_count,

        "cost_items":
            cost_count,

        "total_records":
            (
                product_count
                + service_count
                + cost_count
            )

    }


# ==========================================================
# BACKUP DATABASE
# ==========================================================

def backup_database():

    initialize_database()

    backup_dir = (
        DATA_DIR / "backups"
    )

    backup_dir.mkdir(
        parents=True,
        exist_ok=True
    )

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_file = (
        backup_dir /
        f"solar_pv_designer_{timestamp}.db"
    )

    source = get_connection()

    destination = sqlite3.connect(
        backup_file
    )

    try:

        source.backup(
            destination
        )

        destination.close()

        source.close()

        return {

            "success":
                True,

            "file":
                str(backup_file)

        }

    except Exception as error:

        try:
            destination.close()
        except Exception:
            pass

        try:
            source.close()
        except Exception:
            pass

        return {

            "success":
                False,

            "message":
                str(error)

        }


# ==========================================================
# INITIALIZE WHEN IMPORTED
# ==========================================================

initialize_database()
