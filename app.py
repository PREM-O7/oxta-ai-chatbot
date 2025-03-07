from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# DeepSeek API settings
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual API endpoint
conversation_history = {}  # Context memory for users

@app.route('/')
def home():
    return "Oxta AI Backend is Running!"

def chat_with_deepseek(prompt, user_id, model="deepseek-chat", max_tokens=150):
    """
    Sends a prompt to the DeepSeek API and returns the AI's response.
    Maintains context memory for each user.
    """
    global conversation_history
    DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Load API key dynamically

    if not DEEPSEEK_API_KEY:
        return "Error: DeepSeek API key is missing."

    headers = {
        "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
        "Content-Type": "application/json"
    }

    if user_id not in conversation_history:
        conversation_history[user_id] = []

    conversation_history[user_id].append({"role": "user", "content": prompt})

    payload = {
        "model": model,
        "messages": conversation_history[user_id],
        "max_tokens": max_tokens
    }

    try:
        response = requests.post(DEEPSEEK_API_URL, headers=headers, data=json.dumps(payload))
        response.raise_for_status()  # Raise an error for HTTP issues

        response_data = response.json()
        ai_response = response_data["choices"][0]["message"]["content"].strip()
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})

        return ai_response
    except requests.exceptions.RequestException as e:
        return f"DeepSeek API Error: {str(e)}"

def get_weather(city):
    """
    Fetches weather data using OpenWeatherMap API.
    """
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    if not OPENWEATHER_API_KEY:
        return "Error: OpenWeather API key is missing."

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"

    try:
        response = requests.get(url)
        response.raise_for_status()
        weather_data = response.json()
        return f"Weather in {city}: {weather_data['weather'][0]['description']}, Temperature: {weather_data['main']['temp']}°C"
    except requests.exceptions.RequestException as e:
        return f"Weather API Error: {str(e)}"

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint for chatting with OXTA AI.
    """
    data = request.json
    user_id = data.get("user_id")
    prompt = data.get("prompt")

    if not user_id or not prompt:
        return jsonify({"error": "Missing user_id or prompt"}), 400

    if "weather" in prompt.lower():
        city = prompt.split("in ")[-1].strip()
        response = get_weather(city)
    else:
        response = chat_with_deepseek(prompt, user_id)

    return jsonify({"response": response})

# Deployment Configuration
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get PORT from Render for deployment
    app.run(host="0.0.0.0", port=port)
