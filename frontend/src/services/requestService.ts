import type { MRF } from "../types/materialRequest";

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