import streamlit as st

st.set_page_config(
    page_title="Streamlit Test",
    page_icon="✅"
)

st.title("✅ Streamlit Basic Test")

st.success("If you can see this message, Streamlit is working correctly.")

st.write("The basic Streamlit application loaded successfully.")

name = st.text_input("Enter your name")

if name:
    st.write(f"Hello, {name}!")
