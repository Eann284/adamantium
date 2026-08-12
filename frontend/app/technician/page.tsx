import React from 'react'
import { AuthOptions } from 'next-auth'
import { getServerSession } from 'next-auth'
import { getProducts } from '@/src/services/productsService'
import { authOptions } from '@/src/lib/authOptions'
import MaterialRequestForm from '@/src/components/technician/MaterialRequestForm'


async function TechnicianDashboard() {

    const session = await getServerSession(authOptions);
    if (!session?.user?.accessToken) {
    throw new Error("Unauthorized");
  }

    const products = await getProducts(session.user.accessToken);
  return (
    <div>
      <h1>Technician</h1>

      <section>
        <MaterialRequestForm accessToken={session.user.accessToken} products={products}/>
      </section>
    </div>
  )
}

export default TechnicianDashboard
