import { getPendingRequests } from '@/src/services/requestService'
import { Session } from 'next-auth';
import React from 'react'
import RequestCard from '../RequestCard';
import PendingList from '../PendingList';
import SupervisorClient from '../SupervisorClient';


interface Props {
  session: Session
}

async function SupervisorDashboard({session}:Props) {

    const pendingRequests = await getPendingRequests(session?.user?.accessToken);

  return (
    <SupervisorClient pending={pendingRequests} accessToken={session?.user?.accessToken}/>
  )
}

export default SupervisorDashboard
