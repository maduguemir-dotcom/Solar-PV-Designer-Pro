# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA(TM) - Product Library UI v2.4
# ==========================================================
"""Category-aware product library UI for Solar PV Designer Pro Africa v2.4.

The UI prefers the project's existing library_store.py/product_engine.py.  It
keeps the public function names used by the existing diagnostics and adds a
category-specific Add Product form and category-specific library views.
"""
import inspect
import json
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path

import pandas as pd
import streamlit as st

APP_DIR = Path(__file__).resolve().parent
DB_PATH = APP_DIR / "product_library.db"
BACKUP_DIR = APP_DIR / "backups"

PRODUCT_CATEGORIES = [
    "Solar Panel", "Battery", "Inverter", "Charge Controller",
    "Mounting Structure", "Solar Cable", "Protection",
    "Labour & Services", "Transport & Logistics", "Other",
]
PRODUCT_TECHNOLOGIES = [
    "Monocrystalline", "Polycrystalline", "Thin Film", "Lithium",
    "LiFePO4", "Lead Acid", "AGM", "Gel", "Hybrid", "Off Grid",
    "On Grid", "MPPT", "PWM", "Other",
]
CURRENCIES = ["USD", "UGX", "NGN", "KES", "TZS", "RWF", "GHS", "ZAR", "ETB", "EUR", "GBP"]
META = {
    "Solar Panel": ("☀️", "Photovoltaic modules and solar panels."),
    "Battery": ("🔋", "Energy-storage batteries and battery banks."),
    "Inverter": ("⚡", "Off-grid, on-grid and hybrid inverters."),
    "Charge Controller": ("🔌", "MPPT and PWM solar charge controllers."),
    "Mounting Structure": ("🏗️", "Roof, ground and other PV mounting structures."),
    "Solar Cable": ("🔗", "PV cables, wires and accessories."),
    "Protection": ("🛡️", "Breakers, fuses, SPD and isolation devices."),
    "Labour & Services": ("🔧", "Installation, commissioning and maintenance services."),
    "Transport & Logistics": ("🚚", "Delivery, transport and logistics."),
    "Other": ("📦", "Other project components and procurement items."),
}

