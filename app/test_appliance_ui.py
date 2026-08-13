import streamlit as st

from appliance_ui import (
    render_appliance_energy_designer
)

st.set_page_config(
    page_title="Appliance Energy UI Test",
    page_icon="🔌",
    layout="wide"
)

st.title(
    "🔌 Appliance Energy Designer Test"
)

total_energy = (
    render_appliance_energy_designer()
)

st.write(
    f"Total demand: {total_energy:.2f} kWh/day"
)
