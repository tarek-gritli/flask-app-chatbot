from flask import Flask, render_template, request, jsonify
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("No GEMINI_API_KEY set for Flask application")


url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=" + GEMINI_API_KEY

# Define the headers
headers = {
    "Content-Type": "application/json"
}

# Function to generate responses using Gemini API
def generate_response(prompt_text):
    # Define the request payload
    data = {
        "contents": [{
            "parts": [{"text": prompt_text}]
        }]
    }

    # Make the POST request
    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        response_data = response.json()
        return response_data['candidates'][0]['content']['parts'][0]['text']
    else:
        return f"Error: {response.status_code} - {response.text}"

# Route for the home page
@app.route("/")
def home():
    return render_template("index.html")

# Route to handle chatbot responses
@app.route("/chat", methods=["POST"])
def chat():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    # Generate a response using the Gemini API
    bot_response = generate_response(user_input)
    return jsonify({"response": bot_response})

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)