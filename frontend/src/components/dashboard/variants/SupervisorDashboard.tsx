import { getPendingRequests } from '@/src/services/requestService'
import { Session } from 'next-auth';
import React from 'react'
import SupervisorClient from '../SupervisorClient';
import { getProducts } from '@/src/services/productsService';


interface Props {
  session: Session
}

async function SupervisorDashboard({session}:Props) {

    const pendingRequests = await getPendingRequests(session?.user?.accessToken);
    const products = await getProducts(session.user.accessToken)

  return (
    <SupervisorClient pending={pendingRequests} products={products} accessToken={session?.user?.accessToken}/>
  )
}

export default SupervisorDashboard
