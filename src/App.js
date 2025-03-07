import React, { useState } from "react";
import "./App.css";

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const userId = "user_123"; // Replace with a unique user ID

  const handleSend = async () => {
    if (!input.trim()) return;

    // Add user message to the chat
    setMessages((prev) => [...prev, { role: "user", content: input }]);

    // Send message to the backend
    const response = await fetch("http://localhost:5000/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, prompt: input }),
    });

    const data = await response.json();
    setMessages((prev) => [...prev, { role: "assistant", content: data.response }]);

    // Clear input
    setInput("");
  };

  return (
    <div className="App">
      <h1>OXTA AI</h1>
      <div className="chat-window">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.role}`}>
            <strong>{msg.role === "user" ? "You" : "OXTA AI"}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === "Enter" && handleSend()}
        />
        <button onClick={handleSend}>Send</button>
      </div>
    </div>
  );
}

export default App;
