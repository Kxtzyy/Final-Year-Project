import React, { useState, useEffect } from "react";
import { API } from '../api'

interface Conversation {
    id: number;
    user_id: number;
    title: string;
}

interface Props {
    userId: number;
    activeConversationId: number | null;
    onSelectConversation: (id: number) => void;
    onNewConversation: (id: number) => void;
}

function Sidebar({ userId, activeConversationId, onSelectConversation, onNewConversation }: Props){
    const [conversations, setConversations] = useState<Conversation[]>([]);

    useEffect(() => {
        fetchConversations();
    }, []);

    const fetchConversations = async () => {
        const response = await fetch(`${ API }/conversations/${userId}`);
        const data = await response.json();
        setConversations(Array.isArray(data) ? data : []);
    };

    const handleNewChat = async() => {
        const response = await fetch(`${API}/conversations`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ user_id: userId, title: "New Chat" }),
        });
        const data = await response.json();
        setConversations(prev => [data, ...prev]);
        onNewConversation(data.id);
    };

    return (
    <div className="w-64 h-full bg-gray-900 border-r border-gray-800 flex flex-col">
        <div className="p-3">
            <button
            onClick={handleNewChat}
            className="w-full bg-indigo-600 hover:bg-indigo-500 text-white text-sm rounded-lg py-2 transition-colors"
            >
            + New Chat
            </button>
        </div>

        <div className="flex-1 overflow-y-auto px-2 flex flex-col gap-1">
            {conversations.length === 0 && (
            <p className="text-xs text-gray-600 text-center mt-4">No conversations yet</p>
            )}
            {conversations.map((conv) => (
            <button
                key={conv.id}
                onClick={() => onSelectConversation(conv.id)}
                className={`w-full text-left px-3 py-2 rounded-lg text-sm truncate transition-colors ${
                conv.id === activeConversationId
                    ? "bg-gray-700 text-gray-100"
                    : "text-gray-400 hover:bg-gray-800 hover:text-gray-200"
                }`}
            >
                {conv.title}
            </button>
            ))}
        </div>
    </div>
    )
}

export default Sidebar;