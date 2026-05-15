import react, { useState } from 'react';

const API = "http://100.112.20.52:8000";

interface User{
    id: number;
    username: string;
}

interface Props{
    onLogin: (user: User) => void;
}

function LoginScreen({ onLogin }: Props) {
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");
    const [isRegister, setIsRegister] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    
    // Sends login or register request depending on current mode
    const handleSubmit = async () => {
        if (!username.trim() || !password.trim()) return;
        setLoading(true);
        setError("");

        const endpoint = isRegister ? "/register" : "/login";
        const response = await fetch(`${API}${endpoint}`, {
            method: "POST",
            headers: {"Content-Type" : "application/json"},
            body: JSON.stringify({username, password}),
        });
        
        const data = await response.json();
        setLoading(false);

        // Display error message returned by the backend if request failed
        if(!response.ok){
            setError(data.detail || "Something went wrong");
            return;
        }
    
        // Persist the user object to localStorage and update authentication state
        localStorage.setItem("user", JSON.stringify(data));
        onLogin(data);
    };

    // Allows form submission via the Enter key
    const handleKeyPress = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter") handleSubmit();
    };

    return (
        <div className='flex flex-col items-center justify-center h-screen bg-gray-950 text-gray-100'>
            <div className='w-full max-w-sm bg-gray-900 border border-gray-800 rounded-2xl px-8 py-10 flex flex-col gap-4'>
                <h1 className='text-xl font-semibold text-center'>
                    {isRegister ? "Create Account":"Sign in"}
                </h1>
                {/* Username input box */}
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                    onKeyDown={handleKeyPress}
                    className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-sm outline-none focus:border-indigo-500"
                />
                {/* Password input box */}
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    onKeyDown={handleKeyPress}
                    className="bg-gray-800 border border-gray-700 rounded-lg px-4 py-2 text-sm outline-none focus:border-indigo-500"
                />
                {error && <p className="text-red-400 text-xs text-center">{error}</p>}

                {/* Login or register button */}
                <button
                onClick={handleSubmit}
                disabled={loading}
                className="bg-indigo-600 hover:bg-indigo-500 disabled:opacity-40 rounded-lg py-2 text-sm font-medium transition-colors"
                >
                {loading ? "..." : isRegister ? "Register" : "Login"}
                </button>

                {/* Toggles between login and register mode */}
                <p className="text-xs text-center text-gray-500">
                    {isRegister ? "Already have an account?" : "Don't have an account?"}{" "}
                    <span
                        className="text-indigo-400 cursor-pointer hover:underline"
                        onClick={() => { setIsRegister(!isRegister); setError(""); }}
                    >
                        {isRegister ? "Sign in" : "Register"}
                    </span>
                </p>
            </div>
        </div>
    )
}

export default LoginScreen;