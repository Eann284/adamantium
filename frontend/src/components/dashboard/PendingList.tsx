import { MaterialRequest } from '@/src/types/materialRequest'
import React from 'react'
import RequestCard from './RequestCard'

interface Props {
    pendingRequests: MaterialRequest[];
    onView: (request: MaterialRequest) => void
}

function PendingList({pendingRequests, onView}:Props) {
  return (
   <section className='ring ring-gray-400 p-4 h-full overflow-y-auto min-h-0'>
      <ul>
        {pendingRequests.map(req=>(
            <li key={req.mrf_id}>
               <RequestCard requests={req} onView={onView}/>
            </li>
        ))}
      </ul>
      </section>
  )
}

export default PendingList
