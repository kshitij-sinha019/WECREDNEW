import streamlit as st
from groq import Groq

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

st.set_page_config(page_title="WeCredit Chatbot", page_icon="💳", layout="centered")

st.markdown(
    """
    <h2 style="text-align:center; color:#3b82f6;">💳 WeCredit AI Chatbot</h2>
    <p style="text-align:center;">Ask me about personal loans, credit cards, and business loans!</p>
    <hr>
    """,
    unsafe_allow_html=True,
)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    role_style = (
        "background-color:#f1f5f9; padding:10px; border-radius:10px; width:fit-content;"
        if message["role"] == "user"
        else "background-color:#dbeafe; padding:10px; border-radius:10px; width:fit-content;"
    )
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

user_input = st.text_input("💬 Type your question...", key="chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("⏳ Generating response..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a financial assistant specializing in loans, credit reports, and investment advice."},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=200
            )

            bot_response = chat_completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
