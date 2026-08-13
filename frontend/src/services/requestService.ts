import type { MRF } from "../types/materialRequest";
import type { MaterialRequest } from "../types/materialRequest";

export async function createMaterialRequest(
    accessToken: string,
    data: MRF
) {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/requests/`, {
        method: 'POST',
        headers: {
            "Content-Type":"application/json",
            Authorization: `Bearer ${accessToken}`
        },
        body: JSON.stringify(data),
    });

    if (!response.ok) {
        throw new Error ("Failed to Create Request");
    }

    return response.json()
}

export async function getSentRequests(accessToken: string): Promise<MaterialRequest[]>{
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/requests/sent`,{
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    })

    if (!response.ok) {
        throw new Error("Failed to fetch sent requests");
    }

    return response.json()
}

export async function getAllRequests(accessToken: string): Promise<MaterialRequest[]> {
     const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/requests/all`,{
        headers: {
            Authorization: `Bearer ${accessToken}`
        }
    })

    if (!response.ok) {
        throw new Error("Failed to fetch all requests");
    }

    return response.json()
}