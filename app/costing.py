# ==========================================================
# SOLAR PV DESIGNER PRO AFRICA™
# Cost Diary Module - Version 2.4.0
# Developed by: Engr. Prof. Ibrahim Sani Madugu
# ==========================================================

"""User-defined equipment and project cost diary.

The module deliberately does not assume live exchange rates.
Each item keeps its own currency so users can record real
local-market prices without introducing misleading conversions.
"""

from datetime import date


CURRENCIES = {
    "UGX": "Ugandan Shilling",
    "NGN": "Nigerian Naira",
    "USD": "US Dollar",
    "KES": "Kenyan Shilling",
    "TZS": "Tanzanian Shilling",
    "RWF": "Rwandan Franc",
    "GHS": "Ghanaian Cedi",
    "ZAR": "South African Rand",
    "ETB": "Ethiopian Birr",
    "GBP": "British Pound",
    "EUR": "Euro",
}


DEFAULT_COST_ITEMS = [
    "Solar Panel",
    "Battery",
    "Inverter",
    "Charge Controller",
    "Mounting Structure",
    "Cable",
    "Protection/Breaker",
    "Installation",
    "Transport",
    "Other",
]


def calculate_item_total(quantity, unit_price):
    """Return quantity × unit price."""
    try:
        return max(float(quantity), 0.0) * max(float(unit_price), 0.0)
    except (TypeError, ValueError):
        return 0.0


def create_cost_record(
    item,
    category,
    quantity,
    unit_price,
    currency,
    supplier="",
    notes="",
):
    """Create a normalized cost-diary record."""
    qty = max(float(quantity), 0.0)
    price = max(float(unit_price), 0.0)

    return {
        "Date": str(date.today()),
        "Item": str(item).strip() or "Unnamed Item",
        "Category": str(category).strip() or "Other",
        "Quantity": qty,
        "Unit Price": price,
        "Currency": str(currency),
        "Total Cost": calculate_item_total(qty, price),
        "Supplier": str(supplier).strip(),
        "Notes": str(notes).strip(),
    }


def summarize_costs(records):
    """Summarize diary totals by currency."""
    summary = {}
    for record in records or []:
        currency = record.get("Currency", "UGX")
        total = float(record.get("Total Cost", 0.0) or 0.0)
        summary[currency] = summary.get(currency, 0.0) + total
    return summary


def display_cost_diary(st):
    """Render the complete v2.4 cost diary in Streamlit.

    Returns the current list of cost records.
    """
    if "cost_diary" not in st.session_state:
        st.session_state["cost_diary"] = []

    records = st.session_state["cost_diary"]

    st.subheader("💰 Project Cost Diary")
    st.caption(
        "Record actual market prices for panels, batteries, "
        "inverters and other project items. Prices remain in "
        "the currency selected for each item."
    )

    with st.form("cost_diary_form", clear_on_submit=True):
        c1, c2, c3 = st.columns(3)

        with c1:
            item = st.text_input(
                "Item",
                placeholder="e.g. 550 W Solar Panel",
            )
            category = st.selectbox(
                "Category",
                [
                    "Solar Panel",
                    "Battery",
                    "Inverter",
                    "Charge Controller",
                    "Balance of System",
                    "Installation",
                    "Transport",
                    "Other",
                ],
            )

        with c2:
            quantity = st.number_input(
                "Quantity",
                min_value=0.01,
                value=1.0,
                step=1.0,
            )
            currency = st.selectbox(
                "Currency",
                list(CURRENCIES.keys()),
                format_func=lambda code: f"{code} — {CURRENCIES[code]}",
            )

        with c3:
            unit_price = st.number_input(
                "Unit Price",
                min_value=0.0,
                value=0.0,
                step=100.0,
            )
            supplier = st.text_input(
                "Supplier (optional)",
                placeholder="Supplier / shop",
            )

        notes = st.text_input(
            "Notes (optional)",
            placeholder="Brand, model, warranty, quotation number, etc.",
        )

        submitted = st.form_submit_button(
            "➕ Add Cost Item",
            use_container_width=True,
        )

    if submitted:
        if not item.strip():
            st.warning("Please enter an item name.")
        elif unit_price <= 0:
            st.warning("Please enter a unit price greater than zero.")
        else:
            records.append(
                create_cost_record(
                    item=item,
                    category=category,
                    quantity=quantity,
                    unit_price=unit_price,
                    currency=currency,
                    supplier=supplier,
                    notes=notes,
                )
            )
            st.session_state["cost_diary"] = records
            st.success("Cost item added to the diary.")

    if records:
        import pandas as pd

        st.markdown("#### 📋 Recorded Costs")
        df = pd.DataFrame(records)
        st.dataframe(df, use_container_width=True, hide_index=True)

        st.markdown("#### 💵 Totals by Currency")
        summary = summarize_costs(records)

        cols = st.columns(min(max(len(summary), 1), 4))
        for index, (currency_code, total) in enumerate(summary.items()):
            cols[index % len(cols)].metric(
                currency_code,
                f"{total:,.2f}",
            )

        b1, b2 = st.columns(2)
        with b1:
            if st.button(
                "🗑️ Clear Cost Diary",
                use_container_width=True,
                key="clear_cost_diary",
            ):
                st.session_state["cost_diary"] = []
                st.rerun()

        with b2:
            csv_data = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "📥 Download Cost Diary CSV",
                data=csv_data,
                file_name="solar_pv_cost_diary.csv",
                mime="text/csv",
                use_container_width=True,
            )
    else:
        st.info("No cost items have been recorded yet.")

    return st.session_state["cost_diary"]
