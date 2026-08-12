import streamlit as st

st.title("Appliance Energy Import Test")

try:

    import appliance_energy

    st.success(
        "✅ appliance_energy.py imported successfully."
    )

    st.write(
        "Available functions:"
    )

    st.write(
        [
            name
            for name in dir(appliance_energy)
            if not name.startswith("_")
        ]
    )

except Exception as error:

    st.error(
        f"❌ Import failed: {error}"
    )

    st.exception(error)
