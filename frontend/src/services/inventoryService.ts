import { Inventory, InventorySummary } from "../types/inventory";

export async function getInventory(
    accessToken:string
): Promise<InventorySummary> {


    const response = await fetch( `${process.env.NEXT_PUBLIC_API_URL}/inventory/summary`,
         {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        }
    );
    
     if (!response.ok) {
        throw new Error("Failed to fetch inventory summary");
    }


    return response.json()
}

export async function getAllInventory(
    accessToken: string
): Promise<Inventory[]> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/inventory/all`,
        {
            headers: {
                Authorization: `Bearer ${accessToken}`
            }
        }
    );
    if (!response.ok) {
        throw new Error("Failed to fetch inventory items");
    }

    return response.json()
}