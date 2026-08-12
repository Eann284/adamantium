import { getSession } from "next-auth/react";

const API_BASE = process.env.NEXT_PUBLIC_API_URL

async function getAuthToken() {
    const session = await getSession();
    return session?.user?.accessToken
}

async function request<T>(endpoint: string,options: RequestInit = {}): Promise<T> {

    const token = await getAuthToken();

    const headers: Record<string, string> = {
        'Content-Type': 'application/json',
    }

    

    if (token) {
        headers['Authorization'] = `Bearer ${token}`
    }

    if (options.headers) {
    const customHeaders = options.headers as Record<string, string>
    Object.assign(headers, customHeaders)
  }

    const res = await fetch(`${API_BASE}${endpoint}`, {
        ...options,
        headers,
    })

    if (!res.ok) {
        const error = await res.json()
        throw new Error(error.detail || error.message || `HTTP ${res.status}`)
    }

    if (res.status === 204) {
        return {} as T
    }

    return res.json()
}

export const api = {
    get:<T>(endpoint:string, options?:RequestInit)=>request<T>(endpoint, {...options, method:'GET'}),

    post:<T>(endpoint: string, body?:unknown, options?:RequestInit)=>request<T>(endpoint, 
        {...options,
            method: 'POST',
            body: body ? JSON.stringify(body): undefined
        }),
    put:<T>(endpoint: string, body?:unknown, options?:RequestInit)=>request<T>(endpoint, 
        {...options,
            method: 'PUT',
            body: body ? JSON.stringify(body): undefined
        }),
    delete:<T>(endpoint: string, body?:unknown, options?:RequestInit)=>request<T>(endpoint, 
        {...options,
            method: 'DELETE',
        })




}