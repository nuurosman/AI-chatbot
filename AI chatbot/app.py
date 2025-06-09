from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime
from markdown import markdown

# Initialize Flask app
app = Flask(__name__)

# Configure Gemini API - Replace with your actual API key
GOOGLE_API_KEY = "AIzaSyAKDZABFyzc32_eTpTdb-Qvt2SXQF-bQMM"

# Initialize Gemini
try:
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('models/gemini-1.5-flash')
    chat = model.start_chat(history=[])
    print("Gemini API initialized successfully")
except Exception as e:
    print(f"Failed to initialize Gemini API: {str(e)}")
    chat = None  # Fallback for when API fails

def get_season(month):
    """Determine the season based on the month."""
    if month in [12, 1, 2]:
        return "Winter"
    elif month in [3, 4, 5]:
        return "Spring"
    elif month in [6, 7, 8]:
        return "Summer"
    elif month in [9, 10, 11]:
        return "Autumn"
    return "Unknown"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat_response():
    user_input = request.json.get('message')
    if not user_input:
        return jsonify({"error": "No message provided"}), 400

    print(f"User Input: {user_input}") 

    try:
        user_input_lower = user_input.lower()
        current_date = datetime.now()
        response = None

        # Handle special queries
        if "date" in user_input_lower and ("today" in user_input_lower or "current" in user_input_lower):
            response = f"Today is {current_date.strftime('%B %d, %Y')}."
        elif "season" in user_input_lower:
            season = get_season(current_date.month)
            response = f"The current season is {season}."
        elif "day" in user_input_lower and "week" in user_input_lower:
            response = f"Today is {current_date.strftime('%A')}."
        
        # Use Gemini API for other queries
        if response is None:
            if chat is None:
                return jsonify({"error": "Chat service is currently unavailable"}), 503
            response = chat.send_message(user_input).text
            
        # Format code blocks
        if "```" in response:
            response = response.replace("```", "")
            response = f"<pre><code>{response}</code></pre>"

        formatted_response = f"<div>{markdown(response)}</div>"
        print(f"Bot Response: {formatted_response}")
        return jsonify({"response": formatted_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({
            "error": "Sorry, something went wrong. Please try again.",
            "details": str(e)
        }), 500

if __name__ == '__main__':
    app.run(debug=True)