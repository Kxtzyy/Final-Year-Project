  import React, { useEffect } from 'react';
  import ReactMarkdown from 'react-markdown';
  import {Prism as SyntaxHighlighter} from 'react-syntax-highlighter';
  import { oneDark } from 'react-syntax-highlighter/dist/esm/styles/prism';
  import logo from './logo.svg';
  import { useState } from 'react';
  import LoginScreen from './components/LoginScreen';
  import Sidebar from './components/Sidebar';

  interface Message {
    agent: string;
    content: string;
  }

  interface User {
    id: number;
    username: String;
  }

  function App() {
    const [user, setUser] = useState<User | null>(null);
    const [task, setTask] = useState("");
    const [messages, setMessages] = useState<Message[]>([]);
    const [loading, setLoading] = useState(false);
    const [conversationId, setConversationId] = useState<number | null>(null);

    useEffect(() => {
      const stored = localStorage.getItem("user");
      if (stored) setUser(JSON.parse(stored));
    }, []);

    const handleLogin = (user: User) => setUser(user);

    const handleLogout = () => {
      localStorage.removeItem("user");
      setUser(null);
      setMessages([]);
    }

    const handleSelectConversation = async (id: number) => {
      setConversationId(id);
      setMessages([]);

      const response = await fetch(`http://100.112.20.52:8000/messages/${id}`);
      const data = await response.json();
      setMessages(Array.isArray(data) ? data : []);
    }

    const submitHandler = async() => {
      if (!task.trim()) return;
      setLoading(true);
      setMessages([]);

      const response = await fetch("http://100.112.20.52:8000/run", {
        method: "POST",
        headers: {
          "Content-Type" : "application/json",
          "Accept" : "application/json"
        },
        body: JSON.stringify({task, conversation_id: conversationId}),
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

    if(!user) return <LoginScreen onLogin={handleLogin} />;
    return (
      <div className='flex flex-col h-screen bg-gray-950 text-gray-100'>
        <div className='flex items-center justify-between px-4 py-3 border-b border-gray-800'>
          <span className='text-sm text-gray-400'> Signed in as <span className='text-gray-200'>{user.username}</span></span>
          <button onClick={handleLogout} className='text-xs text-gray-500 hover:text-gray-300 transition-colors'>
            Sign out
          </button>
        </div>
        <div className='flex flex-1 overflow-hidden'>
          <Sidebar
            userId= {user.id}
            activeConversationId={conversationId}
            onSelectConversation={handleSelectConversation}
            onNewConversation={(id) => { setConversationId(id); setMessages([]); }}
            onDeleteConversation={(id) => {if (conversationId === id) { setConversationId(null); setMessages([]); }}}
            />
          <div className='flex flex-col flex-1 overflow-hidden'>
            <div className='flex-1 overflow-y-auto px-4 py-6 space-y-4'>
              {messages.map((msg, i) => (
                <div key={i} className={`flex ${msg.agent === "user" ? "justify-end" : "justify-start"}`}>
                  <div className={`max-w-[75%] rounded-xl px-4 py-3 text-sm leading-relaxed ${
                    msg.agent === "user"
                    ? "bg-indigo-600 text-white"
                    : "bg-gray-900 border border-gray-800 text-gray-100 prose prose-invert max-w-none"
                  }`}>
                    {msg.agent === "user" ? (
                      <p>{msg.content}</p>
                    ) : (
                      <ReactMarkdown
                        components={{
                          code({ node, className, children, ...props}: any) {
                            const match = /language-(\w+)/.exec(className || '');
                            const isBlock = match || String(children).includes('\n');
                            return isBlock ? (
                              <SyntaxHighlighter style= {oneDark} language={match?.[1] || 'text'} PreTag="div">
                                {String(children).replace(/\n$/, '')}
                              </SyntaxHighlighter>
                            ) : (
                              <code className='bg-gray-800 px-1 py-0.5 rounded text-emerald-400 text-xs' {...props}>
                                {children}
                              </code>
                            );
                          }
                        }}
                      >
                        {msg.content.replace(/\\n/g, '\n')}
                      </ReactMarkdown>
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className='flex gap-1.5 px-4 py-3'>
                  <span className='w-2 h-2 rounded-full bg-gray-500 animate-bounce [animation-delay:0ms]'/>
                  <span className='w-2 h-2 rounded-full bg-gray-500 animate-bounce [animation-delay:150ms]'/>
                  <span className='w-2 h-2 rounded-full bg-gray-500 animate-bounce [animation-delay:300ms]'/>
                </div>
              )}
            </div>
            <div className='px-4 pb-6 border-t border-gray-800'>
              <div className='flex items-end gap-2 bg-gray-900 border border-gray-700 rounded-xl px-4 py-3'>
                <textarea
                  rows={1}
                  value={task}
                  onChange={(e) => setTask(e.target.value)}
                  onKeyDown={handleKeyPress}
                  placeholder={conversationId ? "How can I help?" : "Create or select a conversation to start"}
                  disabled={loading || !conversationId}
                  className='flex-1 bg-transparent text-sm text-gray-100 placeholder-gray-600 outline-none resize-none'
                />
                <button
                  onClick={submitHandler}
                  disabled={loading || !task.trim() || !conversationId}
                  className='w-8 h-8 rounded-lg bg-indigo-600 hover:bg-indigo-500 disabled:opacity-30 disabled:cursor-not-allowed flex items-center justify-center transition-colors'
                >
                  <span className='text-white text-sm'>→</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    );
  }

  export default App;