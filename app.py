import streamlit as st
import requests

st.set_page_config(
    page_title="CareerCompass AI",
    page_icon="🧭",
    layout="centered"
)


st.title("🧭 CareerCompass AI")
st.caption("Your personal career guidance counselor")


if "messages" not in st.session_state:
    st.session_state.messages=[]

if "history" not in st.session_state:
    st.session_state.history=[]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt :=st.chat_input("Ask about careers,resume tips,interview prep..."):
    with st.chat_message("user"):
        st.markdown(prompt)
    
    st.session_state.messages.append({
        "role":"user",
        "content":prompt
    })

    with st.spinner("Thinking.."):
        try:
            response=requests.post(
                "http://localhost:8000/chat",
                json={
                    "message": prompt,
                    "history": st.session_state.history
                })
            reply=response.json()["reply"]
        except Exception as e:
            reply = "⚠️ Could not reach the backend. Is FastAPI running?"

    with st.chat_message("assistant"):
        st.markdown(reply)

    st.session_state.messages.append({
        "role":"assistant",
        "content":reply
    })

    st.session_state.history.append({
        "role":"user",
        "content":prompt
    })
    st.session_state.history.append({
        "role":"assistant",
        "content":reply
    })
