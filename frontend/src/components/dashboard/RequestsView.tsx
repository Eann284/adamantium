import React from 'react'
import { MaterialRequest } from '@/src/types/materialRequest'

interface Props {
    requests: MaterialRequest[]
}

function RequestsView({requests}: Props) {
  return (
    <div className='flex flex-col gap-2'>
      {
        requests.map((req)=>(
            <div key={req.mrf_id} className='ring ring-gray-400 rounded-lg p-2'>
                <h1>{req.requestor_email}</h1>
                <h1>{req.release_status}</h1>
            </div>
        ))
      }
    </div>
  )
}


export default RequestsView
