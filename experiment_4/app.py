import os
import json
import requests
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Load College Data
try:
    with open('data/college_data.json', 'r') as file:
        college_data = json.load(file)
except Exception as e:
    college_data = {"error": "Failed to load college data."}

def get_system_prompt():
    """Generates the system prompt based on the loaded college data."""
    college_info_str = json.dumps(college_data, indent=2)
    prompt = f"""You are the AI Admission Assistant for ABC Institute of Technology.

Your task is to answer student questions about admissions politely, clearly, and concisely.

Rules:
1. Use ONLY the college information provided below.
2. Do not invent fees, dates, eligibility criteria, courses, or procedures.
3. If the information is unavailable in the knowledge base, clearly say so.
4. Maintain context from previous messages.
5. Answer in simple and professional language.
6. Ask for clarification when the student's query is ambiguous.
7. Use bullet points where appropriate for readability.
8. Do not pretend to be a human counselor.
9. If asked about something completely unrelated (e.g., "Who is the Prime Minister?"), politely explain that you specialize only in ABC Institute of Technology admissions.

College Information:
{college_info_str}
"""
    return prompt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return jsonify({"error": "API key is not configured. Please add OPENAI_API_KEY to your .env file."}), 500

    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Invalid request. Message is required."}), 400
        
    user_message = data['message'].strip()
    if not user_message:
        return jsonify({"error": "Message cannot be empty."}), 400

    conversation_history = data.get('history', [])
    
    messages = [{"role": "system", "content": get_system_prompt()}]
    for msg in conversation_history:
        messages.append({"role": msg['role'], "content": msg['content']})
    messages.append({"role": "user", "content": user_message})

    try:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": messages,
            "temperature": 0.3,
            "max_tokens": 300
        }
        
        response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=15)
        
        if response.status_code == 200:
            result = response.json()
            reply = result["choices"][0]["message"]["content"].strip()
            return jsonify({"response": reply})
        elif response.status_code == 401:
            return jsonify({"error": "Authentication Failed: Invalid OpenAI API Key."}), 401
        elif response.status_code == 429:
            return jsonify({"error": "Rate Limit Exceeded: Please try again later."}), 429
        else:
            return jsonify({"error": f"API Error: {response.text}"}), response.status_code
            
    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Network Error: Could not connect to the API server."}), 503
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
