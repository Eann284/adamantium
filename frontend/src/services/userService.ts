import { User } from "../types/user";


export async function getUsers(accessToken: string): Promise<User> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/admin/users`,{
        headers: {
            Authorization: `Bearer ${accessToken}`,
        },
    })

    if (!response.ok) {
    throw new Error("Failed to fetch users");
    }

    return response.json();
}