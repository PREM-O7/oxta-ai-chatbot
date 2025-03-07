# OXTA AI - Chatbot

OXTA AI is an AI chatbot built with Flask (Python) for the backend and React for the frontend. It integrates with DeepSeek for AI-generated responses and OpenWeatherMap for weather information. This project maintains context memory across multiple user interactions.

## Features

- **Context Memory**: The chatbot retains conversation history to provide context-aware responses.
- **AI Responses**: AI-generated responses powered by DeepSeek.
- **Weather Integration**: Get real-time weather data via the OpenWeatherMap API.
- **React Frontend**: A simple, user-friendly React-based UI for chatting with the bot.

## Requirements

- Python 3.x
- Node.js (for the frontend)
- Flask
- React
- OpenWeatherMap API key
- DeepSeek API key

## Setup Instructions

### Backend Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Create a `.env` file in the root directory and add your API keys:
   ```bash
   DEEPSEEK_API_KEY=your_deepseek_api_key
   OPENWEATHER_API_KEY=your_openweathermap_api_key
   ```

3. Run the Flask app:
   ```bash
   python app.py
   ```

### Frontend Setup

1. Navigate to the frontend directory and install dependencies:
   ```bash
   cd src
   npm install
   ```

2. Start the React development server:
   ```bash
   npm start
   ```

The frontend should now be accessible at `http://localhost:3000` and the backend at `http://localhost:5000`.

## Deployment

You can deploy the backend on platforms like Heroku or AWS, and the frontend on Vercel or Netlify. Remember to update the API URL in the React app for the deployed backend.

## License

This project is licensed under the MIT License.
