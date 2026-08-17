import { MaterialRequest } from '@/src/types/materialRequest'
import React from 'react'
import RequestCard from './RequestCard'
import ReleaseCard from './ReleaseCard';

interface Props {
    pendingReleases: MaterialRequest[];
    onView: (request: MaterialRequest) => void
}

function PendingList({pendingReleases, onView}:Props) {
  return (
   <section className='ring ring-gray-400 p-4 h-full overflow-y-auto min-h-0'>
      <ul>
        {pendingReleases.map(req=>(
            <li key={req.mrf_id}>
               <ReleaseCard releases={req} onView={()=>onView(req)}/>
            </li>
        ))}
      </ul>
      </section>
  )
}

export default PendingList
