import streamlit as st
from pathlib import Path
import library_store

st.set_page_config(
    page_title="Library Files Diagnostic",
    page_icon="🗄️",
    layout="wide",
)

st.title("🗄️ Product Library Files Diagnostic")

st.subheader("library_store.py location")

st.code(str(Path(library_store.__file__).resolve()))

st.divider()

st.subheader("Files near library_store.py")

base = Path(library_store.__file__).resolve().parent

files = []

for path in base.rglob("*"):
    if path.is_file():
        files.append(path)

for path in files:
    st.write(str(path))

st.divider()

st.subheader("Library-related paths exposed by library_store.py")

for name in dir(library_store):
    if name.startswith("_"):
        continue

    if any(
        word in name.lower()
        for word in [
            "file",
            "path",
            "product",
            "library",
            "data",
            "database",
        ]
    ):
        try:
            value = getattr(library_store, name)

            if not callable(value):
                st.write(f"**{name}:**")
                st.code(str(value))

        except Exception:
            pass
