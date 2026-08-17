import { getPendingReleases } from '@/src/services/requestService'
import { Session } from 'next-auth'
import React from 'react'
import CustodianClient from '../CustodianClient';

interface Props {
    session: Session
}

async function CustodianDashboard({session}:Props) {

    const pendingReleases = await getPendingReleases(session?.user?.accessToken);

  return (
      <CustodianClient pending={pendingReleases} accessToken={session.user.accessToken}/>
  )
}

export default CustodianDashboard
