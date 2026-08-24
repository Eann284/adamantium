import { getPendingReleases } from '@/src/services/requestService'
import { Session } from 'next-auth'
import React from 'react'
import CustodianClient from '../CustodianClient';
import { getProducts } from '@/src/services/productsService';

interface Props {
    session: Session
}

async function CustodianDashboard({session}:Props) {

    const pendingReleases = await getPendingReleases(session?.user?.accessToken);
    const products = await getProducts(session.user.accessToken)

  return (
      <CustodianClient pending={pendingReleases} products={products} accessToken={session.user.accessToken}/>
  )
}

export default CustodianDashboard
