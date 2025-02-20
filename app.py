from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS  # Enable CORS for frontend communication

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Allow all frontend requests

# Load API key
api_key = "your_groq_api_key"  # Replace with your actual API key
if not api_key:
    raise ValueError("Missing API key. Set your API key before running.")

client = Groq(api_key=api_key)

# Default Homepage Route
@app.route('/', methods=['GET'])
def home():
    return "Welcome to the WeCredit Chatbot API! Use /chat for interactions."

# Chatbot Route
@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "")

        if not user_message:
            return jsonify({"error": "Message is required"}), 400

        # Call Groq API for response
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chatbot for WeCredit, specializing in loans, credit cards, and financial topics."},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=250  # ✅ Reduced tokens for faster response
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  # Make sure it's accessible
