import type { Request } from "../types/materialRequest";


export async function getAllRequests(accessToken: string): Promise<Request[]> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/requests/all`,
        {
            headers:{
                Authorization: `Bearer ${accessToken}`
            }
        }
        
    )
    if (!response.ok) {
        throw new Error("Failed to fetch requests");
    }

    return response.json()
}