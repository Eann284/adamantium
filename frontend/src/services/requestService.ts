import type { MRF, MRFItem } from "../types/materialRequest";
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

// get pending

export async function getPendingRequests(accessToken: string): Promise<MaterialRequest[]>{
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/requests/pending`,
        {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }   
        }
    )
    if (!response.ok) {
        throw new Error("Failed to fetch pending requests");
    }

    return response.json()
}


// get pending by ID
export async function getPendingRequestsById(accessToken: string, mrf_id: number): Promise<MaterialRequest[]>{
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/requests/pending/${mrf_id}`,
        {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }   
        }
    )
    if (!response.ok) {
        throw new Error(`Failed to fetch pending request ${mrf_id}`);
    }

    return response.json()
}


export async function approveRequest(
    accessToken: string,
    mrf_id: number
) {
    const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/requests/${mrf_id}/approve`,
        {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        }
    );

    if (!response.ok) {
        throw new Error("Failed to approve request");
    }

    return response.json();
}

export async function disapproveRequest(
    accessToken: string,
    mrf_id: number
) {
    const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/requests/${mrf_id}/disapprove`,
        {
            method: "PUT",
            headers: {
                Authorization: `Bearer ${accessToken}`,
            },
        }
    );

    if (!response.ok) {
        throw new Error("Failed to approve request");
    }

    return response.json();
}

export async function editRequest(accessToken: string, mrf_id: number, items: MRFItem[]){
    const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/requests/${mrf_id}/edit`,
        {
            method: "PUT",
            headers: {
                "Content-Type": "application/json",
                Authorization: `Bearer ${accessToken}`,
            },
            body: JSON.stringify(items),
        }
    );
    if (!response.ok) {
        throw new Error(`Failed to edit request ${mrf_id}`);
    }

    return response.json();
}