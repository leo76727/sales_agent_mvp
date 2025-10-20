
import streamlit as st
import requests

st.set_page_config(page_title="Sales Agent Dashboard", layout="wide")

st.title("💼 Sales Agent Dashboard")

with st.sidebar:
    st.header("Controls")
    if st.button("Generate Daily Report"):
        resp = requests.post("http://localhost:8000/api/generate_report").json()
        st.success(resp["report"])

st.subheader("Client Positions")
pos = requests.get("http://localhost:8000/api/positions").json()
st.json(pos)

st.subheader("Chat with LLM Agent")
prompt = st.text_area("Enter your inquiry:")
if st.button("Send to LLM"):
    resp = requests.post("http://localhost:8000/api/llm", json={"prompt": prompt}).json()
    st.write("Response:", resp["response"])

st.subheader("LLM Interaction Logs")
logs = requests.get("http://localhost:8000/api/logs").json()
st.json(logs)
