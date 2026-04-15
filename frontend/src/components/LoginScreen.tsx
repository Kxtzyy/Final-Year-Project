import react, {useState} from 'react';

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
    const [password, setpassword] = useState("");
    const [isRegister, setIsRegister] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    
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

        if(!response.ok){
            setError(data.detail || "Something went wrong");
            return;
        }
        
        localStorage.setItem("user", JSON.stringify(data));
        onLogin(data);
    };
    const handleKeyPress = (e: KeyboardEvent) => {
        if (e.key === "Enter") handleSubmit();
    };

    return (
        <div className='flex flex-col items-center justify-center h-screen bg-gray-950 text-gray-100'>
            <div className='w-full max-w-sm bg-gray-900 border border-gray-800 rounded-2xl px-8 py-10 flex flex-col gap-4'>
                <h1 className='text-xl font-semibold text-center'>
                    {isRegister ? "Create Account":"Sign in"}
                </h1>
                
            </div>
        </div>
    )
}

export default LoginScreen;