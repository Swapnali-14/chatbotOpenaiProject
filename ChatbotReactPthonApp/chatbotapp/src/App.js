import React, { useState } from "react";
import axios from "axios";
import './App.css';  // Import your CSS file

function App() {
  const [userInput, setUserInput] = useState("");
  const [chatHistory, setChatHistory] = useState([]);

  
  const handleUserInput = (e) => {
    setUserInput(e.target.value);
  };

  const handleSendMessage = async () => {
    if (!userInput) return;

    const userMessage = {
      type: "user",
      message: userInput,
    };

    setChatHistory([...chatHistory, userMessage]);

    try {
      // Send the user input to the backend
      const response = await axios.post("http://localhost:5000/query", {
        query: userInput,
      });

      const botMessage = {
        type: "bot",
        message: response.data.message,
      };

      setChatHistory([...chatHistory, userMessage, botMessage]);
      setUserInput(""); // Clear input field
    } catch (error) {
      console.error("Error sending message to backend", error);
    }
  };

  return (
    <div className="chat-container">
      <div className="chat-history">
        {chatHistory.map((msg, idx) => (
          <div key={idx} className={`message ${msg.type}`}>
            {msg.message}
          </div>
        ))}
      </div>
      <div className="input-container">
        <input
          type="text"
          value={userInput}
          onChange={handleUserInput}
          placeholder="Ask me something..."
        />
        <button onClick={handleSendMessage}>Send</button>
      </div>
    </div>
  );
}

export default App;
