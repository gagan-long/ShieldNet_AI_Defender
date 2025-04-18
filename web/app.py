import streamlit as st
from core.llm_security.garak_scanner import CustomInjectionDetector

st.title("ShieldNet Dashboard")
user_input = st.text_area("Enter prompt:")

if st.button("Scan"):
    detector = CustomInjectionDetector()
    if detector.detect(user_input):
        st.error("Malicious input detected!")
    else:
        st.success("Input appears safe")
