from flask import Flask, request, jsonify
import requests
import json
import os

app = Flask(__name__)

# DeepSeek API settings
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"  # Replace with the actual API endpoint
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")  # Store your API key in environment variables

# Context memory
conversation_history = {}

# Headers for the DeepSeek API request
headers = {
    "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
    "Content-Type": "application/json"
}

def chat_with_deepseek(prompt, user_id, model="deepseek-chat", max_tokens=150):
    """
    Sends a prompt to the DeepSeek API and returns the AI's response.
    Maintains context memory for each user.
    """
    global conversation_history

    # Initialize conversation history for the user if it doesn't exist
    if user_id not in conversation_history:
        conversation_history[user_id] = []

    # Add the user's prompt to the conversation history
    conversation_history[user_id].append({"role": "user", "content": prompt})

    # Prepare the payload with the full conversation history
    payload = {
        "model": model,
        "messages": conversation_history[user_id],
        "max_tokens": max_tokens
    }

    # Send the request to DeepSeek API
    response = requests.post(DEEPSEEK_API_URL, headers=headers, data=json.dumps(payload))

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the response
        response_data = response.json()
        ai_response = response_data["choices"][0]["message"]["content"].strip()

        # Add the AI's response to the conversation history
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})

        return ai_response
    else:
        # Handle errors
        print(f"Error: {response.status_code} - {response.text}")
        return None

def get_weather(city):
    """
    Fetches weather data using OpenWeatherMap API.
    """
    OPENWEATHER_API_KEY = os.getenv("OPENWEATHER_API_KEY")
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API_KEY}&units=metric"
    response = requests.get(url)
    if response.status_code == 200:
        weather_data = response.json()
        return f"Weather in {city}: {weather_data['weather'][0]['description']}, Temperature: {weather_data['main']['temp']}°C"
    else:
        return "Sorry, I couldn't fetch the weather data."

@app.route("/chat", methods=["POST"])
def chat():
    """
    Endpoint for chatting with OXTA AI.
    """
    data = request.json
    user_id = data.get("user_id")
    prompt = data.get("prompt")

    # Check if the user is asking for weather
    if "weather" in prompt.lower():
        city = prompt.split("in ")[-1].strip()
        response = get_weather(city)
    else:
        # Get AI response
        response = chat_with_deepseek(prompt, user_id)

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(debug=True)
