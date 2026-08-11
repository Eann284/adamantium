import React from 'react'
import { Request } from '@/src/types/materialRequest'

interface Props {
    requests: Request[]
}

function RequestsView({requests}: Props) {
  return (
    <div>
      {
        requests.map((req)=>(
            <div key={req.mrf_id}>
                <h1>{req.requestor_email}</h1>
                <h1>{req.release_status}</h1>
            </div>
        ))
      }
    </div>
  )
}

interface Props {
    requests: Request[]
}

export default RequestsView