# field: key, label, type, unit, default, min, max, step, options
SCHEMA = {
    "Solar Panel": [
        ("Electrical Specifications", [
            ("rated_power_w", "Rated Power", "number", "W", 550, 0, None, 10, None),
            ("voc_v", "Open-Circuit Voltage (Voc)", "number", "V", 49.8, 0, None, .1, None),
            ("vmp_v", "Maximum-Power Voltage (Vmp)", "number", "V", 41.5, 0, None, .1, None),
            ("isc_a", "Short-Circuit Current (Isc)", "number", "A", 14, 0, None, .1, None),
            ("imp_a", "Maximum-Power Current (Imp)", "number", "A", 13.25, 0, None, .1, None),
            ("efficiency_percent", "Module Efficiency", "number", "%", 21, 0, 100, .1, None),
            ("max_system_voltage_v", "Maximum System Voltage", "number", "V", 1000, 0, None, 10, None),
            ("max_series_fuse_a", "Maximum Series Fuse", "number", "A", 25, 0, None, 1, None),
        ]),
        ("Physical Specifications", [
            ("length_mm", "Length", "number", "mm", 2278, 0, None, 1, None),
            ("width_mm", "Width", "number", "mm", 1134, 0, None, 1, None),
            ("thickness_mm", "Thickness", "number", "mm", 35, 0, None, 1, None),
            ("weight_kg", "Weight", "number", "kg", 28, 0, None, .1, None),
            ("cell_count", "Cell Count", "", "", 144, 0, None, 1, None),
            ("cell_technology", "Cell Technology", "select", "", "N-Type TOPCon", None, None, None, ["P-Type PERC", "N-Type TOPCon", "HJT", "IBC", "Thin Film", "Other"]),
        ]),
        ("Warranty", [("product_warranty_years", "Product Warranty", "number", "years", 12, 0, 50, 1, None), ("performance_warranty_years", "Performance Warranty", "number", "years", 25, 0, 50, 1, None)]),
    ],
    "Battery": [
        ("Electrical & Energy", [
            ("nominal_voltage_v", "Nominal Voltage", "number", "V", 51.2, 0, None, .1, None),
            ("capacity_ah", "Capacity", "number", "Ah", 100, 0, None, 1, None),
            ("energy_kwh", "Nominal Energy", "number", "kWh", 5.12, 0, None, .01, None),
            ("depth_of_discharge_percent", "Depth of Discharge", "number", "%", 90, 0, 100, 1, None),
            ("max_charge_current_a", "Maximum Charge Current", "number", "A", 100, 0, None, 1, None),
            ("max_discharge_current_a", "Maximum Discharge Current", "number", "A", 100, 0, None, 1, None),
            ("round_trip_efficiency_percent", "Round-Trip Efficiency", "number", "%", 95, 0, 100, .1, None),
            ("chemistry", "Chemistry", "select", "", "LiFePO4", None, None, None, ["LiFePO4", "NMC", "Lead Acid", "AGM", "Gel", "Other"]),
            ("cycle_life", "Cycle Life", "number", "cycles", 6000, 0, None, 100, None),
            ("warranty_years", "Warranty", "number", "years", 5, 0, 30, 1, None),
        ]),
    ],
    "Inverter": [
        ("Power & Voltage", [
            ("rated_power_w", "Rated Output Power", "number", "W", 5000, 0, None, 100, None),
            ("surge_power_w", "Surge Power", "number", "W", 10000, 0, None, 100, None),
            ("dc_nominal_voltage_v", "DC Nominal Voltage", "number", "V", 48, 0, None, 1, None),
            ("ac_output_voltage_v", "AC Output Voltage", "number", "V", 230, 0, None, 1, None),
            ("frequency_hz", "Frequency", "number", "Hz", 50, 0, None, 1, None),
            ("phase", "Phase", "select", "", "Single Phase", None, None, None, ["Single Phase", "Three Phase"]),
            ("max_pv_input_power_w", "Maximum PV Input Power", "number", "W", 6500, 0, None, 100, None),
            ("mppt_min_voltage_v", "MPPT Minimum Voltage", "number", "V", 120, 0, None, 1, None),
            ("mppt_max_voltage_v", "MPPT Maximum Voltage", "number", "V", 450, 0, None, 1, None),
            ("mppt_count", "Number of MPPTs", "number", "", 2, 0, None, 1, None),
            ("efficiency_percent", "Efficiency", "number", "%", 95, 0, 100, .1, None),
            ("warranty_years", "Warranty", "number", "years", 5, 0, 30, 1, None),
        ]),
    ],
    "Charge Controller": [
        ("Controller Specifications", [
            ("controller_type", "Controller Type", "select", "", "MPPT", None, None, None, ["MPPT", "PWM"]),
            ("system_voltage_v", "System Voltage", "number", "V", 48, 0, None, 1, None),
            ("max_charge_current_a", "Maximum Charge Current", "number", "A", 100, 0, None, 1, None),
            ("max_pv_input_power_w", "Maximum PV Input Power", "number", "W", 5000, 0, None, 100, None),
            ("max_pv_voltage_v", "Maximum PV Voltage", "number", "V", 150, 0, None, 1, None),
            ("efficiency_percent", "Efficiency", "number", "%", 98, 0, 100, .1, None),
            ("warranty_years", "Warranty", "number", "years", 3, 0, 30, 1, None),
        ]),
    ],
    "Mounting Structure": [
        ("Structure", [
            ("structure_type", "Structure Type", "select", "", "Roof Mount", None, None, None, ["Roof Mount", "Ground Mount", "Carport", "Pole Mount", "Other"]),
            ("material", "Material", "select", "", "Aluminium", None, None, None, ["Aluminium", "Galvanized Steel", "Stainless Steel", "Other"]),
            ("panel_capacity", "Panel Capacity", "number", "panels", 10, 1, None, 1, None),
            ("roof_type", "Roof Type", "select", "", "Metal", None, None, None, ["Metal", "Tile", "Concrete", "Thatch", "Other"]),
            ("wind_rating_kmh", "Wind Rating", "number", "km/h", 150, 0, None, 5, None),
            ("warranty_years", "Warranty", "number", "years", 10, 0, 30, 1, None),
        ]),
    ],
    "Solar Cable": [
        ("Cable Specifications", [
            ("cross_section_mm2", "Cross Section", "number", "mm²", 6, .5, None, .5, None),
            ("conductor_material", "Conductor Material", "select", "", "Copper", None, None, None, ["Copper", "Aluminium"]),
            ("cable_length_m", "Cable Length", "number", "m", 100, 0, None, 1, None),
            ("voltage_rating_v", "Voltage Rating", "number", "V", 1500, 0, None, 10, None),
            ("uv_resistant", "UV Resistant", "select", "", "Yes", None, None, None, ["Yes", "No"]),
        ]),
    ],
    "Protection": [
        ("Protection Specifications", [
            ("protection_type", "Protection Type", "select", "", "DC Breaker", None, None, None, ["DC Breaker", "AC Breaker", "Fuse", "SPD", "Isolator", "Other"]),
            ("rated_voltage_v", "Rated Voltage", "number", "V", 1000, 0, None, 10, None),
            ("rated_current_a", "Rated Current", "number", "A", 25, 0, None, 1, None),
            ("poles", "Poles", "number", "", 2, 1, 4, 1, None),
            ("breaking_capacity_ka", "Breaking Capacity", "number", "kA", 10, 0, None, .5, None),
            ("dc_or_ac", "Application", "select", "", "DC", None, None, None, ["DC", "AC", "DC/AC"]),
        ]),
    ],
    "Labour & Services": [
        ("Service", [
            ("service_type", "Service Type", "select", "", "Installation", None, None, None, ["Installation", "Commissioning", "Maintenance", "Inspection", "Consultancy", "Other"]),
            ("billing_unit", "Billing Unit", "select", "", "Project", None, None, None, ["Project", "Hour", "Day", "Panel", "kW"]),
            ("estimated_hours", "Estimated Hours", "number", "hours", 8, 0, None, .5, None),
            ("labour_rate", "Labour Rate", "number", "per unit", 0, 0, None, 100, None),
        ]),
    ],
    "Transport & Logistics": [
        ("Logistics", [
            ("service_type", "Service Type", "select", "", "Delivery", None, None, None, ["Delivery", "Transport", "Other"]),
            ("billing_unit", "Billing Unit", "select", "", "Trip", None, None, None, ["Trip", "Day", "km"]),
            ("distance_km", "Distance", "number", "km", 0, 0, None, 1, None),
            ("vehicle_type", "Vehicle Type", "select", "", "Pickup", None, None, None, ["Pickup", "Truck", "Van", "Motorcycle", "Other"]),
            ("transport_rate", "Transport Rate", "number", "per unit", 0, 0, None, 100, None),
        ]),
    ],
    "Other": [
        ("General Specifications", [
            ("description", "Description", "text", "", "", None, None, None, None),
            ("unit", "Unit", "text", "", "piece", None, None, None, None),
            ("warranty_years", "Warranty", "number", "years", 0, 0, 30, 1, None),
        ]),
    ],
}


