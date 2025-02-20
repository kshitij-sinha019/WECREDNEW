import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="WeCredit Chatbot", page_icon="💳", layout="centered")

# Load API Key from Secrets (Ensure it's set in Streamlit Cloud)
api_key = st.secrets["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"]
client = Groq(api_key=api_key)

# Header UI
st.markdown(
    "<h2 style='text-align:center; color:#3b82f6;'>💳 WeCredit AI Chatbot</h2>"
    "<p style='text-align:center;'>Ask me about personal loans, credit cards, and business loans!</p><hr>",
    unsafe_allow_html=True,
)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I'm WeCredit AI. How can I assist you today?"}
    ]

# Display Chat Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
if user_input := st.chat_input("💬 Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    try:
        with st.spinner("⏳ Thinking..."):
            response = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are a financial AI chatbot."}] + st.session_state.messages[-5:],
                model="llama-3.3-70b-versatile",
                max_tokens=300
            )
            bot_response = response.choices[0].message.content

            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
