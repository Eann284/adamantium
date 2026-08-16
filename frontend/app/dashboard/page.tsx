import AdminDashboard from '@/src/components/dashboard/variants/AdminDashboard';
import SupervisorDashboard from '@/src/components/dashboard/variants/SupervisorDashboard';
import TechnicianDashboard from '@/src/components/dashboard/variants/TechnicianDashboard.tsx';
import { authOptions } from '@/src/lib/authOptions'
import { getServerSession } from 'next-auth'
import React from 'react'

async function page() {

  const session = await getServerSession(authOptions);

  switch (session?.user.role) {
    case "Admin":
      return <AdminDashboard session={session}/>;

    case "Technician":
      return <TechnicianDashboard session={session}/>

    case "Supervisor":
      return <SupervisorDashboard session={session}/>
  }
  
}

export default page
