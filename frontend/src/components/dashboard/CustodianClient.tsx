"use client";

import { MaterialRequest } from "@/src/types/materialRequest";
import { useState } from "react";
import PendingReleaseList from "./PendingReleaseList";
import ReleaseDetails from "./ReleaseDetails";

interface Props {
    pending: MaterialRequest[];
    accessToken: string
}

function SupervisorClient({pending, accessToken}:Props) {

    const [selectedRequest, setSelectedRequest] = useState<MaterialRequest |null>(null)

    
  return (
    
      <main className='h-full flex flex-col p-4 gap-2'>
        
    <div className='grid 
      grid-cols-2 gap-2 flex-1 min-h-0
      '>

    {/* left panel */}
    <PendingReleaseList pendingReleases={pending} onView={setSelectedRequest}/>

    {/* right panel split vertically */}

    <section className='ring ring-gray-400 grid grid-cols-1 p-2'>
        <div  className="p-2 h-70 overflow-y-auto min-h-0">
            <ReleaseDetails release={selectedRequest} accessToken={accessToken}/>
        </div>
        <div>bottom</div>
    </section>

</div>
    </main>

  )
}

export default SupervisorClient