def get_category_icon(category):
    return META.get(category, META["Other"])[0]


def get_category_description(category):
    return META.get(category, META["Other"])[1]


def get_category_sections(category):
    return {
        section: [
            {"name": f[0], "label": f[1], "type": f[2], "unit": f[3],
             "default": f[4], "min": f[5], "max": f[6], "step": f[7],
             "options": f[8] or []}
            for f in fields
        ]
        for section, fields in SCHEMA.get(category, SCHEMA["Other"])
    }


def _engine(name):
    try:
        import library_store
        fn = getattr(library_store, name, None)
        if callable(fn):
            return fn
    except Exception:
        pass
    try:
        import product_engine
        fn = getattr(product_engine, name, None)
        if callable(fn):
            return fn
    except Exception:
        pass
    return None


def _call(fn, **kwargs):
    if fn is None:
        raise RuntimeError("Storage function not available")
    try:
        sig = inspect.signature(fn)
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
            return fn(**kwargs)
        accepted = {k: v for k, v in kwargs.items() if k in sig.parameters}
        return fn(**accepted)
    except Exception:
        return fn(**kwargs)


def _fallback_init():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL,
            category TEXT, manufacturer TEXT, model TEXT, technology TEXT,
            supplier TEXT, country TEXT, rated_power_w REAL DEFAULT 0,
            voltage_v REAL DEFAULT 0, capacity_ah REAL DEFAULT 0,
            energy_kwh REAL DEFAULT 0, efficiency_percent REAL DEFAULT 0,
            warranty_years REAL DEFAULT 0, price REAL DEFAULT 0,
            currency TEXT DEFAULT 'USD', quantity REAL DEFAULT 0,
            notes TEXT, specifications TEXT, created_at TEXT)""")


def initialize_database():
    fn = _engine("initialize_database") or _engine("initialize_product_database")
    if fn:
        try:
            return fn()
        except Exception:
            pass
    _fallback_init()


def initialize_product_database():
    return initialize_database()


def _fallback_products():
    _fallback_init()
    with sqlite3.connect(DB_PATH) as con:
        con.row_factory = sqlite3.Row
        rows = con.execute("SELECT * FROM products ORDER BY category, name").fetchall()
    result = []
    for row in rows:
        p = dict(row)
        try:
            p["specifications"] = json.loads(p.get("specifications") or "{}")
        except Exception:
            p["specifications"] = {}
        result.append(p)
    return result


def get_products():
    fn = _engine("get_products") or _engine("load_products") or _engine("list_products")
    if fn:
        try:
            result = fn()
            if isinstance(result, dict):
                result = result.get("products", result.get("data", []))
            if isinstance(result, list):
                return result
        except Exception:
            pass
    return _fallback_products()


def get_product(product_id):
    fn = _engine("get_product")
    if fn:
        try:
            return _call(fn, product_id=product_id, id=product_id)
        except Exception:
            pass
    for p in get_products():
        if str(p.get("id", p.get("ID", ""))) == str(product_id):
            return p
    return None


def add_product(product):
    fn = _engine("add_product") or _engine("save_product") or _engine("insert_product")
    if fn:
        try:
            result = _call(fn, product=product, data=product)
            if isinstance(result, dict):
                return result.get("id", result.get("product_id", result))
            return result
        except Exception:
            pass
    _fallback_init()
    with sqlite3.connect(DB_PATH) as con:
        cur = con.execute("""INSERT INTO products
            (name, category, manufacturer, model, technology, supplier, country,
             rated_power_w, voltage_v, capacity_ah, energy_kwh, efficiency_percent,
             warranty_years, price, currency, quantity, notes, specifications, created_at)
            VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
            (product.get("name", ""), product.get("category", "Other"), product.get("manufacturer", ""),
             product.get("model", ""), product.get("technology", ""), product.get("supplier", ""),
             product.get("country", ""), product.get("rated_power_w", 0), product.get("voltage_v", 0),
             product.get("capacity_ah", 0), product.get("energy_kwh", 0), product.get("efficiency_percent", 0),
             product.get("warranty_years", 0), product.get("price", 0), product.get("currency", "USD"),
             product.get("quantity", 0), product.get("notes", ""), json.dumps(product.get("specifications", {})),
             datetime.now().isoformat(timespec="seconds")))
        return cur.lastrowid


