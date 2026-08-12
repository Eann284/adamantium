"use client";

import { getTotalProductsStock } from '@/src/services/inventoryService';
import { ProductStockByArea } from '@/src/types/inventory'
import { Product } from '@/src/types/product'
import React, { useState } from 'react'

interface Props {
  stock: ProductStockByArea
  products: Product[],
  accessToken: string
}

function ProductStockView({stock, products, accessToken}: Props) {

  const [productId, setProductId] = useState<number|null>(null);
  const [productStock, setProductStock] = useState<ProductStockByArea|null>(null);


  const handleViewStock = async()=> {
    if (productId === null) {
      return;
    }

    try {
      const data = await getTotalProductsStock(
        accessToken,
        productId
      );

      setProductStock(data)
      
    } catch (error) {
     console.error(error);     
    }
  }

  return (
    <div>
      
      <div>

        <select name="" id=""
        value={productId ?? ""}
          onChange={(e)=> {
            setProductId(Number(e.target.value))
          }}
        >
          <option value="">Select</option>
          {products.map((product)=>(
            <option key={product.id} 
            value={product.id}>
              {product.product_name}
            </option>
          ))}
        </select>

        <button onClick={handleViewStock}>
          View
        </button>


        {productStock && (
          <div>
          <h2>{productStock.product_name}</h2>

          {productStock.areas.map((area) => (
            <div key={area.area}>
              <span>
                {area.area} - {area.stock}
              </span>
            </div>  
          ))}
        </div>
        )}
      </div>
    </div>
  )
}

export default ProductStockView
