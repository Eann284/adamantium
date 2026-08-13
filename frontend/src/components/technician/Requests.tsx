import { MaterialRequest } from '@/src/types/materialRequest'
import React from 'react'

interface Props {
    requests: MaterialRequest[]
}

function Requests({requests}:Props) {
  return (
    <div className='flex flex-col gap-2'>
      {requests.map(req=>(
        <div className="ring p-4 rounded-md" key={req.mrf_id}>
            <h1 className='text-lg'>{req.date}</h1>

            <div className='grid grid-cols-2'>
                <div>
                    <p>Approval Status: {req.approval_status}</p>
                    <p>Approved by: {req.approval_status != "Approved" ? "-" : req.approved_by}</p>
                </div>

                <div>
                    <p>Release Status: {req.release_status}</p>
                    <p>Released by: {req.release_status != "Released" ? "-" : req.released_by}</p>
                </div>
            </div>

            <section>
                

            <table className='table-fixed w-full'>
                <thead className='text-left'>
                    <th>Item</th>
                    <th>Quantity</th>
                </thead>

            <tbody>

            {req.items.map(item=>(
                <tr key={item.product_id} className='col-span-2'>
                    <td>Product {item.product_id}</td>
                    <td>{item.quantity}</td>
                </tr>
            ))}
            </tbody>
            </table>
            </section>
        </div>
      ))}
    </div>
  )
}

export default Requests