def delete_product(product_id):
    fn = _engine("delete_product") or _engine("remove_product")
    if fn:
        try:
            return _call(fn, product_id=product_id, id=product_id)
        except Exception:
            pass
    _fallback_init()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("DELETE FROM products WHERE id=?", (int(product_id),))
    return True


def update_product(product_id, product):
    fn = _engine("update_product") or _engine("edit_product")
    if fn:
        try:
            return _call(fn, product_id=product_id, id=product_id, product=product, data=product)
        except Exception:
            pass
    _fallback_init()
    with sqlite3.connect(DB_PATH) as con:
        con.execute("""UPDATE products SET name=?, category=?, manufacturer=?, model=?, technology=?,
            supplier=?, country=?, rated_power_w=?, voltage_v=?, capacity_ah=?, energy_kwh=?,
            efficiency_percent=?, warranty_years=?, price=?, currency=?, quantity=?, notes=?, specifications=?
            WHERE id=?""",
            (product.get("name", ""), product.get("category", "Other"), product.get("manufacturer", ""),
             product.get("model", ""), product.get("technology", ""), product.get("supplier", ""),
             product.get("country", ""), product.get("rated_power_w", 0), product.get("voltage_v", 0),
             product.get("capacity_ah", 0), product.get("energy_kwh", 0), product.get("efficiency_percent", 0),
             product.get("warranty_years", 0), product.get("price", 0), product.get("currency", "USD"),
             product.get("quantity", 0), product.get("notes", ""), json.dumps(product.get("specifications", {})), int(product_id)))
    return True


