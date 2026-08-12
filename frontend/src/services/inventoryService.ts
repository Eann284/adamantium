import { Inventory, InventorySummary, AllProductStockByArea, StockByArea, ProductStockByArea } from "../types/inventory";

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

export async function getTotalProductsStock(accessToken: string, product_id: number): Promise<ProductStockByArea>{
    const response = await fetch(`
        ${process.env.NEXT_PUBLIC_API_URL}/inventory/product/${product_id}`,
       { headers: {
            Authorization: `Bearer ${accessToken}`
        }}
    )

    if (!response.ok) {
        throw new Error (`Failed to Get Product Stock of ${product_id}`)
    }

    return response.json()
}