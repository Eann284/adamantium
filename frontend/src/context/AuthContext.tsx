import { createContext, useState, useEffect, type ReactNode } from "react";
import toast from 'react-hot-toast'


interface User {
    id: number;
    name: string;
    email: string;
    role: string;
    area: string;
    stock: number;
}

interface AuthContextType {
    user: User | null
    token: string | null
    login: (email: string, password: string) => Promise<void>
    logout: () => void
    isAuthenticated: boolean
    isLoading: boolean
}

// eslint-disable-next-line react-refresh/only-export-components
export const AuthContext = createContext<AuthContextType | undefined>(undefined)

const API_URL = 'http://localhost:8000'

export const AuthProvider = ({children}:{children: ReactNode}) => {
    const [user, setUser] =  useState<User | null>(null);
    const [token, setToken] =  useState<string | null>(null);
    const [isLoading, setIsLoading] = useState(true);

    useEffect(()=>{
        const storedToken = localStorage.getItem('access_token');
        const storedUser = localStorage.getItem('user');

        if (storedToken && storedUser) {
            // eslint-disable-next-line react-hooks/set-state-in-effect
            setToken(storedToken)
            setUser(JSON.parse(storedUser))
        }
        setIsLoading(false)
    }, [])
    
    const login = async(email: string, password: string) => {
        const formData = new URLSearchParams({
            username: email,
            password: password
        })

        const response = await fetch(`${API_URL}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type' : 'application/x-www-form-urlencoded'
            },
            body: formData
        })

        if (!response.ok){
            const error = await response.json()
            throw new Error(error.detail || 'Login Failed')
        }

        const data = await response.json()

        localStorage.setItem('access_token', data.access_token)
        localStorage.setItem('user', JSON.stringify(data.user))

        toast.success(data.user.name)
    }

    const logout =()=>{
        localStorage.removeItem('access_token')
        localStorage.removeItem('user')
        setToken(null)
        setUser(null)
        toast.success('Logged out')
    }

    return(
        <AuthContext.Provider value={{
            user, token,
            login, logout,
            isAuthenticated: !!user && !!token,
            isLoading
        }}>
            {children}
        </AuthContext.Provider>
    )
}

