import streamlit as st
from pathlib import Path
import json
import library_store

st.set_page_config(
    page_title="Product Library File Inspector",
    page_icon="🔎",
    layout="wide",
)

st.title("🔎 Product Library File Inspector")

file_path = Path(library_store.PRODUCT_LIBRARY_FILE)

st.write("### Product Library File")
st.code(str(file_path))

if not file_path.exists():
    st.error("❌ product_library.json does not exist.")
    st.stop()

st.success("✅ product_library.json exists.")

st.write("### File Size")
st.write(f"{file_path.stat().st_size:,} bytes")

st.divider()

try:
    with open(file_path, "r", encoding="utf-8") as f:
        raw = f.read()

    st.write("### Raw File Contents")

    if not raw.strip():
        st.warning("The JSON file is EMPTY.")
    else:
        st.code(raw)

    st.divider()

    st.write("### Parsed JSON")

    if raw.strip():
        data = json.loads(raw)

        st.write("Data type:", type(data).__name__)

        if isinstance(data, list):
            st.write("Number of records:", len(data))

        elif isinstance(data, dict):
            st.write("Dictionary keys:")
            st.write(list(data.keys()))

        st.json(data)

except json.JSONDecodeError as exc:
    st.error("❌ The product library file contains invalid JSON.")
    st.exception(exc)

except Exception as exc:
    st.error("❌ Unable to inspect the product library.")
    st.exception(exc)
