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



if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8001, reload=True)
