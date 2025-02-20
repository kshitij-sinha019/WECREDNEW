import streamlit as st
import requests

# Streamlit UI Setup
st.set_page_config(page_title="WeCredit Chatbot", layout="wide")

st.title("💳 WeCredit FinTech Chatbot")
st.write("Ask me anything about loans, credit cards, or financial services!")

# Update with your Flask backend URL
API_URL = "http://127.0.0.1:5000/chat"  # Change if deploying online

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display previous messages
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User Input Handling
user_input = st.chat_input("Type your message...")

if user_input:
    with st.chat_message("user"):
        st.write(user_input)

    st.session_state["messages"].append({"role": "user", "content": user_input})

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"message": user_input}, timeout=10)
                if response.status_code == 200:
                    bot_reply = response.json().get("response", "I'm not sure.")
                else:
                    bot_reply = "Error: Slow response from API."
            except requests.exceptions.RequestException:
                bot_reply = "Error: Unable to connect to the chatbot backend."

        st.write(bot_reply)
        st.session_state["messages"].append({"role": "assistant", "content": bot_reply})