def create_product(**kwargs):
    fn = _engine("create_product")
    if fn:
        try:
            result = fn(**kwargs)
            return result if isinstance(result, dict) else {"success": True, "product": result}
        except Exception as exc:
            return {"success": False, "message": str(exc)}
    return {"success": True, "product": kwargs}


def validate_category_fields(category, specifications):
    errors = []
    if category == "Solar Panel" and float(specifications.get("rated_power_w", 0) or 0) <= 0:
        errors.append("Solar panel rated power must be greater than zero.")
    if category == "Battery" and float(specifications.get("capacity_ah", 0) or 0) <= 0:
        errors.append("Battery capacity must be greater than zero.")
    if category == "Inverter" and float(specifications.get("rated_power_w", 0) or 0) <= 0:
        errors.append("Inverter rated output power must be greater than zero.")
    if category == "Charge Controller" and float(specifications.get("max_charge_current_a", 0) or 0) <= 0:
        errors.append("Charge-controller charge current must be greater than zero.")
    return errors


def filter_products_by_category(products, category):
    return [p for p in products if str(p.get("category", "Other")) == str(category)]


def filter_products_by_technology(products, technology):
    return [p for p in products if str(p.get("technology", "")).lower() == str(technology).lower()]


def search_products(products, query):
    q = str(query or "").strip().lower()
    if not q:
        return list(products)
    out = []
    for p in products:
        text = " ".join(str(p.get(k, "")) for k in ["name", "category", "manufacturer", "model", "technology", "supplier", "country", "notes"])
        text += " " + json.dumps(p.get("specifications", {}), ensure_ascii=False)
        if q in text.lower():
            out.append(p)
    return out


def database_search_products(query="", category="All"):
    products = get_products()
    if category != "All":
        products = filter_products_by_category(products, category)
    return search_products(products, query)


def _num(v, default=0.0):
    try:
        return float(v)
    except (TypeError, ValueError):
        return default


def _spec(p, key, default=""):
    specs = p.get("specifications") or {}
    return specs.get(key, p.get(key, default))


def _build_product(name, category, manufacturer, model, technology, supplier, country, price, currency, quantity, notes, specs):
    return {
        "name": name.strip(), "category": category, "manufacturer": manufacturer.strip(), "model": model.strip(),
        "technology": technology, "supplier": supplier.strip(), "country": country.strip(),
        "rated_power_w": _num(specs.get("rated_power_w")),
        "voltage_v": _num(specs.get("nominal_voltage_v", specs.get("dc_nominal_voltage_v", specs.get("vmp_v")))),
        "capacity_ah": _num(specs.get("capacity_ah")), "energy_kwh": _num(specs.get("energy_kwh")),
        "efficiency_percent": _num(specs.get("efficiency_percent", specs.get("round_trip_efficiency_percent"))),
        "warranty_years": _num(specs.get("warranty_years", specs.get("product_warranty_years"))),
        "price": float(price), "currency": currency, "quantity": float(quantity), "notes": notes.strip(),
        "specifications": specs,
    }


