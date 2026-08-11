
export interface AreaSummary {
    area: string
    total_stock: number;
    product_count: number
}


export interface InventorySummary {
    total: number;
    per_area: AreaSummary[]
}