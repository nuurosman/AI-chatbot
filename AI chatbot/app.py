from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
import os
from datetime import datetime
from markdown import markdown

GOOGLE_API_KEY = "***INCLUDE API KEY***"
genai.configure(api_key=GOOGLE_API_KEY)

model = genai.GenerativeModel('models/gemini-1.5-flash')
chat = model.start_chat(history=[])

app = Flask(__name__)

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

        if "date" in user_input_lower and ("today" in user_input_lower or "current" in user_input_lower):
            response = f"Today is {current_date.strftime('%B %d, %Y')}."
        elif "season" in user_input_lower:
            season = get_season(current_date.month)
            response = f"The current season is {season}."
        elif "day" in user_input_lower and "week" in user_input_lower:
            response = f"Today is {current_date.strftime('%A')}."
        
        if response is None:
            response = chat.send_message(user_input).text
            
        if "```" in response:
            response = response.replace("```", "")
            response = f"<pre><code>{response}</code></pre>"

        formatted_response = f"<div>{markdown(response)}</div>"
        print(f"Bot Response: {formatted_response}")
        return jsonify({"response": formatted_response})

    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