def add_product_form(default_category=None):
    st.subheader("➕ Add Product to Library")
    category = st.selectbox("Product Category", PRODUCT_CATEGORIES,
                            index=PRODUCT_CATEGORIES.index(default_category) if default_category in PRODUCT_CATEGORIES else 0,
                            format_func=lambda x: f"{get_category_icon(x)} {x}", key="pui_category")
    st.info(f"{get_category_icon(category)} **{category}** — {get_category_description(category)}")

    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("Product Name", placeholder="e.g. 550W Solar Panel", key="pui_name")
        manufacturer = st.text_input("Manufacturer", key="pui_manufacturer")
        model = st.text_input("Model", key="pui_model")
    with c2:
        technology = st.selectbox("Technology", PRODUCT_TECHNOLOGIES, key="pui_technology")
        supplier = st.text_input("Supplier", key="pui_supplier")
        country = st.text_input("Country", key="pui_country")

    specs = {}
    for section, fields in get_category_sections(category).items():
        st.markdown(f"### ⚙️ {section}")
        cols = st.columns(2)
        for i, f in enumerate(fields):
            with cols[i % 2]:
                label = f["label"] + (f" ({f['unit']})" if f["unit"] else "")
                key = f"pui_{category}_{f['name']}"
                if f["type"] == "number":
                    kwargs = {"label": label, "value": _num(f["default"]), "step": float(f["step"] or 1), "key": key}
                    if f["min"] is not None: kwargs["min_value"] = float(f["min"])
                    if f["max"] is not None: kwargs["max_value"] = float(f["max"])
                    value = st.number_input(**kwargs)
                elif f["type"] == "select":
                    options = f["options"] or ["Other"]
                    value = st.selectbox(label, options, index=options.index(f["default"]) if f["default"] in options else 0, key=key)
                else:
                    value = st.text_input(label, value=str(f["default"]), key=key)
                specs[f["name"]] = value

    st.markdown("### 💰 Commercial Information")
    c1, c2, c3 = st.columns(3)
    with c1: price = st.number_input("Unit Price", min_value=0.0, value=0.0, step=100.0, key="pui_price")
    with c2: currency = st.selectbox("Currency", CURRENCIES, key="pui_currency")
    with c3: quantity = st.number_input("Available Quantity", min_value=0.0, value=0.0, step=1.0, key="pui_quantity")
    notes = st.text_area("Notes", key="pui_notes")

    errors = validate_category_fields(category, specs)
    for e in errors: st.warning(e)

    if st.button("💾 Save Product to Library", type="primary", use_container_width=True, key="pui_save"):
        if not name.strip():
            st.error("Product name is required.")
            return None
        if errors:
            st.error("Please correct the category-specific fields before saving.")
            return None
        product = _build_product(name, category, manufacturer, model, technology, supplier, country, price, currency, quantity, notes, specs)
        validation = create_product(**product)
        if isinstance(validation, dict) and not validation.get("success", True):
            st.error(validation.get("message", "Product validation failed."))
            return None
        pid = add_product(product)
        st.success(f"✅ {get_category_icon(category)} {name} saved to the {category} library. ID: {pid}")
        return product
    return None


