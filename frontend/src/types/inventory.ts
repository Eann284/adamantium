
export interface AreaSummary {
    area: string
    total_stock: number;
    product_count: number
}


export interface InventorySummary {
    total: number;
    per_area: AreaSummary[]
}
export interface Inventory {
    id: number
    product_id: number
    product_name: string
    area: "Cavite" | "Laguna" | "Quezon" | "Rizal"
    stock: number
}
    