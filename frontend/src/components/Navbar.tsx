import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Session } from 'next-auth'
import React from 'react'

interface Props {
  session: Session | null;
}

function Navbar({session}:Props) {


  const getBadgeClass = (role:string) => {
            switch (role) {
            case "Admin":
                return "bg-green-500 text-white";
            case "Custodian":
                return "bg-yellow-500 text-white";
            case "Supervisor":
                return "bg-red-500 text-white";
            case "Technician":
                return "bg-orange-500 text-white";
        
            default:
                return "bg-gray-500 text-white";
            }
        }

  return (
    <nav className='flex flex-row justify-between items-center px-4 bg-blue-500 h-12 p-3'>
      <div className='flex flex-row gap-2 items-center'>
      <Badge variant="default" className={`${getBadgeClass(session!.user.role)} w-20 font-bold`}>{session?.user.role}</Badge>
      <h1 className='text-lg font-semibold text-white'>{session?.user.name}</h1>
      </div>
      <Button variant="default" className="bg-red-600 text-white font-semibold cursor-pointer w-20 rounded-sm h-8">Log out</Button>

    </nav>
  )
}

export default Navbar;
