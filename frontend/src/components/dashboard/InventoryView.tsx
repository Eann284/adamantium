import { Inventory } from '@/src/types/inventory'
import React from 'react'

interface Props {
    inventory: Inventory[]
}

function InventoryView({inventory}:Props) {
  return (
    <div>
      {inventory.map((i)=>(
        <div key={i.id}>
          <h1>Product: {i.product_name}</h1>
          <h1>Area: {i.area}</h1>
        </div>
      ))}
    </div>
  )
}


export default InventoryView