def _rows(category, products):
    if category == "Solar Panel":
        return [{"Product":p.get("name",""),"Manufacturer":p.get("manufacturer",""),"Model":p.get("model",""),"Technology":p.get("technology",""),"Power (W)":_spec(p,"rated_power_w"),"Voc (V)":_spec(p,"voc_v"),"Vmp (V)":_spec(p,"vmp_v"),"Isc (A)":_spec(p,"isc_a"),"Efficiency (%)":_spec(p,"efficiency_percent"),"Price":p.get("price",""),"Currency":p.get("currency","")} for p in products]
    if category == "Battery":
        return [{"Product":p.get("name",""),"Manufacturer":p.get("manufacturer",""),"Model":p.get("model",""),"Technology":p.get("technology",""),"Voltage (V)":_spec(p,"nominal_voltage_v",p.get("voltage_v","")),"Capacity (Ah)":_spec(p,"capacity_ah"),"Energy (kWh)":_spec(p,"energy_kwh"),"DoD (%)":_spec(p,"depth_of_discharge_percent"),"Cycle Life":_spec(p,"cycle_life"),"Price":p.get("price",""),"Currency":p.get("currency","")} for p in products]
    if category == "Inverter":
        return [{"Product":p.get("name",""),"Manufacturer":p.get("manufacturer",""),"Model":p.get("model",""),"Technology":p.get("technology",""),"Power (W)":_spec(p,"rated_power_w"),"Surge (W)":_spec(p,"surge_power_w"),"DC Voltage (V)":_spec(p,"dc_nominal_voltage_v",p.get("voltage_v","")),"AC Voltage (V)":_spec(p,"ac_output_voltage_v"),"MPPT Min (V)":_spec(p,"mppt_min_voltage_v"),"MPPT Max (V)":_spec(p,"mppt_max_voltage_v"),"Efficiency (%)":_spec(p,"efficiency_percent"),"Price":p.get("price",""),"Currency":p.get("currency","")} for p in products]
    if category == "Charge Controller":
        return [{"Product":p.get("name",""),"Manufacturer":p.get("manufacturer",""),"Model":p.get("model",""),"Type":_spec(p,"controller_type",p.get("technology","")),"System Voltage (V)":_spec(p,"system_voltage_v"),"Charge Current (A)":_spec(p,"max_charge_current_a"),"PV Input (W)":_spec(p,"max_pv_input_power_w"),"PV Voltage (V)":_spec(p,"max_pv_voltage_v"),"Efficiency (%)":_spec(p,"efficiency_percent"),"Price":p.get("price",""),"Currency":p.get("currency","")} for p in products]
    return [{"Product":p.get("name",""),"Category":p.get("category",""),"Manufacturer":p.get("manufacturer",""),"Model":p.get("model",""),"Technology":p.get("technology",""),"Supplier":p.get("supplier",""),"Country":p.get("country",""),"Price":p.get("price",""),"Currency":p.get("currency","")} for p in products]


def display_product_library():
    products = get_products()
    st.subheader("📚 Product Library")
    if not products:
        st.info("No products are currently stored in the library.")
        return
    query = st.text_input("🔎 Search Library", placeholder="Product, manufacturer, model, technology...", key="pui_library_search")
    products = search_products(products, query)
    labels = ["🌐 All Products"] + [f"{get_category_icon(c)} {c}" for c in PRODUCT_CATEGORIES]
    selected = st.radio("Library Category", labels, horizontal=True, key="pui_library_category")
    category = None if selected == "🌐 All Products" else selected.split(" ", 1)[1]
    filtered = products if category is None else filter_products_by_category(products, category)
    st.markdown(f"## {get_category_icon(category) if category else '🌐'} {category or 'All Products'}")
    st.caption(f"{len(filtered)} product(s)")
    if not filtered:
        st.info("No products are available in this category.")
        return
    st.dataframe(pd.DataFrame(_rows(category, filtered) if category else _rows("Other", filtered)), use_container_width=True, hide_index=True)


def product_search_interface():
    st.subheader("🔎 Search Products")
    products = get_products()
    c1, c2 = st.columns([2,1])
    with c1: q = st.text_input("Search", key="pui_search")
    with c2: cat = st.selectbox("Category", ["All"] + PRODUCT_CATEGORIES, key="pui_search_cat")
    if cat != "All": products = filter_products_by_category(products, cat)
    results = search_products(products, q)
    st.caption(f"{len(results)} result(s)")
    for p in results:
        with st.expander(f"{get_category_icon(p.get('category','Other'))} {p.get('name','Unnamed Product')}"):
            st.write(f"**Manufacturer:** {p.get('manufacturer','')}")
            st.write(f"**Model:** {p.get('model','')}")
            st.write(f"**Category:** {p.get('category','')}")
            st.write(f"**Price:** {p.get('price','')} {p.get('currency','')}")
            if p.get("specifications"): st.json(p["specifications"])
    return results


