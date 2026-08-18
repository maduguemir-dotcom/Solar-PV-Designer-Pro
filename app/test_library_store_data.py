import streamlit as st

st.set_page_config(
    page_title="Library Store Diagnostic",
    page_icon="🗄️",
    layout="wide",
)

st.title("🗄️ Library Store Diagnostic")

try:
    import library_store

    st.success("library_store.py imported successfully.")

    st.subheader("Available functions")

    functions = [
        name
        for name in dir(library_store)
        if not name.startswith("_")
        and callable(getattr(library_store, name))
    ]

    st.write(functions)

    st.divider()

    # Try the common product-library functions individually.
    for function_name in [
        "get_products",
        "load_library",
        "load_product_library",
        "get_product_library",
        "list_products",
        "load_data",
    ]:
        function = getattr(library_store, function_name, None)

        if function is None:
            continue

        st.subheader(function_name)

        try:
            result = function()

            if isinstance(result, list):
                st.write("Records:", len(result))
            elif isinstance(result, dict):
                st.write("Dictionary keys:", list(result.keys()))
            else:
                st.write("Result type:", type(result).__name__)

            st.json(result)

        except TypeError as exc:
            st.warning(
                f"{function_name} exists but requires arguments: {exc}"
            )

        except Exception as exc:
            st.error(
                f"{function_name} failed: {exc}"
            )

except Exception as exc:
    st.error("library_store.py could not be imported.")
    st.exception(exc)
