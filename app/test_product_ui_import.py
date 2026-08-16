import streamlit as st
import product_ui

st.title("🔧 Product UI Import Diagnostic")

st.success("product_ui.py imported successfully.")

st.subheader("Available functions")

functions = [
    name
    for name in dir(product_ui)
    if not name.startswith("_")
    and callable(getattr(product_ui, name))
]

st.write(functions)

st.subheader("Required functions")

required = [
    "display_product_library_ui",
    "add_product_form",
    "product_search_interface",
    "display_product_library",
    "product_details",
    "product_comparison",
    "delete_product_interface",
    "database_management",
]

for function_name in required:

    if hasattr(product_ui, function_name):

        st.success(
            f"✅ {function_name}"
        )

    else:

        st.error(
            f"❌ {function_name} is missing"
        )
