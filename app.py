import streamlit as st
import requests
import PyPDF2
import io
import random
import os 
AVATAR_OPTIONS = [
    "avatars/dog.png",
    "avatars/cat.png",
    "avatars/hamster.png",
    "avatars/panda.png",
    "avatars/penguin.png"
]

if "user_avatar" not in st.session_state:
    st.session_state.user_avatar = random.choice(AVATAR_OPTIONS)

st.set_page_config(
    page_title="HireTrail AI",
    page_icon="logo.png",
    layout="centered"
)
st.caption("⚡ First response may take 30s if the server was sleeping ,it's free hosting!")
st.markdown("""
<style>
.stApp { background-color: #1a1b1e; }
[data-testid="stAppViewContainer"] { background-color: #1a1b1e; }
[data-testid="stHeader"] { background-color: #1a1b1e; }
.block-container { background-color: #1a1b1e; }
[data-testid="stSidebar"] { background-color: #141518; }
[data-testid="stSidebar"] * { color: #e0e0e0; }
[data-testid="stBottomBlockContainer"] { background-color: #1a1b1e !important; }
.stChatFloatingInputContainer { background-color: #1a1b1e !important; }
[data-testid="stChatMessageContainer"] div[data-testid="stChatMessage"]:has(img[alt="user"]),
[data-testid="stChatMessageContainer"] div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) {
    flex-direction: row-reverse !important;
}
[data-testid="stChatMessageContainer"] div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stMarkdownContainer"] {
    background-color: #2d5a8e !important;
    color: white !important;
    padding: 10px 14px !important;
    border-radius: 18px 18px 0px 18px !important;
    display: inline-block !important;
    text-align: left !important;
}
[data-testid="stChatMessageContainer"] div[data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-assistant"]) [data-testid="stMarkdownContainer"] {
    background-color: #242527 !important;
    color: white !important;
    padding: 10px 14px !important;
    border-radius: 18px 18px 18px 0px !important;
    display: inline-block !important;
}
[data-testid="stChatMessage"] img {
    border-radius: 50% !important;
    width: 38px !important;
    height: 38px !important;
    object-fit: cover !important;
}
[data-testid="chatAvatarIcon-user"],
[data-testid="chatAvatarIcon-assistant"] {
    border-radius: 50% !important;
    overflow: hidden !important;
    width: 38px !important;
    height: 38px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
}
h1, h2, h3, p, label { color: #e0e0e0 !important; }
</style>
""", unsafe_allow_html=True)


with st.sidebar:
    st.header("📄 Resume")
    st.caption("Upload for personalized advice")

    uploaded_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        pdf_reader = PyPDF2.PdfReader(io.BytesIO(uploaded_file.read()))
        resume_text = ""
        for page in pdf_reader.pages:
            resume_text += page.extract_text()
        st.session_state.resume_text = resume_text
        st.success("✅ Resume loaded!")

    if "resume_text" in st.session_state and st.session_state.resume_text:
        st.markdown("🟢 **Resume active** — bot knows your background")
    else:
        st.markdown("⚪ **No resume uploaded yet**")

# ─── SESSION STATE ───
if "messages" not in st.session_state:
    st.session_state.messages = []
if "history" not in st.session_state:
    st.session_state.history = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "is_thinking" not in st.session_state:
    st.session_state.is_thinking = False 

# ─── MAIN CHAT ───
st.title("HireTrail AI")
st.caption("Your personal career guidance counselor")

# Display existing messages
for msg in st.session_state.messages:
    if msg["role"] == "user":
        with st.chat_message("user", avatar=st.session_state.user_avatar):
            st.markdown(msg["content"])
    else:
        with st.chat_message("assistant", avatar="logo.png"):
            st.markdown(msg["content"])

# Show waiting indicator if bot is thinking
if st.session_state.is_thinking:
    with st.chat_message("assistant", avatar="logo.png"):
        st.markdown("""
        <div style="color: #aaaaaa; font-size: 14px; margin-bottom: 6px;">
        </div>
        <div style="display: flex; align-items: center; gap: 8px;">
            <div style="
                width: 8px; height: 8px; border-radius: 50%;
                background: #aaaaaa;
                animation: bounce 1s infinite;">
            </div>
            <div style="
                width: 8px; height: 8px; border-radius: 50%;
                background: #aaaaaa;
                animation: bounce 1s infinite 0.2s;">
            </div>
            <div style="
                width: 8px; height: 8px; border-radius: 50%;
                background: #aaaaaa;
                animation: bounce 1s infinite 0.4s;">
            </div>
        </div>
        <style>
        @keyframes bounce {
            0%, 100% { transform: translateY(0); opacity: 0.4; }
            50% { transform: translateY(-6px); opacity: 1; }
        }
        </style>
        """, unsafe_allow_html=True)

# ─── CHAT INPUT ───

if not st.session_state.is_thinking:
    prompt = st.chat_input("Ask about careers, resume, jobs, interviews...")
else:
   
    st.chat_input("Please wait for response...", disabled=True)
    prompt = None

if prompt:
    
    with st.chat_message("user", avatar=st.session_state.user_avatar):
        st.markdown(prompt)

    st.session_state.messages.append({"role": "user", "content": prompt})

    
    st.session_state.is_thinking = True
    st.rerun()  # rerun to disable input immediately

# If thinking state is active and last message is from user — fetch response
if st.session_state.is_thinking and st.session_state.messages[-1]["role"] == "user":
    try:

            BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")
            response = requests.post(f"{BACKEND_URL}/chat",
                json={
                    "message": st.session_state.messages[-1]["content"],
                    "history": st.session_state.history,
                    "resume_text": st.session_state.resume_text
                },
                timeout=60
            )

            if response.status_code != 200:
                reply = f"Backend error {response.status_code}: {response.text}"
            else:
                reply = response.json()["reply"]

    except requests.exceptions.Timeout:
            reply = "⏱️ Request timed out. Please try again."
    except Exception as e:
            reply = f"Error: {str(e)}"

    # Add reply and unlock input
    with st.chat_message("assistant", avatar="logo.png"):
        st.markdown(reply)

    st.session_state.messages.append({"role": "assistant", "content": reply})
    st.session_state.history.append({
        "role": "user",
        "content": st.session_state.messages[-2]["content"]
    })
    st.session_state.history.append({"role": "assistant", "content": reply})

    # Unlock input
    st.session_state.is_thinking = False
    st.rerun()
