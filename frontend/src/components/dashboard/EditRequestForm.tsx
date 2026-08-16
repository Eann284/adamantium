"use client"

import { editRequest } from '@/src/services/requestService'
import { MaterialRequest, MRFItem } from '@/src/types/materialRequest'
import { Product } from '@/src/types/product'
import React, { useState } from 'react'


interface Props {
    request: MaterialRequest
    products: Product[]
    accessToken: string
}

function EditRequestForm({request, products, accessToken}:Props) {

    const [items, setItems] = useState<MRFItem[]>(request.items);

    const handleSave = async () => {
    await editRequest(
        accessToken,
        request.mrf_id,
        items
    );
};

    const productMap = Object.fromEntries(
        products.map(product => [
            product.id,
            product.product_name
        ])
    );

  return (
    <form className='border p-10 w-150 mx-auto'>
    <h1 className='text-2xl'>MRF-{request.mrf_id}</h1>
    <p>Requested by {request.requestor_email}</p>

        <div className='grid grid-cols-[auto_1fr] gap-10'>
    <section>
        <div className='font-semibold'>Items:</div>

        {items.map((item, index) => (
            <div key={item.product_id} className='grid grid-cols-2 gap-3'>


                <p>{productMap[item.product_id]}</p>

                <input
                    type="number"
                    value={item.quantity}
                    className='ring ring-gray-400 px-2 w-30'
                    
                    onChange={(e)=>{
                        const updated = [...items];

                        updated[index].quantity = Number(e.target.value);

                        setItems(updated);
                    }}
                />

            </div>
        ))}
     
       
        </section>
        <div className='flex flex-col justify-center ring ring-gray-400 rounded-md p-4'>
            <h1>Requested by:</h1>
            <h1>{request.requestor_email}</h1>
        </div>
    </div>
        <button type="button" className='w-full text-center mt-3 border rounded-lg' onClick={handleSave}>
            Save Changes
        </button>
    </form>
  )
}

export default EditRequestForm
