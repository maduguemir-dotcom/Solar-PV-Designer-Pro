"""
Solar PV Designer Pro Africa™ - Product Management UI

Management layer on top of the existing product_ui.py.
Keeps product_engine.py and library_store.py untouched.
"""

import inspect
import streamlit as st

try:
    import product_ui as _product_ui
    _IMPORT_ERROR = None
except Exception as exc:
    _product_ui = None
    _IMPORT_ERROR = exc

CATEGORIES = [
    "Solar Panel", "Battery", "Inverter", "Charge Controller",
    "Mounting Structure", "Solar Cable", "Protection",
    "Labour & Services", "Transport & Logistics", "Other",
]

ICONS = {
    "Solar Panel": "☀️", "Battery": "🔋", "Inverter": "⚡",
    "Charge Controller": "🔌", "Mounting Structure": "🏗️",
    "Solar Cable": "🔗", "Protection": "🛡️",
    "Labour & Services": "🔧", "Transport & Logistics": "🚚",
    "Other": "📦",
}

FIELDS = {
    "Solar Panel": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Technology","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("rated_power_w","Rated Power (W)","number"),("voltage_v","Nominal Voltage (V)","number"),
        ("voc_v","Voc (V)","number"),("vmp_v","Vmp (V)","number"),
        ("isc_a","Isc (A)","number"),("imp_a","Imp (A)","number"),
        ("efficiency_percent","Efficiency (%)","number"),
        ("max_system_voltage_v","Maximum System Voltage (V)","number"),
        ("max_series_fuse_a","Maximum Series Fuse (A)","number"),
        ("length_mm","Length (mm)","number"),("width_mm","Width (mm)","number"),
        ("thickness_mm","Thickness (mm)","number"),("weight_kg","Weight (kg)","number"),
        ("cell_count","Cell Count","number"),("cell_technology","Cell Technology","text"),
        ("price","Unit Price","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Battery": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Technology","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("voltage_v","Nominal Voltage (V)","number"),("capacity_ah","Capacity (Ah)","number"),
        ("energy_kwh","Energy (kWh)","number"),("dod_percent","Depth of Discharge (%)","number"),
        ("efficiency_percent","Efficiency (%)","number"),("cycle_life","Cycle Life","number"),
        ("max_charge_current_a","Maximum Charge Current (A)","number"),
        ("max_discharge_current_a","Maximum Discharge Current (A)","number"),
        ("warranty_years","Warranty (years)","number"),("price","Unit Price","number"),
        ("currency","Currency","text"),("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Inverter": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Technology","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("rated_power_w","Rated Power (W)","number"),("surge_power_w","Surge Power (W)","number"),
        ("voltage_v","Battery / DC Voltage (V)","number"),("efficiency_percent","Efficiency (%)","number"),
        ("mppt_voltage_min_v","MPPT Minimum Voltage (V)","number"),
        ("mppt_voltage_max_v","MPPT Maximum Voltage (V)","number"),
        ("max_pv_power_w","Maximum PV Input (W)","number"),
        ("max_pv_current_a","Maximum PV Current (A)","number"),
        ("phase","Phase","text"),("warranty_years","Warranty (years)","number"),
        ("price","Unit Price","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Charge Controller": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Technology","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("rated_current_a","Rated Current (A)","number"),("voltage_v","Battery Voltage (V)","number"),
        ("max_pv_voltage_v","Maximum PV Voltage (V)","number"),
        ("max_pv_power_w","Maximum PV Power (W)","number"),
        ("efficiency_percent","Efficiency (%)","number"),("warranty_years","Warranty (years)","number"),
        ("price","Unit Price","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Mounting Structure": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Structure Type","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("material","Material","text"),("module_capacity","Module Capacity","number"),
        ("roof_type","Roof / Ground Type","text"),("price","Unit Price","number"),
        ("currency","Currency","text"),("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Solar Cable": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Cable Type","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("cross_section_mm2","Cross-section (mm²)","number"),
        ("voltage_rating_v","Voltage Rating (V)","number"),
        ("current_rating_a","Current Rating (A)","number"),("length_m","Length (m)","number"),
        ("price","Unit Price","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Protection": [
        ("name","Product Name","text"),("manufacturer","Manufacturer","text"),
        ("model","Model","text"),("technology","Protection Type","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("rated_current_a","Rated Current (A)","number"),("voltage_v","Voltage (V)","number"),
        ("poles","Poles","number"),("breaking_capacity_ka","Breaking Capacity (kA)","number"),
        ("price","Unit Price","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Labour & Services": [
        ("name","Service Name","text"),("manufacturer","Provider / Company","text"),
        ("model","Service Code","text"),("technology","Service Type","text"),
        ("supplier","Supplier / Contractor","text"),("country","Country","text"),
        ("unit","Billing Unit","text"),("price","Unit Cost","number"),
        ("currency","Currency","text"),("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Transport & Logistics": [
        ("name","Service Name","text"),("manufacturer","Provider / Company","text"),
        ("model","Service Code","text"),("technology","Transport Type","text"),
        ("supplier","Transporter","text"),("country","Country","text"),
        ("distance_km","Distance (km)","number"),("unit","Billing Unit","text"),
        ("price","Unit Cost","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
    "Other": [
        ("name","Product / Item Name","text"),("manufacturer","Manufacturer / Provider","text"),
        ("model","Model / Code","text"),("technology","Type","text"),
        ("supplier","Supplier","text"),("country","Country","text"),
        ("price","Unit Price","number"),("currency","Currency","text"),
        ("quantity","Quantity","number"),("notes","Notes","textarea"),
    ],
}

def _fn(name):
    return getattr(_product_ui, name, None) if _product_ui else None

def _call(fn, **kwargs):
    if fn is None:
        raise RuntimeError("Required function is unavailable in product_ui.py.")
    try:
        sig = inspect.signature(fn)
        if any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values()):
            return fn(**kwargs)
        return fn(**{k:v for k,v in kwargs.items() if k in sig.parameters})
    except (TypeError, ValueError):
        return fn(**kwargs)

def get_products():
    fn = _fn("get_products")
    if not fn:
        return []
    result = _call(fn)
    if result is None:
        return []
    if isinstance(result, dict):
        return result.get("products", [result])
    return list(result)

def _id(p):
    for k in ("id","product_id","productId","ID"):
        if p.get(k) is not None:
            return p[k]
    return None

def _name(p):
    return str(p.get("name") or p.get("product_name") or p.get("productName") or "Unnamed Product")

def _category(p):
    c = str(p.get("category") or p.get("product_category") or "Other")
    return c if c in CATEGORIES else "Other"

def update_existing_product(product_id, values):
    fn = _fn("update_product")
    if not fn:
        return {"success": False, "message": "update_product() is unavailable in product_ui.py."}
    try:
        result = _call(fn, product_id=product_id, id=product_id, **values)
        return result if isinstance(result, dict) else {"success": True, "message": "Product updated successfully."}
    except Exception as exc:
        return {"success": False, "message": str(exc)}

def delete_existing_product(product_id):
    fn = _fn("delete_product")
    if not fn:
        return {"success": False, "message": "delete_product() is unavailable in product_ui.py."}
    try:
        result = _call(fn, product_id=product_id, id=product_id)
        return result if isinstance(result, dict) else {"success": True, "message": "Product deleted successfully."}
    except Exception as exc:
        return {"success": False, "message": str(exc)}

def _edit_form(product):
    category = _category(product)
    values = {"category": category}
    left, right = st.columns(2)
    for i,(field,label,kind) in enumerate(FIELDS[category]):
        with (left if i % 2 == 0 else right):
            value = product.get(field)
            key = f"pm_{_id(product)}_{field}"
            if kind == "number":
                try: value = float(value or 0)
                except Exception: value = 0.0
                values[field] = st.number_input(label, value=value, step=0.01, key=key)
            elif kind == "textarea":
                values[field] = st.text_area(label, value=str(value or ""), key=key)
            else:
                values[field] = st.text_input(label, value=str(value or ""), key=key)
    return values

def _details(product):
    category = _category(product)
    st.markdown(f"### {ICONS.get(category,'📦')} {_name(product)}")
    st.caption(f"Category: {category} | ID: {_id(product)}")
    rows = []
    for field,label,_kind in FIELDS[category]:
        if field in product:
            rows.append({"Field": label, "Value": product[field]})
    if rows:
        st.dataframe(rows, use_container_width=True, hide_index=True)
    else:
        st.json(product)

def display_product_management_ui():
    if _IMPORT_ERROR:
        st.error("product_ui.py could not be imported.")
        st.exception(_IMPORT_ERROR)
        return

    st.title("🧰 Product Library Management")
    st.caption("Edit, inspect and safely delete records from the existing product library.")

    products = get_products()
    if not products:
        st.info("No products found in the library.")
        return

    st.metric("Products in Library", len(products))

    edit_tab, delete_tab, details_tab = st.tabs(["✏️ Edit Product","🗑️ Delete Product","📋 Product Details"])

    with edit_tab:
        c1,c2 = st.columns(2)
        with c1:
            category = st.selectbox("Category", ["All Categories"] + CATEGORIES, key="pm_edit_category")
        with c2:
            query = st.text_input("Search Product", key="pm_edit_search", placeholder="Name, manufacturer, model...")

        filtered = [p for p in products if category == "All Categories" or _category(p) == category]
        if query.strip():
            q=query.lower().strip()
            filtered=[p for p in filtered if q in str(p).lower()]

        if not filtered:
            st.warning("No matching products found.")
        else:
            labels=[f"{ICONS.get(_category(p),'📦')} {_name(p)} | {_category(p)} | ID {_id(p)}" for p in filtered]
            idx=st.selectbox("Select Product", range(len(filtered)), format_func=lambda i:labels[i], key="pm_edit_select")
            selected=filtered[idx]
            st.divider()
            st.markdown(f"### {ICONS.get(_category(selected),'📦')} {_category(selected)}")
            values=_edit_form(selected)
            if st.button("💾 Save Changes", type="primary", use_container_width=True, key="pm_save"):
                pid=_id(selected)
                if pid is None:
                    st.error("Selected product has no database ID.")
                else:
                    result=update_existing_product(pid, values)
                    if result.get("success",False):
                        st.success(result.get("message","Product updated successfully."))
                        st.rerun()
                    else:
                        st.error(result.get("message","Unable to update product."))

    with delete_tab:
        category=st.selectbox("Category", ["All Categories"] + CATEGORIES, key="pm_delete_category")
        filtered=[p for p in products if category == "All Categories" or _category(p)==category]
        if not filtered:
            st.warning("No products found.")
        else:
            labels=[f"{ICONS.get(_category(p),'📦')} {_name(p)} | {_category(p)} | ID {_id(p)}" for p in filtered]
            idx=st.selectbox("Select Product to Delete", range(len(filtered)), format_func=lambda i:labels[i], key="pm_delete_select")
            selected=filtered[idx]
            _details(selected)
            confirm=st.checkbox("I understand this product will be permanently deleted.", key="pm_delete_confirm")
            if st.button("🗑️ Permanently Delete Product", disabled=not confirm, use_container_width=True, key="pm_delete"):
                pid=_id(selected)
                if pid is None:
                    st.error("Selected product has no database ID.")
                else:
                    result=delete_existing_product(pid)
                    if result.get("success",False):
                        st.success(result.get("message","Product deleted successfully."))
                        st.rerun()
                    else:
                        st.error(result.get("message","Unable to delete product."))

    with details_tab:
        category=st.selectbox("Category", ["All Categories"] + CATEGORIES, key="pm_details_category")
        filtered=[p for p in products if category == "All Categories" or _category(p)==category]
        if not filtered:
            st.warning("No products found.")
        else:
            labels=[f"{ICONS.get(_category(p),'📦')} {_name(p)} | {_category(p)} | ID {_id(p)}" for p in filtered]
            idx=st.selectbox("Select Product", range(len(filtered)), format_func=lambda i:labels[i], key="pm_details_select")
            _details(filtered[idx])

product_management_interface = display_product_management_ui
display_management_ui = display_product_management_ui

__all__ = [
    "display_product_management_ui",
    "product_management_interface",
    "display_management_ui",
    "get_products",
    "update_existing_product",
    "delete_existing_product",
]
