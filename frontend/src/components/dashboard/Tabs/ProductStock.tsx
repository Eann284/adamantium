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

function ProductStockView({products, accessToken}: Props) {

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

        <section className='grid grid-cols-2 gap-3'>

        <select name="" id="" className='ring ring-gray-400 w-full'
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

        <button onClick={handleViewStock} className='bg-blue-500 rounded-md text-white font-bold'>
          View Stock
        </button>
        </section>


        {productStock && (
          <div className=''>
            <h2 className='text-lg font-semibold'>Stock for {productStock.product_name}</h2>

            <table className='ring ring-gray-400 w-full table-fixed divide-gray-400'>

            {productStock.areas.map((area) => (
              <tr key={area.area}>
                <td className='px-1 font-semibold'>{area.area}</td>
                <td>{area.stock}</td>
              </tr>  
            ))}
            </table>
          </div>
        )}
      </div>
    </div>
  )
}

export default ProductStockView
