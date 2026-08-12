import streamlit as st
import appliance_energy

st.set_page_config(
    page_title="Appliance Energy Diagnostic",
    page_icon="🔌"
)

st.title("🔌 Appliance Energy Module Diagnostic")

st.success("✅ appliance_energy.py imported successfully.")

st.subheader("Functions available in appliance_energy.py")

functions = []

for name in dir(appliance_energy):

    if not name.startswith("_"):

        obj = getattr(
            appliance_energy,
            name
        )

        if callable(obj):

            functions.append(name)


if functions:

    for function in functions:

        st.code(function)

else:

    st.warning(
        "No callable functions were found."
    )


st.subheader("Module Contents")

st.write(
    dir(appliance_energy)
)
