from flask import Flask, request, jsonify
from groq import Groq
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={r"/chat": {"origins": "*"}})  # Allow all origins

# Load API Key
api_key = "your_groq_api_key"  # Replace with actual key
if not api_key:
    raise ValueError("API key missing. Set it before running.")

client = Groq(api_key=api_key)

@app.route('/', methods=['GET'])
def home():
    return "WeCredit Chatbot API is running."

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "Message cannot be empty."}), 400

        # Generate response using Groq API
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are a chatbot for WeCredit, helping users with financial queries."},
                {"role": "user", "content": user_message}
            ],
            model="llama-3.3-70b-versatile",
            max_tokens=150  # 🔹 Reduce for speed
        )

        bot_response = chat_completion.choices[0].message.content
        return jsonify({"response": bot_response})

    except Exception as e:
        return jsonify({"error": f"Server error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000, threaded=True)  # 🔹 Faster responses
