import streamlit as st

from cost_engine import (
    SUPPORTED_CURRENCIES,
    create_cost_item,
    calculate_total_cost,
    calculate_category_totals,
    create_cost_summary,
    format_money,
    get_default_cost_items,
)


st.title("💰 Cost Engine Diagnostic")

st.success(
    "cost_engine.py imported successfully."
)


st.subheader("Supported Currencies")

st.json(
    SUPPORTED_CURRENCIES
)


items = get_default_cost_items()


items[0]["quantity"] = 10
items[0]["unit_price"] = 150
items[0]["currency"] = "USD"

items[1]["quantity"] = 2
items[1]["unit_price"] = 500
items[1]["currency"] = "USD"

items[2]["quantity"] = 1
items[2]["unit_price"] = 1000
items[2]["currency"] = "USD"


st.subheader("Sample Cost Items")

st.dataframe(
    items,
    use_container_width=True
)


st.subheader("Total Cost")

st.json(
    calculate_total_cost(items)
)


st.subheader("Category Totals")

st.json(
    calculate_category_totals(items)
)


st.subheader("Complete Cost Summary")

st.json(
    create_cost_summary(items)
)


st.subheader("Formatted Example")

st.write(
    format_money(
        3250,
        "USD"
    )
)
