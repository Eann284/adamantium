import { getServerSession } from 'next-auth'
import React from 'react'
import { getPendingRequestsById } from '@/src/services/requestService'
import { authOptions } from '@/src/lib/authOptions';
import EditRequestForm from './EditRequestForm';
import { getProducts } from '@/src/services/productsService';

interface Props {
    mrf_id: string,
  
}

async function EditRequest({mrf_id}:Props) {

    const mrfId = Number(mrf_id);

    const session = await getServerSession(authOptions); 

    const request = await getPendingRequestsById(
        session!.user.accessToken,
        mrfId
    )

    const products = await getProducts(session!.user.accessToken);

return (
    <div className='flex flex-col h-screen p-4 gap-2'>

         <div className='grid 
      grid-cols-1 gap-2 flex-1 min-h-0
      '>
        <EditRequestForm request={request} products={products}accessToken={session!.user.accessToken}/>
      </div>
    </div>
  )
}

export default EditRequest
