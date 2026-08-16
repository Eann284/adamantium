import { MaterialRequest } from '@/src/types/materialRequest'
import React from 'react'

interface Props {
    requests: MaterialRequest;
    onView: (request: MaterialRequest)=>void
}

function RequestCard({requests, onView}:Props) {
  return (
    
    <div key={requests.mrf_id} className='border'>
      <h1>MRF-{requests.mrf_id} - {requests.requestor_email}</h1>
      <div>{requests.approval_status}</div>
      <button onClick={()=>onView(requests)}>View</button>
      {/* <ul>
        {requests.items.map((item)=>(
            <li key={item.product_id}>
                <section className='grid grid-cols-2'>
                <div className='font-bold'>
                    Product
                </div>
                <div className='font-bold'>
                    Quantity
                </div>
                <div>
                    {item.product_id}
                </div>
                <div>
                    {item.quantity}
                </div>
                </section>

            </li>
        ))}
      </ul> */}
    </div>
  )
}

export default RequestCard
