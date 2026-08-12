import type {Dashboard } from "../types/dashboard";


export async function getDashboard(accessToken:string):Promise<Dashboard> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/dash`,
        {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        }
    );

    if (!response.ok) {
         throw new Error("Failed to fetch dashboard data");
    }

    return response.json()

}   