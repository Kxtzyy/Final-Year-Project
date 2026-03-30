import React from 'react';
import logo from './logo.svg';
import './App.css';
import { useState } from 'react';
interface Message {
  agent: string;
  content: string;
}

function App() {
  const [task, setTask] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  const submitHandler = async() => {
    if (!task.trim()) return;
    setLoading(true);
    setMessages([]);

    const response = await fetch("http://100.112.20.52:8000/run", {
      method: "POST",
      headers: {
        "Content-Type" : "applications/json",
        "Accept" : "application/json"
      },
      body: JSON.stringify({task}),
    });
    const data = await response.json();
    console.log(JSON.stringify({ task }));
    console.log(data);
    setMessages(data.result);
    setLoading(false);
  }
  return (
    <div style={{ maxWidth: "800px", margin: "0 auto", padding: "20px" }}>
      <h1>Coding Assistant</h1>

      <textarea
        value={task}
        onChange={(e) => setTask(e.target.value)}
        placeholder="Enter your task..."
        rows={4}
        style={{ width: "100%", marginBottom: "10px" }}
      />
      <button onClick={submitHandler} disabled={loading}>
        {loading ? "Thinking..." : "Submit"}
      </button>

      <div style={{ marginTop: "20px" }}>
        {messages.map((msg, i) => (
          <div key={i} style={{ marginBottom: "20px" }}>
            <strong>[{msg.agent}]</strong>
            <pre style={{ whiteSpace: "pre-wrap" }}>{msg.content}</pre>
            <hr />
          </div>
        ))}
      </div>
    </div>
  );
}

export default App;
