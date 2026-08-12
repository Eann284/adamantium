import { Product } from '@/src/types/product'
import React from 'react'


interface Props {
    products: Product[]
}

function AllProducts({products}:Props) {
  return (
    <div>
      <div>
        {products.map(product=>(
            <div key={product.id}>
                {product.product_name}
            </div>
        ))}
      </div>
    </div>
  )
}

export default AllProducts
