import React from 'react'
import { getServerSession } from 'next-auth'
import { getProducts } from '@/src/services/productsService'
import { authOptions } from '@/src/lib/authOptions'
import { getSentRequests } from '@/src/services/requestService'
import MaterialRequestForm from '@/src/components/technician/MaterialRequestForm'
import NameCard from '../../technician/NameCard'
import Requests from '../../technician/Requests'


async function TechnicianDashboard() {

    const session = await getServerSession(authOptions);

    const name = session?.user.name?.toString() ?? ""
    const role = session?.user.role?.toString() ?? ""

    if (!session?.user?.accessToken) {
    throw new Error("Unauthorized");
  }

    const products = await getProducts(session.user.accessToken);
    const requests = await getSentRequests(session.user.accessToken)
  return (
    <main className='flex flex-col h-screen p-4 gap-2'>
      
      <div className='flex items-center justify-center'>
        <h1 className='ring w-full text-center'>Technician Dashboard</h1>
      </div>

      <div>
        <NameCard name={name} role={role}/>
      </div>

      <div className='grid 
      grid-cols-1 gap-2 flex-1 min-h-0
      lg:grid-cols-2
      '>

        <section className='ring ring-gray-400 h-full p-4'>
          <MaterialRequestForm accessToken={session.user.accessToken} products={products}/>
        </section>
        
        <section className='ring ring-gray-400 p-4 h-full overflow-y-auto min-h-0'>
          <Requests requests={requests}/>
        </section>
        </div>

    </main>
  )
}

export default TechnicianDashboard
