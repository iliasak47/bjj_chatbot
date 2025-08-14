import streamlit as st
import requests
import os

st.set_page_config(page_title="BJJ Chatbot (API-powered)", page_icon="🥋")

st.title("🥋 BJJ Chatbot via API")

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000/ask")


# --- Session state initialization ---
if "history" not in st.session_state:
    st.session_state.history = []

if "last_segments" not in st.session_state:
    st.session_state.last_segments = []

if "latest_qa" not in st.session_state:
    st.session_state.latest_qa = None

# --- Optional: clear history button ---
col1, col2 = st.columns([1, 4])
with col1:
    if st.button("🗑️ Clear chat"):
        st.session_state.history = []
        st.session_state.last_segments = []
        st.session_state.latest_qa = None

# --- Chat history display (top) ---
if st.session_state.history:
    st.markdown("### 🕓 Conversation")
    for item in reversed(st.session_state.history):
        with st.chat_message("user"):
            st.markdown(item["question"])
        with st.chat_message("assistant"):
            st.markdown(item["answer"])

# --- Input field ---
user_question = st.text_input("💬 Ask a new question:")

# --- Submit ---
if st.button("Submit") and user_question.strip():
    with st.spinner("Processing..."):
        try:
            response = requests.post(API_URL, json={"question": user_question})
            response.raise_for_status()
            data = response.json()

            # Save current interaction
            st.session_state.latest_qa = {
                "question": user_question,
                "answer": data["answer"],
                "segments": data["segments"]
            }

            # Add to history
            st.session_state.history.append({
                "question": user_question,
                "answer": data["answer"]
            })

        except Exception as e:
            st.error(f"Error: {e}")

# --- Show latest answer (after submit)
if st.session_state.latest_qa:
    st.markdown("### 🧠 Latest Answer")
    with st.chat_message("user"):
        st.markdown(st.session_state.latest_qa["question"])
    with st.chat_message("assistant"):
        st.markdown(st.session_state.latest_qa["answer"])

    st.markdown("### 📚 Context Segments")
    for seg in st.session_state.latest_qa["segments"]:
        st.markdown(f"""
        - **Instructional**: `{seg.get("instructional", "N/A")}`
        - **Volume**: `{seg.get("volume", "N/A")}`
        - **Chapter**: `{seg.get("chapter", "N/A")}`
        - ⏱️ `{int(seg.get("start", 0))}s - {int(seg.get("end", 0))}s`
        ---
        """)
