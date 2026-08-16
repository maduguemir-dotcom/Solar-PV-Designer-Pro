import streamlit as st

from product_schema import (
    get_product_categories,
    get_product_schema,
    get_category_fields,
    get_category_sections,
    get_category_icon,
    get_category_description,
    get_field_names,
    get_default_specifications,
    validate_category_fields,
)


st.set_page_config(
    page_title="Product Schema Diagnostic",
    page_icon="🧩",
    layout="wide",
)


st.title(
    "🧩 Product Category Schema Diagnostic"
)

st.success(
    "product_schema.py imported successfully."
)


# ==========================================================
# CATEGORIES
# ==========================================================

st.subheader(
    "Product Categories"
)

categories = get_product_categories()

st.write(
    categories
)


# ==========================================================
# CATEGORY SELECTOR
# ==========================================================

selected_category = st.selectbox(
    "Select a category to inspect",
    categories,
    key="schema_category_selector"
)


st.subheader(
    f"{get_category_icon(selected_category)} "
    f"{selected_category}"
)

st.write(
    get_category_description(
        selected_category
    )
)


# ==========================================================
# SECTIONS
# ==========================================================

sections = get_category_sections(
    selected_category
)

for section_name, fields in sections.items():

    st.markdown(
        f"### {section_name}"
    )

    rows = []

    for field in fields:

        rows.append({

            "Field":
                field.get(
                    "name",
                    ""
                ),

            "Label":
                field.get(
                    "label",
                    ""
                ),

            "Type":
                field.get(
                    "type",
                    ""
                ),

            "Unit":
                field.get(
                    "unit",
                    ""
                ),

            "Default":
                field.get(
                    "default",
                    ""
                ),

            "Options":
                ", ".join(
                    field.get(
                        "options",
                        []
                    )
                )

        })

    st.dataframe(
        rows,
        use_container_width=True,
        hide_index=True
    )


# ==========================================================
# FIELD NAMES
# ==========================================================

st.subheader(
    "Field Names"
)

st.json(
    get_field_names(
        selected_category
    )
)


# ==========================================================
# DEFAULT VALUES
# ==========================================================

st.subheader(
    "Default Specifications"
)

st.json(
    get_default_specifications(
        selected_category
    )
)


# ==========================================================
# VALIDATION TEST
# ==========================================================

st.subheader(
    "Validation Test"
)

test_values = (
    get_default_specifications(
        selected_category
    )
)

errors = validate_category_fields(
    selected_category,
    test_values
)

if errors:

    st.error(
        errors
    )

else:

    st.success(
        "Default specifications passed validation."
    )
