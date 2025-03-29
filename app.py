import streamlit as st
import requests
import speech_recognition as sr
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Streamlit page setup
st.set_page_config(page_title="AI Chatbot", page_icon="🤖")

st.title("🤖 Yuvraj's AI")
st.write("Ask me anything!")

# Backend API URL
API_URL = "http://127.0.0.1:8000/chat/"

# Initialize chat history (store full history but only display recent)
if "history" not in st.session_state:
    st.session_state.history = []

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio)
            return text
        except sr.UnknownValueError:
            return "Could not understand audio."
        except sr.RequestError:
            return "Could not request results. Check your internet connection."

# Display only the last 5 messages in the UI
for msg in st.session_state.history[-5:]:  # Show only last 5 exchanges
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Voice Input Button
if st.button("🎤 Speak"):
    user_input = recognize_speech()
    st.write(f"You said: {user_input}")
else:
    user_input = st.chat_input("Type your message...")

if user_input:
    # Show user input
    with st.chat_message("user"):
        st.markdown(user_input)

    # Send user input + full history to backend
    payload = {"message": user_input, "history": st.session_state.history}
    response = requests.post(API_URL, json=payload).json()

    # Extract bot reply
    bot_reply = response.get("reply", "I couldn't understand that.")

    # Show bot reply
    with st.chat_message("assistant"):
        st.markdown(bot_reply)

    # Update full history
    st.session_state.history.append({"role": "user", "content": user_input})
    st.session_state.history.append({"role": "assistant", "content": bot_reply})
