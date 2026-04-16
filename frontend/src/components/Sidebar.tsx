import React, { useState, useEffect, useRef } from "react";
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
    onDeleteConversation: (id: number) => void;
}

function Sidebar({ userId, activeConversationId, onSelectConversation, onNewConversation, onDeleteConversation }: Props){
    const [conversations, setConversations] = useState<Conversation[]>([]);
    const [menuOpenId, setMenuOpenId] = useState<number | null>(null);
    const menuRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        fetchConversations();
    }, []);

    useEffect(() => {
        const handleClickOutside = (e: MouseEvent) => {
            if (menuRef.current && !menuRef.current.contains(e.target as Node)) {
                setMenuOpenId(null);
            }
        };
        document.addEventListener("mousedown", handleClickOutside);
        return () => document.removeEventListener("mousedown", handleClickOutside);
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

    const handleDelete = async (id: number) => {
        const response = await fetch(`${API}/conversations/ ${userId}/${id}`, {
            method: "DELETE",
        });
        if (response.ok){
            setConversations(prev => prev.filter(c => c.id !== id));
            setMenuOpenId(null);
            onDeleteConversation(id);
        }
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
                <div
                    key = {conv.id}
                    className={`relative flex items-center rounded-lg group ${
                        conv.id === activeConversationId
                        ? "bg-gray-700"
                        : "hover:bg-gray-800"
                    }`}
                >
                    <button
                        onClick = {() => onSelectConversation(conv.id)}
                        className = "flex-1 text-left px-3 py-2 text-sm truncate transition-colors text-gray-400 group-hover:text-gray-200"
                    >
                        {conv.title}
                    </button>
                    <button
                        onClick={(e) => {e.stopPropagation(); setMenuOpenId(menuOpenId === conv.id ? null : conv.id); }}
                        className="w-6 h-6 flex items-center justify-center text-gray-400 hover:text-gray-100 opacity-0 group-hover:opacity-100 transition-opacity mr-1"
                    >
                        <span style={{ fontSize: "40px", lineHeight: 1 }} className="pb-2 ">···</span>
                    </button>

                    {menuOpenId === conv.id && (
                        <div
                            ref={menuRef}
                            className="absolute right-0 top-8 z-10 bg-gray-800 border border-gray-700 rounded-lg shadow-lg py-1 w-32"
                        >
                            <button
                                onClick={() => handleDelete(conv.id)}
                                className="w-full text-left px-3 py-2 text-sm text-red-400 hover:bg-gray-700 transition-colors"
                            >
                                Delete
                            </button>
                        </div>
                    )}
                </div>
            ))}
        </div>
    </div>
    )
}

export default Sidebar;