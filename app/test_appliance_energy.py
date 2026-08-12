import streamlit as st

from appliance_energy import (
    calculate_appliance_energy,
    create_appliance_record,
    analyze_appliance_load
)


st.title(
    "⚡ Appliance Energy Calculator Test"
)


# ----------------------------------------------------------
# Test individual appliance
# ----------------------------------------------------------

st.header(
    "1. Individual Appliance"
)

result = calculate_appliance_energy(

    wattage=100,

    hours_per_day=5,

    quantity=1

)

st.write(result)


# ----------------------------------------------------------
# Test appliance records
# ----------------------------------------------------------

st.header(
    "2. Appliance Records"
)

appliances = [

    create_appliance_record(
        "LED Light",
        "Lighting",
        10,
        6,
        10
    ),

    create_appliance_record(
        "Television",
        "Entertainment",
        100,
        5,
        1
    ),

    create_appliance_record(
        "Fan",
        "Cooling",
        60,
        8,
        3
    ),

    create_appliance_record(
        "Refrigerator",
        "Kitchen",
        150,
        10,
        1
    )

]

st.dataframe(
    appliances,
    use_container_width=True
)


# ----------------------------------------------------------
# Complete analysis
# ----------------------------------------------------------

st.header(
    "3. Complete Load Analysis"
)

analysis = analyze_appliance_load(
    appliances
)


col1, col2, col3 = st.columns(3)


col1.metric(
    "Daily Energy",
    f"{analysis['total_daily_kwh']:.2f} kWh"
)


col2.metric(
    "Daily Energy",
    f"{analysis['total_daily_wh']:.0f} Wh"
)


col3.metric(
    "Monthly Energy",
    f"{analysis['total_monthly_kwh']:.2f} kWh"
)


st.subheader(
    "Appliance Contributions"
)

st.dataframe(
    analysis[
        "appliances"
    ],
    use_container_width=True
)


st.subheader(
    "Category Summary"
)

st.write(
    analysis[
        "category_summary"
    ]
)
