import { MaterialRequest } from '@/src/types/materialRequest'
import React from 'react'

interface Props {
    releases: MaterialRequest;
    onView: ()=>void
}

function ReleaseCard({releases, onView}:Props) {
  return (
    
    <div key={releases.mrf_id} className='border'>
      <h1>MRF-{releases.mrf_id} - {releases.requestor_email}</h1>
      <div>{releases.release_status}</div>
      <button onClick={onView}>View</button>
    </div>
  )
}

export default ReleaseCard
