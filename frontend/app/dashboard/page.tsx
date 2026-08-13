import AdminDashboard from '@/src/components/dashboard/variants/AdminDashboard';
import TechnicianDashboard from '@/src/components/dashboard/variants/TechnicianDashboard.tsx';
import { authOptions } from '@/src/lib/authOptions'
import { getServerSession } from 'next-auth'
import React from 'react'

async function page() {

  const session = await getServerSession(authOptions);

  switch (session?.user.role) {
    case "Admin":
      return <AdminDashboard/>;

    case "Technician":
      return <TechnicianDashboard/>
  }
  
}

export default page
