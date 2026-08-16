import streamlit as st
import inspect
import product_ui


st.set_page_config(
    page_title="Product UI Structure Diagnostic",
    page_icon="🔍",
    layout="wide",
)


st.title("🔍 Product UI Structure Diagnostic")


# ==========================================================
# ADD PRODUCT FORM
# ==========================================================

st.subheader("1. add_product_form()")

try:

    source = inspect.getsource(
        product_ui.add_product_form
    )

    st.success(
        "add_product_form() found."
    )

    st.write(
        f"Source length: {len(source)} characters"
    )

    st.code(
        source[:5000],
        language="python"
    )

except Exception as error:

    st.error(
        f"Could not inspect add_product_form(): {error}"
    )


# ==========================================================
# MAIN UI
# ==========================================================

st.subheader(
    "2. display_product_library_ui()"
)

try:

    source = inspect.getsource(
        product_ui.display_product_library_ui
    )

    st.success(
        "display_product_library_ui() found."
    )

    st.write(
        f"Source length: {len(source)} characters"
    )

    # Show relevant section
    keywords = [
        "add_product_form",
        "Add Product",
        "Product Name",
        "Rated Power",
        "Battery Capacity",
        "Energy Capacity",
    ]

    lines = source.splitlines()

    relevant_lines = []

    for number, line in enumerate(lines, start=1):

        if any(
            keyword.lower()
            in line.lower()
            for keyword in keywords
        ):

            start = max(
                0,
                number - 8
            )

            end = min(
                len(lines),
                number + 12
            )

            relevant_lines.append(
                f"\n--- Lines {start + 1}-{end} ---\n"
            )

            for i in range(
                start,
                end
            ):

                relevant_lines.append(
                    f"{i + 1}: {lines[i]}"
                )

    if relevant_lines:

        st.code(
            "\n".join(
                relevant_lines
            ),
            language="python"
        )

    else:

        st.info(
            "No matching Add Product code was found "
            "inside display_product_library_ui()."
        )

except Exception as error:

    st.error(
        "Could not inspect "
        f"display_product_library_ui(): {error}"
    )


# ==========================================================
# FUNCTION LIST
# ==========================================================

st.subheader(
    "3. Product UI Functions"
)

functions = []

for name in dir(product_ui):

    if name.startswith("_"):
        continue

    obj = getattr(
        product_ui,
        name
    )

    if callable(obj):

        functions.append(name)

st.write(
    functions
)