def product_details():
    st.subheader("🔍 Product Details")
    products = get_products()
    if not products: st.info("No products available."); return
    labels = [f"{get_category_icon(p.get('category','Other'))} {p.get('name','Unnamed')} — {p.get('model','')}" for p in products]
    selected = st.selectbox("Select Product", labels, key="pui_detail")
    p = products[labels.index(selected)]
    st.markdown(f"## {get_category_icon(p.get('category','Other'))} {p.get('name','')}")
    st.json(p)


def compare_products(products=None):
    st.subheader("⚖️ Compare Products")
    products = get_products() if products is None else products
    if len(products) < 2: st.info("At least two products are required for comparison."); return
    labels = [f"{p.get('name','Unnamed')} — {p.get('model','')}" for p in products]
    selected = st.multiselect("Select products", labels, max_selections=5, key="pui_compare")
    chosen = [products[labels.index(x)] for x in selected]
    if len(chosen) < 2: st.info("Select at least two products."); return
    rows=[]
    for p in chosen:
        row={"Product":p.get("name",""),"Category":p.get("category",""),"Manufacturer":p.get("manufacturer",""),"Model":p.get("model",""),"Technology":p.get("technology",""),"Price":p.get("price",""),"Currency":p.get("currency","")}
        row.update(p.get("specifications") or {})
        rows.append(row)
    st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)


def product_comparison(): return compare_products()


def backup_database():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)
    fn = _engine("backup_database") or _engine("backup_product_database")
    if fn:
        try:
            result = _call(fn, backup_dir=str(BACKUP_DIR))
            st.success("✅ Database backup completed.")
            return result
        except Exception:
            pass
    if not DB_PATH.exists():
        st.warning("No fallback SQLite database file was found.")
        return None
    target = BACKUP_DIR / f"product_library_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
    shutil.copy2(DB_PATH, target)
    st.success(f"✅ Backup created: {target.name}")
    return str(target)


def database_management():
    st.subheader("⚙️ Database Management")
    products=get_products()
    a,b,c=st.columns(3)
    a.metric("Products", len(products)); b.metric("Categories", len(set(p.get("category","Other") for p in products))); c.metric("Database", "SQLite")
    if st.button("💾 Backup Product Database", use_container_width=True, key="pui_backup"):
        backup_database()
    if not products: return
    labels=[f"{p.get('name','Unnamed')} — {p.get('category','Other')} — {p.get('model','')}" for p in products]
    selected=st.selectbox("Product to delete", labels, key="pui_delete_select")
    confirm=st.checkbox("I understand that deletion is permanent.", key="pui_delete_confirm")
    if st.button("🗑️ Delete Selected Product", disabled=not confirm, key="pui_delete"):
        p=products[labels.index(selected)]
        delete_product(p.get("id",p.get("ID")))
        st.success("Product deleted.")
        st.rerun()


def delete_product_interface(): return database_management()
def refresh_product_library(): return get_products()


def display_product_library_ui():
    initialize_database()
    st.title("☀️ Solar Product Library")
    st.caption("Persistent solar equipment database for Solar PV Designer Pro Africa™")
    st.success("Products are stored in the SQLite database and persist between application sessions.")
    tabs=st.tabs(["➕ Add Product","📚 Library","🔎 Details","⚖️ Compare","⚙️ Manage"])
    with tabs[0]: add_product_form()
    with tabs[1]: display_product_library()
    with tabs[2]: product_details()
    with tabs[3]: product_comparison()
    with tabs[4]: database_management()

initialize_database()
