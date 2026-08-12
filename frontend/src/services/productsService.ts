import { Product } from "../types/product";




export async function getProducts(accessToken: string): Promise<Product[]> {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/products/`,
        {
            headers:{
                Authorization: `Bearer ${accessToken}`
            }
        }
        
    )
    if (!response.ok) {
        throw new Error("Failed to fetch products");
    }

    return response.json()
}