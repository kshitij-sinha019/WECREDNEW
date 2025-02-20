import streamlit as st
from groq import Groq

st.set_page_config(page_title="WeCredit Chatbot", page_icon="💳", layout="centered")

st.markdown(
    """
    <style>
        body { font-family: 'Arial', sans-serif; }
        .chat-container { 
            max-width: 700px; 
            margin: auto; 
            padding: 20px; 
            border-radius: 10px; 
            background-color: #f8f9fa;
            box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.1);
        }
        .chat-bubble {
            padding: 10px 15px; 
            border-radius: 10px; 
            margin-bottom: 10px;
            max-width: 80%;
            word-wrap: break-word;
        }
        .user-bubble { 
            background-color: #3b82f6; 
            color: white; 
            align-self: flex-end; 
        }
        .bot-bubble { 
            background-color: #d1e7ff; 
            color: black; 
            align-self: flex-start; 
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="chat-container">
        <h2 style="text-align:center; color:#3b82f6;">💳 WeCredit AI Chatbot</h2>
        <p style="text-align:center;">Your financial assistant for personal loans, credit cards, and business loans.</p>
        <hr>
    </div>
    """,
    unsafe_allow_html=True,
)

api_key = st.secrets["GROQ_API_KEY"]
client = Groq(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

chat_area = st.container()

for message in st.session_state.messages:
    role_class = "user-bubble" if message["role"] == "user" else "bot-bubble"
    chat_area.markdown(
        f"""
        <div class="chat-bubble {role_class}">{message["content"]}</div>
        """,
        unsafe_allow_html=True,
    )

user_input = st.text_input("💬 Ask me anything about loans, credit, and finance:", key="chat_input")

if user_input:
    st.session_state.messages.append({"role": "user", "content": user_input})

    try:
        with st.spinner("⏳ Thinking..."):
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are a financial AI assistant specializing in personal loans, credit scores, and banking in India."},
                    {"role": "user", "content": user_input}
                ],
                model="llama-3.3-70b-versatile",
                max_tokens=250
            )

            bot_response = chat_completion.choices[0].message.content
            st.session_state.messages.append({"role": "assistant", "content": bot_response})

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
