import streamlit as st
from groq import Groq

# Page Configuration
st.set_page_config(page_title="WeCredit Chatbot", page_icon="💳", layout="centered")

# Header UI
st.markdown(
    """
    <h2 style="text-align:center; color:#3b82f6;">💳 WeCredit AI Chatbot</h2>
    <p style="text-align:center;">Ask me about personal loans, credit cards, and business loans!</p>
    <hr>
    """,
    unsafe_allow_html=True,
)

# API Key (Replace with Env Variable in Production)
api_key = "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"
client = Groq(api_key=api_key)

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Custom Chat Display UI
for message in st.session_state.messages:
    role_style = "background-color:#f1f5f9; padding:10px; border-radius:10px; width:fit-content;" if message["role"] == "user" else "background-color:#dbeafe; padding:10px; border-radius:10px; width:fit-content;"
    align = "justify-content:flex-end;" if message["role"] == "user" else "justify-content:flex-start;"
    
    st.markdown(
        f"""
        <div style="display:flex; {align}">
            <div style="{role_style}">
                {message["content"]}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# Chat Input Box
user_input = st.text_input("💬 Type your question...", key="chat_input")

# Handle User Input
if user_input:
    # Display User Message
    st.session_state.messages.append({"role": "user", "content": user_input})
    
    # Fetch Response from Groq API
    try:
        with st.spinner("⏳ Generating response..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a helpful AI chatbot for WeCredit. You specialize in financial topics such as loans, credit reports, interest rates in India, and investment advice."},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile"
            )

            bot_response = chat_completion.choices[0].message.content

            # Append to Chat History
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"❌ Error: {str(e)}") 
