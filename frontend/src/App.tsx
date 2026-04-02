import React from 'react';
import logo from './logo.svg';
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
    console.log(data);  // check what's actually coming back
    setMessages(Array.isArray(data) ? data : []);
    setLoading(false);
  };
  const handleKeyPress = (e: React.KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key == "Enter" && !e.shiftKey) {
      e.preventDefault();
      submitHandler();
    } 
  }
  return (
    <div className="flex flex-col h-screen bg-gray-950 text-gray-100">
      <div className= 'flex-1'/>
        <div className="px-4 pb-6 pt-2 border-t border-gray-800">
          <div className="flex items-end gap-2 bg-gray-900 border border-gray-700 rounded-x1 px-4 py-3">
          <textarea
          rows={1}
          value={task}
          onChange={(e) => setTask(e.target.value)}
          onKeyDown={handleKeyPress}
          placeholder='How can I Help?'
          disabled = {loading}
          className='flex-1 bg-transparent text-sm text-gray-100 placeholder-gray-600 outline-none resize-none'
        />
        <button
        onClick={submitHandler}
        disabled={loading || !task.trim()}
        className='w-8 h-8 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center transition-colors'
        >
          <span className='text-white text-sm'></span>
        </button>
        </div>
      </div>
    </div>
  );
}

export default App;